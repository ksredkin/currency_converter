from dotenv import load_dotenv
import os

class Config:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        load_dotenv()

        self.api_url = os.getenv("API_URL")
        self.api_key = os.getenv("API_KEY")

        if not self.api_url:
            raise ValueError("API_URL не установлен в .env файле")

        if not self.api_key:
            raise ValueError("API_KEY не установлен в .env файле")
        
    def get_api_url(self) -> str:
        return self.api_url

    def get_api_key(self) -> str:
        return self.api_key