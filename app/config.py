from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/books"
    LOG_LEVEL: str = "INFO"
    JSONBIN_API_KEY: str = os.getenv('JSONBIN_API_KEY')

    model_config = {
        "env_file": ".env",
        "extra": "ignore",  # если вдруг в .env попадёт что-то лишнее
    }

settings = Settings()