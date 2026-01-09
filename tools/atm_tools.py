import csv
from datetime import datetime
from pathlib import Path


def create_file(path_filename):
    if path_filename.exists():
        print(f"File {path_filename} exists.")
        return False
    else:
        print(f"File {path_filename} does not exist...creating new file")
        # headers = ["nome", "data_nascimento", "cpf", "endereco"]
        headers = ["name", "date_of_birth", "cpf", "address"]
        if "list_accounts.csv" in str(path_filename):
            # headers = ["agencia", "numero", "titular", "saldo"]
            headers = ["agency_bank", "number_bank", "holder_account", "balance", "cpf_client"]
        with open(path_filename, "a") as _f:
            csv.writer(_f).writerow(headers)


def search_name_by_cpf(cpf: str, clients):
    # O next() interrompe a busca assim que encontra o primeiro resultado (curto-circuito),
    # sem precisar olhar o resto da lista.
    # O uso do None evita exceções caso o registro não exista.
    return next((client for client in clients if client['cpf'] == cpf), None)


def is_account_exists(new_cpf_client: str, accounts):
    return [account for account in accounts if account['cpf_client'] == new_cpf_client]


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
