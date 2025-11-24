def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    if not card_number:
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    clean = "".join(filter(str.isdigit, card_number))
    if len(clean) < 16:
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    return f"{clean[:4]} {clean[4:6]}** **** {clean[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    if not account_number:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    clean = "".join(filter(str.isdigit, account_number))
    if len(clean) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"**{clean[-4:]}"