import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


DEFAULT_CONFIG = {
    "workdir": "",
    "siril_path": ""
}


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)