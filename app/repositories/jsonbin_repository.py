from typing import List, Optional
from app.schemas.book import Book, BookCreate, BookUpdate
from app.external.jsonbin import JsonBinClient


class JsonBinRepository:
    def __init__(self, client: JsonBinClient, bin_id: str):
        self.client = client
        self.bin_id = bin_id

    def get_books(self) -> List[Book]:
        data = self.client.get_data(self.bin_id)
        books_raw = data.get("books", [])  # ожидаем {"books": [...]}
        return [Book(**item) for item in books_raw]

    def get_book(self, book_id: int) -> Optional[Book]:
        books = self.get_books()
        return next((b for b in books if b.id == book_id), None)

    def add_book(self, book_create: BookCreate) -> Book:
        books = self.get_books()
        new_id = max((b.id for b in books), default=0) + 1
        new_book = Book(id=new_id, **book_create.model_dump())
        books.append(new_book)
        self._save_books(books)
        return new_book

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        books = self.get_books()
        for i, book in enumerate(books):
            if book.id == book_id:
                updated = book.model_copy(update=book_update.model_dump())
                books[i] = updated
                self._save_books(books)
                return updated
        return None

    def delete_book(self, book_id: int) -> bool:
        books = self.get_books()
        new_books = [b for b in books if b.id != book_id]
        if len(new_books) == len(books):
            return False
        self._save_books(new_books)
        return True

    def _save_books(self, books: List[Book]) -> None:
        payload = {"books": [book.model_dump() for book in books]}
        self.client.update_data(self.bin_id, payload)
