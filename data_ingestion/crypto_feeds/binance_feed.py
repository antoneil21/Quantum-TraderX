import asyncio
import json
import websockets
import logging

class BinanceWebsocketFeed:
    """Real-time Binance WebSockets for tick-level data."""
    
    def __init__(self, symbols=["btcusdt", "ethusdt"]):
        self.symbols = symbols
        self.base_url = "wss://stream.binance.com:9443/ws"

    async def start_stream(self, state_manager):
        streams = "/".join([f"{sym}@trade" for sym in self.symbols])
        url = f"{self.base_url}/{streams}"
        
        while True:
            try:
                async for websocket in websockets.connect(url):
                    logging.info(f"Connected to Binance WebSocket: {self.symbols}")
                    async for message in websocket:
                        data = json.loads(message)
                        trade_data = {
                            "exchange": "Binance",
                            "symbol": data.get("s"),
                            "price": float(data.get("p", 0)),
                            "quantity": float(data.get("q", 0)),
                            "timestamp": data.get("T")
                        }
                        
                        # Push live tick data to Redis for the agents to ingest
                        await state_manager.client.set(
                            f"price:binance:{trade_data['symbol']}", 
                            json.dumps(trade_data)
                        )
            except websockets.ConnectionClosed:
                logging.warning("Binance WebSocket disconnected. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                logging.error(f"Binance WebSocket Error: {e}")
                await asyncio.sleep(5)
