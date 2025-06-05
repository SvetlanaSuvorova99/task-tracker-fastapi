from typing import List
from app.schemas.book import BookCreate, BookUpdate, Book
from app.core.logger import get_logger
from app.external.open_library import OpenLibraryClient
from fastapi import HTTPException, status
from app.repositories.interfaces.book_repository_interface import BookRepositoryInterface
from app.repositories.jsonbin_repository import JsonBinRepository

logger = get_logger()

class BookService:
    def __init__(
        self,
        open_library_client: OpenLibraryClient,
        book_repository: BookRepositoryInterface,
    ):
        self.open_library = open_library_client
        self.repo = book_repository

    def get_books(self) -> List[Book]:
        return self.repo.get_books()

    def get_book(self, book_id: int) -> Book:
        book = self.repo.get_book(book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    async def create_book(self, book_create: BookCreate) -> Book:
        ol_data = self.open_library.get_book_info(book_create.title)
        if ol_data:
            logger.info(f"Обогащаем книгу данными из OpenLibrary: {ol_data.get('title')}")
            book_create.description = ol_data.get("description", "")
            book_create.cover = ol_data.get("cover", "")

        saved_book = self.repo.add_book(book_create)

        if isinstance(self.repo, JsonBinRepository):
            jsonbin_id = self.repo.client.save_data(book_create.model_dump())
            logger.info(f"Книга сохранена на jsonbin.io с ID: {jsonbin_id}")

        return saved_book

    def update_book(self, book_id: int, book_update: BookUpdate) -> Book:
        book = self.repo.update_book(book_id, book_update)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    def delete_book(self, book_id: int) -> None:
        success = self.repo.delete_book(book_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
