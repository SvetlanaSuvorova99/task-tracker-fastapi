from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOOK_STORAGE_TYPE: str = "file"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/books"
    LOG_LEVEL: str = "INFO"
    JSONBIN_API_KEY: str
    JSONBIN_API_URL: str = "https://api.jsonbin.io/v3"
    JSONBIN_BIN_ID: str
    OPENLIBRARY_API_URL: str = "https://openlibrary.org"
    OPENLIBRARY_COVER_URL: str = "https://covers.openlibrary.org/b/id"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

