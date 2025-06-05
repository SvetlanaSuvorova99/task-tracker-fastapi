from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    """Базовые данные книги."""
    title: str
    author: str
    year: int
    genre: str
    pages: int
    available: bool
    description: Optional[str] = None
    cover: Optional[str] = None
    rating: Optional[float] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True