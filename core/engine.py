import asyncio
import logging
from core.commander import CommanderNode
from db.redis_state_manager import RedisStateManager
from safety_sentinel.arbiter_consensus import ArbiterConsensus

logging.basicConfig(level=logging.INFO)

class TradingEngine:
    """High-frequency event loop orchestrating agent communication and trade execution."""
    
    def __init__(self):
        self.commander = CommanderNode()
        self.cache = RedisStateManager()
        self.consensus = ArbiterConsensus()
        self.is_running = False

    async def start_event_loop(self):
        self.is_running = True
        logging.info("Quantum-TraderX High-Frequency Event Loop Started.")
        
        while self.is_running:
            try:
                # 1. Fetch pending trade signals from Redis state cache
                proposals = await self.cache.get_pending_proposals()
                
                if proposals:
                    # 2. Verify 3-agent Arbiter Consensus
                    approved_proposals = self.consensus.validate_consensus(proposals)
                    
                    if approved_proposals:
                        market_snapshot = await self.cache.get_market_snapshot()
                        
                        # 3. Commander evaluation via Gemini logic
                        decision = await self.commander.evaluate_trade_proposals(
                            market_snapshot, approved_proposals
                        )
                        
                        if decision.get("action") == "EXECUTE":
                            await self.execute_trade(decision)
                            
            except Exception as e:
                logging.error(f"Event Loop Error: {e}")
                
            await asyncio.sleep(0.005)  # Millisecond execution pulse

    async def execute_trade(self, decision: dict):
        logging.info(f"[EXECUTION] Trade Executed: {decision}")

if __name__ == "__main__":
    engine = TradingEngine()
    asyncio.run(engine.start_event_loop())
