import FreeSimpleGUI as sg


class ListAccountsGUI:
    def __init__(self, accounts):
        sg.theme("SystemDefault")
        self.accounts = accounts
        self.layout = [
            [sg.Text("Listar Contas", font=("Arial", 14, "bold"), )],
            [sg.Text("CPF", size=(18, 1)), sg.Input(key="-NUMBER-CPF-")],
            [
                sg.Multiline("", size=(50, 5), key="-ACCOUNTS-LIST-", disabled=True)
            ],
            [
                sg.Push(),
                sg.Button("Carregar Contas", key="-LOAD_ACCOUNTS-", button_color=("white", "#A93226")),
                sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#A93226")),
            ],
        ]
        self.window = sg.Window("Novo cliente", self.layout, finalize=True)

    def run(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-LOAD_ACCOUNTS-":
                cpf = values.get("-NUMBER-CPF-", "")
                list_accounts = []
                for index, account in enumerate(self.accounts):
                    info_account = f'Conta {index + 1}: {account}'
                    list_accounts.append(info_account)
                texto_formatado = "- " + "\n- ".join(list_accounts)
                self.window["-ACCOUNTS-LIST-"].update(texto_formatado)
        self.window.close()
