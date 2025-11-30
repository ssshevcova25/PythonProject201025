from typing import Iterator, Dict, Any, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте операции
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне
    """
    for number in range(start, end + 1):
        card_str = str(number).zfill(16)
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted_card