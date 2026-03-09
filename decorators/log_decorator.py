"""
Модуль с декоратором log для логирования вызовов функций.
"""
import functools
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None):
    """
    Декоратор для логирования вызовов функций.

    Аргументы:
        filename (Optional[str]): Имя файла для записи логов.
                                  Если None, логи выводятся в консоль.

    Returns:
        Callable: Обернутая функция с логированием.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Запоминаем время начала выполнения
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Пытаемся выполнить функцию
                result = func(*args, **kwargs)
                log_message = f"{start_time} - {func.__name__} ok\n"

                # Выводим лог в нужное место
                _write_log(log_message, filename)

                # Возвращаем результат функции
                return result

            except Exception as e:
                # Если произошла ошибка, логируем её
                error_message = (
                    f"{start_time} - {func.__name__} error: "
                    f"{type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}\n"
                )
                _write_log(error_message, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper
    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
    Вспомогательная функция для записи лога в файл или консоль.

    Args:
        message (str): Сообщение для записи.
        filename (Optional[str]): Имя файла. Если None, вывод в консоль.
    """
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message, end='')
