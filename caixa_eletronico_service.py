from modelos import ContaCorrente


class OperacaoBancaria:
    def __init__(self, conta: ContaCorrente):
        self.conta = conta
        self.limite_diario_de_saque = 3
        self.limite_maximo_por_saque = 500
        self.opcao = ""

    def atualizar_conta(self, conta: ContaCorrente) -> None:
        """Atualiza a conta alvo das operações bancárias."""
        self.conta = conta

    def validar_se_a_quantia_digitada_nao_eh_negativa(self, dinheiro):
        return dinheiro >= 0

    def deposito(self, dinheiro):
        if not self.validar_se_a_quantia_digitada_nao_eh_negativa(dinheiro):
            return False, "Não é permitido valor negativo. Digite novamente!!!"
        try:
            self.conta.depositar(dinheiro)
        except ValueError as exc:
            return False, str(exc)
        return True, f"Depósito de R$ {dinheiro:.2f} efetuado."

    def tem_saldo(self, valor_a_sacar):
        # Valor requerido é menor que o saldo. Ex. valor a sacar = 100, saldo = 150
        return valor_a_sacar <= self.conta.saldo

    def esta_no_limite_diario_por_saque(self):
        # Enquanto o limite de saque for maior que 0 por sacar
        return self.limite_diario_de_saque > 0

    def valor_por_saque(self, valor):
        # Se o valor requerido for o permitido está autorizado
        return valor <= self.limite_maximo_por_saque

    def saque(self, dinheiro):
        # Verifica se NÃO atingiu o limite diário de saque
        if self.esta_no_limite_diario_por_saque():
            # Verifica se o valor permitido está autorizado
            if not self.valor_por_saque(dinheiro):
                return False, "Não é permitido valor acima de R$ 500,00"
            # Verifica se tem saldo suficiente
            if not self.tem_saldo(dinheiro):
                return False, "Valor maior do que saldo. Reveja!"
            try:
                self.conta.sacar(dinheiro)
            except ValueError as exc:
                return False, str(exc)
            self.limite_diario_de_saque -= 1
        else:
            return False, "Limite máximo por saque diário atingido"
        return True, f"Saque de R$ {dinheiro:.2f} realizado."

    def extrato(self):
        return self.conta.extrato

    def mostrar_saldo(self):
        return self.conta.saldo

    # def main(self):
    #     while self.opcao != "q":
    #         opcao = input("O que deseja fazer? Depositar(d)-Retirada(r)-Extrato(e)-Saldo(s)-Sair(q)..:")
    #         if opcao == "d":
    #             dinheiro = int(input("Digite a quantia a ser depositada...:"))
    #             self.deposito(dinheiro)
    #         elif opcao == "r":
    #             dinheiro = int(input("Digite a quantia a ser sacada..:"))
    #             self.saque(dinheiro)
    #         elif opcao == "s":
    #             print(self.saldo())
    #         elif opcao == "e":
    #             print(self.extrato())
    #         elif opcao == "q":
    #             break
    #         else:
    #             print("Opção inválida. Reveja!!")
