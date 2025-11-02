"""
1 - DECORADOR DE LOG

Implemene um decorador que seja aplica a todas as
funções de transações(depósito, saque, criação de contas, etc).
Esse decorador deve registrar (printar) a data e hora de cada
transação, bem como o tipo de transação

---------------------------------------------------
2 - GERADOR DE RELATÓRIOS

Crie um gerador que permita iterar sobre as transações de
uma conta e retorne, uma a uma, as transações que foram
realizdas. Esse gerador deve também ter uma forma de filtrar
as transações baseado em seu tipo (por exemplo, apenas
saques ou apenas depósitos)

---------------------------------------------------
3 - ITERADOR PERSONALIZADO

Implemente um iterador personalizado ContaIterador que
permita iterar sobre todas as contas do banco, retornando
informações básicas de cada conta (número, saldo atual, etc).
"""
import textwrap


class ContaIterador:
    def __init__(self, contas):
        ...

    def __iter__(self):
        ...

    def __next__(self):
        ...

class PessoaFisica(Cliente):
    ...

class Conta:
    ...

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data_hora": transacao.data_hora,
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        ...

class Transacao:
    ...

class Saque(Transacao):
    ...

class Deposito(Transacao):
    ...

def log_transacao(func):
    ...

def menu():
    ...

def filtrar_cliente(cpf, clientes):
    ...

def recuperar_conta_cliente(cliente):
    ...

@log_transacao
def depositar(cliente):
    ...

@log_transacao
def sacar(clientes):
    ...

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=================== EXTRATO ===================")
    # TODO: atualizar a implementação para atualizar o gerador definido em Historio
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}\n")
    print("===============================================")

@log_transacao
def criar_cliente(clientes):
    ...

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    ...

def listar_contas(contas):
    # TODO: alterar implementação, para utilizar a classe ContaIterador
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione a operação desejada. @@@")

main()