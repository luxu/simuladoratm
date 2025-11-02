def log(prefixo):
    print(f"🏭 Fabrica de decorator rodou — prefixo = {prefixo!r}")
    def decorator(func):
        print(f"🛠️ Decorator rodou — recebendo a função {func.__name__}")
        def wrapper(*args, **kwargs):
            print(f"🔁 Wrapper rodou — chamada da função {func.__name__}")
            print(f"{prefixo} → Antes de executar {func.__name__}")
            resultado = func(*args, **kwargs)
            print(f"{prefixo} ← Depois de executar {func.__name__}")
            return resultado
        return wrapper
    return decorator
print("📌 Início do script")
@log("DEBUG")
def somar(a, b):
    print("🧮 Executando somar...")
    return a + b
print("📌 Função definida, mas ainda não chamada")
print("\n--- Primeira chamada ---")
resultado1 = somar(2, 3)
print(f"Resultado = {resultado1}")
print("\n--- Segunda chamada ---")
resultado2 = somar(10, 20)
print(f"Resultado = {resultado2}")