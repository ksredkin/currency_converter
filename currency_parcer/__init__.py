import requests
from dotenv import load_dotenv
import os
import time

class CurrencyAPIClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def get_currencies_to_usd(self) -> dict:
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

class Converter:
    def __init__(self, currencies_to_usd: dict):
        self.currencies_to_usd = currencies_to_usd

    def convert_currency(self, currency_from: str, currency_to: str) -> float:
        if not currency_from.upper() in self.currencies_to_usd or not currency_to.upper() in self.currencies_to_usd:
            return None
        return float(f"{(self.currencies_to_usd.get(currency_to.upper()) / self.currencies_to_usd.get(currency_from.upper())):.5f}")

def main():
    print("=== Парсер валют ===")

    load_dotenv()
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise "Необходим API_KEY!"

    if not api_url:
        raise "Необходим API_URL!"

    currency_api_client = CurrencyAPIClient(api_url, api_key)
    currencies_to_usd = currency_api_client.get_currencies_to_usd()
    converter = Converter(currencies_to_usd)

    sep = lambda: print("="*40)

    while True:
        sep()
        print("""Что хотите сделать?
1 - курс валюты по отношению к введённой
2 - курс всех валют по отношению к введённой
3 - выход""")
        
        inp = input("Выбор: ")

        sep()

        match inp:
            case "1":
                currency_from = input("Какую валюту хотите перевести?: ")
                currency_to = input("В какую валюту хотите перевести?: ")
                
                if not currency_from.upper() in currencies_to_usd or not currency_to.upper() in currencies_to_usd:
                    sep()
                    print("Ошибка: Некорректные названия валют!")
                    continue
                
                sep()
                
                print(f"{currency_from} = {converter.convert_currency(currency_from, currency_to)}{currency_to}")
            case "2":
                currency_to = input("В какую валюту хотите перевести?: ")
                
                if not currency_to.upper() in currencies_to_usd:
                    sep()
                    print("Ошибка: Некорректное названия валюты!")
                    continue

                sep()

                for currency in currencies_to_usd.keys():
                    if currency != currency_to:
                        print(f"{currency} = {converter.convert_currency(currency, currency_to)}{currency_to}")

            case "3":
                print("Выход..")
                sep()
                time.sleep(0.75)
                break

            case any:
                print("Ошибка: Такого варианта нет! Попробуйте снова!")

if __name__ == "__main__":
    main()