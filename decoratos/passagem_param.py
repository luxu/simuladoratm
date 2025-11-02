def dizer_oi(nome):
    print("executando dizer_oi")
    return f"Oi {nome}"

def incentivar_aprender(nome):
    print("executando incentivar_aprender")
    return f"Oi {nome}, vamos aprender Python juntos!"

def mensagem_para_luciano(funcao_mensagem, nome):
    return funcao_mensagem(nome)

print(mensagem_para_luciano(dizer_oi,"Luciano"))
print(mensagem_para_luciano(incentivar_aprender, "Pedro"))
