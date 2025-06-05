from app.external.jsonbin import JsonBinClient
from app.config import settings

def get_jsonbin_client() -> JsonBinClient:
    return JsonBinClient(api_key=settings.JSONBIN_API_KEY)