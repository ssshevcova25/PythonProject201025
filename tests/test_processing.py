import pytest
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import processing


@pytest.fixture
def sample_operations():
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-15T10:30:00.000000'},
        {'id': 2, 'state': 'CANCELED', 'date': '2024-01-10T14:20:00.000000'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-20T09:15:00.000000'},
        {'id': 4, 'state': 'PENDING', 'date': '2024-01-05T16:45:00.000000'},
        {'id': 5, 'state': 'EXECUTED', 'date': '2024-01-25T11:00:00.000000'},
    ]


class TestProcessing:
    def test_filter_by_state_default(self, sample_operations):
        """Тестирование фильтрации по умолчанию (EXECUTED)"""
        result = processing.filter_by_state(sample_operations)
        assert len(result) == 3
        assert all(op['state'] == 'EXECUTED' for op in result)

    def test_filter_by_state_canceled(self, sample_operations):
        """Тестирование фильтрации по CANCELED"""
        result = processing.filter_by_state(sample_operations, 'CANCELED')
        assert len(result) == 1
        assert result[0]['state'] == 'CANCELED'

    def test_filter_by_state_pending(self, sample_operations):
        """Тестирование фильтрации по PENDING"""
        result = processing.filter_by_state(sample_operations, 'PENDING')
        assert len(result) == 1
        assert result[0]['state'] == 'PENDING'

    def test_filter_by_state_no_matches(self, sample_operations):
        """Тестирование фильтрации когда нет совпадений"""
        result = processing.filter_by_state(sample_operations, 'COMPLETED')
        assert result == []

    def test_filter_by_state_empty_list(self):
        """Тестирование фильтрации пустого списка"""
        assert processing.filter_by_state([]) == []

    def test_sort_by_date_descending(self, sample_operations):
        """Тестирование сортировки по убыванию"""
        result = processing.sort_by_date(sample_operations)
        dates = [op['date'] for op in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_date_ascending(self, sample_operations):
        """Тестирование сортировки по возрастанию"""
        result = processing.sort_by_date(sample_operations, False)
        dates = [op['date'] for op in result]
        assert dates == sorted(dates)

    def test_sort_by_date_empty_list(self):
        """Тестирование сортировки пустого списка"""
        assert processing.sort_by_date([]) == []

    def test_sort_by_date_single_element(self):
        """Тестирование сортировки списка с одним элементом"""
        single_op = [{'id': 1, 'state': 'EXECUTED', 'date': '2024-01-15T10:30:00.000000'}]
        result = processing.sort_by_date(single_op)
        assert result == single_op