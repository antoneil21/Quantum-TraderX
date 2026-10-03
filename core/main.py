import asyncio
from db.redis_state_manager import RedisStateManager
from core.engine import TradingEngine
from data_ingestion.crypto_feeds.binance_feed import BinanceWebsocketFeed
from data_ingestion.crypto_feeds.dexscreener_feed import DexScreenerFeed
from data_ingestion.sports_oracles.polymarket_feed import PolymarketFeed

async def main():
    """Bootstraps the entire Quantum-TraderX node and fires up the agents."""
    
    state_manager = RedisStateManager()
    engine = TradingEngine()
    
    # Initialize Data Feeds
    binance = BinanceWebsocketFeed(symbols=["btcusdt", "ethusdt", "solusdt"])
    
    # Example DexScreener token (WETH on Ethereum)
    dexscreener = DexScreenerFeed(token_addresses=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"])
    
    # Example Polymarket ID
    polymarket = PolymarketFeed(market_ids=["1"]) 

    # Run everything concurrently
    await asyncio.gather(
        engine.start_event_loop(),
        binance.start_stream(state_manager),
        dexscreener.start_polling(state_manager),
        polymarket.start_polling(state_manager)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Quantum-TraderX gracefully shut down.")
