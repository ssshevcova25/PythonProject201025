import pytest
import logging
import os
import tempfile
import sys
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.append(str(Path(__file__).parent.parent / 'src'))

# Теперь импортируем модули
import utils
import masks


class TestLogging:
    """Тесты для функционала логирования"""

    def test_utils_logging_success(self):
        """Тестирование логирования успешных операций в utils"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = [{"id": 1, "amount": "100.50"}]
            import json
            json.dump(test_data, f)
            temp_filename = f.name

        try:
            result = utils.read_json_file(temp_filename)

            # Проверяем что файл лога создан и содержит записи
            log_file = Path("logs/utils.log")
            assert log_file.exists()

            log_content = log_file.read_text(encoding='utf-8')
            assert "Успешно загружено" in log_content
            assert temp_filename in log_content

        finally:
            os.unlink(temp_filename)

    def test_utils_logging_file_not_found(self):
        """Тестирование логирования ошибок в utils"""
        result = utils.read_json_file("nonexistent_file.json")

        log_file = Path("logs/utils.log")
        if log_file.exists():
            log_content = log_file.read_text(encoding='utf-8')
            assert "Файл не найден" in log_content
            assert "nonexistent_file.json" in log_content

    def test_masks_logging_success(self):
        """Тестирование логирования успешных операций в masks"""
        result = masks.get_mask_card_number("1234567890123456")

        log_file = Path("logs/masks.log")
        assert log_file.exists()

        log_content = log_file.read_text(encoding='utf-8')
        assert "Успешная маскировка карты" in log_content
        assert "1234567890123456" in log_content

    def test_masks_logging_error(self):
        """Тестирование логирования ошибок в masks"""
        with pytest.raises(ValueError):
            masks.get_mask_card_number("123")

        log_file = Path("logs/masks.log")
        assert log_file.exists()

        log_content = log_file.read_text(encoding='utf-8')
        assert "ERROR" in log_content
        assert "слишком короткий" in log_content

    def test_log_format(self):
        """Тестирование формата логов"""
        # Используем функцию setup_logger из utils
        logger = utils.setup_logger('format_test', 'format_test.log')
        test_message = "Test log message"
        logger.info(test_message)

        log_file = Path("logs/format_test.log")
        log_content = log_file.read_text(encoding='utf-8')

        # Проверяем формат: timestamp - name - level - message
        lines = log_content.strip().split('\n')
        last_line = lines[-1]

        assert ' - ' in last_line
        parts = last_line.split(' - ')
        assert len(parts) >= 4
        assert 'format_test' in parts[1]
        assert 'INFO' in parts[2]
        assert test_message in parts[3]