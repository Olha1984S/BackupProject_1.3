import json
from pathlib import Path


APP_NAME = "BackupManager"


def get_config_path():
    """
    Returns the path to the user's configuration file.
    """

    app_data = Path.home() / "AppData" / "Local" / APP_NAME
    return app_data / "config.json"


def config_exists():
    """
    Checks whether the configuration file exists.
    """

    return get_config_path().is_file()


def save_config(config):
    """
    Saves user configuration to config.json.
    """

    config_path = get_config_path()

    # Create BackupManager folder if it does not exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with config_path.open("w", encoding="utf-8") as file:
        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_config():
    """
    Loads user configuration from config.json.

    Returns:
        dict: saved configuration
        None: if configuration file does not exist
    """

    config_path = get_config_path()

    if not config_path.is_file():
        return None

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)