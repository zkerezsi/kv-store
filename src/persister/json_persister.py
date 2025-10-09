import json
import os
from pathlib import Path
from typing import Dict

from src.persister.persister import Persister


class JSONPersister(Persister):
    path: Path

    def __init__(self, path: Path):
        self.path = path

    def load(self) -> Dict[str, str]:
        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                return json.load(file)
        return {}

    def save(self, data: Dict[str, str]):
        with open(self.path, "w") as file:
            json.dump(data, file)
