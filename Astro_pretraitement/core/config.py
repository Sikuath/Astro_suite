import json
from pathlib import Path


CONFIG_FILE = Path("config.json")


DEFAULT_CONFIG = {
    "lights_folder": "",
    "rejected_folder": ""
}


def load_config():

    if not CONFIG_FILE.exists():

        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except json.JSONDecodeError:

        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG



def save_config(config):

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )