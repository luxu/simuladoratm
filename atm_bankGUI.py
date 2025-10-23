import FreeSimpleGUI as sg

from partials import elements_screen
from atm_service import BankOperation

class BankGUI:
    def __init__(self, banking_operation):
        sg.theme("SystemDefault")
        self.bank_operation = banking_operation
        total = banking_operation['account'][0]['total']
        self.bankOperation = BankOperation(total)
        layout = elements_screen.get_layout(banking_operation)
        self.window = sg.Window("Simulador Caixa Eletrônico - Estilo CAIXA", layout, finalize=True, background_color="#BFBFBF")

    def screen_update(self, msg):
        self.window["-SCREEN-"].update(msg)

    def run(self):
        operacao_atual = None
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-EXIT-"):
                sg.popup_auto_close("Saindo...", auto_close_duration=0.5)
                break
            # Teclado numérico insere no campo de valor
            if isinstance(event, str) and event.isdigit():
                self.window["-VALUE-"].update(values["-VALUE-"] + event)
            if event == "-RESET-":
                self.window["-VALUE-"].update("")

            # Seleção de operação
            if event in ("-BALANCE-", "-EXTRACT-", "-SAKE-", "-DEPOSIT-"):
                operacao_atual = event
                if event == "-BALANCE-":
                    msg = f"Saldo atual: R$ {float(self.bankOperation.balance()):.2f}"
                elif event == "-EXTRACT-":
                    operacoes = self.bankOperation.extract()
                    msg = "Últimas operações:\n" + "\n".join(operacoes[-5:]) if operacoes else "Nenhuma movimentação registrada."
                else:
                    msg = f"Digite o valor para {event[1:].capitalize().lower()} e pressione Confirmar."
                self.screen_update(msg)

            # Confirmar operação
            if event in {"-CONFIRM-", "-OK-"}:
                if operacao_atual in ("-SAKE-", "-DEPOSIT-"):
                    try:
                        value = float(values["-VALUE-"])
                        msg = ''
                        if operacao_atual == "-SAKE-":
                            success, msg = self.bankOperation.sake(value)
                            if success:
                                msg += f"\nSaldo atual: R$ {float(self.bankOperation.balance()):.2f}"
                        elif operacao_atual == "-DEPOSIT-":
                            success, msg = self.bankOperation.deposit(value)
                            if success:
                                msg += f"\nSaldo atual: R$ {float(self.bankOperation.balance()):.2f}"
                        self.window["-VALUE-"].update("")
                    except ValueError as err:
                        msg = f'Erro ao realizar {operacao_atual[1:].capitalize()}: {err}'
                    self.screen_update(msg)
                operacao_atual = None

            # Cancelar
            if event == "-CANCEL-":
                operacao_atual = None
                self.window["-VALUE-"].update("")
                self.screen_update("Operação cancelada. Escolha outra opção.")
        self.window.close()
