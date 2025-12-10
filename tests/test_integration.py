import unittest

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты (можно запускать реже)"""
    
    def test_full_flow_with_mock(self):
        """Тестируем полный поток с mock стратегией"""
        from currency_parcer.__init__ import CurrencyConverterApp
        
        app = CurrencyConverterApp("mock-exchange-rates")
        
        rates = app.get_rates()
        self.assertIn("USD", rates)
        
        result = app.convert_currency("USD", "EUR")
        self.assertIsInstance(result, float)
        
        result2 = app.convert_currency("USD", "EUR")
        self.assertEqual(result, result2)
        
        print("✓ Полный поток работает корректно")
    
    def test_error_handling(self):
        """Тестируем обработку ошибок"""
        from currency_parcer.strategies import OpenExchangeRatesStrategy
        from unittest.mock import patch
        
        with patch('currency_parcer.strategies.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            strategy = OpenExchangeRatesStrategy("http://test.com", "bad_key")
            
            with self.assertRaises(Exception):
                strategy.get_rates()
            
            print("✓ Обработка ошибок API работает")

if __name__ == '__main__':
    unittest.main(verbosity=2)