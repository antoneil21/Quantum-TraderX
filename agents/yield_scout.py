import aiohttp
import asyncio

class YieldScout:
    """Hunts highest APY opportunities across DeFi/Crypto protocols via DefiLlama."""
    
    def __init__(self, min_tvl: float = 1_000_000, min_apy: float = 5.0):
        self.min_tvl = min_tvl
        self.min_apy = min_apy
        self.defillama_url = "https://yields.llama.fi/pools"

    async def find_yield_opportunities(self) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.defillama_url) as response:
                if response.status != 200:
                    return []
                data = await response.json()
                
                opportunities = []
                for pool in data.get("data", []):
                    tvl = pool.get("tvlUsd", 0)
                    apy = pool.get("apy", 0)
                    
                    if tvl >= self.min_tvl and apy >= self.min_apy:
                        opportunities.append({
                            "agent": "yield_scout",
                            "chain": pool.get("chain"),
                            "project": pool.get("project"),
                            "symbol": pool.get("symbol"),
                            "apy": round(apy, 2),
                            "tvl_usd": round(tvl, 2),
                            "vote": "BUY",
                            "asset": pool.get("symbol")
                        })
                
                # Sort by highest APY
                return sorted(opportunities, key=lambda x: x["apy"], reverse=True)[:10]
