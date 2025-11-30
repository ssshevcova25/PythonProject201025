import re
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений

    Args:
        data: Список словарей с данными о транзакциях
        search: Строка для поиска в описании

    Returns:
        Список словарей с транзакциями, содержащими искомую строку
    """
    if not data or not search:
        return []

    result = []
    # Создаем регулярное выражение для поиска без учета регистра
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям

    Args:
        data: Список словарей с данными о транзакциях
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством операций по каждой категории
    """
    if not data or not categories:
        return {}

    # Приводим категории к нижнему регистру для сравнения
    categories_lower = [cat.lower() for cat in categories]
    result = {category: 0 for category in categories}

    for transaction in data:
        description = transaction.get('description', '').lower()

        for i, category in enumerate(categories_lower):
            if category in description:
                result[categories[i]] += 1
                break  # Если нашли совпадение, переходим к следующей транзакции

    return result