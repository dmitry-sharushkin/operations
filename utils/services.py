import json
import datetime
import os.path

JSON_DATA_PATH = "../data/operations.json"


def load_json(JSON_DATA_PATH):
    with open(JSON_DATA_PATH, encoding="utf8") as f:
        json_dict = json.load(f)
    return json_dict

