class GuardrailAgent:
    """Hard-coded max drawdown limits to protect bankroll."""
    
    def __init__(self, max_daily_drawdown_pct: float = 0.05, max_trade_pct: float = 0.02):
        self.max_daily_drawdown_pct = max_daily_drawdown_pct
        self.max_trade_pct = max_trade_pct

    def validate_trade(self, portfolio_value: float, current_drawdown_pct: float, trade_amount: float) -> tuple[bool, str]:
        if current_drawdown_pct >= self.max_daily_drawdown_pct:
            return False, f"HALT: Max daily drawdown limit ({self.max_daily_drawdown_pct * 100}%) reached."
            
        if trade_amount > (portfolio_value * self.max_trade_pct):
            return False, f"REJECTED: Trade size exceeds max single trade risk threshold ({self.max_trade_pct * 100}%)."
            
        return True, "PASSED"
