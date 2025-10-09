import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
STORAGE_PATH = Path(os.getenv("STORAGE_PATH") or "store.json")
