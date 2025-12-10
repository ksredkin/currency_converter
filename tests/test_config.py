import unittest
from unittest.mock import patch
import os
from currency_parcer.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        Config._instance = None
    
    def test_singleton_pattern(self):
        """Проверяем, что Config действительно Singleton"""
        config1 = Config()
        config2 = Config()
        
        self.assertIs(config1, config2, \
            "Singleton должен возвращать один и тот же экземпляр")
        print("✓ Singleton работает правильно")
    
    @patch.dict(os.environ, {
        'API_URL': 'https://api.test.com',
        'API_KEY': 'test_key_123'
    }, clear=True)
    def test_load_config_from_env(self):
        """Проверяем загрузку конфигурации из переменных окружения"""
        config = Config()
        
        self.assertEqual(config.get_api_url(), 'https://api.test.com')
        self.assertEqual(config.get_api_key(), 'test_key_123')
        print("✓ Конфиг загружается из .env")
    
    @patch.dict(os.environ, {'API_URL': 'https://api.test.com', 'API_KEY': ""}, clear=True)
    def test_missing_api_key_raises_error(self):
        """Проверяем, что отсутствие API_KEY вызывает ошибку"""
        with self.assertRaises(ValueError) as context:
            Config()
        
        error_message = str(context.exception)
        self.assertIn('API_KEY', error_message)
        print(f"✓ Правильная ошибка: {error_message}")
    
    @patch.dict(os.environ, {"API_KEY": "test_key", "API_URL": ""}, clear=True)
    def test_missing_api_url_raises_error(self):
        """Проверяем, что отсутствие API_URL вызывает ошибку"""
        with self.assertRaises(ValueError) as context:
            Config()
        
        error_message = str(context.exception)
        self.assertIn('API_URL', error_message)
        print(f"✓ Правильная ошибка: {error_message}")
    
    @patch.dict(os.environ, {
        'API_URL': 'https://api.test.com',
        'API_KEY': 'test_key_123'
    }, clear=True)
    def test_get_methods_return_strings(self):
        """Проверяем, что методы возвращают строки"""
        config = Config()
        
        url = config.get_api_url()
        key = config.get_api_key()
        
        self.assertIsInstance(url, str)
        self.assertIsInstance(key, str)
        print("✓ Методы возвращают строки")

if __name__ == '__main__':
    unittest.main(verbosity=2)