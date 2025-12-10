from currency_parcer.strategies import MockExchangeStrategy, OpenExchangeRatesStrategy, ExchangeRateStrategy
from currency_parcer.config import Config

class ExchangeRateFactory:
    """Создает стратегию для получения курса валют по отношению к доллару"""
    def create_strategy(self, strategy: str = "open-exchange-rates") -> ExchangeRateStrategy:
        config = Config() 
        
        strategies = {
            "open-exchange-rates": OpenExchangeRatesStrategy(config.get_api_url(), config.get_api_key()),
            "mock-exchange-rates": MockExchangeStrategy()
        }

        if strategy not in strategies:
            raise ValueError(f"Неизвестная стратегия: {strategy}")
        
        return strategies.get(strategy)