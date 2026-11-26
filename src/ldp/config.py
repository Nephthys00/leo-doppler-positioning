"""Load project settings from config/default.yaml and config/local.yaml."""
from pathlib import Path

import yaml

def load_config(config_dir: str = "config") -> dict:
    """Read default.yaml, then replace its sections with those in local.yaml (if it exists)."""
    folder = Path(config_dir)
    with open (folder/"default.yaml",encoding="utf-8") as file :
        config = yaml.safe_load(file)
        # Defaults include a generic example observer, used when local.yaml is missing

    local_path=folder/"local.yaml"
    if local_path.exists(): #if local.yaml exists, load it
        with open(local_path,encoding="utf-8") as file:
            config.update(yaml.safe_load(file))
    return config