class QuantumTraderError(Exception):
    """Base exception for all custom Quantum-TraderX errors."""
    pass

class SafetyGuardrailTriggered(QuantumTraderError):
    """Raised when the GuardrailAgent halts trading to protect the bankroll."""
    pass

class ConsensusFailedError(QuantumTraderError):
    """Raised when 3-agent agreement is not reached."""
    pass

class MarketDataTimeoutError(QuantumTraderError):
    """Raised when WebSockets or Oracle feeds go stale."""
    pass
