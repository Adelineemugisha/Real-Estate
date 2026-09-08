import httpx
from config import settings


class LocationIQService:
    BASE_URL = "https://us1.locationiq.com/v1/search.php"

    @staticmethod
    async def geocode(address: str) -> dict | None:
        params = {
            "key": settings.LOCATIONIQ_API_KEY,
            "q": address,
            "format": "json",
            "limit": 1,
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(LocationIQService.BASE_URL, params=params)
            response.raise_for_status()
            results = response.json()
            if results:
                return {
                    "lat": float(results[0]["lat"]),
                    "lon": float(results[0]["lon"]),
                }
        return None

    @staticmethod
    def build_address(location) -> str:
        parts = [location.street_address, location.city, location.state_province]
        if location.country:
            parts.append(location.country)
        if location.postal_code:
            parts.append(location.postal_code)
        return ", ".join(parts)
