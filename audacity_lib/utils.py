import json
import re


def extract_json(text):
    json_ = None
    match = re.search('\[[^\]]*\]', text)
    if match:
        print(match[0])
        json_ = json.loads(match[0])
    return json_


def half_steps_to_percent_change(half_steps):
    return 100.0 * ((2.0 ** (half_steps / 12.0)) - 1.0)


def pan_generator():
    while True:
        yield "PanRight:"
        yield "PanLeft:"
