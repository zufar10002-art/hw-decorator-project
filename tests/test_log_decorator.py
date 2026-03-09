"""
Тесты для декоратора log.
"""
import pytest

from decorators.log_decorator import log


def test_log_to_console_success(capsys):
    """Тест успешного логирования в консоль."""
    @log()
    def add(a, b):
        return a + b

    result = add(3, 5)
    captured = capsys.readouterr()

    assert result == 8
    assert "add ok" in captured.out
    assert "2026" in captured.out


def test_log_to_console_error(capsys):
    """Тест логирования ошибки в консоль."""
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_to_file_success(tmp_path):
    """Тест успешного логирования в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(4, 7)
    assert result == 28

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "multiply ok" in content
    assert "2026" in content


def test_log_to_file_error(tmp_path):
    """Тест логирования ошибки в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def subtract(a, b):
        return a - b

    with pytest.raises(TypeError):
        subtract(None, 5)

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "subtract error: TypeError" in content
    assert "Inputs: (None, 5), {}" in content


def test_multiple_calls_same_file(tmp_path):
    """Тест множественных вызовов с записью в один файл."""
    log_file = tmp_path / "multiple.txt"

    @log(filename=str(log_file))
    def concat(a, b):
        return f"{a}{b}"

    concat("Hello, ", "World!")
    concat("Foo", "Bar")

    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 2
    assert "concat ok" in lines[0]
    assert "concat ok" in lines[1]


def test_different_functions_same_file(tmp_path):
    """Тест разных функций в один файл."""
    log_file = tmp_path / "shared.txt"

    @log(filename=str(log_file))
    def func1():
        return 1

    @log(filename=str(log_file))
    def func2():
        return 2

    func1()
    func2()

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "func1 ok" in content
    assert "func2 ok" in content


def test_preserves_return_value():
    """Тест сохранения возвращаемого значения."""
    @log()
    def get_value():
        return 42

    assert get_value() == 42


def test_preserves_docstring():
    """Тест сохранения docstring функции."""
    @log()
    def documented_func():
        """This is a docstring."""
        return True

    assert documented_func.__doc__ == "This is a docstring."
    assert documented_func.__name__ == "documented_func"
