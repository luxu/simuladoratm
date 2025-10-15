import FreeSimpleGUI as sg


class TelaInicialGUI:
    """Tela inicial do simulador com as opções principais."""

    def __init__(self):
        sg.theme("SystemDefault")
        self.layout = [
            [
                sg.Text(
                    "Simulador Caixa Eletrônico",
                    font=("Arial", 16, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Push(),
                sg.Button(
                    "Entrar no banco",
                    key="-LOGIN-",
                    size=(18, 2),
                    button_color=("white", "#2E86C1"),
                ),
                sg.Push(),
            ],
            [
                sg.Push(),
                sg.Button(
                    "Criar nova conta",
                    key="-CADASTRO-",
                    size=(18, 2),
                    button_color=("white", "#1E8449"),
                ),
                sg.Push(),
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Push(),
                sg.Button("Sair", key="-SAIR-", button_color=("white", "#A93226")),
                sg.Push(),
            ],
        ]
        self.window = sg.Window("Bem-vindo", self.layout, finalize=True)

    def run(self):
        escolha = None
        while True:
            event, _ = self.window.read()
            if event in (sg.WIN_CLOSED, "-SAIR-"):
                break
            if event == "-LOGIN-":
                escolha = "login"
                break
            if event == "-CADASTRO-":
                escolha = "cadastro"
                break
        self.window.close()
        return escolha
