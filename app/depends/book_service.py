from fastapi import Depends
from app.services.book_service import BookService
from app.external.open_library import OpenLibraryClient
from app.depends.external.open_library import get_open_library_client
from app.repositories.interfaces.book_repository_interface import BookRepositoryInterface
from app.depends.repository.book_repository import get_book_repository


def get_book_service(
    open_library_client: OpenLibraryClient = Depends(get_open_library_client),
    book_repository: BookRepositoryInterface = Depends(get_book_repository),
) -> BookService:
    return BookService(
        open_library_client=open_library_client,
        book_repository=book_repository,
    )

