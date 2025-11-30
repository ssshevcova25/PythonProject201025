from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по статусу

    Args:
        operations: Список словарей с операциями
        state: Статус для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список операций
    """
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате

    Args:
        operations: Список словарей с операциями
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Отсортированный список операций
    """
    return sorted(operations, key=lambda x: x['date'], reverse=reverse)