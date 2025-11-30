import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency = operation_amount.get("currency", {})
    currency_code = currency.get("code", "RUB")

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        amount = 0.0

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        converted_amount = _convert_via_api(amount, currency_code)
        return converted_amount

    return amount


def _convert_via_api(amount: float, from_currency: str) -> float:
    """
    Конвертирует сумму через внешнее API
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not api_key:
        raise ValueError("API ключ для конвертации валют не найден")

    url = "https://api.apilayer.com/exchangerates_data/convert"

    headers = {
        "apikey": api_key
    }

    params = {
        "from": from_currency,
        "to": "RUB",
        "amount": amount
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success", False):
            return data["result"]
        else:
            raise ValueError(f"API error: {data.get('error', {}).get('info', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка при обращении к API: {e}")