import json
from typing import List, Dict, Any
import os


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с данными о транзакциях
    """
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, IOError, PermissionError):
        return []