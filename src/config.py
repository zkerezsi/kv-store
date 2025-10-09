import os
from pathlib import Path

STORAGE_PATH = Path(os.getenv("STORAGE_PATH") or "store.json")
CLI_ENABLED = os.getenv("CLI_ENABLED", "false") == "true"
