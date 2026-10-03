import numpy as np

class QuantModeler:
    """Real-time mathematical edge detection."""
    
    @staticmethod
    def calculate_z_score(price_series: list) -> float:
        """Detects statistical mean-reversion opportunities."""
        if len(price_series) < 20:
            return 0.0
        arr = np.array(price_series)
        mean = np.mean(arr)
        std = np.std(arr)
        if std == 0:
            return 0.0
        return float((arr[-1] - mean) / std)

    def generate_signal(self, price_series: list) -> dict:
        z_score = self.calculate_z_score(price_series)
        
        if z_score < -2.0:
            return {"signal": "BUY", "edge": abs(z_score), "strategy": "Mean Reversion"}
        elif z_score > 2.0:
            return {"signal": "SELL", "edge": abs(z_score), "strategy": "Mean Reversion"}
        
        return {"signal": "HOLD", "edge": 0.0, "strategy": "None"}
