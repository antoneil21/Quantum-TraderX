class SmartContractAuditor:
    """Scans Web3 code and bytecode for common rug-pull indicators."""
    
    DANGEROUS_OPCODES = ["SELFDESTRUCT", "DELEGATECALL"]
    
    def audit_contract_source(self, source_code: str) -> dict:
        flags = []
        
        if "function mint(" in source_code and "onlyOwner" not in source_code:
            flags.append("UNPROTECTED_MINT_FUNCTION")
        if "selfdestruct" in source_code.lower():
            flags.append("SELFDESTRUCT_FOUND")
        if "blackList" in source_code or "isBlacklisted" in source_code:
            flags.append("BLACKLIST_LOGIC_PRESENT")
        if "maxTxAmount" in source_code and "0" in source_code:
            flags.append("POTENTIAL_HONEYPOT_SETTER")

        is_safe = len(flags) == 0
        return {
            "safe": is_safe,
            "risk_score": len(flags) * 25,
            "flags": flags
        }
