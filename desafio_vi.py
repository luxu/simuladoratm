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
from datetime import datetime
import textwrap
import random

NUMERO_TRANSACOES = 2

class ContaIterador:
    def __init__(self, contas):
        ...

    def __iter__(self):
        ...

    def __next__(self):
        ...


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= NUMERO_TRANSACOES:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


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
                "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_transacao == data_atual:
                transacoes.append(transacao)
        return transacoes


class Transacao:
    ...


class Saque(Transacao):
    ...


class Deposito(Transacao):
    ...


def log_transacao(func):
    # Data/Hora que chamou a função
    # Nome da função (Dep, sacar, etc)
    ...



def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def recuperar_conta_cliente(cliente):
    return cliente.contas[0]


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
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']:\n\tR$ {transacao['valor']:.2f}}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}\n")
    print("===============================================")


def criar_cliente(clientes):
    nome = input("Informe o nome do cliente: ")
    cpf = input("Informe o CPF do cliente: ")
    data = {"nome": nome, "cpf": cpf}
    clientes.append(data)
    return clientes


def criar_conta(clientes, contas):
    print(f'Os clientes do banco:\n{clientes}')
    cpf_escolhido = input("\nInforme o CPF do cliente: ")
    nome_cliente = ''
    for cliente in clientes:
        if cliente.get("cpf") == cpf_escolhido:
            nome_cliente = cliente.get("nome")
    print(f"Bem vindo...{nome_cliente}. Vamos criar uma conta...")
    nro_conta = ''
    for index, _ in enumerate(range(6)):
        nro_conta += "-" if index == 4 else str(random.randint(0, 9))
    dados_conta = {
        "C/C": nro_conta,
        "cliente": nome_cliente,
    }
    # {'nro_conta': '8473-7', 'clientes': {'nome': 'Luciano', 'cpf': '2222'}}
    # {'nro_conta': '8473-7', 'clientes': 'Luciano(2222)'}}
    contas.append(dados_conta)
    return contas


def listar_contas(contas):
    # TODO: alterar implementação, para utilizar a classe ContaIterador
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def menu():
    opcoes_menu = """
    D -> Depositar
    S -> Sacar
    E -> Exibir extrato
    NU -> Criar cliente
    NC -> Criar conta
    LC -> Listar conta
    Q -> Sair    
    """
    print(textwrap.dedent(opcoes_menu))
    choice = input('Digite as opções abaixo:\n')
    return choice


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao.lower() == "d":
            depositar(clientes)
        elif opcao.lower() == "s":
            sacar(clientes)
        elif opcao.lower() == "e":
            exibir_extrato(clientes)
        elif opcao.lower() == "nu":
            criar_cliente(clientes)
        elif opcao.lower() == "nc":
            criar_conta(clientes, contas)
        elif opcao.lower() == "lc":
            listar_contas(contas)
        elif opcao.lower() == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione a operação desejada. @@@")
main()
