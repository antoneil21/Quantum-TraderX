import aiohttp
import asyncio
import json
import logging

class DexScreenerFeed:
    """Polls DexScreener API for on-chain liquidity, volume, and price data."""
    
    def __init__(self, token_addresses: list):
        self.token_addresses = token_addresses
        self.base_url = "https://api.dexscreener.com/latest/dex/tokens/"

    async def fetch_token_data(self, session, token_address):
        url = f"{self.base_url}{token_address}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            logging.error(f"DexScreener API error for {token_address}: {response.status}")
            return None

    async def start_polling(self, state_manager, interval=5):
        async with aiohttp.ClientSession() as session:
            logging.info("Started polling DexScreener...")
            while True:
                for token in self.token_addresses:
                    data = await self.fetch_token_data(session, token)
                    
                    if data and data.get("pairs"):
                        best_pair = data["pairs"][0] # Grab the highest liquidity pair
                        token_data = {
                            "exchange": "DEX",
                            "symbol": best_pair.get("baseToken", {}).get("symbol"),
                            "price_usd": float(best_pair.get("priceUsd", 0)),
                            "liquidity_usd": float(best_pair.get("liquidity", {}).get("usd", 0)),
                            "volume_24h": float(best_pair.get("volume", {}).get("h24", 0)),
                            "chain": best_pair.get("chainId")
                        }
                        
                        await state_manager.client.set(
                            f"price:dex:{token_data['symbol']}", 
                            json.dumps(token_data)
                        )
                await asyncio.sleep(interval) # Respect API rate limits
