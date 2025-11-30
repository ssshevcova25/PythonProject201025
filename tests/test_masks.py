import pytest
import sys
import os
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import masks


class TestMasks:
    def test_get_mask_card_number_valid(self):
        assert masks.get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    def test_get_mask_card_number_with_spaces(self):
        assert masks.get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"

    def test_get_mask_card_number_short(self):
        with pytest.raises(ValueError):
            masks.get_mask_card_number("1234567890")

    def test_get_mask_account_valid(self):
        assert masks.get_mask_account("12345678901234567890") == "**7890"

    def test_get_mask_account_short(self):
        with pytest.raises(ValueError):
            masks.get_mask_account("123")