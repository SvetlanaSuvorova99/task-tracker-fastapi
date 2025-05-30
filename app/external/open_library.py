from typing import Optional
from app.external.base_api_client import BaseApiClient


class OpenLibraryClient(BaseApiClient):
    def __init__(self):
        super().__init__("https://openlibrary.org")

    def get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """Реализация обязательного абстрактного метода"""
        response = self.client.get(endpoint, params=params)
        if response.status_code != 200:
            return None
        return response.json()

    def get_book_info(self, title: str) -> Optional[dict]:
        """
        Получаем основную информацию о книге по названию.
        Возвращаем описание, обложку и рейтинг книги.
        """
        data = self.get("/search.json", params={"title": title})
        if data and data.get("docs"):
            # Извлекаем первую книгу из найденных
            book_data = data["docs"][0]

            # Строим результат с нужными полями
            result = {
                "description": self.get_description(book_data),  # Получаем описание
                "cover": self.get_cover_url(book_data),  # Получаем URL обложки
                "rating": self.get_rating(book_data)  # Получаем рейтинг
            }

            return result
        return None
    @staticmethod
    def get_description(book_data: dict) -> str:
        """
        Получаем описание книги.
        Если описание не найдено, возвращаем 'Описание не найдено'.
        """
        # OpenLibrary может хранить описание книги в поле subject
        if "subject" in book_data:
            return book_data["subject"][0] if isinstance(book_data["subject"], list) else book_data["subject"]
        return "Описание не найдено"

    @staticmethod
    def get_cover_url(book_data: dict) -> Optional[str]:
        """
        Получаем URL обложки книги, если она есть.
        """
        cover_id = book_data.get("cover_i")
        if cover_id:
            # Составляем полный URL для обложки
            return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        return None

    @staticmethod
    def get_rating(book_data: dict) -> Optional[float]:
        """
        Получаем рейтинг книги, если он есть.
        """
        # Рейтинг книги может быть в поле average_rating, но не всегда
        return book_data.get("average_rating", None)