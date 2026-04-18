import os
from src.blockchain.mantle_client import MantleClient

class TreasuryGuard:
    def __init__(self):
        self.client = MantleClient()
        # threshold for a profitable stake (example: 1 MNT)
        self.min_stake = 1.0 
        # Max gas price we are willing to pay (in Gwei)
        self.max_gas = 15 

    def analyze(self):
        print("\n--- 🤖 Agentic Analysis ---")
        balance = self.client.get_mnt_balance()
        # Handle the "No Address Set" string from our earlier failsafe
        current_balance = float(balance) if isinstance(balance, (int, float)) else 0.0
        
        gas_price_wei = self.client.w3.eth.gas_price
        gas_gwei = gas_price_wei / 10**9

        print(f"Current Balance: {current_balance} MNT")
        print(f"Current Gas: {gas_gwei:.2f} Gwei")

        if current_balance > self.min_stake and gas_gwei <= self.max_gas:
            return "✅ STATUS: OPTIMAL. Recommendation: Stake MNT for mETH."
        elif current_balance <= self.min_stake:
            return "⏳ STATUS: HOLDING. Reason: Insufficient balance for gas efficiency."
        else:
            return "⛽ STATUS: WAITING. Reason: Gas prices too high for target ROI."

if __name__ == "__main__":
    guard = TreasuryGuard()
    decision = guard.analyze()
    print(decision)