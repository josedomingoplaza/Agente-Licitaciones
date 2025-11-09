import os
import json

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                if not text or not text.strip():
                    return default
                return json.loads(text)
        except json.JSONDecodeError:
            print(f"Warning: JSON decode error reading {path}, returning default.")
            return default
        except Exception as e:
            print(f"Warning: error reading {path}: {e}")
            return default
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)