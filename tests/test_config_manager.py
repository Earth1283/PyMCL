import pytest
from pymcl.config_manager import ConfigManager
import shutil
from pathlib import Path

# Mock constants if needed, or rely on the logic in config_manager to pick up local settings
# For testing, we want to ensure we don't overwrite real user data.
# ConfigManager logic:
# if LOCAL_SETTINGS.exists(): ... else: DEFAULT_DATA_DIR ...

@pytest.fixture
def clean_config(tmp_path, monkeypatch):
    """
    Fixture to ensure ConfigManager uses a temporary directory
    and is reset between tests.
    """
    # Create a temp dir for config
    d = tmp_path / "config"
    d.mkdir()
    settings_file = d / "settings.json"
    
    # Patch the ConfigManager's file paths
    # We need to patch where the module DEFINES them.
    # Note: Since they are global variables in the module, we patch them there.
    monkeypatch.setattr("pymcl.config_manager.SETTINGS_FILE", settings_file)
    monkeypatch.setattr("pymcl.config_manager.CONFIG_DIR", d)
    
    # Reset singleton
    ConfigManager._instance = None
    
    return ConfigManager()

def test_config_defaults(clean_config):
    cm = clean_config
    assert cm.get("non_existent") is None
    assert cm.get("non_existent", "default") == "default"

def test_config_set_get(clean_config):
    cm = clean_config
    cm.set("theme", "dark")
    assert cm.get("theme") == "dark"

def test_config_persistence(clean_config):
    cm = clean_config
    cm.set("auto_login", True)
    cm.save()
    
    # Reset singleton to force reload from disk
    ConfigManager._instance = None
    cm2 = ConfigManager()
    
    assert cm2.get("auto_login") is True
