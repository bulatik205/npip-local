import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

DEFAULT_CONFIG = {
    "saveMode": True
}


def load_config() -> dict:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def get_save_mode() -> bool:
    config = load_config()
    return config.get("saveMode", True)


def set_save_mode(value: bool) -> None:
    config = load_config()
    config["saveMode"] = value
    save_config(config)