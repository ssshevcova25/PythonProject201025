import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.processing import filter_by_state, sort_by_date



@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми данными операций"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-15T10:30:00.000000'},
        {'id': 2, 'state': 'CANCELED', 'date': '2024-01-10T14:20:00.000000'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-20T09:15:00.000000'},
        {'id': 4, 'state': 'PENDING', 'date': '2024-01-05T16:45:00.000000'},
        {'id': 5, 'state': 'EXECUTED', 'date': '2024-01-25T11:00:00.000000'},
    ]


@pytest.fixture
def operations_with_same_date():
    """Фикстура с операциями с одинаковыми датами"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-15T10:30:00.000000'},
        {'id': 2, 'state': 'CANCELED', 'date': '2024-01-15T10:30:00.000000'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-10T14:20:00.000000'},
    ]


class TestProcessing:
    """Тесты для модуля processing"""

    def test_filter_by_state_default(self, sample_operations):
        """Тестирование фильтрации по умолчанию (EXECUTED)"""
        result = filter_by_state(sample_operations)
        assert len(result) == 3
        assert all(op['state'] == 'EXECUTED' for op in result)

    @pytest.mark.parametrize("state, expected_count", [
        ('CANCELED', 1),
        ('PENDING', 1),
        ('EXECUTED', 3),
    ])
    def test_filter_by_state_different_states(self, sample_operations, state, expected_count):
        """Тестирование фильтрации по разным статусам"""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count
        assert all(op['state'] == state for op in result)

    def test_filter_by_state_no_matches(self, sample_operations):
        """Тестирование фильтрации когда нет совпадений"""
        result = filter_by_state(sample_operations, 'COMPLETED')
        assert result == []

    def test_filter_by_state_empty_list(self):
        """Тестирование фильтрации пустого списка"""
        assert filter_by_state([]) == []

    def test_sort_by_date_descending(self, sample_operations):
        """Тестирование сортировки по убыванию"""
        result = sort_by_date(sample_operations)
        dates = [op['date'] for op in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_date_ascending(self, sample_operations):
        """Тестирование сортировки по возрастанию"""
        result = sort_by_date(sample_operations, False)
        dates = [op['date'] for op in result]
        assert dates == sorted(dates)

    def test_sort_by_date_same_dates(self, operations_with_same_date):
        """Тестирование сортировки с одинаковыми датами"""
        result = sort_by_date(operations_with_same_date)
        # Проверяем что порядок сохраняется для одинаковых дат
        assert result[0]['date'] == '2024-01-15T10:30:00.000000'
        assert result[1]['date'] == '2024-01-15T10:30:00.000000'
        assert result[2]['date'] == '2024-01-10T14:20:00.000000'

    def test_sort_by_date_empty_list(self):
        """Тестирование сортировки пустого списка"""
        assert sort_by_date([]) == []