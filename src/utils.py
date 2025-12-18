# src/utils.py
import os
from datetime import datetime

def ensure_dirs():
    os.makedirs('models', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)

def now_iso():
    return datetime.utcnow().isoformat()