def meu_gerador(numeros: list[int]):
    for numero in numeros:
        print("executa antes do yield")
        yield numero * 2
        print("executa depois do yield")

for i in meu_gerador(numeros=[1, 2, 3]):
    print("executa antes do for")
    print(i)
    print("executa depois do for")
