import json
import os
from pathlib import Path

# Determine default data directory (mirrors constants.py logic to avoid circular import)
if os.name == "nt":
    DEFAULT_DATA_DIR = Path("D:/pymcl-data")
else:
    DEFAULT_DATA_DIR = Path.home() / ".pymcl-data"

# Check for portable settings file first
LOCAL_SETTINGS = Path("settings.json")
if LOCAL_SETTINGS.exists():
    SETTINGS_FILE = LOCAL_SETTINGS
    CONFIG_DIR = Path(".")
else:
    CONFIG_DIR = DEFAULT_DATA_DIR
    SETTINGS_FILE = CONFIG_DIR / "settings.json"

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self._settings = {}
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as f:
                    self._settings = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Error loading settings: {e}")

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self._settings, f, indent=4)
        except OSError as e:
            print(f"Error saving settings: {e}")

    def get_all(self):
        return self._settings.copy()
