import FreeSimpleGUI as sg

from caixa_eletronico_cadastroGUI import CadastroGUI
from caixa_eletronico_contaGUI import ContaGUI
from caixa_eletronico_loginGUI import LoginGUI
from caixa_eletronico_service import OperacaoBancaria
from caixa_eletronico_telaInicialGUI import TelaInicialGUI
from modelos import Cliente, ContaCorrente


class BancoGUI:
    def __init__(self, operacao_bancaria, conta_corrente: ContaCorrente):
        sg.theme("SystemDefault")
        self.conta_corrente = conta_corrente
        self.operacao_bancaria = operacao_bancaria
        cliente = self.conta_corrente.cliente
        # Cabeçalho com logotipo e título
        self.header = [
            [
                sg.Push(background_color="#003366"),
                sg.Image(filename="logo_caixa.png", size=(120, 50), background_color="#003366"),
                sg.Column(
                    [
                        [
                            sg.Text(
                                "SIMULADOR CAIXA ELETRÔNICO",
                                font=("Arial", 14, "bold"),
                                text_color="white",
                                background_color="#003366",
                                pad=(0, 0),
                            )
                        ],
                        [
                            sg.Text(
                                "AUTOATENDIMENTO",
                                font=("Arial", 11),
                                text_color="white",
                                background_color="#003366",
                                pad=(0, 0),
                            )
                        ],
                    ],
                    background_color="#003366",
                    pad=(10, 5),
                    element_justification="center",
                ),
                sg.Push(background_color="#003366"),
            ],
        ]
        self.header_frame = sg.Frame(
            "",
            self.header,
            background_color="#003366",
            border_width=0,
            pad=(0, 0),
            element_justification="center",
            expand_x=True,
        )
        mensagem_inicial = "Bem-vindo ao Autoatendimento CAIXA"
        if cliente:
            mensagem_inicial = (
                f"Bem-vindo, {cliente.nome}!\n"
                f"Conta ativa: {self.conta_corrente.id}\n"
                f"Saldo atual: R$ {self.conta_corrente.saldo:.2f}"
            )

        self.display_layout = [
            [sg.Text("AUTO-ATENDIMENTO", font=("Arial", 12, "bold"), text_color="white", background_color="#003366")],
            [
                sg.Multiline(
                    f"{mensagem_inicial}\n\nSelecione uma operação utilizando os botões laterais.",
                    size=(40, 10),
                    key="-TELA-",
                    disabled=True,
                    background_color="#0060A8",
                    text_color="white",
                    border_width=0,
                    font=("Consolas", 11),
                    pad=(5, 5),
                )
            ],
        ]
        self.display_frame = sg.Frame("", self.display_layout, background_color="#003366", border_width=0, pad=(0, 0))

        # Botões laterais
        self.left_buttons = [
            [sg.Button("Saldo", size=(8, 2), button_color=("black", "#C0C0C0"), key="-SALDO-")],
            [sg.Button("Saque", size=(8, 2), button_color=("black", "#C0C0C0"), key="-SAQUE-")],
            [sg.Button("Depósito", size=(8, 2), button_color=("black", "#C0C0C0"), key="-DEPOSITO-")],
            [sg.Button("Extrato", size=(8, 2), button_color=("black", "#C0C0C0"), key="-EXTRATO-")],
        ]
        self.right_buttons = [
            [sg.Button("Cancelar", size=(8, 2), button_color=("white", "#A93226"), key="-CANCELA-")],
            [sg.Button("Confirmar", size=(8, 2), button_color=("white", "#1E8449"), key="-CONFIRMA-")],
            [sg.Button("Limpar", size=(8, 2), button_color=("black", "#F1C40F"), key="-LIMPA-")],
            [sg.Button("Sair", size=(8, 2), button_color=("white", "#2E86C1"), key="-SAIR-")],
        ]
        # Teclado numérico (opcional)
        self.teclado_layout = [
            [sg.Button(str(i), size=(4, 2), font=("Arial", 10, "bold")) for i in range(1, 4)],
            [sg.Button(str(i), size=(4, 2), font=("Arial", 10, "bold")) for i in range(4, 7)],
            [sg.Button(str(i), size=(4, 2), font=("Arial", 10, "bold")) for i in range(7, 10)],
            [sg.Push(), sg.Button("0", size=(4, 2), font=("Arial", 10, "bold")), sg.Push()],
        ]
        # Linha do valor
        valor_layout = [
            [
                sg.Text("Valor: R$", font=("Arial", 11)),
                sg.Input(key="-VALOR-", size=(15, 1), font=("Arial", 11)),
                sg.Button("OK", key="-OK-"),
            ]
        ]
        # Layout completo
        self.layout = [
            [self.header_frame],
            [
                sg.Frame(
                    "",
                    [
                        [
                            sg.Text(
                                f"Cliente: {cliente.nome}",
                                font=("Arial", 10, "bold"),
                                text_color="black",
                                background_color="#C0C0C0",
                            ),
                            sg.Push(),
                            sg.Text(
                                f"Conta: {self.conta_corrente.id}",
                                key="-CONTA-ATIVA-",
                                font=("Arial", 10, "bold"),
                                text_color="black",
                                background_color="#C0C0C0",
                            ),
                        ]
                    ],
                    pad=(10, 0),
                    background_color="#C0C0C0",
                    border_width=0,
                )
            ],
            [
                sg.Column(self.left_buttons, element_justification="right", pad=(10, 10)),
                sg.Frame("", [[self.display_frame]], background_color="#C0C0C0", pad=(10, 10), border_width=5),
                sg.Column(self.right_buttons, pad=(10, 10)),
            ],
            [sg.HorizontalSeparator()],
            [sg.Frame("Entrada de Valor", valor_layout, border_width=1, background_color="#E8E8E8")],
            [
                sg.Frame(
                    "Teclado Numérico",
                    self.teclado_layout,
                    border_width=1,
                    background_color="#E8E8E8",
                    pad=(0, 10),
                    element_justification="center",
                )
            ],
        ]
        self.title = "Simulador Caixa Eletrônico"
        self.window = sg.Window(
            "Simulador Caixa Eletrônico - Estilo CAIXA", self.layout, finalize=True, background_color="#BFBFBF"
        )

    def atualizar_tela(self, msg):
        """Atualiza a tela de mensagens"""
        self.window["-TELA-"].update(msg)

    # def registrar(self, operacao, valor=0):
    #     """Salva operação no extrato"""
    #     ...
    #     self.extrato.append(f"{operacao}: R$ {valor:.2f}" if valor else operacao)

    def run(self):
        operacao_atual = None
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-SAIR-"):
                sg.popup_auto_close("Saindo...", auto_close_duration=0.5)
                break

            # Teclado numérico insere no campo de valor
            if isinstance(event, str) and event.isdigit():
                self.window["-VALOR-"].update(values["-VALOR-"] + event)

            # Limpar campo
            if event == "-LIMPA-":
                self.window["-VALOR-"].update("")

            # Seleção de operação
            if event in ("-SALDO-", "-SAQUE-", "-DEPOSITO-", "-EXTRATO-"):
                operacao_atual = event
                if event == "-SALDO-":
                    msg = f"Saldo atual: R$ {self.operacao_bancaria.mostrar_saldo():.2f}"
                    self.atualizar_tela(msg)
                    # self.registrar("Consulta de saldo")
                elif event == "-EXTRATO-":
                    operacoes = self.operacao_bancaria.extrato()
                    if operacoes:
                        msg = "Últimas operações:\n" + "\n".join(operacoes[-5:])
                    else:
                        msg = "Nenhuma movimentação registrada."
                    self.atualizar_tela(msg)
                else:
                    msg = f"Digite o valor para {event[1:].capitalize().lower()} e pressione Confirmar."
                    self.atualizar_tela(msg)

            # Confirmar operação
            if event in {"-CONFIRMA-", "-OK-"}:
                if operacao_atual in ("-SAQUE-", "-DEPOSITO-"):
                    try:
                        valor = float(values["-VALOR-"])
                        if operacao_atual == "-SAQUE-":
                            sucesso, mensagem = self.operacao_bancaria.saque(valor)
                            if sucesso:
                                mensagem += f"\nSaldo atual: R$ {self.operacao_bancaria.mostrar_saldo():.2f}"
                            self.atualizar_tela(mensagem)
                        elif operacao_atual == "-DEPOSITO-":
                            sucesso, msg = self.operacao_bancaria.deposito(valor)
                            if sucesso:
                                msg += f"\nSaldo atual: R$ {self.operacao_bancaria.mostrar_saldo():.2f}"
                            self.atualizar_tela(msg)
                        self.window["-VALOR-"].update("")
                    except ValueError:
                        self.atualizar_tela("Digite um valor válido.")
                operacao_atual = None

            # Cancelar
            if event == "-CANCELA-":
                operacao_atual = None
                self.window["-VALOR-"].update("")
                self.atualizar_tela("Operação cancelada. Escolha outra opção.")

        self.window.close()


