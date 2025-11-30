import pytest
import sys
import os
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import widget


class TestWidget:
    def test_mask_account_card_visa(self):
        """Тестирование маскировки карты Visa"""
        result = widget.mask_account_card("Visa Platinum 1234567890123456")
        assert result == "Visa Platinum 1234 56** **** 3456"

    def test_mask_account_card_account(self):
        """Тестирование маскировки счета"""
        result = widget.mask_account_card("Счет 12345678901234567890")
        assert result == "Счет **7890"

    def test_mask_account_card_maestro(self):
        """Тестирование маскировки карты Maestro"""
        result = widget.mask_account_card("Maestro 1596837868705199")
        assert result == "Maestro 1596 83** **** 5199"

    def test_mask_account_card_mastercard(self):
        """Тестирование маскировки карты MasterCard"""
        result = widget.mask_account_card("MasterCard 7158300734726758")
        assert result == "MasterCard 7158 30** **** 6758"

    def test_mask_account_card_invalid(self):
        """Тестирование маскировки некорректных данных"""
        # Только текст без цифр
        assert widget.mask_account_card("Just Text") == "Just Text"

        # Одно слово
        assert widget.mask_account_card("SingleWord") == "SingleWord"

        # Текст с пробелами но без цифр в последней части
        assert widget.mask_account_card("Some Text Here") == "Some Text Here"

        # Текст где последняя часть не содержит цифр
        assert widget.mask_account_card("Card Number ABC") == "Card Number ABC"

    def test_mask_account_card_empty(self):
        """Тестирование маскировки пустой строки"""
        assert widget.mask_account_card("") == ""

    def test_mask_account_card_short_number(self):
        """Тестирование маскировки с коротким номером"""
        # Для карты с коротким номером
        result = widget.mask_account_card("Card 1234")
        assert result == "Card 1234"  # Должен вернуть номер как есть

        # Для счета с коротким номером
        result = widget.mask_account_card("Счет 123")
        assert result == "Счет 123"  # Должен вернуть номер как есть

    def test_get_date(self):
        """Тестирование преобразования даты"""
        result = widget.get_date("2024-03-11T02:26:18.671407")
        assert result == "11.03.2024"

    def test_get_date_another_format(self):
        """Тестирование преобразования другой даты"""
        result = widget.get_date("2023-12-31T23:59:59.999999")
        assert result == "31.12.2023"

    def test_get_date_short_string(self):
        """Тестирование преобразования короткой строки даты"""
        result = widget.get_date("2024-03-11")
        assert result == "11.03.2024"