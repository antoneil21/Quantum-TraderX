class ArbiterConsensus:
    """Requires at least 3 agent approvals before enabling trade execution."""
    
    def __init__(self, required_agreements: int = 3):
        self.required_agreements = required_agreements

    def validate_consensus(self, agent_votes: list) -> list:
        """
        agent_votes expected structure:
        [{"agent": "yield_scout", "vote": "BUY", "asset": "ETH"}, ...]
        """
        asset_votes = {}
        
        for vote in agent_votes:
            key = (vote.get("asset"), vote.get("vote"))
            if key not in asset_votes:
                asset_votes[key] = []
            asset_votes[key].append(vote)
            
        approved = []
        for (asset, action), votes in asset_votes.items():
            if len(votes) >= self.required_agreements and action != "HOLD":
                approved.append({
                    "asset": asset,
                    "action": action,
                    "votes_count": len(votes),
                    "supporting_agents": [v.get("agent") for v in votes]
                })
                
        return approved
