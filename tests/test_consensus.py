import pytest
from safety_sentinel.arbiter_consensus import ArbiterConsensus

def test_consensus_requires_three_votes():
    arbiter = ArbiterConsensus(required_agreements=3)
    
    # 2 agents vote BUY -> Should fail consensus
    votes_two = [
        {"agent": "yield_scout", "vote": "BUY", "asset": "ETH"},
        {"agent": "quant_modeler", "vote": "BUY", "asset": "ETH"}
    ]
    assert len(arbiter.validate_consensus(votes_two)) == 0

    # 3 agents vote BUY -> Should pass consensus
    votes_three = [
        {"agent": "yield_scout", "vote": "BUY", "asset": "ETH"},
        {"agent": "quant_modeler", "vote": "BUY", "asset": "ETH"},
        {"agent": "mev_arbitrage", "vote": "BUY", "asset": "ETH"}
    ]
    approved = arbiter.validate_consensus(votes_three)
    assert len(approved) == 1
    assert approved[0]["asset"] == "ETH"
    assert approved[0]["action"] == "BUY"
