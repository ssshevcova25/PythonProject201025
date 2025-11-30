import pytest
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import generators


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
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
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        }
    ]


class TestGenerators:
    def test_filter_by_currency_usd(self, sample_transactions):
        usd_transactions = list(generators.filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2

    def test_transaction_descriptions(self, sample_transactions):
        descriptions = list(generators.transaction_descriptions(sample_transactions))
        assert len(descriptions) == 2
        assert "Перевод организации" in descriptions

    def test_card_number_generator(self):
        card_numbers = list(generators.card_number_generator(1, 3))
        assert len(card_numbers) == 3
        assert card_numbers[0] == "0000 0000 0000 0001"