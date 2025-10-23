import re

import FreeSimpleGUI as sg

class RegisterClientGUI:
    def __init__(self, clients):
        sg.theme("SystemDefault")
        self.clients = clients
        self.layout = [
            [sg.Text("Cadastrar Cliente - Todas novas contas começam com R$ 1.000,00", font=("Arial", 14, "bold"), )],
            [sg.Text("Nome", size=(18, 1)), sg.Input(key="-NAME-", focus=True)],
            [sg.Text("CPF", size=(18, 1)), sg.Input(key="-CPF-")],
            [sg.Text("", key="-ERROS-", size=(40, 3), text_color="red", background_color="lightyellow",visible=False, )],
            [sg.Push(),sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#A93226")),
                sg.Button("Cadastrar cliente", key="-CADASTRAR-", button_color=("white", "#1E8449"), ),
            ],
        ]
        self.window = sg.Window("Novo cliente", self.layout, finalize=True)

    def _validar_campos(self, values):
        errors = []
        dados = {}
        cpf = values.get("-CPF-", "")
        cpf_numbers = re.sub(r"\D", "", cpf)
        # Validar se os dados não vieram vazios
        if len(cpf_numbers) < 1:
            errors.append("CPF está em branco. Preencha.")
        name = values.get("-NAME-", "").strip()
        if not name:
            errors.append("Nome é obrigatório.")
        # Validar se os dados já existem
        name_client_exists = [client for client in self.clients if client.get('name') == name]
        if name_client_exists:
            errors.append("Nome já cadastrado. Reveja!")
            return errors, dados
        cpf_client_exists = [client for client in self.clients if client.get('cpf') == cpf_numbers]
        if cpf_client_exists:
            errors.append("CPF já cadastrado. Reveja!")
            return errors, dados
        dados = {
            "name": name,
            "cpf": cpf_numbers,
            "password": '123'
        }
        return errors, dados

    def run(self):
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                cadastro = None
                break
            if event == "-CADASTRAR-":
                erros, cadastro = self._validar_campos(values)
                if erros:
                    self.window["-ERROS-"].update("\n".join(erros), visible=True)
                    continue
                self.window["-ERROS-"].update("", visible=False)
                # Se vier NULO quer dizer q o cliente já existe
                if cadastro is None:
                    msg = 'Cliente já está cadastrado. Só criar a conta corrente!'
                else:
                    msg = f'Cliente não cadastrado!\n{cadastro}'
                print(msg)
                break
        self.window.close()
        return cadastro
