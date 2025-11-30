import json
from typing import List, Dict, Any
import os


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к JSON файлу

    Returns:
        Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    try:
        # Проверяем существует ли файл
        if not os.path.exists(file_path):
            return []

        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем что данные - это список
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, IOError, PermissionError):
        # Возвращаем пустой список при любых ошибках
        return []