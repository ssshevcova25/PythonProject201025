import pytest
import sys
import os
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import generators


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]


class TestGenerators:
    """Тесты для модуля generators"""

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тестирование фильтрации по USD"""
        usd_transactions = list(generators.filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2
        assert all(
            tx["operationAmount"]["currency"]["code"] == "USD"
            for tx in usd_transactions
        )

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тестирование фильтрации по RUB"""
        rub_transactions = list(generators.filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1
        assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_by_currency_empty_result(self, sample_transactions):
        """Тестирование фильтрации когда нет совпадений"""
        eur_transactions = list(generators.filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_filter_by_currency_empty_list(self):
        """Тестирование фильтрации пустого списка"""
        result = list(generators.filter_by_currency([], "USD"))
        assert result == []

    def test_transaction_descriptions(self, sample_transactions):
        """Тестирование генератора описаний транзакций"""
        descriptions = list(generators.transaction_descriptions(sample_transactions))
        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет"
        ]
        assert descriptions == expected_descriptions

    def test_transaction_descriptions_empty_list(self):
        """Тестирование генератора описаний с пустым списком"""
        descriptions = list(generators.transaction_descriptions([]))
        assert descriptions == []

    @pytest.mark.parametrize("start,end,expected_count,expected_first,expected_last", [
        (1, 5, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (9999999999999995, 9999999999999999, 5, "9999 9999 9999 9995", "9999 9999 9999 9999"),
        (1234567890123456, 1234567890123456, 1, "1234 5678 9012 3456", "1234 5678 9012 3456"),
    ])
    def test_card_number_generator(self, start, end, expected_count, expected_first, expected_last):
        """Тестирование генератора номеров карт с различными диапазонами"""
        card_numbers = list(generators.card_number_generator(start, end))
        assert len(card_numbers) == expected_count
        assert card_numbers[0] == expected_first
        assert card_numbers[-1] == expected_last

    def test_card_number_generator_format(self):
        """Тестирование формата номеров карт"""
        card_numbers = list(generators.card_number_generator(1, 1))
        card_number = card_numbers[0]
        # Проверяем формат XXXX XXXX XXXX XXXX
        assert len(card_number) == 19  # 16 цифр + 3 пробела
        assert card_number.count(" ") == 3
        parts = card_number.split(" ")
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)