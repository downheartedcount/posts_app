import httpx
import logging

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(
            self,
            base_url: str = "https://jsonplaceholder.typicode.com",
            timeout: int = 10
    ):
        self.base_url = base_url
        self.client = None
        self.timeout = timeout

    async def startup(self):
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout, connect=5.0)
        )

    async def shutdown(self):
        if self.client:
            await self.client.aclose()

    async def get(self, endpoint: str):
        if not self.client:
            raise RuntimeError(
                "HTTPClient not initialized. Call startup() first."
            )
        try:
            response = await self.client.get(endpoint)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed GET {endpoint}: {e}")
            raise
