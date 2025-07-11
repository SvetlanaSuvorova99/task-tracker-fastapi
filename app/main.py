from fastapi import FastAPI
from app.api.v1.endpoints import books
from app.core.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="Book Catalog API",
    description="REST API для управления каталогом книг с обогащением из OpenLibrary",
    version="1.0.0",
    contact={"name": "Your Name", "email": "you@example.com"},
    openapi_tags=[{"name": "Books", "description": "Операции с книгами"}]
)

app.include_router(books.router, prefix="/books", tags=["Books"])
