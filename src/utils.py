import json
from typing import List, Dict, Any
import os
import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Настраивает и возвращает логгер для модуля

    Args:
        name: Имя логгера (обычно __name__ модуля)
        log_file: Имя файла для записи логов
        level: Уровень логирования

    Returns:
        Настроенный логгер
    """
    # Создаем папку logs если ее нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Проверяем чтобы не добавлять обработчики повторно
    if logger.handlers:
        return logger

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Создаем файловый обработчик
    file_handler = logging.FileHandler(log_dir / log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger


# Настраиваем логгер для модуля utils
logger = setup_logger('utils', 'utils.log')


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к JSON файлу

    Returns:
        Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    logger.debug(f"Попытка чтения файла: {file_path}")

    try:
        # Проверяем существует ли файл
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем что данные - это список
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} записей из файла: {file_path}")
            return data
        else:
            logger.warning(f"Файл {file_path} не содержит список. Тип данных: {type(data)}")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except IOError as e:
        logger.error(f"Ошибка ввода-вывода при чтении файла {file_path}: {e}")
        return []
    except PermissionError as e:
        logger.error(f"Ошибка прав доступа к файлу {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []