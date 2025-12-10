import time
from currency_parcer.factory import ExchangeRateFactory
from datetime import datetime, timezone, timedelta

class CurrencyConverterApp:
    def __init__(self, exchange_rate_strategy: str = "open-exchange-rates"):
        exchange_rate_factory = ExchangeRateFactory()
        self.exchange_rate_strategy = exchange_rate_factory.create_strategy(exchange_rate_strategy)

        self.rates_cache = None
        self.rates_cache_updated_at = None

    def get_rates(self, force: bool = False) -> dict:
        """Получает, кеширует и возвращает курс валют по отношению к USD"""
        try:
            if not self.rates_cache or self.rates_cache_updated_at + timedelta(seconds=300) < datetime.now(timezone.utc) or force:
                print("Обновление кеша курса валют..")
                self.rates_cache = self.exchange_rate_strategy.get_rates()
                self.rates_cache_updated_at = datetime.now(timezone.utc)
            return self.rates_cache

        except Exception as e:
            print(f"Не удалось обновить курсы: {e}")
            if self.rates_cache:
                print("Используются устаревшие курсы (кеш)")
                return self.rates_cache
            else:
                raise Exception("Нет данных о курсах валют")

    def convert_currency(self, currency_from: str, currency_to: str) -> float | None:
        """Возвращает отношение одной валюты к другой, при некорректных видах валют возвращает None"""
        currencies_to_usd = self.get_rates()
        if not currency_from.upper() in currencies_to_usd or not currency_to.upper() in currencies_to_usd:
            return None
        return currencies_to_usd.get(currency_to.upper()) / currencies_to_usd.get(currency_from.upper())

    def run(self):
        sep = lambda: print("="*40)
        sep()
        print("="*7 + " Конвертер (парсер) валют " + "="*7)

        while True:
            sep()
            print("""Что хотите сделать?
1 - курс валюты по отношению к введённой
2 - курс всех валют по отношению к введённой
3 - обновить кеш курса валют
4 - выход""")            
            inp = input("Выбор: ")

            sep()

            match inp:
                case "1":
                    currency_from = input("Какую валюту хотите перевести?: ")
                    currency_to = input("В какую валюту хотите перевести?: ")
                    
                    sep()

                    rate = self.convert_currency(currency_from, currency_to)

                    if not rate:
                        print("Ошибка: Некорректные названия валют!")
                        continue
                    
                    print(f"1 {currency_from.upper()} = {rate:.4f} {currency_to.upper()}")
                case "2":
                    currency_to = input("В какую валюту хотите перевести?: ")
                    
                    sep()

                    rates_keys = self.get_rates().keys()

                    if not currency_to.upper() in rates_keys:
                        print("Ошибка: Некорректное названия валюты!")
                        continue

                    for currency in rates_keys:
                        if currency != currency_to.upper():
                            rate = self.convert_currency(currency, currency_to)
                            print(f"1 {currency.upper()} = {rate:.4f} {currency_to.upper()}")

                case "3":
                    self.get_rates(force=True)

                case "4":
                    print("Выход..")
                    sep()
                    time.sleep(0.75)
                    break

                case any:
                    print("Ошибка: Такого варианта нет! Попробуйте снова!") 

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.run()