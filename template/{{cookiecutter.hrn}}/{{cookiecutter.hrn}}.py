#!/usr/bin/env python

import random
import sys

sys.path.insert(0, "..")

from audacity_lib import client, utils


client = client.Client(open_file="files/input-{uuid}.wav")

reply = client.do("GetInfo: Type=Tracks")
track_info = utils.extract_json(reply)
audio_length_sec = track_info[0]["end"]
print("Total Audio Length (sec):", audio_length_sec)


# client.do("Save:")
# client.do("ExportMp3:")
# client.do("Exit:")
