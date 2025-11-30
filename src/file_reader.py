import pandas as pd
from typing import List, Dict, Any


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    try:
        # Читаем CSV файл с помощью pandas
        df = pd.read_csv(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        return transactions

    except Exception:
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к Excel файлу

    Returns:
        Список словарей с данными о транзакций или пустой список в случае ошибки
    """
    try:
        # Читаем Excel файл с помощью pandas
        df = pd.read_excel(file_path, engine='openpyxl')

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        return transactions

    except Exception:
        return []