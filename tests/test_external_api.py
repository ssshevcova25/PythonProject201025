import pytest
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

import external_api


class TestExternalAPI:
    def test_convert_currency_rub(self):
        """Тестирование конвертации RUB транзакции"""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {
                    "code": "RUB"
                }
            }
        }

        result = external_api.convert_currency(transaction)
        assert result == 1000.50

    def test_convert_currency_usd(self):
        """Тестирование конвертации USD транзакции"""
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        result = external_api.convert_currency(transaction)
        # Должен использовать фиксированный курс
        assert result == 100.00 * 75.0

    def test_convert_currency_eur(self):
        """Тестирование конвертации EUR транзакции"""
        transaction = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "EUR"
                }
            }
        }

        result = external_api.convert_currency(transaction)
        # Должен использовать фиксированный курс
        assert result == 50.00 * 85.0

    def test_convert_currency_unknown_currency(self):
        """Тестирование конвертации неизвестной валюты"""
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "GBP"  # Не поддерживаемая валюта
                }
            }
        }

        result = external_api.convert_currency(transaction)
        assert result == 100.00

    def test_convert_currency_invalid_amount(self):
        """Тестирование конвертации с невалидной суммой"""
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {
                    "code": "RUB"
                }
            }
        }

        result = external_api.convert_currency(transaction)
        assert result == 0.0

    def test_convert_currency_missing_operation_amount(self):
        """Тестирование конвертации без operationAmount"""
        transaction = {
            "id": 1,
            "description": "Test"
        }

        result = external_api.convert_currency(transaction)
        assert result == 0.0

    def test_convert_currency_missing_currency(self):
        """Тестирование конвертации без currency"""
        transaction = {
            "operationAmount": {
                "amount": "100.00"
            }
        }

        result = external_api.convert_currency(transaction)
        assert result == 100.00

    @patch('external_api.requests.get')
    def test_convert_via_api_success(self, mock_get):
        """Тестирование успешной конвертации через API"""
        # Мокаем ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": 7500.0
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Мокаем переменную окружения
        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            result = external_api._convert_via_api(100.0, "USD")

            assert result == 7500.0
            mock_get.assert_called_once()

    @patch('external_api.requests.get')
    def test_convert_via_api_no_key(self, mock_get):
        """Тестирование конвертации без API ключа"""
        # Убедимся что ключа нет
        if 'EXCHANGE_RATE_API_KEY' in os.environ:
            del os.environ['EXCHANGE_RATE_API_KEY']

        result = external_api._convert_via_api(100.0, "USD")
        assert result == 100.0 * 75.0
        mock_get.assert_not_called()  # API не должно вызываться