import csv
from typing import Dict, List

from tools.atm_tools import log_transacao

from datetime import datetime

NUMBER_TRANSACTIONS = 2


class ModelRepository:

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
        if "balance" in record and not isinstance(record["balance"], str):
            record = {**record, "balance": str(record["balance"])}
        self._records.append(record)

    def save(self) -> None:
        with open(self.csv_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for record in self._records:
                writer.writerow({field: str(record.get(field, "")) for field in self.fieldnames})


class ClientRepository(ModelRepository):
    """Repository for managing client records stored in a CSV file."""

    fieldnames = ["name", "date_of_birth", "cpf", "address"]
    def __init__(self, csv_path: str):
        super().__init__(csv_path)
        self.accounts = []

    def execute_transaction(self, account, transaction):
        if len(account.history.day_transactions) >= NUMBER_TRANSACTIONS:
            print("Você excedeu o número de transações permitidas para hoje!.")
            return
        transaction.add_transaction(account)

    def add_account(self, account):
        self.accounts.append(account.account)


class AccountRepository(ModelRepository):
    """Repository for managing account records stored in a CSV file."""

    # fieldnames = ["agencia", "numero", "titular", "saldo"]
    fieldnames = ["agency_bank", "number_bank", "holder_account", "balance", "cpf_client"]

    def list_accounts(self) -> List[Dict[str, str]]:
        list_accounts = []
        with open(self.csv_path, "r") as _f:
            accounts = csv.DictReader(_f)
            for account in accounts:
                list_accounts.append(account)
        return list_accounts


class HistoryRepository(ModelRepository):

    fieldnames = ["transaction_type", "transaction_balance", "transaction_data"]

    # def add_transaction(self, transaction):
    #     self._transactions.append(
    #         {
    #             "transaction_type": transaction.type,
    #             "transaction_balance": transaction.balance,
    #             "transaction_data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    #         }
    #     )
    #
    # def day_transactions(self):
    #     data_actual = datetime.now().date()
    #     transactions = []
    #     for transaction in self._transactions:
    #         data_transaction = datetime.strptime(transaction["data"], "%d-%m-%Y %H:%M:%S").date()
    #         if data_actual == data_transaction:
    #             transactions.append(transaction)
    #     return transactions
