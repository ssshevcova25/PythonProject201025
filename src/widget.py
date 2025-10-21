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


# Тест
if __name__ == "__main__":
    tests = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305"
    ]

    for test in tests:
        print(f"{test} -> {mask_account_card(test)}")

def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    return f"{date_string[8:10]}.{date_string[5:7]}.{date_string[:4]}"


# Тест
if __name__ == "__main__":
    date_test = "2024-03-11T02:26:18.671407"
    print(f"{date_test} -> {get_date(date_test)}")  # 2024-03-11T02:26:18.671407 -> 11.03.2024