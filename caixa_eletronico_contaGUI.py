import re

import FreeSimpleGUI as sg

from modelos import Cliente, ContaCorrente


class ContaGUI:
    def __init__(self, clientes):
        sg.theme("SystemDefault")
        self.clientes = clientes
        self.layout = [
            [sg.Text("Cadastro do Usuário", font=("Arial", 14, "bold"))],
            [sg.Text("Nome", size=(18, 1)), sg.Input(key="-NOME-", focus=True)],
            [sg.Text("CPF", size=(18, 1)), sg.Input(key="-CPF-")],
            [sg.Text("Senha", size=(18, 1)), sg.Input(key="-SENHA-", password_char="*")],
            [sg.Text("Depósito inicial", size=(18, 1)), sg.Input(key="-DEPOSITO-")],
            [
                sg.Text(
                    "",
                    key="-ERROS-",
                    size=(40, 3),
                    text_color="red",
                    background_color="lightyellow",
                    visible=False,
                )
            ],
            [
                sg.Push(),
                sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#A93226")),
                sg.Button("Cadastrar", key="-CADASTRAR-", button_color=("white", "#1E8449")),
            ],
        ]
        self.window = sg.Window("Cadastro", self.layout, finalize=True)

    def _validar_campos(self, values):
        erros = []

        cpf = values.get("-CPF-", "")
        cpf_numeros = re.sub(r"\D", "", cpf)
        if len(cpf_numeros) != 11:
            erros.append("CPF deve conter 11 dígitos numéricos.")

        cliente_existente = self.clientes.get(cpf_numeros)

        nome = values.get("-NOME-", "").strip()
        senha = values.get("-SENHA-", "")

        if cliente_existente is None:
            if not nome:
                erros.append("Nome é obrigatório.")
            if len(senha) < 4:
                erros.append("Senha deve ter pelo menos 4 caracteres.")
        else:
            nome = cliente_existente.nome
            senha = cliente_existente.senha

        deposito_raw = values.get("-DEPOSITO-", "").replace(",", ".")
        try:
            deposito = float(deposito_raw)
            if deposito < 0:
                erros.append("Depósito inicial não pode ser negativo.")
        except ValueError:
            erros.append("Informe um valor numérico para o depósito inicial.")
            deposito = None

        return erros, {
            "nome": nome,
            "cpf": cpf_numeros,
            "senha": senha,
            "deposito_inicial": deposito if deposito is not None else 0.0,
            "cliente_existente": cliente_existente,
        }

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
                cliente = cadastro["cliente_existente"]
                novo_cliente = cliente is None
                if cliente is None:
                    cliente = Cliente(
                        nome=cadastro["nome"],
                        cpf=cadastro["cpf"],
                        senha=cadastro["senha"],
                    )
                    self.clientes[cadastro["cpf"]] = cliente
                conta = ContaCorrente(cliente, saldo_inicial=cadastro["deposito_inicial"])
                cadastro = {
                    "cliente": cliente,
                    "conta": conta,
                    "novo_cliente": novo_cliente,
                }
                break

        self.window.close()
        return cadastro