def main():
    catalogo_clientes: dict[str, Cliente] = {}
    catalogo_contas: dict[str, ContaCorrente] = {}

    while True:
        tela_inicial = TelaInicialGUI()
        escolha = tela_inicial.run()

        if escolha is None:
            break

        conta_selecionada: ContaCorrente | None = None
        cliente_selecionado: Cliente | None = None

        if escolha == "cadastro_cliente":
            cadastro_gui = CadastroGUI(catalogo_clientes)
            cadastro = cadastro_gui.run()
            if cadastro is None:
                continue
            cliente_selecionado = cadastro["cliente"]
            conta_selecionada = cadastro["conta"]
            catalogo_clientes[cliente_selecionado.cpf] = cliente_selecionado
            catalogo_contas[conta_selecionada.id] = conta_selecionada
        elif escolha == "cadastro_conta":
            if not catalogo_clientes:
                sg.popup_ok(
                    "Nenhum cliente cadastrado. Cadastre um cliente antes de criar contas."
                )
                continue
            conta_gui = ContaGUI(catalogo_clientes)
            cadastro_conta = conta_gui.run()
            if cadastro_conta is None:
                continue
            cliente_selecionado = cadastro_conta["cliente"]
            conta_selecionada = cadastro_conta["conta"]
            catalogo_contas[conta_selecionada.id] = conta_selecionada
        elif escolha == "login":
            if not catalogo_clientes:
                sg.popup_ok("Nenhum cliente cadastrado. Crie uma conta para acessar.")
                continue
            login_gui = LoginGUI(catalogo_clientes)
            acesso = login_gui.run()
            if acesso is None:
                continue
            cliente_selecionado = acesso["cliente"]
            conta_selecionada = acesso["conta"]
        else:
            continue

        if conta_selecionada is None:
            continue

        operacao_bancaria = OperacaoBancaria(conta_selecionada)
        banco_gui = BancoGUI(operacao_bancaria, conta_corrente=conta_selecionada)
        banco_gui.run()


if __name__ == "__main__":
    main()
