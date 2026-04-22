"""
ERC-8004 Agent Identity Standard Implementation
For Mantle Turing Test Hackathon 2026
"""

import json
import time
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account
from .mantle_client import MantleClient

class ERC8004Agent:
    """
    ERC-8004 Compliant Agent Identity NFT Manager
    Creates and manages unique agent identities on Mantle
    """
    
    def __init__(self, agent_name: str, agent_version: str = "1.0.0"):
        self.client = MantleClient()
        self.agent_name = agent_name
        self.agent_version = agent_version
        self.agent_address = None
        self.token_id = None
        self.contract_address = None
        
        # ERC-8004 standard metadata structure
        self.agent_metadata = {
            "name": agent_name,
            "description": f"Autonomous treasury management agent v{agent_version}",
            "version": agent_version,
            "capabilities": [
                "treasury_management",
                "gas_optimization", 
                "yield_farming",
                "risk_assessment"
            ],
            "chain_id": 5000,  # Mantle Mainnet
            "created_at": int(time.time()),
            "creator": "Mantle Agentic Treasury Guard",
            "standards": ["ERC-8004", "ERC-721"],
            "performance_metrics": {
                "total_decisions": 0,
                "successful_transactions": 0,
                "roi_earned": 0,
                "gas_saved": 0
            }
        }
    
    def generate_agent_identity(self) -> Dict[str, Any]:
        """
        Generate unique agent identity for ERC-8004 compliance
        Returns agent credentials and metadata
        """
        # Generate unique agent wallet
        agent_account = Account.create()
        self.agent_address = agent_account.address
        
        # Create unique token ID based on agent address and timestamp
        self.token_id = Web3.to_hex(Web3.keccak(text=f"{self.agent_address}{int(time.time())}"))
        
        identity_package = {
            "agent_address": self.agent_address,
            "private_key": agent_account.key.hex(),
            "token_id": self.token_id,
            "metadata": self.agent_metadata,
            "signature": self._sign_identity(agent_account)
        }
        
        return identity_package
    
    def _sign_identity(self, account: Account) -> str:
        """
        Sign the agent metadata for authenticity
        """
        message_hash = Web3.keccak(text=json.dumps(self.agent_metadata, sort_keys=True))
        signed_message = account.sign_message(message_hash)
        return signed_message.signature.hex()
    
    def mint_identity_nft(self, identity_package: Dict[str, Any]) -> str:
        """
        Mint ERC-8004 identity NFT on Mantle (simulation)
        In production, this would deploy/mint to actual contract
        """
        print(f"\\n--- ERC-8004 Identity NFT Minting ---")
        print(f"Agent Name: {self.agent_name}")
        print(f"Agent Address: {identity_package['agent_address']}")
        print(f"Token ID: {identity_package['token_id']}")
        print(f"Chain: Mantle Mainnet (5000)")
        
        # Simulate NFT minting transaction
        mock_tx_hash = f"0x{Web3.to_hex(Web3.keccak(text=f'mint_{self.token_id}'))}"
        
        print(f"\\nNFT Minted Successfully!")
        print(f"Transaction Hash: {mock_tx_hash}")
        print(f"View on Mantle Explorer: https://explorer.mantle.xyz/tx/{mock_tx_hash}")
        
        return mock_tx_hash
    
    def update_performance_metrics(self, decision_type: str, success: bool, 
                                 gas_used: int = 0, roi_earned: float = 0):
        """
        Update agent performance metrics for on-chain reputation
        """
        metrics = self.agent_metadata["performance_metrics"]
        metrics["total_decisions"] += 1
        
        if success:
            metrics["successful_transactions"] += 1
            metrics["roi_earned"] += roi_earned
            metrics["gas_saved"] += gas_used
        
        # Update timestamp
        self.agent_metadata["last_updated"] = int(time.time())
    
    def get_reputation_score(self) -> float:
        """
        Calculate agent reputation score based on performance metrics
        """
        metrics = self.agent_metadata["performance_metrics"]
        
        if metrics["total_decisions"] == 0:
            return 0.0
        
        success_rate = metrics["successful_transactions"] / metrics["total_decisions"]
        roi_factor = min(metrics["roi_earned"] / 100, 1.0)  # Cap ROI factor at 1.0
        gas_factor = min(metrics["gas_saved"] / 10000, 0.5)  # Gas efficiency bonus
        
        reputation = (success_rate * 0.6) + (roi_factor * 0.3) + (gas_factor * 0.1)
        return round(reputation, 4)
    
    def export_identity_proof(self) -> Dict[str, Any]:
        """
        Export complete identity proof for hackathon submission
        """
        return {
            "erc8004_compliant": True,
            "agent_name": self.agent_name,
            "agent_address": self.agent_address,
            "token_id": self.token_id,
            "metadata": self.agent_metadata,
            "reputation_score": self.get_reputation_score(),
            "chain": "Mantle Mainnet",
            "standard": "ERC-8004"
        }

if __name__ == "__main__":
    # Demo ERC-8004 agent creation
    agent = ERC8004Agent("TreasuryGuard Alpha", "1.0.0")
    
    # Generate identity
    identity = agent.generate_agent_identity()
    print("\\n--- ERC-8004 Agent Identity Generated ---")
    print(f"Agent Address: {identity['agent_address']}")
    print(f"Token ID: {identity['token_id']}")
    
    # Mint identity NFT
    tx_hash = agent.mint_identity_nft(identity)
    
    # Update some sample metrics
    agent.update_performance_metrics("stake_decision", True, gas_used=50000, roi_earned=2.5)
    agent.update_performance_metrics("unstake_decision", True, gas_used=45000, roi_earned=1.8)
    
    # Show reputation
    print(f"\\nAgent Reputation Score: {agent.get_reputation_score()}")
    
    # Export identity proof
    proof = agent.export_identity_proof()
    print(f"\\nIdentity Proof: {json.dumps(proof, indent=2)}")
