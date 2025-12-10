import unittest
from unittest.mock import Mock, patch
from currency_parcer.strategies import OpenExchangeRatesStrategy, MockExchangeStrategy

class TestMockExchangeStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = MockExchangeStrategy()
    
    def test_get_rates_returns_dict(self):
        rates = self.strategy.get_rates()
        self.assertIsInstance(rates, dict)
    
    def test_get_rates_contains_usd(self):
        rates = self.strategy.get_rates()
        self.assertIn("USD", rates)
        self.assertEqual(rates["USD"], 1.0)
    
    def test_get_rates_has_correct_structure(self):
        rates = self.strategy.get_rates()
        for currency, rate in rates.items():
            self.assertIsInstance(currency, str)
            self.assertIsInstance(rate, (int, float))

class TestOpenExchangeRatesStrategy(unittest.TestCase):
    @patch('currency_parcer.strategies.requests.get')
    def test_successful_api_call(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "conversion_rates": {
                "USD": 1.0,
                "EUR": 0.92,
                "RUB": 92.5
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        strategy = OpenExchangeRatesStrategy("http://test.com/{api_key}", "test_key")
        rates = strategy.get_rates()
        
        self.assertEqual(rates["USD"], 1.0)
        self.assertEqual(rates["EUR"], 0.92)
        mock_get.assert_called_once_with("http://test.com/test_key")
    
    @patch('currency_parcer.strategies.requests.get')
    def test_api_error_handling(self, mock_get):
        mock_get.side_effect = Exception("API Error")
        
        strategy = OpenExchangeRatesStrategy("http://test.com/{api_key}", "test_key")
        
        with self.assertRaises(Exception) as context:
            strategy.get_rates()
        
        self.assertIn("API Error", str(context.exception))

if __name__ == '__main__':
    unittest.main(verbosity=2)