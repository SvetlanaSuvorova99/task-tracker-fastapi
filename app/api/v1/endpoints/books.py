from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book_service import BookService
from app.db.session import get_db
from app.external.jsonbin import JsonBinClient  # Импортируем клиента для jsonbin.io
from app.config import settings  # Импортируем настройки для получения API-ключа jsonbin.io

# Инициализация клиента jsonbin.io
jsonbin_client = JsonBinClient(api_key=settings.JSONBIN_API_KEY)

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[Book], summary="Список всех книг")
def get_books(db: Session = Depends(get_db)):
    # Инициализация BookService с клиентом jsonbin.io
    book_service = BookService(db, jsonbin_client)
    return book_service.get_books()

@router.get("/{book_id}", response_model=Book, summary="Получить книгу по ID")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book_service = BookService(db, jsonbin_client)
    return book_service.get_book(book_id)

@router.post("/", response_model=Book, summary="Добавить новую книгу")
async def add_book(book_create: BookCreate, db: Session = Depends(get_db)):
    book_service = BookService(db, jsonbin_client)
    return await book_service.create_book(book_create)

@router.put("/{book_id}", response_model=Book, summary="Обновить книгу")
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book_service = BookService(db, jsonbin_client)
    return book_service.update_book(book_id, book_update)

@router.delete("/{book_id}", status_code=204, summary="Удалить книгу")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_service = BookService(db, jsonbin_client)
    book_service.delete_book(book_id)
    return None