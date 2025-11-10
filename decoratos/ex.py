def countdown(n):
    while n > 0:
        yield n
        n -= 1
# print(list(countdown(3)))

def capitalize_decorator(func):
    def wrapper():
        return func().upper()
    return wrapper

@capitalize_decorator
def greet():
    return "Hello"

print(greet())
