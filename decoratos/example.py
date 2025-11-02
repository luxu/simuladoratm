name = "Luciano"
dados = [
    'Masculino',
    51
]

def my_decorator(function_parameter):
    def function_internal(*args, **kwargs):
        print("Antes da função ser executada.")
        print(f'DADOS do {name}: {dados}')
        result = function_parameter(*args, **kwargs)
        print("Depois da função ser executada.")
        return result
    return function_internal

# SEM DECORADOR
def dizer_oi(name,dados=[]):
    msg = f"Olá, Asimover..:{name}!"
    # print(msg)
    return msg

# Aplicando o decorador manualmente
decorada = my_decorator(
    dizer_oi(name,dados)
)
decorada()

# COM DECORADOR
# @my_decorator
# def dizer_oi(nome):
#     return f"Olá, Asimover..:{nome}!"
# print(
#     dizer_oi(
#         name
#     )
# )
