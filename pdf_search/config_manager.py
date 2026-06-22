import json
import os

CONFIG_FILE = "urls_config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default_config = {"urls": []}
        save_config(default_config)
        return default_config
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def add_url(url):
    config = load_config()
    # Check if url already exists
    for item in config["urls"]:
        if item["url"] == url:
            return False # Already exists
    
    config["urls"].append({
        "url": url,
        "scraped": False,
        "files": []
    })
    save_config(config)
    return True

def get_urls():
    config = load_config()
    return config["urls"]

def update_url_scraped(url, files):
    config = load_config()
    for item in config["urls"]:
        if item["url"] == url:
            item["scraped"] = True
            item["files"] = files
            break
    save_config(config)
