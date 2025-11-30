import pandas as pd
from typing import List, Dict, Any
import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Настраивает и возвращает логгер для модуля
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_dir / log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# Настраиваем логгер для модуля file_reader
logger = setup_logger('file_reader', 'file_reader.log')


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с данными о транзакциях или пустой список в случае ошибки
    """
    logger.debug(f"Попытка чтения CSV файла: {file_path}")

    try:
        # Читаем CSV файл с помощью pandas
        df = pd.read_csv(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        logger.info(f"Успешно загружено {len(transactions)} записей из CSV файла: {file_path}")
        return transactions

    except FileNotFoundError:
        logger.error(f"CSV файл не найден: {file_path}")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"CSV файл пустой: {file_path}")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV файла {file_path}: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel файл и возвращает список словарей с данными о транзакциях

    Args:
        file_path: Путь к Excel файлу

    Returns:
        Список словарей с данными о транзакций или пустой список в случае ошибки
    """
    logger.debug(f"Попытка чтения Excel файла: {file_path}")

    try:
        # Читаем Excel файл с помощью pandas
        df = pd.read_excel(file_path, engine='openpyxl')

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        logger.info(f"Успешно загружено {len(transactions)} записей из Excel файла: {file_path}")
        return transactions

    except FileNotFoundError:
        logger.error(f"Excel файл не найден: {file_path}")
        return []
    except ValueError as e:
        logger.error(f"Ошибка значения при чтении Excel файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel файла {file_path}: {e}")
        return []