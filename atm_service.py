from functools import wraps


def ensure_positive_amount(fn):
    """Validate and sanitize monetary values before executing the operation."""

    @wraps(fn)
    def wrapper(self, value, *args, **kwargs):
        error_msg = "Valor inválido. Informe um número maior que zero."
        try:
            amount = float(str(value).replace(",", "."))
        except (TypeError, ValueError):
            return False, error_msg

        if amount <= 0:
            return False, error_msg

        return fn(self, amount, *args, **kwargs)

    return wrapper


class BankOperation:
    def __init__(self, account):
        self.account = float(account)
        self.operation = []

    def is_value(self, amount_to_withdraw):
        # Valor requerido é menor que o saldo. Ex. valor a sacar = 100, saldo = 150
        return amount_to_withdraw <= self.account

    def balance(self):
        return self.account

    def extract(self):
        return self.operation

    @ensure_positive_amount
    def deposit(self, amount):
        value_old = f'R$ {float(self.account):.2f}'
        self.account += amount
        value_formatted = f'R$ {amount:.2f}'
        value_new = f'R$ {float(self.account):.2f}'
        msg = f"{value_formatted} | +{value_old} | {value_new}"
        self.operation.append(msg)
        return True, f"Depósito de {value_formatted} realizado."

    @ensure_positive_amount
    def sake(self, amount):
        # Verifica se tem saldo suficiente
        if not self.is_value(amount):
            return False, "Valor maior do que saldo. Reveja!"
        value_old = f'R$ {float(self.account):.2f}'
        self.account -= amount
        value_formatted = f'R$ {amount:.2f}'
        value_new = f'R$ {float(self.account):.2f}'
        msg = f"{value_formatted} | -{value_old} | {value_new}"
        self.operation.append(msg)
        return True, f"Saque de {value_formatted} realizado."
