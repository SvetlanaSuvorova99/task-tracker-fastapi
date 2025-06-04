from fastapi import APIRouter, Depends
from typing import List
from app.schemas.book import Book, BookCreate, BookUpdate
from app.depends.book_service import get_book_service
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[Book])
def get_books(book_service: BookService = Depends(get_book_service)):
    return book_service.get_books()

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    return book_service.get_book(book_id)

@router.post("/", response_model=Book)
async def add_book(book_create: BookCreate, book_service: BookService = Depends(get_book_service)):
    return await book_service.create_book(book_create)

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, book_service: BookService = Depends(get_book_service)):
    return book_service.update_book(book_id, book_update)

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    book_service.delete_book(book_id)
    return None
