import csv
from typing import Dict, List


class ClientRepository:
    """Repository for managing client records stored in a CSV file."""

    fieldnames = ["name", "cpf"]

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self._records: List[Dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.csv_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row:
                        continue
                    record = {field: (row.get(field, "") or "").strip() for field in self.fieldnames}
                    if any(record.values()):
                        self._records.append(record)
        except FileNotFoundError:
            # Start with an empty dataset if the file does not exist yet.
            self._records = []

    def all(self) -> List[Dict[str, str]]:
        return self._records

    def add(self, record: Dict[str, str]) -> None:
        self._records.append(record)

    def save(self) -> None:
        with open(self.csv_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for record in self._records:
                writer.writerow({field: str(record.get(field, "")) for field in self.fieldnames})


class AccountRepository:
    """Repository for managing account records stored in a CSV file."""

    fieldnames = ["cpf", "number_account", "total"]

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self._records: List[Dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.csv_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not row:
                        continue
                    record = {field: (row.get(field, "") or "").strip() for field in self.fieldnames}
                    if any(record.values()):
                        self._records.append(record)
        except FileNotFoundError:
            self._records = []

    def all(self) -> List[Dict[str, str]]:
        return self._records

    def add(self, record: Dict[str, str]) -> None:
        # Ensure totals are stored as strings for consistent serialization
        if "total" in record and not isinstance(record["total"], str):
            record = {**record, "total": str(record["total"])}
        self._records.append(record)

    def save(self) -> None:
        with open(self.csv_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for record in self._records:
                writer.writerow({field: str(record.get(field, "")) for field in self.fieldnames})
