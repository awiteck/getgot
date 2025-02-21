from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")


settings = Settings()