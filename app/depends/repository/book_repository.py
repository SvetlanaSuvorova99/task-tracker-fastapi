from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository
from app.depends.db import get_db

def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    return BookRepository(db)
