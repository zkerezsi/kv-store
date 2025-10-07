import io
import os
import csv
from typing import Dict

from src.persister.persister import Persister


def dict_to_csv_str(dictionary: Dict[str, str]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["key", "value"])
    for key, value in dictionary.items():
        writer.writerow([key, value])
    return output.getvalue()


def csv_str_to_dict(csv_str: str) -> Dict[str, str]:
    dictionary: Dict[str, str] = {}
    lines = csv_str.strip().split("\r\n")
    for line in lines[1:]:
        key, value = [item.strip() for item in line.split(",", 1)]
        dictionary[key] = value
    return dictionary


class CSVPersister(Persister):
    filename: str

    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> Dict[str, str]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                csv_str = file.read()
                return csv_str_to_dict(csv_str)
        return {}

    def save(self, data: Dict[str, str]):
        with open(self.filename, "w") as file:
            csv_str = dict_to_csv_str(data)
            file.write(csv_str)
