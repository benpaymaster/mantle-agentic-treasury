"""
RealClaw Trading Agent for Mantle Turing Test Hackathon - Phase 1: ClawHack
Optimized for MerchantMoe, Fluxion, and Agnidex protocols
Competes for Giga Claw (volume) and Sharp Claw (ROI) prizes
"""

import json
import time
from typing import Dict, Any, List, Tuple
from src.blockchain.mantle_client import MantleClient
from src.blockchain.erc8004_agent import ERC8004Agent
from src.blockchain.on_chain_logger import OnChainLogger

class RealClawTrader:
    """
    AI Trading Agent for RealClaw Platform
    Implements strategies for volume generation and ROI optimization
    """
    
    def __init__(self, agent_name: str = "TreasuryGuard ClawTrader"):
        self.client = MantleClient()
        self.agent_identity = ERC8004Agent(agent_name, "1.0.0")
        self.on_chain_logger = OnChainLogger(self.agent_identity.agent_address)
        
        # Trading configuration
        self.min_trade_amount = 10.0  # Minimum $10 equivalent
        self.max_gas_price = 15  # Max 15 Gwei
        self.target_protocols = ["MerchantMoe", "Fluxion", "Agnidex"]
        
        # Competition tracking
        self.initial_portfolio_value = 0.0
        self.current_portfolio_value = 0.0
        self.total_trading_volume = 0.0
        self.trade_count = 0
        self.start_time = int(time.time())
        
        # Strategy parameters
        self.volume_weight = 0.6  # Focus on volume for Giga Claw
        self.roi_weight = 0.4     # Balance with ROI for Sharp Claw
        
        print(f"\\n--- RealClaw Trading Agent Initialized ---")
        print(f"Agent ID: {self.agent_identity.agent_address}")
        print(f"Competition: ClawHack Phase 1")
        print(f"Target Protocols: {', '.join(self.target_protocols)}")
        print(f"Strategy: Volume + ROI Balanced ({self.volume_weight}/{self.roi_weight})")
    
    def analyze_market_conditions(self) -> Dict[str, Any]:
        """
        Analyze current market conditions across target protocols
        """
        gas_price_wei = self.client.w3.eth.gas_price
        gas_gwei = gas_price_wei / 10**9
        
        market_data = {
            "gas_gwei": gas_gwei,
            "gas_acceptable": gas_gwei <= self.max_gas_price,
            "timestamp": int(time.time()),
            "protocol_opportunities": {}
        }
        
        # Simulate protocol analysis (in production, use real DEX data)
        for protocol in self.target_protocols:
            market_data["protocol_opportunities"][protocol] = {
                "liquidity_score": self._simulate_liquidity_score(protocol),
                "volatility_score": self._simulate_volatility_score(protocol),
                "volume_potential": self._simulate_volume_potential(protocol),
                "roi_potential": self._simulate_roi_potential(protocol)
            }
        
        return market_data
    
    def _simulate_liquidity_score(self, protocol: str) -> float:
        """Simulate liquidity scoring for protocol"""
        base_scores = {"MerchantMoe": 0.85, "Fluxion": 0.75, "Agnidex": 0.80}
        return base_scores.get(protocol, 0.7) + (hash(protocol) % 10) / 100
    
    def _simulate_volatility_score(self, protocol: str) -> float:
        """Simulate volatility scoring for protocol"""
        return 0.3 + (hash(f"vol_{protocol}") % 40) / 100
    
    def _simulate_volume_potential(self, protocol: str) -> float:
        """Simulate volume potential for protocol"""
        base_potential = {"MerchantMoe": 0.9, "Fluxion": 0.8, "Agnidex": 0.85}
        return base_potential.get(protocol, 0.7)
    
    def _simulate_roi_potential(self, protocol: str) -> float:
        """Simulate ROI potential for protocol"""
        return 0.02 + (hash(f"roi_{protocol}") % 30) / 1000  # 2-5% range
    
    def calculate_portfolio_value(self) -> float:
        """
        Calculate current portfolio value across all tokens
        $MNT, $USDC, $USDT, $USDe
        """
        # Get MNT balance
        mnt_balance = float(self.client.get_mnt_balance()) if isinstance(self.client.get_mnt_balance(), (int, float)) else 0.0
        
        # Simulate other token balances (in production, query actual contracts)
        usdc_balance = self._simulate_token_balance("USDC")
        usdt_balance = self._simulate_token_balance("USDT") 
        usde_balance = self._simulate_token_balance("USDe")
        
        # Simulate token prices (in production, use price oracle)
        mnt_price = 0.5  # $0.50 per MNT
        usdc_price = 1.0
        usdt_price = 1.0
        usde_price = 1.0
        
        total_value = (mnt_balance * mnt_price + 
                      usdc_balance * usdc_price + 
                      usdt_balance * usdt_price + 
                      usde_balance * usde_price)
        
        self.current_portfolio_value = total_value
        return total_value
    
    def _simulate_token_balance(self, token: str) -> float:
        """Simulate token balance for demo purposes"""
        return 50.0 + (hash(token) % 100)  # $50-150 range
    
    def execute_trading_strategy(self) -> Dict[str, Any]:
        """
        Execute trading strategy based on market conditions
        """
        market_data = self.analyze_market_conditions()
        portfolio_value = self.calculate_portfolio_value()
        
        if self.initial_portfolio_value == 0.0:
            self.initial_portfolio_value = portfolio_value
        
        # Determine best protocol for current conditions
        best_protocol = self._select_best_protocol(market_data)
        
        # Calculate trade parameters
        trade_decision = self._calculate_trade_parameters(best_protocol, market_data, portfolio_value)
        
        # Execute trade (simulation)
        execution_result = self._execute_trade(best_protocol, trade_decision, market_data)
        
        # Log to on-chain record
        self.on_chain_logger.log_decision(
            "trading_decision",
            {
                "protocol": best_protocol,
                "market_data": market_data,
                "trade_decision": trade_decision,
                "portfolio_value": portfolio_value
            },
            execution_result["outcome"],
            gas_used=execution_result.get("gas_used", 0)
        )
        
        # Update agent metrics
        self.agent_identity.update_performance_metrics(
            "trade_execution", 
            execution_result["success"],
            execution_result.get("gas_saved", 0),
            execution_result.get("profit", 0)
        )
        
        return execution_result
    
    def _select_best_protocol(self, market_data: Dict[str, Any]) -> str:
        """Select best protocol based on weighted scoring"""
        best_score = 0
        best_protocol = self.target_protocols[0]
        
        for protocol in self.target_protocols:
            opp = market_data["protocol_opportunities"][protocol]
            
            # Weighted score for competition
            score = (opp["volume_potential"] * self.volume_weight + 
                    opp["roi_potential"] * self.roi_weight * 10)  # Scale ROI
            
            if score > best_score:
                best_score = score
                best_protocol = protocol
        
        return best_protocol
    
    def _calculate_trade_parameters(self, protocol: str, market_data: Dict[str, Any], portfolio_value: float) -> Dict[str, Any]:
        """Calculate optimal trade parameters"""
        opp = market_data["protocol_opportunities"][protocol]
        
        # Base trade amount on portfolio size and market conditions
        trade_fraction = 0.1 + (opp["liquidity_score"] * 0.2)  # 10-30% of portfolio
        trade_amount = max(self.min_trade_amount, portfolio_value * trade_fraction)
        
        # Determine trade direction based on volatility and ROI potential
        if opp["volatility_score"] > 0.6 and opp["roi_potential"] > 0.03:
            trade_direction = "buy"  # High volatility + good ROI = buy opportunity
        elif opp["volatility_score"] < 0.4:
            trade_direction = "sell"  # Low volatility = take profits
        else:
            trade_direction = "hold"  # Moderate conditions = hold
        
        return {
            "protocol": protocol,
            "direction": trade_direction,
            "amount": trade_amount,
            "expected_gas": 25000 + (opp["liquidity_score"] * 10000),
            "expected_roi": opp["roi_potential"],
            "volume_contribution": trade_amount * 2  # Assume 2x volume with swaps
        }
    
    def _execute_trade(self, protocol: str, trade_params: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trade on selected protocol"""
        self.trade_count += 1
        
        # Simulate trade execution
        success = True
        gas_used = int(trade_params["expected_gas"])
        profit = 0.0
        
        if trade_params["direction"] == "buy":
            # Simulate successful buy with some profit
            profit = trade_params["amount"] * trade_params["expected_roi"] * 0.8
            self.total_trading_volume += trade_params["volume_contribution"]
            outcome = f"BUY {trade_params['amount']:.2f} on {protocol} - Profit: ${profit:.2f}"
        elif trade_params["direction"] == "sell":
            # Simulate sell with profit taking
            profit = trade_params["amount"] * 0.02  # 2% profit on sell
            self.total_trading_volume += trade_params["volume_contribution"]
            outcome = f"SELL {trade_params['amount']:.2f} on {protocol} - Profit: ${profit:.2f}"
        else:
            outcome = f"HOLD - Market conditions suboptimal on {protocol}"
            gas_used = 0
        
        # Calculate gas savings
        gas_savings = max(0, (self.max_gas_price - market_data["gas_gwei"]) * gas_used / 10**9)
        
        return {
            "success": success,
            "outcome": outcome,
            "gas_used": gas_used,
            "gas_saved": gas_savings,
            "profit": profit,
            "protocol": protocol,
            "trade_count": self.trade_count
        }
    
    def get_competition_metrics(self) -> Dict[str, Any]:
        """
        Get current competition metrics for leaderboard tracking
        """
        current_roi = 0.0
        if self.initial_portfolio_value > 0:
            current_roi = (self.current_portfolio_value / self.initial_portfolio_value) - 1
        
        return {
            "agent_id": self.agent_identity.agent_address,
            "competition": "ClawHack Phase 1",
            "total_trading_volume": self.total_trading_volume,
            "current_portfolio_value": self.current_portfolio_value,
            "initial_portfolio_value": self.initial_portfolio_value,
            "roi_percentage": current_roi * 100,
            "trade_count": self.trade_count,
            "reputation_score": self.agent_identity.get_reputation_score(),
            "uptime_hours": (int(time.time()) - self.start_time) / 3600,
            "giga_claw_ranking_data": {
                "volume_score": self.total_trading_volume,
                "target_protocols": self.target_protocols
            },
            "sharp_claw_ranking_data": {
                "roi_score": current_roi,
                "asset_change_rate": current_roi
            }
        }
    
    def run_competition_cycle(self) -> Dict[str, Any]:
        """
        Run one complete competition cycle
        """
        print(f"\\n--- Competition Cycle #{self.trade_count + 1} ---")
        
        # Execute trading strategy
        result = self.execute_trading_strategy()
        
        # Get competition metrics
        metrics = self.get_competition_metrics()
        
        print(f"Trade Result: {result['outcome']}")
        print(f"Total Volume: ${metrics['total_trading_volume']:.2f}")
        print(f"Current ROI: {metrics['roi_percentage']:.2f}%")
        print(f"Reputation: {metrics['reputation_score']:.4f}")
        
        return {
            "trade_result": result,
            "competition_metrics": metrics,
            "timestamp": int(time.time())
        }

if __name__ == "__main__":
    # Demo RealClaw trading agent
    trader = RealClawTrader("TreasuryGuard ClawTrader Alpha")
    
    # Run few competition cycles
    for i in range(3):
        cycle_result = trader.run_competition_cycle()
        time.sleep(1)  # Brief pause between cycles
    
    # Final competition report
    final_metrics = trader.get_competition_metrics()
    print(f"\\n--- Final Competition Report ---")
    print(f"Total Trading Volume: ${final_metrics['total_trading_volume']:.2f}")
    print(f"Final ROI: {final_metrics['roi_percentage']:.2f}%")
    print(f"Total Trades: {final_metrics['trade_count']}")
    print(f"Agent Reputation: {final_metrics['reputation_score']:.4f}")
