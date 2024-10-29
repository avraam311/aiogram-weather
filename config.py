import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Config:
    def __init__(self):
        self.bot_token: str = os.getenv('BOT_TOKEN')
        self.weather_api_key: str = os.getenv('WEATHER_API_KEY')
        self.weather_api_url: str = os.getenv('WEATHER_API_URL')
        self.redis_username: str = os.getenv('REDIS_USERNAME')
        self.redis_password: str = os.getenv('REDIS_PASSWORD')
        self.redis_host: str = os.getenv('REDIS_HOST')
        self.redis_port: int = int(os.getenv('REDIS_PORT'))
        self.redis_db: int = int(os.getenv('REDIS_DB'))

    def validate(self) -> None:
        if not self.bot_token:
            raise ValueError("BOT_TOKEN не установлен")
        if not self.weather_api_key:
            raise ValueError("WEATHER_API_KEY не установлен")
        if not self.weather_api_url:
            raise ValueError("WEATHER_API_URL не установлен")
        if not self.redis_username:
            raise ValueError("REDIS_USERNAME не установлен")
        if not self.redis_password:
            raise ValueError("REDIS_PASSWORD не установлен")
        if not self.redis_host:
            raise ValueError("REDIS_HOST не установлен")
        if not self.redis_port:
            raise ValueError("REDIS_PORT не установлен")
        if not self.redis_db:
            raise ValueError("REDIS_DB не установлен")
