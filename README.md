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

A janela inicial permitirá criar um novo cadastro ou acessar uma conta existente. Após o login é possível efetuar depósitos, saques e consultar o extrato diretamente pela interface gráfica.

## Dicas

- Para iniciar com dados limpos basta encerrar o programa; todas as informações ficam apenas em memória.
- Se o FreeSimpleGUI apresentar mensagens sobre temas ou fontes, verifique se o sistema operacional possui as fontes padrões do Windows instaladas.
