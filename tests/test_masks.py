import pytest
import sys
import os

# Добавляем путь к src для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.masks import get_mask_card_number, get_mask_account


class TestMasks:
    """Тесты для модуля masks"""

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("1111222233334444", "1111 22** **** 4444"),
    ])
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Тестирование маскировки валидных номеров карт"""
        assert get_mask_card_number(card_number) == expected

    def test_get_mask_card_number_with_spaces(self):
        """Тестирование маскировки номера карты с пробелами"""
        assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"

    def test_get_mask_card_number_short(self):
        """Тестирование маскировки короткого номера карты"""
        with pytest.raises(ValueError, match="Номер карты должен содержать минимум 16 цифр"):
            get_mask_card_number("1234567890")

    def test_get_mask_card_number_empty(self):
        """Тестирование маскировки пустой строки"""
        with pytest.raises(ValueError, match="Номер карты должен содержать минимум 16 цифр"):
            get_mask_card_number("")

    @pytest.mark.parametrize("account_number, expected", [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("1234", "**1234"),
    ])
    def test_get_mask_account_valid(self, account_number, expected):
        """Тестирование маскировки валидных номеров счетов"""
        assert get_mask_account(account_number) == expected

    def test_get_mask_account_with_spaces(self):
        """Тестирование маскировки номера счета с пробелами"""
        assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"

    def test_get_mask_account_short(self):
        """Тестирование маскировки короткого номера счета"""
        with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
            get_mask_account("123")

    def test_get_mask_account_empty(self):
        """Тестирование маскировки пустого номера счета"""
        with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 цифры"):
            get_mask_account("")