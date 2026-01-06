import csv

def create_file(path_filename):
    if path_filename.exists():
        print(f"File {path_filename} exists.")
        return False
    else:
        print(f"File {path_filename} does not exist...creating new file")
        headers = ["nome", "data_nascimento", "cpf", "endereco"]
        if "list_accounts.csv" in str(path_filename):
            headers = ["agencia", "numero", "titular", "saldo"]
        with open(path_filename, "a") as _f:
            csv.writer(_f).writerow(headers)
