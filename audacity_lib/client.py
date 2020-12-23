import time
import os
import subprocess
import json
import uuid
from pathlib import Path

from audacity_lib import pipeclient


class Client(object):

    def __init__(self, open_file=None):
        commands = []

        cwd = Path(os.getcwd())

        try:
            self.config = json.load(open('../config.json'))
        except Exception as e:
            print('Fix your config.json!', e)
            exit(1)

        commands.append(self.config['audacity_exe_path'])

        if open_file:
            new_file = cwd / Path(open_file.replace('{uuid}', str(uuid.uuid1())))
            input_file = cwd / Path(open_file.replace('-{uuid}', ''))
            subprocess.call(f"cp {input_file} {new_file}", shell=True)

            commands.append(str(new_file))

        print("Starting Audacity...")
        print(f"Running '{commands[0]}'")
        subprocess.call(commands[0] + "&", shell=True)
        input("Is Audacity ready?<enter>")
        if open_file:
            print("Opening new project...")
            print(f"Running '{commands}'")
            subprocess.call(" ".join(commands), shell=True)
            # TODO make automatic
            input("Is project ready?<enter>")

        self.client = pipeclient.PipeClient()

    def do(self, command, mute=False):
        reply = ''
        self.client.write(command)
        while reply == '':
            time.sleep(0.1)
            reply = self.client.read()
        if not mute:
            print(reply)

        return reply
