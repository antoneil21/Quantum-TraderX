import aiohttp
import asyncio
import json
import logging

class PolymarketFeed:
    """Fetches prediction market odds and volume from the Polymarket Gamma API."""
    
    def __init__(self, market_ids: list):
        self.market_ids = market_ids
        self.base_url = "https://gamma-api.polymarket.com/markets"

    async def fetch_market_odds(self, session, market_id):
        url = f"{self.base_url}/{market_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            logging.error(f"Polymarket API error for {market_id}: {response.status}")
            return None

    async def start_polling(self, state_manager, interval=10):
        async with aiohttp.ClientSession() as session:
            logging.info("Started polling Polymarket Oracles...")
            while True:
                for market_id in self.market_ids:
                    data = await self.fetch_market_odds(session, market_id)
                    
                    if data:
                        market_data = {
                            "oracle": "Polymarket",
                            "question": data.get("question"),
                            # Polymarket returns outcomes and prices as stringified JSON arrays
                            "outcomes": json.loads(data.get("outcomes", "[]")),
                            "outcome_prices": json.loads(data.get("outcomePrices", "[]")),
                            "liquidity": float(data.get("liquidity", 0)),
                            "volume": float(data.get("volume", 0)),
                            "active": data.get("active")
                        }
                        
                        await state_manager.client.set(
                            f"odds:poly:{market_id}", 
                            json.dumps(market_data)
                        )
                await asyncio.sleep(interval)
