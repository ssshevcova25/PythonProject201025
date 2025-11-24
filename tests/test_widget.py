import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.widget import mask_account_card, get_date


class TestWidget:
    """Тесты для модуля widget"""

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ])
    def test_mask_account_card_cards(self, input_data, expected):
        """Тестирование маскировки карт"""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("input_data, expected", [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ])
    def test_mask_account_card_accounts(self, input_data, expected):
        """Тестирование маскировки счетов"""
        assert mask_account_card(input_data) == expected

    def test_mask_account_card_empty(self):
        """Тестирование маскировки пустой строки"""
        assert mask_account_card("") == ""

    def test_mask_account_card_invalid(self):
        """Тестирование маскировки некорректных данных"""
        assert mask_account_card("Just Text") == "Just Text"

    @pytest.mark.parametrize("date_string, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ])
    def test_get_date_valid(self, date_string, expected):
        """Тестирование преобразования валидных дат"""
        assert get_date(date_string) == expected

    def test_get_date_short_string(self):
        """Тестирование преобразования короткой строки"""
        assert get_date("2024-03-11") == "11.03.2024"