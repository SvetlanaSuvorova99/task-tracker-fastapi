from typing import List, Optional, cast
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        result = self.db.query(Book).offset(skip).limit(limit).all()
        return cast(List[Book], result)

    def get_book(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter_by(id=book_id).first()

    def add_book(self, book_create: BookCreate) -> Book:
        book = Book(**book_create.model_dump())  # <--- для Pydantic 2.x
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        book = self.get_book(book_id)
        if not book:
            return None
        for field, value in book_update.model_dump().items():
            setattr(book, field, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if not book:
            return False
        self.db.delete(book)
        self.db.commit()
        return True
