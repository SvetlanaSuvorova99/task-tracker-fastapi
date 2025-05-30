import httpx
from typing import Dict, Any

class JsonBinClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.jsonbin.io/v3"
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key  # API-ключ для доступа к jsonbin.io
        }

    async def save_data(self, data: Dict[str, Any]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/b", json=data, headers=self.headers
            )
            response.raise_for_status()  # Поднимет исключение в случае ошибки
            return response.json()["metadata"]["id"]  # Возвращаем ID записи

    async def get_data(self, bin_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/b/{bin_id}", headers=self.headers
            )
            response.raise_for_status()  # Поднимет исключение в случае ошибки
            return response.json()["record"]