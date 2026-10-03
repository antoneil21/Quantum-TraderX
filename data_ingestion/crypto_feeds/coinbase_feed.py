import asyncio
import json
import websockets
import logging

class CoinbaseWebsocketFeed:
    """Real-time Coinbase Advanced Trade WebSocket client."""
    
    def __init__(self, product_ids=["BTC-USD", "ETH-USD"]):
        self.product_ids = product_ids
        self.ws_url = "wss://ws-feed.exchange.coinbase.com"

    async def start_stream(self, state_manager):
        subscribe_msg = {
            "type": "subscribe",
            "product_ids": self.product_ids,
            "channels": ["ticker"]
        }
        
        while True:
            try:
                async for websocket in websockets.connect(self.ws_url):
                    await websocket.send(json.dumps(subscribe_msg))
                    async for message in websocket:
                        data = json.loads(message)
                        if data.get("type") == "ticker":
                            ticker_data = {
                                "exchange": "Coinbase",
                                "symbol": data.get("product_id"),
                                "price": float(data.get("price", 0)),
                                "volume": float(data.get("volume_24h", 0)),
                                "timestamp": data.get("time")
                            }
                            await state_manager.client.set(
                                f"price:coinbase:{ticker_data['symbol']}", 
                                json.dumps(ticker_data)
                            )
            except Exception as e:
                logging.error(f"Coinbase WS Error: {e}")
                await asyncio.sleep(5)
