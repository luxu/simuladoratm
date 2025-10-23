import FreeSimpleGUI as sg


def _build_side_buttons() -> tuple[list[list[sg.Button]], list[list[sg.Button]]]:
    """Create the side button columns for the banking window."""
    left = [
        [sg.Button("Saldo", size=(8, 2), button_color=("black", "#C0C0C0"), key="-BALANCE-")],
        [sg.Button("Saque", size=(8, 2), button_color=("black", "#C0C0C0"), key="-SAKE-")],
        [sg.Button("Depósito", size=(8, 2), button_color=("black", "#C0C0C0"), key="-DEPOSIT-")],
        [sg.Button("Extrato", size=(8, 2), button_color=("black", "#C0C0C0"), key="-EXTRACT-")],
    ]
    right = [
        [sg.Button("Cancelar", size=(8, 2), button_color=("white", "#A93226"), key="-CANCEL-")],
        [sg.Button("Confirmar", size=(8, 2), button_color=("white", "#1E8449"), key="-CONFIRM-")],
        [sg.Button("Limpar", size=(8, 2), button_color=("black", "#F1C40F"), key="-RESET-")],
        [sg.Button("Voltar ao menu", size=(8, 2), button_color=("white", "#2E86C1"), key="-EXIT-")],
    ]
    return left, right


def _build_value_entry() -> list[list[sg.Element]]:
    """Build the numeric input row used to type custom values."""
    return [[
        sg.Text("Valor: R$", font=("Arial", 11)),
        sg.Input(key="-VALUE-", size=(15, 1), font=("Arial", 11)),
        sg.Button("OK", key="-OK-"),
    ]]


def _build_numeric_keypad() -> list[list[sg.Element]]:
    """Create the keypad buttons used for numeric input."""
    keypad_rows = []
    for start in (1, 4, 7):
        keypad_rows.append([
            sg.Button(str(i), size=(4, 2), font=("Arial", 10, "bold")) for i in range(start, start + 3)
        ])
    keypad_rows.append([
        sg.Push(),
        sg.Button("0", size=(4, 2), font=("Arial", 10, "bold")),
        sg.Push(),
    ])
    return keypad_rows


def _build_header() -> sg.Frame:
    """Construct the header frame for the window."""
    header = [[
        sg.Push(background_color="#003366"),
        sg.Image(filename="logo_caixa.png", size=(120, 50), background_color="#003366"),
        sg.Column([
            [sg.Text(
                "SIMULADOR CX ELETRÔNICO",
                font=("Arial", 14, "bold"),
                text_color="white",
                background_color="#003366",
                pad=(0, 0),
            )],
            [sg.Text(
                "AUTOATENDIMENTO",
                font=("Arial", 11),
                text_color="white",
                background_color="#003366",
                pad=(0, 0),
            )],
        ], background_color="#003366", pad=(10, 5), element_justification="center"),
        sg.Push(background_color="#003366"),
    ]]
    return sg.Frame(
        "",
        header,
        background_color="#003366",
        border_width=0,
        pad=(0, 0),
        element_justification="center",
        expand_x=True,
    )


def get_layout(banking_operation):
    client = banking_operation.get("client")
    current_account = banking_operation.get("account")[0]
    initial_message = (
        f"Bem-vindo, {client['name']}!\n"
        f"Conta ativa: {current_account['number_account']}\n"
        f"Saldo atual: R$ {current_account['total']}"
        if client
        else "Bem-vindo!"
    )
    display_layout = [
        [sg.Text("AUTO-ATENDIMENTO", font=("Arial", 12, "bold"), text_color="white", background_color="#003366")],
        [sg.Multiline(f"{initial_message}\n\nSelecione uma operação utilizando os botões laterais.",
                      size=(40, 10), key="-SCREEN-", disabled=True, background_color="#0060A8", text_color="white",
                      border_width=0, font=("Consolas", 11), pad=(5, 5), )],
    ]
    display_frame = sg.Frame("", display_layout, background_color="#003366", border_width=0, pad=(0, 0))
    left_buttons, right_buttons = _build_side_buttons()
    valor_layout = _build_value_entry()
    teclado_layout = _build_numeric_keypad()
    header_frame = _build_header()
    layout = [
        [header_frame],
        [sg.Frame("", [
            [sg.Text(f"Cliente: {client['name']}", font=("Arial", 10, "bold"), text_color="black",
                     background_color="#C0C0C0", ),
             sg.Push(),
             sg.Text(f"Conta: {current_account['number_account']}", key="-CONTA-ATIVA-", font=("Arial", 10, "bold"),
                     text_color="black", background_color="#C0C0C0", ), ]
        ], pad=(10, 0), background_color="#C0C0C0", border_width=0, )
         ],
        [sg.Column(
            left_buttons, element_justification="right", pad=(10, 10)),
            sg.Frame("", [[display_frame]], background_color="#C0C0C0", pad=(10, 10), border_width=5),
            sg.Column(right_buttons, pad=(10, 10)),
        ],
        [sg.HorizontalSeparator()],
        [sg.Frame("Entrada de Valor", valor_layout, border_width=1, background_color="#E8E8E8")],
        [sg.Frame("Teclado Numérico", teclado_layout, border_width=1, background_color="#E8E8E8", pad=(0, 10),
                  element_justification="center", )],
    ]
    return layout
