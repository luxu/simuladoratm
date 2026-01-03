from abc import ABC, abstractproperty
from datetime import datetime
import textwrap
import random
from pathlib import Path

NUMERO_TRANSACOES = 2


class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência: \t{conta.agencia}
            Número: \t\t{conta.numero}
            Titular: \t{conta.cliente.nome}
            Saldo: \t\tR$ {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


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
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.cpf}')>)"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        if valor < 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor < 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        self._saldo = valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def __repr__(self):
        return f"""<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"""

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
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d-%m-%Y %H:%M:%S"
            ).date()
            if data_transacao == data_atual:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self): ...

    @abstractproperty
    def registrar(self, conta): ...


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nome_funcao = func.__name__.upper()
        resultado = func(*args, **kwargs)
        root_path = Path(__file__).parent
        with open(root_path / "log.txt", "a", encoding="utf-8") as arquivo:
            msg = (
                f"[{data_hora}] Função '{nome_funcao}' executada com argumentos ({args}) e {kwargs}. "
                f"Retornou {resultado}\n"
            )
            arquivo.write(msg)
        return resultado

    return envelope


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def recuperar_conta_cliente(cliente):
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    if not filtrar_cliente(cpf, clientes):
        print(f"Cliente do CPF..:{cpf} não encontrado. Cadastre-o primeiro.")
        return
    # valor = input("Informe o valor do depósito:")


@log_transacao
def sacar(clientes): ...


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
        extrato += f"\n{transacao['data']}\n{transacao['tipo']: \n\tR$ {transacao['valor']: .2f}}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}\n")
    print("===============================================")


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome do cliente: ")
    data_nascimento = input("Informe a data de nascimento do cliente (dd-mm-aaaa): ")
    endereco = input(
        "Informe do endereço (logradouro, nro - bairro - cidade/sigla estado):"
    )

    data = {
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
        "data_nascimento": data_nascimento,
    }

    cliente = PessoaFisica(**data)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(clientes, contas):
    print(f"Os clientes do banco:\n{clientes}")
    cpf_escolhido = input("\nInforme o CPF do cliente: ")
    nome_cliente = ""
    for cliente in clientes:
        if cliente.get("cpf") == cpf_escolhido:
            nome_cliente = cliente.get("nome")
    print(f"Bem vindo...{nome_cliente}. Vamos criar uma conta...")
    nro_conta = ""
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
    =============== MENU ==================
    [d]     Depositar
    [s]     Sacar
    [e]     Exibir extrato
    [nc]    Nova conta
    [lc]    Listar conta
    [nu]    Novo usuário
    [q]     Sair
    """
    print(opcoes_menu)
    choice = input("Digite as opções abaixo:\n")
    return choice


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        match opcao:
            case "d":
                depositar(clientes)
            case "s":
                sacar(clientes)
            case "nu":
                criar_cliente(clientes)
            case "e":
                exibir_extrato(clientes)
            case "nc":
                criar_conta(clientes, contas)
            case "lc":
                listar_contas(contas)
            case "q":
                break
            case _:
                print(
                    "\n@@@ Operação inválida, por favor selecione a operação desejada. @@@"
                )


main()
