import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class MantleClient:
    def __init__(self):
        rpc_url = os.getenv("MANTLE_RPC_URL", "https://rpc.mantle.xyz")
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Use a public address for watching
        self.public_address = os.getenv("PUBLIC_WALLET_ADDRESS")

        if not self.w3.is_connected():
            print("❌ Connection Failed to Mantle RPC")
        else:
            print(f"✅ Connected to Mantle (Chain ID: {self.w3.eth.chain_id})")

    def get_mnt_balance(self):
        if not self.public_address or "your_actual" in self.public_address:
            return "0.0 (No Address Set)"
        
        balance_wei = self.w3.eth.get_balance(self.public_address)
        return Web3.from_wei(balance_wei, 'ether')

if __name__ == "__main__":
    client = MantleClient()
    print(f"📡 Watching Wallet: {client.public_address}")
    print(f"💰 Balance: {client.get_mnt_balance()} MNT")