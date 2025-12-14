import json
import os
from pathlib import Path

CONFIG_DIR = Path("pymcl/config")
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
