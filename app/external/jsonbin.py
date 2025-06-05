import httpx
from typing import Dict, Any
from app.config import settings


class JsonBinClient:
    def __init__(self, api_key: str, base_url: str = settings.JSONBIN_API_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key
        }

    def save_data(self, data: Dict[str, Any]) -> str:
        response = httpx.post(f"{self.base_url}/b", json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()["metadata"]["id"]

    def get_data(self, bin_id: str) -> Dict[str, Any]:
        response = httpx.get(f"{self.base_url}/b/{bin_id}/latest", headers=self.headers)
        response.raise_for_status()
        return response.json()["record"]

    def update_data(self, bin_id: str, data: Dict[str, Any]) -> None:
        response = httpx.put(f"{self.base_url}/b/{bin_id}", json=data, headers=self.headers)
        response.raise_for_status()




