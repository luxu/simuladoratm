"""Modelos de domínio do simulador de caixa eletrônico."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4


class ContaCorrente:
    """Representa uma conta corrente vinculada a um cliente."""
    def __init__(self, cliente: "Cliente", *, conta_id: Optional[str] = None, saldo_inicial: float = 0.0) -> None:
        self.id: str = conta_id or str(uuid4())
        self._cliente: Optional["Cliente"] = None
        self.total: float = 0.0
        self.extrato: List[str] = []
        self.vincular_cliente(cliente)
        if saldo_inicial:
            self.depositar(saldo_inicial, descricao="Depósito inicial")

    @property
    def cliente(self) -> "Cliente":
        assert self._cliente is not None
        return self._cliente

    def vincular_cliente(self, cliente: "Cliente") -> None:
        if self._cliente is not None and self._cliente is not cliente:
            raise ValueError("Conta já vinculada a outro cliente.")
        self._cliente = cliente
        if self not in cliente.contas:
            cliente.contas.append(self)

    def registrar_operacao(self, tipo: str, valor: float, descricao: Optional[str] = None) -> None:
        rotulo = f"{tipo} -> R$ {valor:.2f}"
        if descricao:
            rotulo = f"{rotulo} ({descricao})"
        self.extrato.append(rotulo)

    def depositar(self, valor: float, descricao: Optional[str] = None) -> None:
        if valor < 0:
            raise ValueError("Não é permitido valor negativo.")
        self.total += valor
        self.registrar_operacao("D", valor, descricao)

    def sacar(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("Não é permitido valor negativo.")
        if valor > self.total:
            raise ValueError("Saldo insuficiente.")
        self.total -= valor
        self.registrar_operacao("R", valor)


@dataclass
class Cliente:
    nome: str
    cpf: str
    senha: str
    contas: List["ContaCorrente"] = field(default_factory=list)

    def adicionar_conta(self, conta: ContaCorrente) -> ContaCorrente:
        conta.vincular_cliente(self)
        return conta
