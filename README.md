# Simulador de ATM

Aplicação desktop em Python que simula o fluxo de atendimento de um caixa eletrônico: cadastro, login e operações bancárias básicas utilizando a biblioteca [FreeSimpleGUI](https://freesimplegui.readthedocs.io/).

## Requisitos

- Python 3.13 ou superior
- Sistema operacional com suporte a interfaces gráficas (Windows, macOS ou uma distribuição Linux com servidor gráfico)

## Configuração do ambiente

Você pode utilizar o gerenciador de pacotes [uv](https://docs.astral.sh/uv/) (recomendado) ou apenas `pip`.

### Utilizando uv

```bash
# Instale o uv se ainda não possuir
pip install uv

# Dentro da pasta do projeto, crie o ambiente e instale as dependências
uv sync
```

Isso criará um ambiente virtual em `.venv` e instalará automaticamente a dependência `freesimplegui` descrita em `pyproject.toml`.

### Utilizando apenas pip

Caso prefira usar o `pip` tradicional:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows use: .venv\Scripts\activate
pip install --upgrade pip
pip install freesimplegui
```

## Executando o simulador

Com o ambiente virtual ativado execute:

```bash
python caixa_eletronico.py
```

## Passo a passo de utilização

1. **Tela inicial** – Escolha entre:
   - **Cadastrar cliente**: cria um novo cliente no banco e abre sua primeira conta corrente.
   - **Cadastrar conta**: localiza um cliente existente pelo CPF e registra uma nova conta corrente para ele.
   - **Já tenho cadastro**: abre a tela de login para acessar uma das contas correntes do cliente.
2. **Cadastro de cliente** – Informe nome completo, CPF, senha e depósito inicial. Ao confirmar, o cliente é criado e a conta inicial é registrada automaticamente.
3. **Cadastro de conta** – Digite o CPF de um cliente existente. Se encontrado, o nome é bloqueado para edição; basta informar o depósito inicial para criar a nova conta.
4. **Login** – Informe CPF e senha. Caso o cliente possua múltiplas contas, selecione qual deseja movimentar no combo box exibido no topo da tela de autoatendimento.
5. **Autoatendimento** – Consulte o saldo atual, realize depósitos, saques ou confira o extrato da conta selecionada. Alterações de conta no combo box atualizam os valores imediatamente.
6. **Encerramento** – Feche a janela do autoatendimento ou retorne à tela inicial para sair do simulador. Todos os dados ficam apenas em memória e são descartados quando o programa é encerrado.

## Dicas

- Para iniciar com dados limpos basta encerrar o programa; todas as informações ficam apenas em memória.
- Se o FreeSimpleGUI apresentar mensagens sobre temas ou fontes, verifique se o sistema operacional possui as fontes padrões do Windows instaladas.
