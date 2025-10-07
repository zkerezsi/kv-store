import json
import os
from typing import Dict

from src.persister.persister import Persister


class JSONPersister(Persister):
    filename: str

    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> Dict[str, str]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return {}

    def save(self, data: Dict[str, str]):
        with open(self.filename, "w") as file:
            json.dump(data, file)
