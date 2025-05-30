from fastapi import FastAPI
from app.api.v1.endpoints import books
from app.core.logger import get_logger
from app.external.jsonbin import JsonBinClient  # Импортируем JsonBinClient
from app.config import settings
from app.services.book_service import BookService
from app.db.session import SessionLocal  # Импортируем сессию базы данных

logger = get_logger()

# Создаем клиент для jsonbin.io
jsonbin_client = JsonBinClient(api_key=settings.JSONBIN_API_KEY)

# Создаем экземпляр BookService, передавая клиент jsonbin.io
def get_book_service() -> BookService:
    db = SessionLocal()  # Получаем сессию базы данных
    return BookService(db=db, jsonbin_client=jsonbin_client)

app = FastAPI(
    title="Book Catalog API",
    description="REST API для управления каталогом книг с обогащением из OpenLibrary",
    version="1.0.0",
    contact={"name": "Your Name", "email": "you@example.com"},
    openapi_tags=[{"name": "Books", "description": "Операции с книгами"}]
)

app.include_router(books.router, prefix="/books", tags=["Books"])