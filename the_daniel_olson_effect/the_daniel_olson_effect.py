#!/usr/bin/env python

import random
import sys

import sox
from pydub import AudioSegment, silence
from pydub.playback import play

sys.path.insert(0, "..")


def change_pitch(input_file_path, output_file_path):
    new_pitch = random.randint(-6,6)
    print(f"[*] {input_file_path} new_pitch={new_pitch}")
    tfm = sox.Transformer()
    array = tfm.build_array(input_filepath=input_file_path)
    tfm.pitch(new_pitch)
    tfm.build_file(input_array=array, output_filepath=output_file_path, sample_rate_in=44100)

sound = AudioSegment.from_file("./files/audio_out.wav", format="wav")
#play(sound)

non_silence = silence.detect_nonsilent(sound, min_silence_len=500, silence_thresh=-60)
#non_silence = [((start/1000), (stop/1000)) for start, stop in non_silence]
print("non_silence:", non_silence)

new_fragments = []
fragments = silence.split_on_silence(sound, min_silence_len=500, silence_thresh=-60)
for id_, fragment in enumerate(fragments):
    output_file_path = f"tmp/{id_}_out.wav"
    input_file_path = f"tmp/{id_}.wav"
    fragment.export(input_file_path, format="wav")
    change_pitch(input_file_path, output_file_path)
    new_fragments.append(AudioSegment.from_file(output_file_path, format="wav"))

out = []
last_end = None
for idx_slice, fragment in zip(non_silence, new_fragments):
    print(idx_slice, fragment)

    beg, end = idx_slice
    if not out:
        if beg > 0:
            print(f"[*]Appending silence for {beg}")
            out.append(AudioSegment.silent(duration=beg))
    elif last_end != end:
        duration = (beg-last_end)
        print(f"[*]Appending silence for {duration}")
        out.append(AudioSegment.silent(duration=duration))

    out.append(fragment)
    last_end = end
#print(f"[*]out: {out}")

out = sum(out)
out.export("tmp/output.wav", format="wav")
