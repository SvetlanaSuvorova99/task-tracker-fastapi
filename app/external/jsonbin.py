import httpx
from typing import Dict, Any
from app.config import settings  # импортируем настройки

class JsonBinClient:
    def __init__(self, api_key: str, base_url: str = settings.JSONBIN_API_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key
        }

    async def save_data(self, data: Dict[str, Any]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/b", json=data, headers=self.headers
            )
            response.raise_for_status()
            return response.json()["metadata"]["id"]

    async def get_data(self, bin_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/b/{bin_id}", headers=self.headers
            )
            response.raise_for_status()
            return response.json()["record"]
