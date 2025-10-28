import os, json, click

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "commitr")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def ensure_dir():
  os.makedirs(CONFIG_DIR, exist_ok=True)

def save_config(api_key, model):
  ensure_dir()
  data = {"OPENAI_API_KEY": api_key, "OPENAI_MODEL": model}
  with open(CONFIG_PATH, "w") as f:
    json.dump(data, f, indent=2)
  click.echo(f"Saved config to {CONFIG_PATH}")

def load_config():
  if not os.path.exists(CONFIG_PATH):
    return {}
  with open(CONFIG_PATH) as f:
    return json.load(f)