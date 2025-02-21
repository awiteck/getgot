from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class ModelSettings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

class Settings(BaseSettings):
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

model_settings = ModelSettings()
settings = Settings()
