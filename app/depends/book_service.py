from fastapi import Depends
from app.services.book_service import BookService
from app.external.jsonbin import JsonBinClient
from app.external.open_library import OpenLibraryClient
from app.repositories.book_repository import BookRepository
from app.depends.external.jsonbin import get_jsonbin_client
from app.depends.external.open_library import get_open_library_client
from app.depends.repository.book_repository import get_book_repository

def get_book_service(
    jsonbin_client: JsonBinClient = Depends(get_jsonbin_client),
    open_library_client: OpenLibraryClient = Depends(get_open_library_client),
    book_repository: BookRepository = Depends(get_book_repository)
) -> BookService:
    return BookService(
        jsonbin_client=jsonbin_client,
        open_library_client=open_library_client,
        book_repository=book_repository
    )