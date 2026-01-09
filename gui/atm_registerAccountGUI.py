import string
from random import randint, choice

import FreeSimpleGUI as sg

from tools.atm_tools import search_name_by_cpf, is_account_exists


class RegisterAccountGUI:
    def __init__(self, clients, accounts):
        sg.theme("SystemDefault")
        self.clients = clients
        self.accounts = accounts
        self.cpf_cliente = [client['cpf'] for client in self.clients]
        self.account_section = [
            [sg.Text("Tem contas?:", size=(18, 1)),sg.Text("", size=(30, 1), key="-IS_COUNT-")],
            [sg.Text("Lista de contas:", size=(18, 1))],
            [sg.Multiline("", size=(50, 5), key="-ACCOUNTS-LIST-", disabled=True)],
        ]
        self.layout = [
            [sg.Text("Cadastrar Conta", font=("Arial", 14, "bold"), )],
            [sg.Text("CPF do cliente", size=(18, 1)),sg.Combo(self.cpf_cliente, size=(18, 1), key="-CPF-", enable_events=True)],
            [sg.Text("Nome:", size=(18, 1)),sg.Text("", size=(30, 1), key="-NOME-")],
            [sg.Text("Nova conta:", size=(18, 1)),sg.Text("", size=(30, 1), key="-NEW_ACCOUNT-")],
            [sg.Column(self.account_section, key='-ACCOUNT-SECTION-', visible=False)],
            [sg.Push(), sg.Button("Cancelar", key="-CANCEL-", button_color=("white", "#A93226")),
             sg.Button("Cadastrar conta", key="-REGISTER-", button_color=("white", "#117A65"), ), ],
        ]
        self.window = sg.Window("Nova conta", self.layout, finalize=True)


    def run(self):
        register_account = {}
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-CANCEL-"):
                register_account = {}
                msg = f"Cadastramento cancelado!{register_account}"
                print(msg)
                break
            if event == "-CPF-":
                data_client = search_name_by_cpf(values.get("-CPF-", ""), self.clients)
                print(data_client)
                cpf_client = data_client.get('cpf')
                if cpf_client:
                    self.window["-NOME-"].update(data_client['name'], visible=True)
                    accounts = is_account_exists(cpf_client, self.accounts)
                    if len(accounts) > 0:
                        list_accounts = []
                        for account in accounts:
                            number_bank = account.get('number_bank')
                            list_accounts.append(number_bank)
                        print(f'Info account..: {accounts}')
                        msg = f'Contas cadastradas: {list_accounts}'
                        self.window["-IS_COUNT-"].update(len(accounts))
                        self.window["-ACCOUNTS-LIST-"].update(msg)
                        self.window["-ACCOUNT-SECTION-"].update(visible=True)
                    else:
                        print('Nao tem conta cadastrada!')
                        self.window["-ACCOUNT-SECTION-"].update(visible=False)
                    account_number_new = f"{randint(100000, 999999)}-{choice(string.ascii_uppercase + string.digits)}"
                    while is_account_exists(account_number_new, self.accounts):
                        account_number_new = f"{randint(100000, 999999)}-{choice(string.ascii_uppercase + string.digits)}"
                    print(f'Nova conta gerada: {account_number_new}')
                    self.window["-NEW_ACCOUNT-"].update(account_number_new)
                    # fieldnames = ["agencia", "numero", "titular", "saldo"]
                    # fieldnames = ["agency_bank", "number_bank", "holder_account", "balance"]
                    register_account = {
                        'agency_bank': '0001',
                        'number_bank': account_number_new,
                        'cpf_client': cpf_client,
                        'balance': 0.0,
                        'holder_account': self.clients[0].get('name')
                    }
                    print(f'Conta cadastrada com sucesso..! {register_account}')
            if event == "-REGISTER-":
                break
        self.window.close()
        return register_account

