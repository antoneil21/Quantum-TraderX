import aiohttp
import asyncio
import logging

class SportradarOracle:
    """Fetches real-time sports data and injury reports via Sportradar API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportradar.us/nfl/official/trial/v7/en"

    async def fetch_game_statistics(self, game_id: str) -> dict:
        url = f"{self.base_url}/games/{game_id}/statistics.json?api_key={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "oracle": "Sportradar",
                        "game_id": data.get("id"),
                        "status": data.get("status"),
                        "home_team": data.get("summary", {}).get("home", {}).get("name"),
                        "away_team": data.get("summary", {}).get("away", {}).get("name")
                    }
                logging.error(f"Sportradar API error: {response.status}")
                return {}
