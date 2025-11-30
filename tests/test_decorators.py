import pytest
import os
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import decorators


class TestDecorators:
    def test_log_to_console_success(self, capsys):
        """Тестирование логирования успешной операции в консоль"""

        @decorators.log()
        def successful_function(x, y):
            return x + y

        result = successful_function(2, 3)

        assert result == 5
        captured = capsys.readouterr()
        assert "successful_function ok" in captured.out

    def test_log_to_console_error(self, capsys):
        """Тестирование логирования ошибки в консоль"""

        @decorators.log()
        def failing_function(a, b):
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_function(1, 2)

        captured = capsys.readouterr()
        assert "failing_function error: ValueError" in captured.out

    def test_log_to_file_success(self):
        """Тестирование логирования успешной операции в файл"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_filename = temp_file.name

        try:
            @decorators.log(filename=temp_filename)
            def file_success_function(x, y):
                return x * y

            result = file_success_function(3, 4)

            assert result == 12

            with open(temp_filename, 'r', encoding='utf-8') as f:
                log_content = f.read()

            assert "file_success_function ok" in log_content

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_preserves_function_metadata(self):
        """Тестирование что декоратор сохраняет метаданные функции"""

        @decorators.log()
        def test_function(x: int, y: int) -> int:
            """Тестовая функция для проверки метаданных"""
            return x + y

        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Тестовая функция для проверки метаданных"