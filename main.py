import csv
from pathlib import Path

import FreeSimpleGUI as sg

from gui.atm_bankGUI import BankGUI
from gui.atm_homeScreenGUI import HomeScreenlGUI
from gui.atm_loginGUI import LoginGUI
from gui.atm_registerAccountGUI import RegisterAccountGUI
from gui.atm_registerClientGUI import RegisterClientGUI
from gui.atm_listAccountsGUI import ListAccountsGUI
from repository.atm_repositories import AccountRepository, ClientRepository, HistoryRepository
from tools.atm_tools import create_file

ROOT_PATH = Path(__file__).parent / "databases"


def main():

    accounts_repo, catalog_accounts, catalog_clients, clients_repo, path_filename_accounts = is_files()

    while True:
        home_screen = HomeScreenlGUI()
        choice = home_screen.run()
        if choice is None:
            sg.popup_auto_close("Saindo...", auto_close_duration=0.5)
            break
        elif choice == "register_client":
            register_gui = RegisterClientGUI(catalog_clients)
            register = register_gui.run()
            if register:
                clients_repo.add(register)
                clients_repo.save()
        elif choice == "register_account":
            if not catalog_clients:
                sg.popup_ok("Nenhum cliente cadastrado. Cadastre um cliente antes de criar accounts.")
                continue
            account_gui = RegisterAccountGUI(catalog_clients, catalog_accounts)
            new_account = account_gui.run()
            if len(new_account) > 0:
                accounts_repo.add(new_account)
                accounts_repo.save()
        elif choice == "list_accounts":
            list_accounts = accounts_repo.list_accounts()
            list_number_banks = [account['number_bank'] for account in list_accounts]
            list_accounts_gui = ListAccountsGUI(list_number_banks)
            list_accounts_gui.run()
        elif choice == "login":
            if not catalog_clients or not catalog_accounts:
                sg.popup_ok("Nenhuma conta/cliente cadastrados. Crie para acessar.")
                continue
            login_gui = LoginGUI(catalog_clients, catalog_accounts)
            banking_operation = login_gui.run()
            if not banking_operation:
                continue
            bankGui = BankGUI(banking_operation)
            updated_operation = bankGui.run()
            # updated_operation['account']
            if updated_operation:
                fieldnames = ["agency_bank", "number_bank", "holder_account", "balance", "cpf_client"]
                with open(path_filename_accounts, "a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    for account in catalog_accounts:
                        writer.writerow({key: str(account.get(key, "")) for key in fieldnames})
        else:
            continue


def is_files() -> tuple[AccountRepository, list[dict[str, str]], list[dict[str, str]], ClientRepository, Path]:
    client_csv = "list_client.csv"
    path_filename_client = ROOT_PATH / client_csv
    create_file(path_filename_client)
    clients_repo = ClientRepository(str(path_filename_client))
    catalog_clients = clients_repo.all()

    accounts_csv = "list_accounts.csv"
    path_filename_accounts = ROOT_PATH / accounts_csv
    create_file(path_filename_accounts)
    accounts_repo = AccountRepository(str(path_filename_accounts))
    catalog_accounts = accounts_repo.all()

    history_csv = "list_histories.csv"
    path_filename_history = ROOT_PATH / history_csv
    create_file(path_filename_history)
    HistoryRepository(str(path_filename_history))
    return accounts_repo, catalog_accounts, catalog_clients, clients_repo, path_filename_accounts


if __name__ == "__main__":
    main()
