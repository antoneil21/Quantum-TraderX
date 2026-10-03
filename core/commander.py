import os
import json
import asyncio
from google import genai
from google.genai import types

class CommanderNode:
    """Gemini Pro Thinking reasoning engine for trade orchestration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"

    async def evaluate_trade_proposals(self, market_data: dict, proposals: list) -> dict:
        prompt = f"""
        Act as the Commander Node for Quantum-TraderX.
        Analyze the following agent proposals against current market conditions.
        
        Market Context: {json.dumps(market_data)}
        Proposals: {json.dumps(proposals)}
        
        Return a JSON response with:
        - action: "EXECUTE" or "REJECT"
        - target_agent: name of the agent proposal to execute
        - rationale: brief justification
        - confidence_score: float (0.0 to 1.0)
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
