import re

import FreeSimpleGUI as sg

from modelos import Cliente


class LoginGUI:
    def __init__(self, clientes: dict[str, Cliente]):
        sg.theme("SystemDefault")
        self.clientes = clientes
        self.layout = [
            [sg.Text("Acesso ao Banco", font=("Arial", 14, "bold"))],
            [sg.Text("CPF", size=(18, 1)), sg.Input(key="-CPF-", focus=True, enable_events=True)],
            [sg.Text("Senha", size=(18, 1)), sg.Input(key="-SENHA-", password_char="*")],
            [
                sg.Text("Conta", size=(18, 1)),
                sg.Combo(
                    [],
                    key="-CONTA-",
                    readonly=True,
                    size=(24, 1),
                    enable_events=False,
                ),
            ],
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
                sg.Button("Entrar", key="-ENTRAR-", button_color=("white", "#1E8449")),
            ],
        ]
        self.window = sg.Window("Login", self.layout, finalize=True)

    @staticmethod
    def _sanitizar_cpf(cpf: str) -> str:
        return re.sub(r"\D", "", cpf or "")

    def _atualizar_contas_disponiveis(self, cpf: str) -> None:
        cpf_numeros = self._sanitizar_cpf(cpf)
        cliente = self.clientes.get(cpf_numeros)
        contas = [conta.id for conta in cliente.contas] if cliente else []
        valor_padrao = contas[0] if len(contas) == 1 else ""
        self.window["-CONTA-"].update(values=contas, value=valor_padrao)

    def _validar(self, values):
        erros = []
        cpf = self._sanitizar_cpf(values.get("-CPF-", ""))
        senha = values.get("-SENHA-", "")
        conta_id = values.get("-CONTA-", "")

        cliente = self.clientes.get(cpf)
        if cliente is None:
            erros.append("CPF não encontrado. Cadastre-se primeiro.")
            return erros, None

        if cliente.senha != senha:
            erros.append("Senha incorreta.")

        if not cliente.contas:
            erros.append("Cliente não possui contas cadastradas.")

        conta = None
        if not erros:
            if conta_id:
                conta = next((c for c in cliente.contas if c.id == conta_id), None)
            elif len(cliente.contas) == 1:
                conta = cliente.contas[0]
            else:
                erros.append("Selecione a conta para continuar.")
        return erros, {"cliente": cliente, "conta": conta}

    def run(self):
        acesso = None
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-CPF-":
                self._atualizar_contas_disponiveis(values.get("-CPF-", ""))
            if event == "-ENTRAR-":
                erros, acesso = self._validar(values)
                if erros:
                    self.window["-ERROS-"].update("\n".join(erros), visible=True)
                    continue
                self.window["-ERROS-"].update("", visible=False)
                break
        self.window.close()
        return acesso
