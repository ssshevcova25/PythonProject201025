import pytest
import json
import tempfile
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import utils


class TestUtils:
    def test_read_json_file_valid(self):
        """Тестирование чтения валидного JSON файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = [
                {"id": 1, "amount": "100.50"},
                {"id": 2, "amount": "200.75"}
            ]
            json.dump(test_data, f)
            temp_filename = f.name

        try:
            result = utils.read_json_file(temp_filename)
            assert result == test_data
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_not_list(self):
        """Тестирование чтения JSON файла с не-списком"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = {"id": 1, "amount": "100.50"}  # Не список
            json.dump(test_data, f)
            temp_filename = f.name

        try:
            result = utils.read_json_file(temp_filename)
            assert result == []
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_empty(self):
        """Тестирование чтения пустого файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            # Пустой файл
            temp_filename = f.name

        try:
            result = utils.read_json_file(temp_filename)
            assert result == []
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_invalid_json(self):
        """Тестирование чтения файла с невалидным JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_filename = f.name

        try:
            result = utils.read_json_file(temp_filename)
            assert result == []
        finally:
            os.unlink(temp_filename)

    def test_read_json_file_nonexistent(self):
        """Тестирование чтения несуществующего файла"""
        result = utils.read_json_file("nonexistent_file.json")
        assert result == []

    def test_read_json_file_permission_error(self, monkeypatch):
        """Тестирование обработки ошибки прав доступа"""

        def mock_open(*args, **kwargs):
            raise PermissionError("Access denied")

        monkeypatch.setattr("builtins.open", mock_open)

        result = utils.read_json_file("any_file.json")
        assert result == []