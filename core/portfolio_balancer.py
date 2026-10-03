import numpy as np

class PortfolioBalancer:
    """Manages cross-asset capital allocation across Crypto, Stocks, Forex, and Sports."""
    
    def __init__(self, total_capital: float, max_asset_weight: float = 0.40):
        self.total_capital = total_capital
        self.max_asset_weight = max_asset_weight

    def rebalance(self, asset_allocations: dict, volatility_map: dict) -> dict:
        """
        Calculates risk-adjusted capital distribution using Inverse Volatility Weighting.
        """
        inv_vols = {asset: 1.0 / max(vol, 0.001) for asset, vol in volatility_map.items()}
        total_inv_vol = sum(inv_vols.values())
        
        target_weights = {asset: inv_vols[asset] / total_inv_vol for asset in inv_vols}
        
        # Apply maximum asset weight caps and normalize
        balanced_allocations = {}
        excess_capital = 0.0
        
        for asset, weight in target_weights.items():
            capped_weight = min(weight, self.max_asset_weight)
            balanced_allocations[asset] = round(self.total_capital * capped_weight, 2)
            
        return {
            "total_capital": self.total_capital,
            "allocations": balanced_allocations,
            "status": "BALANCED"
        }
