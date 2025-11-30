def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в переданной строке

    Args:
        account_info: Строка с типом и номером карты/счета

    Returns:
        Строка с замаскированным номером
    """
    if not account_info:
        return account_info

    # Разделяем строку на слова
    parts = account_info.split()

    # Если меньше 2 слов, возвращаем как есть
    if len(parts) < 2:
        return account_info

    # Берем последнюю часть как номер
    number = parts[-1]

    # Проверяем что номер состоит из цифр (может быть с разделителями)
    clean_number = "".join(filter(str.isdigit, number))

    # Если нет цифр или слишком мало цифр - возвращаем как есть
    if not clean_number or len(clean_number) < 4:
        return account_info

    # Все что перед последним элементом - это название
    name = " ".join(parts[:-1])

    # Определяем тип по названию
    if name.lower() == "счет":
        masked_number = f"**{clean_number[-4:]}"
    else:
        if len(clean_number) >= 16:
            masked_number = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"
        else:
            # Для коротких номеров карт возвращаем как есть
            return account_info

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    return f"{date_string[8:10]}.{date_string[5:7]}.{date_string[:4]}"