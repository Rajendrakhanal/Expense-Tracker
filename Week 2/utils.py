import json
import hashlib

def load_data(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": [], "transactions": []}

def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(plain, hashed):
    return hash_password(plain) == hashed
