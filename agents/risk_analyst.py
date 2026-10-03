class RiskAnalyst:
    """Calculates optimal position sizes using the Kelly Criterion."""
    
    def __init__(self, kelly_fraction: float = 0.5):
        self.fraction = kelly_fraction  # Half-Kelly for risk management

    def calculate_kelly_size(self, win_probability: float, win_loss_ratio: float, account_balance: float) -> float:
        """
        Kelly Criterion Formula: f* = (p * b - q) / b
        p = win probability, q = 1 - p, b = odds/ratio
        """
        if win_loss_ratio <= 0 or win_probability <= 0:
            return 0.0
            
        q = 1.0 - win_probability
        kelly_percentage = (win_probability * win_loss_ratio - q) / win_loss_ratio
        
        # Apply Fractional Kelly limit and clamp between 0% and 10% max allocation per trade
        safe_percentage = max(0.0, min(kelly_percentage * self.fraction, 0.10))
        return round(account_balance * safe_percentage, 2)
