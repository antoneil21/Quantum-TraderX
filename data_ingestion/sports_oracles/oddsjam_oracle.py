import aiohttp
import json
import logging

class OddsJamOracle:
    """Fetches real-time odds across major sportsbooks via OddsJam API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.oddsjam.com/v2/games"

    async def fetch_live_odds(self, sport: str = "americanfootball_nfl") -> list:
        headers = {"X-Api-Key": self.api_key}
        params = {"sport": sport, "status": "pending"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=headers, params=params) as response:
                if response.status != 200:
                    logging.error(f"OddsJam API failed: {response.status}")
                    return []
                data = await response.json()
                return data.get("data", [])
