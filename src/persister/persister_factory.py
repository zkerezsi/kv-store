from pathlib import Path

from src.persister.csv_persister import CSVPersister
from src.persister.json_persister import JSONPersister
from src.persister.persister import Persister


def persister_factory(storage_path: Path) -> Persister:
    if storage_path.suffix == ".csv":
        return CSVPersister(storage_path)
    elif storage_path.suffix == ".json":
        return JSONPersister(storage_path)
    raise ValueError("invalid filepath providied")
