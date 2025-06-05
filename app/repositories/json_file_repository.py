import json
from pathlib import Path
from typing import List, Optional
from app.schemas.book import Book, BookCreate, BookUpdate
import logging

logger = logging.getLogger(__name__)

FILE_PATH = Path("data/books.json")

class JsonFileRepository:
    def __init__(self):
        FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not FILE_PATH.exists():
            FILE_PATH.write_text("[]")

    @staticmethod
    def _load_books() -> List[Book]:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Book(**item) for item in data]

    @staticmethod
    def _save_books(books: List[Book]):
        logger.info(f"Сохраняем {len(books)} книг в файл")
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([book.model_dump() for book in books], f, ensure_ascii=False, indent=2)

    def get_books(self) -> List[Book]:
        return self._load_books()

    def get_book(self, book_id: int) -> Optional[Book]:
        return next((b for b in self._load_books() if b.id == book_id), None)

    def add_book(self, book_create: BookCreate) -> Book:
        books = self._load_books()
        new_id = max((b.id for b in books), default=0) + 1
        new_book = Book(id=new_id, **book_create.model_dump())
        books.append(new_book)
        self._save_books(books)
        return new_book

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        books = self._load_books()
        for i, book in enumerate(books):
            if book.id == book_id:
                updated = book.model_copy(update=book_update.model_dump())
                books[i] = updated
                self._save_books(books)
                return updated
        return None

    def delete_book(self, book_id: int) -> bool:
        books = self._load_books()
        new_books = [b for b in books if b.id != book_id]
        if len(new_books) == len(books):
            return False
        self._save_books(new_books)
        return True
