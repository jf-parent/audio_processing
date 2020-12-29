import time
import os
import subprocess
import json
import uuid
from pathlib import Path

from audacity_lib import pipeclient


class Client(object):

    def __init__(self):
        commands = []

        self.uuid = str(uuid.uuid1())

        try:
            self.config = json.load(open('../config.json'))
        except Exception as e:
            print('Fix your config.json!', e)
            exit(1)

        commands.append(self.config['audacity_exe_path'])

        print("Starting Audacity...")
        print(f"Running '{commands[0]}'")
        subprocess.call(commands[0] + "&", shell=True)
        input("Is Audacity ready?<enter>")

        self.client = pipeclient.PipeClient()

    def get_project_name(self):
        return f"outputs/{self.uuid}.aup"

    def do(self, command, mute=False):
        reply = ''
        self.client.write(command)
        while reply == '':
            time.sleep(0.1)
            reply = self.client.read()
        if not mute:
            print(reply)

        return reply
