from datetime import datetime


def once(func):
    def wrapper():
        print("Executado pela primeira vez!")
        func()
        print("Executado pela última vez!")
    return wrapper

def validar_tipo(func):
    def wrapper(*args, **kwargs):
        print("Executado pela primeira vez!")
        func(*args, **kwargs)
        print("Executado pela última vez!")
    return wrapper

# Cree um @tempo que registre o tempo num arquivo log.txt ao invés de imprimir.

def tempo(func):
    def wrapper(*args, **kwargs):
        print("Executado pela primeira vez!")
        func(*args, **kwargs)
        print("Executado pela última vez!")
    return wrapper


def executar_uma_vez():
    soma = 1 + 2
    print(f"Calculando...Resultado: {soma}")
a = 1209
b = 1234
executar_uma_vez()

@once
def executar_outra_vez():
    ...

@validar_tipo
def verificar_se_as_variaveis_sao_inteiros(a,b):
    msg = f'Os números...:{a} e {b} são inteiros!'
    if not isinstance(a, int):
        msg = f'A varíavel...:{a} não é inteiro!'
    if not isinstance(b, int):
        msg = f'A varíavel...:{b} não é inteiro!'
    print(msg)

a = 1209
b = '1234'
verificar_se_as_variaveis_sao_inteiros(a,b)

@tempo
def verificar_tempo_registrar_txt():
    tempo_inicial = datetime.today()
    tempo_final = datetime.today()
    tempo_duracao = tempo_final - tempo_inicial
    print(f'{tempo_inicial} - {tempo_final} = {tempo_duracao}')
verificar_tempo_registrar_txt()