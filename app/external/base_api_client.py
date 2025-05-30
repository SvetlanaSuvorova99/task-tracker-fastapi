from abc import ABC, abstractmethod
import httpx

class BaseApiClient(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=10)

    @abstractmethod
    def get(self, endpoint: str, params: dict = None):
        pass

    def close(self):
        self.client.close()
