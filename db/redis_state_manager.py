import json
import redis.asyncio as redis

class RedisStateManager:
    """Millisecond cache for agent communication and state management."""
    
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    async def push_agent_proposal(self, agent_name: str, proposal: dict):
        proposal["agent"] = agent_name
        await self.client.rpush("queue:proposals", json.dumps(proposal))

    async def get_pending_proposals(self) -> list:
        proposals = []
        while True:
            item = await self.client.lpop("queue:proposals")
            if not item:
                break
            proposals.append(json.loads(item))
        return proposals

    async def get_market_snapshot(self) -> dict:
        raw_data = await self.client.get("state:market_snapshot")
        return json.loads(raw_data) if raw_data else {}
