import csv

import FreeSimpleGUI as sg

from atm_bankGUI import BankGUI
from atm_homeScreenGUI import HomeScreenlGUI
from atm_loginGUI import LoginGUI
from atm_registerAccountGUI import RegisterAccountGUI
from atm_registerClientGUI import RegisterClientGUI


def main():
    catalog_accounts = []
    catalog_clients = []
    with open("list_client.csv", "r") as _f:
        rows = csv.DictReader(_f)
        for row in rows:
            catalog_clients.append({
                'name': row['name'].strip(),
                'cpf': row['cpf'].strip(),
                'password': row['password'].strip(),
            })
    with open("list_accounts.csv", "r") as _f:
        rows = csv.DictReader(_f)
        for row in rows:
            catalog_accounts.append({
                'cpf': row['cpf'].strip(),
                'number_account': row['number_account'].strip(),
                'total': row['total'].strip(),
            })
    while True:
        home_screen = HomeScreenlGUI()
        choice = home_screen.run()
        if choice is None:
            sg.popup_auto_close("Saindo...", auto_close_duration=0.5)
            break
        if choice == "register_client":
            register_gui = RegisterClientGUI(catalog_clients)
            register = register_gui.run()
            if register:
                catalog_clients.append(register)
        elif choice == "register_account":
            if not catalog_clients:
                sg.popup_ok("Nenhum cliente cadastrado. Cadastre um cliente antes de criar accounts.")
                continue
            account_gui = RegisterAccountGUI(catalog_clients, catalog_accounts)
            new_account = account_gui.run()
            if len(new_account) > 0:
                catalog_accounts.append(new_account)
        elif choice == "login":
            if not catalog_clients or not catalog_accounts:
                sg.popup_ok("Nenhuma conta/cliente cadastrados. Crie para acessar.")
                continue
            login_gui = LoginGUI(catalog_clients, catalog_accounts)
            banking_operation = login_gui.run()
            bankGui = BankGUI(banking_operation)
            bankGui.run()
        else:
            continue

if __name__ == "__main__":
    main()
