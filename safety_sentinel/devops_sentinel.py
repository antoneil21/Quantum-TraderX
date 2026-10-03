import time
import aiohttp
import asyncio

class DevOpsSentinel:
    """Monitors server latency, exchange API response times, and health endpoints."""
    
    def __init__(self, endpoints: dict):
        self.endpoints = endpoints # Key: Name, Value: URL

    async def ping_endpoint(self, session: aiohttp.ClientSession, name: str, url: str) -> dict:
        start_time = time.perf_counter()
        try:
            async with session.get(url, timeout=3.0) as response:
                latency_ms = (time.perf_counter() - start_time) * 1000
                return {
                    "endpoint": name,
                    "status": "ONLINE" if response.status == 200 else "DEGRADED",
                    "latency_ms": round(latency_ms, 2)
                }
        except Exception:
            return {
                "endpoint": name,
                "status": "OFFLINE",
                "latency_ms": -1.0
            }

    async def check_system_health((self)) -> list:
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.ping_endpoint(session, name, url) 
                for name, url in self.endpoints.items()
            ]
            return await asyncio.gather(*tasks)
