from abc import ABC, abstractmethod
import requests

class ExchangeRateStrategy(ABC):
    @abstractmethod
    def get_rates(self):
        pass

class OpenExchangeRatesStrategy(ExchangeRateStrategy):
    """Стратегия для получения курса обмена по отношению к USD из стороннего API"""
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def get_rates(self) -> dict:
        try:
            response = requests.get(self.api_url.replace("{api_key}", self.api_key))
            response.raise_for_status()
            return response.json().get("conversion_rates")
        except requests.exceptions.Timeout:
            raise Exception("Время ожидания подключения истекло.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка сети: {e}")
        except Exception as e:
            raise Exception(f"Ошибка при попытке получения курса валют к USD: {e}")
        
class MockExchangeStrategy(ExchangeRateStrategy):
    """Стратегия-заглушка для тестов"""
    def get_rates(self) -> dict:
        return {
            "USD": 1.0,
            "EUR": 0.92,
            "RUB": 92.5,
            "GBP": 0.79
        }
    
    def get_name(self):
        return "Mock (тестовый)"