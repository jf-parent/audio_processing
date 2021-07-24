#!/usr/bin/env python

from glob import glob
import random
import sys
from itertools import cycle

import sox
from pydub import AudioSegment, silence
from pydub.playback import play

sys.path.insert(0, "..")

# TODO apply reverse as an overlay

NB_BACKGROUND_AMBIENT_SOUNDS = 3
ENABLE_CHORUS = True
ENABLE_GAIN = True
ENABLE_PITCH = True
ENABLE_REVERB = True
ENABLE_REVERSE = False
ENABLE_TREMOLO = True

def load_ambient_sounds():
    sounds = []
    for file_ in glob('./sounds/background*'):
        sounds.append(AudioSegment.from_file(file_))
    return sounds

def load_loud_sounds():
    sounds = []
    for file_ in glob('./sounds/loud*'):
        sounds.append(AudioSegment.from_file(file_))
    random.shuffle(sounds)
    return cycle(sounds)

def apply_effects(input_file_path, output_file_path):
    new_pitch = random.randint(-6,6)
    chorus_nb_voice =random.randint(0, 6)

    print(f"[*] {input_file_path}")

    tfm = sox.Transformer()
    array = tfm.build_array(input_filepath=input_file_path)

    # Tremolo
    if ENABLE_TREMOLO and random.randint(0, 100) >= 80:
        new_speed = random.randint(1000, 3000)
        print(f"speed={new_speed}")
        tfm.tremolo(speed=new_speed)

    # Gain
    if ENABLE_GAIN:
        new_gain=5
        print(f"gain={new_gain}")
        tfm.gain(new_gain)

    # Reverb
    if ENABLE_REVERB:
        room_scale = random.randint(10, 100)
        reverberance = random.randint(10, 100)
        print(f"room_scale: {room_scale}")
        tfm.reverb(reverberance=reverberance, room_scale=room_scale)

    # Reverse
    if ENABLE_REVERSE and random.randint(0, 100) > 95:
        print(f"[!!!]reversing audio")
        tfm.reverse()

    # Chorus
    if ENABLE_CHORUS and chorus_nb_voice and random.randint(0, 100) >= 50:
        print(f"chorus={chorus_nb_voice}")
        tfm.chorus(n_voices=chorus_nb_voice)

    # Pitch
    if ENABLE_PITCH:
        print(f"new_pitch={new_pitch}")
        tfm.pitch(new_pitch)

    tfm.build_file(input_array=array, output_filepath=output_file_path, sample_rate_in=44100)

# Import
#sound = AudioSegment.from_file("./files/audio_out.wav", format="wav")
sound = AudioSegment.from_file("./files/sample.wav", format="wav")
#play(sound)

# Detect silence for reference
non_silence = silence.detect_nonsilent(sound, min_silence_len=500, silence_thresh=-60)
print("[*] non_silence:", non_silence)

# Apply Effects
new_fragments = []
fragments = silence.split_on_silence(sound, min_silence_len=500, silence_thresh=-60)
for id_, fragment in enumerate(fragments):
    output_file_path = f"tmp/{id_}_out.wav"
    input_file_path = f"tmp/{id_}.wav"
    fragment.export(input_file_path, format="wav")
    apply_effects(input_file_path, output_file_path)
    new_fragments.append((
        fragment,
        AudioSegment.from_file(output_file_path, format="wav")))

# Rebuild output
out = []
last_end = None
for idx_slice, fragments in zip(non_silence, new_fragments):
    print(idx_slice, fragments)
    orig_fragment, new_fragment = fragments

    beg, end = idx_slice
    if not out:
        if beg > 0:
            print(f"[*]Appending silence for {beg}")
            out.append(AudioSegment.silent(duration=beg))
    elif last_end != end:
        duration = (beg-last_end)
        print(f"[*]Appending silence for {duration}")
        out.append(AudioSegment.silent(duration=duration))

    fragment_ = new_fragment[:len(orig_fragment)]
    out.append(fragment_)
    last_end = beg + len(fragment_)
#print(f"[*]out: {out}")

out.append(AudioSegment.silent(duration=1000))

master_orig = sum(out)
master = master_orig[:]

# Overlay background ambient sounds
ambient_sounds = load_ambient_sounds()
for _ in range(NB_BACKGROUND_AMBIENT_SOUNDS):
    random.shuffle(ambient_sounds)
    sound_ = ambient_sounds.pop()
    print(f"[*] Overlaying background ambient {sound_}")
    master = master.overlay(sound_)

# Overlay background sounds during silence
loud_sounds = load_loud_sounds()
silences = silence.detect_silence(master_orig, min_silence_len=500, silence_thresh=-60)
for silence in silences:
    sound_ = next(loud_sounds)
    print(f"[*] Overlaying background loud noise {sound_} @ {silence}")
    master = master.overlay(sound_, position=silence[0])

master.export("tmp/output.wav", format="wav")
