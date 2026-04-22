"""
Backtesting Engine for TreasuryGuard Strategies
Test and optimize strategies before live deployment
"""

import json
import time
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class MarketCondition:
    timestamp: int
    gas_gwei: float
    mnt_price: float
    meth_apr: float
    volatility_score: float
    liquidity_score: float

@dataclass
class TradeResult:
    timestamp: int
    action: str
    amount: float
    gas_used: int
    profit: float
    portfolio_value: float
    market_conditions: MarketCondition

class BacktestingEngine:
    """
    Comprehensive backtesting system for strategy optimization
    """
    
    def __init__(self):
        self.initial_portfolio = 100.0  # $100 starting value
        self.current_portfolio = self.initial_portfolio
        self.trade_history: List[TradeResult] = []
        self.market_data: List[MarketCondition] = []
        
    def generate_historical_data(self, days: int = 30) -> List[MarketCondition]:
        """
        Generate realistic historical market data for backtesting
        """
        market_data = []
        base_time = int(time.time()) - (days * 24 * 60 * 60)
        
        for day in range(days):
            timestamp = base_time + (day * 24 * 60 * 60)
            
            # Simulate realistic market patterns
            gas_gwei = 5 + (day % 20) + (hash(f"gas_{day}") % 10)
            mnt_price = 0.45 + (day % 100) / 200 + (hash(f"price_{day}") % 50) / 1000
            meth_apr = 3.5 + (day % 30) / 10 + (hash(f"apr_{day}") % 100) / 100
            volatility = 0.2 + (day % 50) / 100
            liquidity = 0.7 + (day % 40) / 100
            
            market_data.append(MarketCondition(
                timestamp=timestamp,
                gas_gwei=gas_gwei,
                mnt_price=mnt_price,
                meth_apr=meth_apr,
                volatility_score=volatility,
                liquidity_score=liquidity
            ))
        
        self.market_data = market_data
        return market_data
    
    def simulate_strategy(self, strategy_name: str, strategy_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate a trading strategy over historical data
        """
        self.current_portfolio = self.initial_portfolio
        self.trade_history = []
        
        if not self.market_data:
            return {"error": "No market data available"}
        
        for condition in self.market_data:
            decision = self._execute_strategy_logic(strategy_name, condition, strategy_params)
            
            if decision["action"] != "hold":
                trade_result = self._execute_trade(decision, condition)
                self.trade_history.append(trade_result)
        
        return self._calculate_performance_metrics(strategy_name)
    
    def _execute_strategy_logic(self, strategy_name: str, condition: MarketCondition, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute specific strategy logic based on market conditions
        """
        if strategy_name == "aggressive_apr_based":
            # Aggressive strategy based on high APR
            if condition.meth_apr >= params.get("apr_threshold", 5.0):
                return {
                    "action": "stake",
                    "amount": self.current_portfolio * params.get("stake_percentage", 0.3),
                    "reasoning": f"High APR ({condition.meth_apr:.2f}%) above threshold"
                }
            else:
                return {"action": "hold", "reasoning": "APR below threshold"}
        
        elif strategy_name == "gas_optimized":
            # Gas-optimized strategy
            if condition.gas_gwei <= params.get("max_gas", 15):
                return {
                    "action": "stake",
                    "amount": self.current_portfolio * params.get("stake_percentage", 0.2),
                    "reasoning": f"Low gas ({condition.gas_gwei:.1f} Gwei) optimal for staking"
                }
            else:
                return {"action": "hold", "reasoning": "Gas too high"}
        
        elif strategy_name == "momentum_based":
            # Momentum-based strategy using volatility
            if condition.volatility_score >= params.get("volatility_threshold", 0.5):
                return {
                    "action": "stake",
                    "amount": self.current_portfolio * params.get("stake_percentage", 0.25),
                    "reasoning": f"High volatility ({condition.volatility_score:.2f}) indicates opportunity"
                }
            else:
                return {"action": "hold", "reasoning": "Low volatility - wait for better conditions"}
        
        elif strategy_name == "hybrid_intelligent":
            # Hybrid strategy combining multiple factors
            apr_score = min(condition.meth_apr / 5.0, 1.0)  # Normalize APR to 0-1
            gas_score = max(0, (20 - condition.gas_gwei) / 20)  # Inverse gas score
            liquidity_score = condition.liquidity_score
            
            combined_score = (apr_score * 0.4) + (gas_score * 0.3) + (liquidity_score * 0.3)
            
            if combined_score >= params.get("combined_threshold", 0.6):
                stake_percentage = params.get("base_stake_percentage", 0.2) + (combined_score * 0.2)
                return {
                    "action": "stake",
                    "amount": self.current_portfolio * min(stake_percentage, 0.5),
                    "reasoning": f"Strong combined score ({combined_score:.2f}) with APR: {condition.meth_apr:.2f}%, Gas: {condition.gas_gwei:.1f}"
                }
            else:
                return {"action": "hold", "reasoning": f"Weak combined score ({combined_score:.2f})"}
        
        else:
            return {"action": "hold", "reasoning": "Unknown strategy"}
    
    def _execute_trade(self, decision: Dict[str, Any], condition: MarketCondition) -> TradeResult:
        """
        Execute a trade and calculate results
        """
        action = decision["action"]
        amount = decision.get("amount", 0)
        
        if action == "stake":
            # Calculate gas cost
            gas_used = 25000
            gas_cost = (gas_used * condition.gas_gwei) / 10**9 * condition.mnt_price
            
            # Calculate profit based on APR
            daily_return = (condition.meth_apr / 100) / 365
            profit = (amount - gas_cost) * daily_return
            
            # Update portfolio
            self.current_portfolio = self.current_portfolio - gas_cost + profit
            
        else:  # hold
            gas_used = 0
            profit = 0
        
        return TradeResult(
            timestamp=condition.timestamp,
            action=action,
            amount=amount,
            gas_used=gas_used,
            profit=profit,
            portfolio_value=self.current_portfolio,
            market_conditions=condition
        )
    
    def _calculate_performance_metrics(self, strategy_name: str) -> Dict[str, Any]:
        """
        Calculate comprehensive performance metrics
        """
        # Always return metrics, even with no trades
        total_trades = len(self.trade_history)
        profitable_trades = sum(1 for trade in self.trade_history if trade.profit > 0)
        total_profit = sum(trade.profit for trade in self.trade_history)
        total_gas_used = sum(trade.gas_used for trade in self.trade_history)
        
        # Calculate ROI (portfolio may change even without trades)
        final_value = self.current_portfolio
        total_roi = ((final_value - self.initial_portfolio) / self.initial_portfolio) * 100
        
        # Calculate daily metrics
        days_active = len(self.market_data)
        avg_daily_profit = total_profit / days_active if days_active > 0 else 0
        avg_daily_gas = total_gas_used / days_active if days_active > 0 else 0
        
        # Calculate win rate
        win_rate = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0
        
        return {
            "name": strategy_name,
            "initial_portfolio": self.initial_portfolio,
            "final_portfolio": final_value,
            "total_roi_percentage": total_roi,
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "win_rate_percentage": win_rate,
            "total_profit": total_profit,
            "total_gas_used": total_gas_used,
            "avg_daily_profit": avg_daily_profit,
            "avg_daily_gas": avg_daily_gas,
            "sharpe_ratio": self._calculate_sharpe_ratio(),
            "max_drawdown": self._calculate_max_drawdown(),
            "no_trades_executed": total_trades == 0
        }
    
    def _calculate_sharpe_ratio(self) -> float:
        """
        Calculate Sharpe ratio for risk-adjusted returns
        """
        if len(self.trade_history) < 2:
            return 0.0
        
        profits = [trade.profit for trade in self.trade_history]
        avg_profit = sum(profits) / len(profits)
        
        # Calculate standard deviation
        variance = sum((profit - avg_profit) ** 2 for profit in profits) / len(profits)
        std_dev = variance ** 0.5
        
        # Assume risk-free rate of 2% annually
        risk_free_daily = 0.02 / 365
        
        return (avg_profit - risk_free_daily) / std_dev if std_dev > 0 else 0.0
    
    def _calculate_max_drawdown(self) -> float:
        """
        Calculate maximum drawdown from peak
        """
        peak = self.initial_portfolio
        max_drawdown = 0.0
        
        for trade in self.trade_history:
            if trade.portfolio_value > peak:
                peak = trade.portfolio_value
            
            drawdown = (peak - trade.portfolio_value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return max_drawdown * 100  # Return as percentage
    
    def compare_strategies(self, strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple strategies and rank them
        """
        results = []
        
        for strategy in strategies:
            result = self.simulate_strategy(strategy["name"], strategy["params"])
            results.append(result)
        
        # Rank by total ROI
        results.sort(key=lambda x: x.get("total_roi_percentage", 0), reverse=True)
        
        return {
            "ranking": results,
            "best_strategy": results[0] if results else None,
            "comparison_summary": self._generate_comparison_summary(results)
        }
    
    def _generate_comparison_summary(self, results: List[Dict[str, Any]]) -> str:
        """
        Generate a human-readable comparison summary
        """
        if not results:
            return "No strategies to compare"
        
        summary = f"\\n=== Strategy Comparison Summary ===\\n"
        
        for i, result in enumerate(results, 1):
            name = result.get("name", "Unknown")
            roi = result.get("total_roi_percentage", 0)
            win_rate = result.get("win_rate_percentage", 0)
            trades = result.get("total_trades", 0)
            
            summary += f"\\n{i}. {name}:"
            summary += f"\\n   - Total ROI: {roi:.2f}%"
            summary += f"\\n   - Win Rate: {win_rate:.1f}%"
            summary += f"\\n   - Total Trades: {trades}"
        
        return summary

if __name__ == "__main__":
    # Demo backtesting engine
    engine = BacktestingEngine()
    
    # Generate historical data
    print("Generating historical market data...")
    market_data = engine.generate_historical_data(days=30)
    print(f"Generated {len(market_data)} days of market data")
    
    # Define strategies to test
    strategies = [
        {
            "name": "aggressive_apr_based",
            "params": {"apr_threshold": 5.0, "stake_percentage": 0.3}
        },
        {
            "name": "gas_optimized", 
            "params": {"max_gas": 15, "stake_percentage": 0.2}
        },
        {
            "name": "momentum_based",
            "params": {"volatility_threshold": 0.5, "stake_percentage": 0.25}
        },
        {
            "name": "hybrid_intelligent",
            "params": {"combined_threshold": 0.6, "base_stake_percentage": 0.2}
        }
    ]
    
    # Compare strategies
    print("\\nRunning strategy comparison...")
    comparison = engine.compare_strategies(strategies)
    
    print(comparison["comparison_summary"])
    
    if comparison["best_strategy"]:
        best = comparison["best_strategy"]
        print(f"\\n=== BEST STRATEGY: {best['strategy_name']} ===")
        print(f"Total ROI: {best['total_roi_percentage']:.2f}%")
        print(f"Win Rate: {best['win_rate_percentage']:.1f}%")
        print(f"Sharpe Ratio: {best['sharpe_ratio']:.3f}")
        print(f"Max Drawdown: {best['max_drawdown']:.2f}%")
