import pytest
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from external_api import convert_currency


class TestExternalAPI:
    """Тесты для модуля external_api"""

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

        result = convert_currency(transaction)
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

        with patch('external_api._convert_via_api') as mock_convert:
            mock_convert.return_value = 7500.0
            result = convert_currency(transaction)

            mock_convert.assert_called_once_with(100.00, "USD")
            assert result == 7500.0

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

        with patch('external_api._convert_via_api') as mock_convert:
            mock_convert.return_value = 4500.0
            result = convert_currency(transaction)

            mock_convert.assert_called_once_with(50.00, "EUR")
            assert result == 4500.0

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

        result = convert_currency(transaction)
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

        result = convert_currency(transaction)
        assert result == 0.0

    def test_convert_currency_missing_operation_amount(self):
        """Тестирование конвертации без operationAmount"""
        transaction = {
            "id": 1,
            "description": "Test"
        }

        result = convert_currency(transaction)
        assert result == 0.0

    @patch('external_api.requests.get')
    def test_convert_via_api_success(self, mock_get):
        """Тестирование успешной конвертации через API"""
        from external_api import _convert_via_api

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
            result = _convert_via_api(100.0, "USD")

            assert result == 7500.0
            mock_get.assert_called_once()

    @patch('external_api.requests.get')
    def test_convert_via_api_failure(self, mock_get):
        """Тестирование неудачной конвертации через API"""
        from external_api import _convert_via_api

        # Мокаем ответ API с ошибкой
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_get.return_value = mock_response

        # Мокаем переменную окружения
        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            with pytest.raises(ValueError, match="API error"):
                _convert_via_api(100.0, "USD")

    def test_convert_via_api_no_api_key(self):
        """Тестирование конвертации без API ключа"""
        from external_api import _convert_via_api

        # Убедимся что ключа нет
        if 'EXCHANGE_RATE_API_KEY' in os.environ:
            del os.environ['EXCHANGE_RATE_API_KEY']

        with pytest.raises(ValueError, match="API ключ для конвертации валют не найден"):
            _convert_via_api(100.0, "USD")