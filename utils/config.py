import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Config:
    """Centralized configuration for the Task Force."""
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    
    # Risk parameters
    MAX_DAILY_DRAWDOWN = float(os.getenv("MAX_DAILY_DRAWDOWN", 0.05))
    MAX_TRADE_SIZE_PCT = float(os.getenv("MAX_TRADE_SIZE_PCT", 0.02))
    
    # API Keys
    SPORTSRADAR_API_KEY = os.getenv("SPORTSRADAR_API_KEY")
    ODDSJAM_API_KEY = os.getenv("ODDSJAM_API_KEY")
