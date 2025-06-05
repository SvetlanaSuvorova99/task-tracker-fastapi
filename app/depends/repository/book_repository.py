from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.book_repository import BookRepository
from app.repositories.json_file_repository import JsonFileRepository
from app.repositories.jsonbin_repository import JsonBinRepository
from app.external.jsonbin import JsonBinClient
from app.config import settings
from app.db.session import get_db
from app.repositories.interfaces.book_repository_interface import BookRepositoryInterface


def get_book_repository(
    db: Session = Depends(get_db),
    jsonbin_client: JsonBinClient = Depends(lambda: JsonBinClient(api_key=settings.JSONBIN_API_KEY))
) -> BookRepositoryInterface:
    print("📦 Используем хранилище:", settings.BOOK_STORAGE_TYPE)
    if settings.BOOK_STORAGE_TYPE == "postgres":
        return BookRepository(db)
    elif settings.BOOK_STORAGE_TYPE == "file":
        return JsonFileRepository()
    elif settings.BOOK_STORAGE_TYPE == "jsonbin":
        return JsonBinRepository(jsonbin_client, settings.JSONBIN_BIN_ID)
    else:
        raise ValueError(f"Unknown storage type: {settings.BOOK_STORAGE_TYPE}")




