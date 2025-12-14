import os
from typing import TypedDict
from .config_manager import ConfigManager

APP_NAME = "PyMCLauncher"
CLIENT_ID = "34851193-4344-4028-b5b8-9fc87315984c"
REDIRECT_URL = "http://localhost:8000"

# Initialize ConfigManager to load settings
config_manager = ConfigManager()
settings = config_manager.get_all()

MINECRAFT_DIR = settings.get("minecraft_dir", os.path.join("D:\\pymcl-data" if os.name == "nt" else os.path.join(os.path.expanduser("~"), ".pymcl-data")))
IMAGES_DIR = settings.get("images_dir", os.path.join(MINECRAFT_DIR, "images"))
MODS_DIR = settings.get("mods_dir", os.path.join(MINECRAFT_DIR, "mods"))
ICON_CACHE_DIR = os.path.join(MODS_DIR, ".icons")

DEFAULT_IMAGE_URL = "https://sm.ign.com/ign_ap/gallery/m/minecraft-/minecraft-vibrant-visuals-comparison-screenshots_25we.jpg"
DEFAULT_IMAGE_PATH = os.path.join(IMAGES_DIR, "default_background.jpg")
VERSIONS_CACHE_PATH = os.path.join(MINECRAFT_DIR, "versions_cache.json")
MICROSOFT_INFO_PATH = os.path.join(MINECRAFT_DIR, "microsoft_info.json")

class MicrosoftInfo(TypedDict):
    access_token: str
    refresh_token: str
    username: str
    uuid: str
    expires_in: int
    login_time: int