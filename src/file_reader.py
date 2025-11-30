
import csv
from typing import List, Dict, Any
import os


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    if not os.path.exists(file_path):
        return []

    transactions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(dict(row))
    except Exception:
        return []

    return transactions


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к Excel файлу

    Returns:
        Список словарей с данными о транзакций или пустой список в случае ошибки
    """
    if not os.path.exists(file_path):
        return []

    try:
        # Импортируем pandas внутри функции
        import pandas as pd

        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            return df.to_dict('records')
        except Exception:
            return []
    except ImportError:
        # pandas не установлен
        return []