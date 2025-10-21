def get_mask_card_number(card_number: str) -> str:
    clean = "".join(filter(str.isdigit, card_number))
    if len(clean) < 16:
        raise ValueError("Номер карты должен содержать минимум 16 цифр")
    return f"{clean[:4]} {clean[4:6]}** **** {clean[-4:]}"

def get_mask_account(account_number: str) -> str:
    clean = "".join(filter(str.isdigit, account_number))
    if len(clean) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")
    return f"**{clean[-4:]}"

if __name__ == "__main__":
    # Этот код выполнится ТОЛЬКО при прямом запуске mask.py
    print("Тестирование функций маскировки:")
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))