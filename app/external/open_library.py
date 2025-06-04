from typing import Optional
from app.external.base_api_client import BaseApiClient
from app.config import settings  # добавь импорт

class OpenLibraryClient(BaseApiClient):
    def __init__(self):
        super().__init__(settings.OPENLIBRARY_API_URL)

    def get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        response = self.client.get(endpoint, params=params)
        if response.status_code != 200:
            return None
        return response.json()

    def get_book_info(self, title: str) -> Optional[dict]:
        data = self.get("/search.json", params={"title": title})
        if data and data.get("docs"):
            book_data = data["docs"][0]
            return {
                "description": self.get_description(book_data),
                "cover": self.get_cover_url(book_data),
                "rating": self.get_rating(book_data)
            }
        return None

    @staticmethod
    def get_description(book_data: dict) -> str:
        if "subject" in book_data:
            return book_data["subject"][0] if isinstance(book_data["subject"], list) else book_data["subject"]
        return "Описание не найдено"

    @staticmethod
    def get_cover_url(book_data: dict) -> Optional[str]:
        cover_id = book_data.get("cover_i")
        if cover_id:
            return f"{settings.OPENLIBRARY_COVER_URL}/{cover_id}-L.jpg"
        return None

    @staticmethod
    def get_rating(book_data: dict) -> Optional[float]:
        return book_data.get("average_rating", None)
