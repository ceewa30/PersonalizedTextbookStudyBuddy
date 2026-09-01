import yaml
from pathlib import Path

def load_config() -> dict:
    """Dynamically locate and load the config.yaml file"""
    # Get project root (navigating up from src/embedding/embedder.py)
    project_root = Path(__file__).resolve().parent.parent.parent
    config_path = project_root / "config.yaml"
    
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config()
    
    print(config)
