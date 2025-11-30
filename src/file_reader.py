import pandas as pd
from typing import List, Dict, Any


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл и возвращает список словарей с данными о транзакциях
    """
    try:
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    except Exception:
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл и возвращает список словарей с данными о транзакциях
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df.to_dict('records')
    except Exception:
        return []
