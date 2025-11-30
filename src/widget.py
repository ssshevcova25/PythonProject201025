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

    # Если только одно слово или нет цифр - возвращаем как есть
    if len(parts) <= 1:
        return account_info

    # Последний элемент - это номер (должен содержать цифры)
    number = parts[-1]

    # Проверяем содержит ли последняя часть цифры
    if not any(char.isdigit() for char in number):
        return account_info

    # Все что перед последним элементом - это название карты/счета
    name = " ".join(parts[:-1])

    # Определяем тип по названию и применяем соответствующую маскировку
    if name.lower() == "счет":
        # Маскировка для счета: **XXXX
        masked_number = f"**{number[-4:]}"
    else:
        # Маскировка для карты: XXXX XX** **** XXXX
        # Убедимся что номер содержит достаточно цифр
        clean_number = "".join(filter(str.isdigit, number))
        if len(clean_number) >= 16:
            masked_number = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"
        else:
            # Если цифр недостаточно, возвращаем исходный номер
            masked_number = number

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    return f"{date_string[8:10]}.{date_string[5:7]}.{date_string[:4]}"