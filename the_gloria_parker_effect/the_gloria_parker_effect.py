#!/usr/bin/env python

import random
import sys

sys.path.insert(0, "..")

from audacity_lib import client, utils


client = client.Client()

files = ["inputs/celine_dion/accompaniment.wav", "inputs/celine_dion/vocals.wav"]
for f in files:
    client.do(f"Import2: Filename={f}")

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
    client.do(f"Select: Track=1 Start={start} End={end}")
    client.do("Copy:")
    client.do("NewStereoTrack:")
    track_id += 1

    client.do(f"Select: Track={track_id}")
    client.do("Paste:")

    pitch_half_steps = random.choice([-12,12,6,-6])
    pitch_percent_change_start = utils.half_steps_to_percent_change(pitch_half_steps)
    client.do(f"SlidingStretch: PitchHalfStepsStart={pitch_half_steps} PitchPercentChangeStart={pitch_percent_change_start}")

    if random.randint(0, 100) >= 50:
        pan = next(pan_g)

        client.do(pan)

        client.do("NewStereoTrack:")
        track_id += 1

        client.do(f"Select: Track={track_id}")
        client.do("Paste:")

        pan = next(pan_g)

        client.do(pan)
        pitch_half_steps *= -1
        pitch_percent_change_start = utils.half_steps_to_percent_change(pitch_half_steps)
        client.do(f"SlidingStretch: PitchHalfStepsStart={pitch_half_steps} PitchPercentChangeStart={pitch_percent_change_start}")

        # input("Validate")

    track_head = end

project_name = client.get_project_name()
client.do(f"SaveProject2: Filename={project_name}")
client.do("ExportMp3:")
client.do("Exit:")
