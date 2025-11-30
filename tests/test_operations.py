import pytest
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import operations


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "state": "EXECUTED",
            "date": "2024-01-15"
        },
        {
            "id": 2,
            "description": "Перевод с карты на карту",
            "state": "EXECUTED",
            "date": "2024-01-16"
        },
        {
            "id": 3,
            "description": "Открытие вклада",
            "state": "CANCELED",
            "date": "2024-01-17"
        },
        {
            "id": 4,
            "description": "Перевод со счета на счет",
            "state": "EXECUTED",
            "date": "2024-01-18"
        }
    ]


class TestOperations:
    def test_process_bank_search_found(self, sample_transactions):
        result = operations.process_bank_search(sample_transactions, "перевод")
        assert len(result) == 3
        assert all("перевод" in t["description"].lower() for t in result)

    def test_process_bank_search_not_found(self, sample_transactions):
        result = operations.process_bank_search(sample_transactions, "кредит")
        assert len(result) == 0

    def test_process_bank_search_case_insensitive(self, sample_transactions):
        result = operations.process_bank_search(sample_transactions, "ПЕРЕВОД")
        assert len(result) == 3

    def test_process_bank_search_empty_data(self):
        result = operations.process_bank_search([], "перевод")
        assert result == []

    def test_process_bank_search_empty_search(self, sample_transactions):
        result = operations.process_bank_search(sample_transactions, "")
        assert result == []

    def test_process_bank_operations(self, sample_transactions):
        categories = ["Перевод", "Вклад"]
        result = operations.process_bank_operations(sample_transactions, categories)

        assert result["Перевод"] == 3
        assert result["Вклад"] == 1

    def test_process_bank_operations_case_insensitive(self, sample_transactions):
        categories = ["перевод", "вклад"]
        result = operations.process_bank_operations(sample_transactions, categories)

        assert result["перевод"] == 3
        assert result["вклад"] == 1

    def test_process_bank_operations_empty_data(self):
        result = operations.process_bank_operations([], ["Перевод"])
        assert result == {}

    def test_process_bank_operations_empty_categories(self, sample_transactions):
        result = operations.process_bank_operations(sample_transactions, [])
        assert result == {}