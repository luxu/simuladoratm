import re

from typing import Optional

import FreeSimpleGUI as sg

from modelos import Cliente, ContaCorrente


class ContaGUI:
    """Interface para criação de novas contas vinculadas a um cliente existente."""

    def __init__(self, clientes: dict[str, Cliente]):
        sg.theme("SystemDefault")
        self.clientes = clientes
        self.layout = [
            [
                sg.Text(
                    "Cadastrar nova conta para cliente existente",
                    font=("Arial", 14, "bold"),
                )
            ],
            [
                sg.Text("CPF do cliente", size=(18, 1)),
                sg.Input(key="-CPF-", focus=True, enable_events=True),
            ],
            [
                sg.Text("Nome do cliente", size=(18, 1)),
                sg.Input(key="-NOME-", disabled=True, use_readonly_for_disable=True),
            ],
            [
                sg.Text("Senha cadastrada", size=(18, 1)),
                sg.Input(
                    key="-SENHA-",
                    password_char="*",
                    disabled=True,
                    use_readonly_for_disable=True,
                ),
            ],
            [
                sg.Text("Depósito inicial", size=(18, 1)),
                sg.Input(key="-DEPOSITO-"),
            ],
            [
                sg.Text(
                    "",
                    key="-ERROS-",
                    size=(45, 3),
                    text_color="red",
                    background_color="lightyellow",
                    visible=False,
                )
            ],
            [
                sg.Push(),
                sg.Button("Cancelar", key="-CANCELAR-", button_color=("white", "#A93226")),
                sg.Button(
                    "Cadastrar conta",
                    key="-CADASTRAR-",
                    button_color=("white", "#117A65"),
                ),
            ],
        ]
        self.window = sg.Window("Nova conta", self.layout, finalize=True)

    @staticmethod
    def _sanitizar_cpf(cpf: str) -> str:
        return re.sub(r"\D", "", cpf or "")

    def _atualizar_cliente(self, cpf: str) -> Optional[Cliente]:
        cpf_limpo = self._sanitizar_cpf(cpf)
        cliente = self.clientes.get(cpf_limpo)
        if cliente:
            self.window["-NOME-"].update(cliente.nome)
            self.window["-SENHA-"].update("********")
            self.window["-ERROS-"].update("", visible=False)
        else:
            self.window["-NOME-"].update("")
            self.window["-SENHA-"].update("")
            if len(cpf_limpo) == 11:
                self.window["-ERROS-"].update(
                    "Cliente não encontrado. Cadastre o cliente antes de criar a conta.",
                    visible=True,
                )
            else:
                self.window["-ERROS-"].update("", visible=False)
        return cliente

    def _validar(self, values):
        erros: list[str] = []
        cpf_limpo = self._sanitizar_cpf(values.get("-CPF-", ""))
        if len(cpf_limpo) != 11:
            erros.append("CPF deve conter 11 dígitos numéricos.")

        cliente = self.clientes.get(cpf_limpo) if not erros else None
        if cliente is None and not erros:
            erros.append("Cliente não encontrado. Cadastre o cliente antes de criar a conta.")

        deposito_raw = (values.get("-DEPOSITO-", "") or "0").replace(",", ".")
        try:
            deposito = float(deposito_raw)
            if deposito < 0:
                erros.append("Depósito inicial não pode ser negativo.")
        except ValueError:
            erros.append("Informe um valor numérico para o depósito inicial.")
            deposito = 0.0

        return erros, {"cliente": cliente, "deposito": deposito}

    def run(self):
        cadastro = None
        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break

            if event == "-CPF-":
                self._atualizar_cliente(values.get("-CPF-", ""))

            if event == "-CADASTRAR-":
                erros, resultado = self._validar(values)
                if erros:
                    self.window["-ERROS-"].update("\n".join(erros), visible=True)
                    continue
                self.window["-ERROS-"].update("", visible=False)
                cliente = resultado["cliente"]
                assert cliente is not None
                conta = ContaCorrente(cliente, saldo_inicial=resultado["deposito"])
                cadastro = {"cliente": cliente, "conta": conta}
                break

        self.window.close()
        return cadastro
