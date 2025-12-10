import unittest
from currency_parcer.__init__ import CurrencyConverterApp

class TestConverter(unittest.TestCase):
    def setUp(self):
        """Создаем конвертер перед каждым тестом"""
        self.converter = CurrencyConverterApp("mock-exchange-rates")
        self.mock_exchange_rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "RUB": 92.5,
            "GBP": 0.79
        }

    def test_get_rates_retutns_dict(self):
        """Проверяем, возвращает ли get_rates словарь"""
        converter_exchange_rates = self.converter.get_rates()
        self.assertIsInstance(converter_exchange_rates, dict)
        print("✓ get_rates возвращает словарь")

    def test_get_rates(self):
        """Проверяем корректность значений из заглушки"""
        converter_exchange_rates = self.converter.get_rates()
        self.assertEqual(converter_exchange_rates, self.mock_exchange_rates)
        print("✓ Заглушка подставлена верно")

    def test_convert_currency(self):
        """Проверяем правильность конвертации"""
        converter_rub_to_usd_rate = self.converter.convert_currency("USD", "RUB")
        converter_eur_to_gbp_rate = self.converter.convert_currency("EUR", "GBP")

        self.assertEqual(converter_rub_to_usd_rate, self.mock_exchange_rates["RUB"] / self.mock_exchange_rates["USD"])
        self.assertEqual(converter_eur_to_gbp_rate, self.mock_exchange_rates["GBP"] / self.mock_exchange_rates["EUR"])
        print("✓ Валюты конвертируются корректно")

    def test_convert_currency_case_insensitive(self):
        """Проверяем, что конвертация не зависит от регистра"""
        result_lower = self.converter.convert_currency("usd", "rub")
        result_upper = self.converter.convert_currency("USD", "RUB")
        
        self.assertEqual(result_lower, result_upper)
        print("✓ Конвертация не зависит от регистра")
    
    def test_convert_currency_returns_float_for_valid(self):
        """Проверяем, что для корректных валют возвращается float"""
        result = self.converter.convert_currency("GBP", "RUB")
        self.assertIsInstance(result, float)
        print("✓ Для корректных валют возвращается float")
    
    def test_convert_currency_returns_none_for_invalid(self):
        """Проверяем, что для некорректных валют возвращается None"""
        result = self.converter.convert_currency("RUB", "USDT")
        self.assertIsNone(result)
        print("✓ Для некорректных валют возвращается None")

    def test_force_update_clears_cache(self):
        """Проверяем принудительное обновление кеша"""
        from unittest.mock import Mock
        
        rates1 = self.converter.get_rates()
        
        mock_get_rates = Mock(return_value={"USD": 2.0})
        self.converter.exchange_rate_strategy.get_rates = mock_get_rates
        
        rates2 = self.converter.get_rates(force=True)
        
        mock_get_rates.assert_called_once()
        self.assertEqual(rates2, {"USD": 2.0})
        print("✓ Принудительное обновление очищает кеш")

if __name__ == '__main__':
    unittest.main(verbosity=2)