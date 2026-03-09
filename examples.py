from decorators.log_decorator import log


# Пример успешного выполнения с логированием в консоль
@log()
def my_sum(a, b):
    return a + b


# Пример успешного выполнения с логированием в файл
@log(filename="mylog.txt")
def my_multiply(a, b):
    return a * b


# Пример с ошибкой
@log()
def division(a, b):
    return a / b


if __name__ == "__main__":
    print("=== Тест 1: Логирование в консоль ===")
    result = my_sum(5, 3)
    print(f"Результат: {result}")

    print("\n=== Тест 2: Логирование в файл mylog.txt ===")
    result = my_multiply(4, 7)
    print(f"Результат: {result}")

    print("\n=== Тест 3: Проверка обработки ошибок ===")
    try:
        result = division(10, 0)
    except ZeroDivisionError:
        print("Ошибка была перехвачена и залогирована")