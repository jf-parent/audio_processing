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

EFFECT_MIN = 2
EFFECT_MAX = 10

TRACK_END = audio_length_sec
track_head = 0
track_id = 0
pan_g = utils.pan_generator()
while track_head < TRACK_END:
    start = track_head
    end = start + random.randint(EFFECT_MIN, EFFECT_MAX)
    end = min(end, TRACK_END)
    client.do(f"Select: Track=0 Start={start} End={end}")
    client.do("Copy:")
    client.do("NewStereoTrack:")
    track_id += 1

    client.do(f"Select: Track={track_id}")
    client.do("Paste:")

    pan = next(pan_g)

    client.do(pan)

    pitch_half_steps = random.randint(-12, 12)
    pitch_percent_change_start = utils.half_steps_to_percent_change(pitch_half_steps)
    client.do(f"SlidingStretch: PitchHalfStepsStart={pitch_half_steps} PitchPercentChangeStart={pitch_percent_change_start}")

    track_head = end

client.do("Save:")
client.do("ExportMp3:")
client.do("Exit:")
