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


# Настраиваем логгер для модуля masks
logger = setup_logger('masks', 'masks.log')


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX

    Args:
        card_number: Номер карты для маскировки

    Returns:
        Замаскированный номер карты

    Raises:
        ValueError: Если номер карты невалидный
    """
    logger.debug(f"Попытка маскировки номера карты: {card_number}")

    if not card_number:
        logger.error("Передана пустая строка для маскировки карты")
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    clean = "".join(filter(str.isdigit, card_number))
    logger.debug(f"Очищенный номер карты: {clean}")

    if len(clean) < 16:
        logger.error(f"Номер карты слишком короткий: {len(clean)} цифр вместо 16")
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    masked = f"{clean[:4]} {clean[4:6]}** **** {clean[-4:]}"
    logger.info(f"Успешная маскировка карты: {card_number} -> {masked}")

    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX

    Args:
        account_number: Номер счета для маскировки

    Returns:
        Замаскированный номер счета

    Raises:
        ValueError: Если номер счета невалидный
    """
    logger.debug(f"Попытка маскировки номера счета: {account_number}")

    if not account_number:
        logger.error("Передана пустая строка для маскировки счета")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    clean = "".join(filter(str.isdigit, account_number))
    logger.debug(f"Очищенный номер счета: {clean}")

    if len(clean) < 4:
        logger.error(f"Номер счета слишком короткий: {len(clean)} цифр вместо 4")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    masked = f"**{clean[-4:]}"
    logger.info(f"Успешная маскировка счета: {account_number} -> {masked}")

    return masked