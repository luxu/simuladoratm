import re

import FreeSimpleGUI as sg


class LoginGUI:
    def __init__(self, clients, accounts):
        sg.theme("SystemDefault")
        self.clients = clients
        self.accounts = accounts
        self.cpf_cliente = [client['cpf'] for client in self.clients]
        self.layout = [
            [sg.Text("Acesso ao Banco", font=("Arial", 14, "bold"))],
            [sg.Text("CPF", size=(18, 1)), sg.Combo(self.cpf_cliente, size=(18, 1), key="-CPF-", enable_events=True)],
            [sg.Text("Conta", size=(18, 1)),
             sg.Combo([], key="-ACCOUNT-", readonly=True, size=(24, 1), enable_events=False, ), ],
            [sg.Text("", key="-ERRORS-", size=(40, 3), text_color="red", background_color="lightyellow",
                     visible=False, )],
            [sg.Push(), sg.Button("Cancelar", key="-CANCEL-", button_color=("white", "#A93226")),
             sg.Button("Entrar", key="-ENTER-", button_color=("white", "#1E8449")), ],
        ]
        self.window = sg.Window("Login", self.layout, finalize=True)

    @staticmethod
    def _sanitizar_cpf(cpf: str) -> str:
        return re.sub(r"\D", "", cpf or "")

    def _update_accounts_available(self, cpf: str) -> None:
        cpf_number = self._sanitizar_cpf(cpf)
        accounts = [account['number_bank'] for account in self.accounts if account['cpf_client'] == cpf_number]
        valor_padrao = accounts[0] if len(accounts) == 1 else ""
        self.window["-ACCOUNT-"].update(values=accounts, value=valor_padrao)

    def _validate(self, values):
        errors = []
        cpf = self._sanitizar_cpf(values.get("-CPF-", ""))
        account_id = values.get("-ACCOUNT-", "")

        client = None
        if not cpf:
            errors.append("Selecione um CPF para continuar.")
        else:
            matching_clients = [client for client in self.clients if client['cpf'] == cpf]
            if not matching_clients:
                errors.append("CPF não encontrado.")
            else:
                client = matching_clients[0]

        account = []
        if account_id:
            account = [account for account in self.accounts if account['number_bank'] == account_id]
            if not account:
                errors.append("Conta selecionada inválida.")
        else:
            errors.append("Selecione uma conta.")

        if errors:
            return errors, None

        return errors, {"client": client, "account": account}

    def run(self):
        access = None
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-CANCEL-"):
                break
            if event == "-CPF-":
                self._update_accounts_available(values.get("-CPF-"))
            if event == "-ENTER-":
                errors, access = self._validate(values)
                if errors:
                    self.window["-ERRORS-"].update("\n".join(errors), visible=True)
                    continue
                self.window["-ERRORS-"].update("", visible=False)
                break
        self.window.close()
        return access
