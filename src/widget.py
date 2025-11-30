def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета"""
    if not account_info:
        return account_info

    *name_parts, number = account_info.split()
    name = " ".join(name_parts)

    if name.lower() == "счет":
        return f"{name} **{number[-4:]}"
    else:
        return f"{name} {number[:4]} {number[4:6]}** **** {number[-4:]}"


def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    return f"{date_string[8:10]}.{date_string[5:7]}.{date_string[:4]}"