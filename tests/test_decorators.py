import pytest
import os
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

# Добавляем путь к src для импорта модулей
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import decorators


class TestDecorators:
    """Тесты для декоратора log"""

    def test_log_to_console_success(self, capsys):
        """Тестирование логирования успешной операции в консоль"""

        @decorators.log()
        def successful_function(x, y):
            return x + y

        result = successful_function(2, 3)

        # Проверяем результат
        assert result == 5

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "successful_function ok" in captured.out

    def test_log_to_console_error(self, capsys):
        """Тестирование логирования ошибки в консоль"""

        @decorators.log()
        def failing_function(a, b):
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_function(1, 2)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "failing_function error: ValueError" in captured.out
        assert "Inputs: (1, 2), {}" in captured.out

    def test_log_to_file_success(self):
        """Тестирование логирования успешной операции в файл"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_filename = temp_file.name

        try:
            @decorators.log(filename=temp_filename)
            def file_success_function(x, y, z=10):
                return x * y + z

            result = file_success_function(3, 4)

            # Проверяем результат
            assert result == 22

            # Проверяем запись в файл
            with open(temp_filename, 'r', encoding='utf-8') as f:
                log_content = f.read()

            assert "file_success_function ok" in log_content

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_to_file_error(self):
        """Тестирование логирования ошибки в файл"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_filename = temp_file.name

        try:
            @decorators.log(filename=temp_filename)
            def file_error_function(a, b, c=0):
                return a / c  # Деление на ноль

            with pytest.raises(ZeroDivisionError):
                file_error_function(10, 5)

            # Проверяем запись в файл
            with open(temp_filename, 'r', encoding='utf-8') as f:
                log_content = f.read()

            assert "file_error_function error: ZeroDivisionError" in log_content
            assert "Inputs: (10, 5), {}" in log_content

        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_preserves_function_metadata(self):
        """Тестирование что декоратор сохраняет метаданные функции"""

        @decorators.log()
        def test_function(x: int, y: int) -> int:
            """Тестовая функция для проверки метаданных"""
            return x + y

        # Проверяем что сохранилось имя и документация
        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Тестовая функция для проверки метаданных"

    def test_log_with_keyword_arguments(self, capsys):
        """Тестирование логирования с keyword arguments"""

        @decorators.log()
        def function_with_kwargs(a, b, c=0, d=1):
            return a + b + c + d

        result = function_with_kwargs(1, 2, c=3, d=4)

        assert result == 10

        captured = capsys.readouterr()
        assert "function_with_kwargs ok" in captured.out

    def test_log_multiple_calls(self, capsys):
        """Тестирование множественных вызовов декорированной функции"""

        @decorators.log()
        def counter_function():
            if not hasattr(counter_function, 'call_count'):
                counter_function.call_count = 0
            counter_function.call_count += 1
            return counter_function.call_count

        # Вызываем несколько раз
        for i in range(3):
            result = counter_function()
            assert result == i + 1

        # Проверяем что было 3 записи в лог
        captured = capsys.readouterr()
        log_lines = captured.out.strip().split('\n')
        assert len(log_lines) == 3
        assert all("counter_function ok" in line for line in log_lines)

    def test_log_with_different_exceptions(self, capsys):
        """Тестирование логирования разных типов исключений"""

        @decorators.log()
        def raise_type_error():
            raise TypeError("Type error message")

        @decorators.log()
        def raise_runtime_error():
            raise RuntimeError("Runtime error message")

        with pytest.raises(TypeError):
            raise_type_error()

        with pytest.raises(RuntimeError):
            raise_runtime_error()

        captured = capsys.readouterr()
        assert "raise_type_error error: TypeError" in captured.out
        assert "raise_runtime_error error: RuntimeError" in captured.out

    def test_log_returns_correct_value(self):
        """Тестирование что декоратор возвращает правильное значение"""

        @decorators.log()
        def return_string():
            return "test_string"

        @decorators.log()
        def return_number():
            return 42

        @decorators.log()
        def return_list():
            return [1, 2, 3]

        assert return_string() == "test_string"
        assert return_number() == 42
        assert return_list() == [1, 2, 3]


# Дополнительные тесты для проверки формата логов
class TestLogFormat:
    """Тесты формата логов"""

    def test_log_format_contains_timestamp(self, capsys):
        """Тестирование что лог содержит временную метку"""

        @decorators.log()
        def timestamp_function():
            return "test"

        timestamp_function()

        captured = capsys.readouterr()
        # Проверяем формат временной метки: YYYY-MM-DD HH:MM:SS
        assert " - timestamp_function ok" in captured.out

    def test_log_error_format(self, capsys):
        """Тестирование формата ошибок"""

        @decorators.log()
        def error_function(x):
            raise ValueError("Custom error")

        with pytest.raises(ValueError):
            error_function("test_arg")

        captured = capsys.readouterr()
        assert "error_function error: ValueError" in captured.out
        assert "Inputs: ('test_arg',), {}" in captured.out