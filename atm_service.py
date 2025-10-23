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

    def deposit(self, value):
        value_old = f'R$ {float(self.account):.2f}'
        self.account += float(value)
        value = f'R$ {float(value):.2f}'
        value_new = f'R$ {float(self.account):.2f}'
        msg = f"{value} | +{value_old} | {value_new}"
        self.operation.append(msg)
        return True, f"Depósito de R$ {value} realizado."

    def sake(self, value):
        # Verifica se tem saldo suficiente
        if not self.is_value(value):
            return False, "Valor maior do que saldo. Reveja!"
        value_old = f'R$ {float(self.account):.2f}'
        self.account -= float(value)
        value = f'R$ {float(value):.2f}'
        value_new = f'R$ {float(self.account):.2f}'
        msg = f"{value} | -{value_old} | {value_new}"
        self.operation.append(msg)
        return True, f"Saque de R$ {value} realizado."
