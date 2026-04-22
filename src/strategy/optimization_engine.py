"""
Strategy Optimization Engine for TreasuryGuard
Automatically finds optimal parameters for maximum competition performance
"""

import json
import time
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import numpy as np
from .backtesting_engine import BacktestingEngine

@dataclass
class StrategyParameters:
    name: str
    params: Dict[str, Any]
    performance_score: float
    roi_percentage: float
    win_rate: float
    sharpe_ratio: float
    max_drawdown: float

class OptimizationEngine:
    """
    Advanced optimization engine for finding best strategy parameters
    """
    
    def __init__(self):
        self.backtesting_engine = BacktestingEngine()
        self.optimization_history: List[StrategyParameters] = []
        self.best_strategy: StrategyParameters = None
        
    def optimize_strategy(self, strategy_name: str, param_ranges: Dict[str, Tuple[float, float]], 
                         iterations: int = 50) -> StrategyParameters:
        """
        Optimize strategy parameters using grid search and random sampling
        """
        print(f"\\n=== Optimizing {strategy_name} Strategy ===")
        
        best_score = 0.0
        best_params = None
        optimization_results = []
        
        for iteration in range(iterations):
            # Generate random parameters within ranges
            current_params = self._generate_random_params(param_ranges)
            
            # Test strategy with these parameters
            result = self.backtesting_engine.simulate_strategy(strategy_name, current_params)
            
            # Calculate composite score
            score = self._calculate_optimization_score(result)
            
            strategy_config = StrategyParameters(
                name=f"{strategy_name}_v{iteration}",
                params=current_params,
                performance_score=score,
                roi_percentage=result.get("total_roi_percentage", 0),
                win_rate=result.get("win_rate_percentage", 0),
                sharpe_ratio=result.get("sharpe_ratio", 0),
                max_drawdown=result.get("max_drawdown", 0)
            )
            
            optimization_results.append(strategy_config)
            
            # Track best performance
            if score > best_score:
                best_score = score
                best_params = current_params
                self.best_strategy = strategy_config
            
            print(f"Iteration {iteration+1}/{iterations}: Score = {score:.3f}, ROI = {strategy_config.roi_percentage:.2f}%")
        
        self.optimization_history.extend(optimization_results)
        
        print(f"\\nBest {strategy_name} Strategy Found:")
        print(f"Score: {best_score:.3f}")
        print(f"Parameters: {best_params}")
        print(f"Expected ROI: {self.best_strategy.roi_percentage:.2f}%")
        
        return self.best_strategy
    
    def _generate_random_params(self, param_ranges: Dict[str, Tuple[float, float]]) -> Dict[str, Any]:
        """
        Generate random parameters within specified ranges
        """
        params = {}
        for param_name, (min_val, max_val) in param_ranges.items():
            if isinstance(min_val, float) or isinstance(max_val, float):
                params[param_name] = np.random.uniform(min_val, max_val)
            else:
                params[param_name] = np.random.randint(min_val, max_val + 1)
        return params
    
    def _calculate_optimization_score(self, result: Dict[str, Any]) -> float:
        """
        Calculate composite optimization score
        """
        roi = result.get("total_roi_percentage", 0)
        win_rate = result.get("win_rate_percentage", 0)
        sharpe = result.get("sharpe_ratio", 0)
        max_drawdown = result.get("max_drawdown", 100)
        
        # Normalize and weight metrics
        roi_score = min(roi / 20.0, 1.0) * 0.4  # 40% weight, cap at 20% ROI
        win_rate_score = (win_rate / 100.0) * 0.3  # 30% weight
        sharpe_score = min(max(sharpe, 0) / 2.0, 1.0) * 0.2  # 20% weight, cap at 2.0
        drawdown_penalty = max(0, (max_drawdown - 10) / 100) * 0.1  # 10% penalty for high drawdown
        
        composite_score = roi_score + win_rate_score + sharpe_score - drawdown_penalty
        return max(0, composite_score)
    
    def multi_strategy_optimization(self) -> Dict[str, StrategyParameters]:
        """
        Optimize multiple strategies and find the best overall
        """
        strategies_config = {
            "aggressive_apr_based": {
                "param_ranges": {
                    "apr_threshold": (4.0, 8.0),
                    "stake_percentage": (0.1, 0.5)
                }
            },
            "gas_optimized": {
                "param_ranges": {
                    "max_gas": (10, 25),
                    "stake_percentage": (0.15, 0.35)
                }
            },
            "momentum_based": {
                "param_ranges": {
                    "volatility_threshold": (0.3, 0.8),
                    "stake_percentage": (0.2, 0.4)
                }
            },
            "hybrid_intelligent": {
                "param_ranges": {
                    "combined_threshold": (0.4, 0.8),
                    "base_stake_percentage": (0.1, 0.3)
                }
            }
        }
        
        optimized_strategies = {}
        
        for strategy_name, config in strategies_config.items():
            print(f"\\n{'='*50}")
            print(f"Optimizing {strategy_name}")
            print(f"{'='*50}")
            
            best_strategy = self.optimize_strategy(
                strategy_name, 
                config["param_ranges"], 
                iterations=30
            )
            
            optimized_strategies[strategy_name] = best_strategy
        
        # Find overall best strategy
        overall_best = max(optimized_strategies.values(), key=lambda s: s.performance_score)
        
        print(f"\\n{'='*60}")
        print(f"OVERALL BEST STRATEGY: {overall_best.name}")
        print(f"Performance Score: {overall_best.performance_score:.3f}")
        print(f"Expected ROI: {overall_best.roi_percentage:.2f}%")
        print(f"Win Rate: {overall_best.win_rate:.1f}%")
        print(f"Sharpe Ratio: {overall_best.sharpe_ratio:.3f}")
        print(f"Max Drawdown: {overall_best.max_drawdown:.2f}%")
        print(f"Parameters: {overall_best.params}")
        print(f"{'='*60}")
        
        return {
            "strategies": optimized_strategies,
            "overall_best": overall_best,
            "optimization_summary": self._generate_optimization_summary(optimized_strategies)
        }
    
    def _generate_optimization_summary(self, strategies: Dict[str, StrategyParameters]) -> str:
        """
        Generate human-readable optimization summary
        """
        summary = "\\n=== Strategy Optimization Summary ===\\n"
        
        sorted_strategies = sorted(strategies.items(), key=lambda x: x[1].performance_score, reverse=True)
        
        for i, (name, strategy) in enumerate(sorted_strategies, 1):
            summary += f"\\n{i}. {strategy.name}:"
            summary += f"\\n   - Performance Score: {strategy.performance_score:.3f}"
            summary += f"\\n   - Expected ROI: {strategy.roi_percentage:.2f}%"
            summary += f"\\n   - Win Rate: {strategy.win_rate:.1f}%"
            summary += f"\\n   - Sharpe Ratio: {strategy.sharpe_ratio:.3f}"
            summary += f"\\n   - Max Drawdown: {strategy.max_drawdown:.2f}%"
        
        return summary
    
    def adaptive_optimization(self, current_performance: Dict[str, Any]) -> StrategyParameters:
        """
        Adaptively optimize based on current performance
        """
        # Analyze current performance to identify weaknesses
        current_roi = current_performance.get("roi_percentage", 0)
        current_win_rate = current_performance.get("win_rate_percentage", 0)
        current_gas_efficiency = current_performance.get("gas_efficiency", {}).get("avg_gas_per_trade", 25000)
        
        # Determine optimization focus
        if current_roi < 5.0:
            # Focus on ROI improvement
            focus_strategy = "aggressive_apr_based"
            param_adjustment = {"apr_threshold": (4.0, 6.0), "stake_percentage": (0.25, 0.45)}
        elif current_win_rate < 60:
            # Focus on win rate improvement
            focus_strategy = "hybrid_intelligent"
            param_adjustment = {"combined_threshold": (0.5, 0.7), "base_stake_percentage": (0.15, 0.25)}
        elif current_gas_efficiency > 20000:
            # Focus on gas optimization
            focus_strategy = "gas_optimized"
            param_adjustment = {"max_gas": (12, 18), "stake_percentage": (0.18, 0.28)}
        else:
            # Balanced optimization
            focus_strategy = "hybrid_intelligent"
            param_adjustment = {"combined_threshold": (0.4, 0.8), "base_stake_percentage": (0.1, 0.3)}
        
        print(f"\\nAdaptive Optimization Focus: {focus_strategy}")
        print(f"Current ROI: {current_roi:.2f}%, Win Rate: {current_win_rate:.1f}%")
        
        optimized = self.optimize_strategy(focus_strategy, param_adjustment, iterations=20)
        
        return optimized
    
    def export_optimization_results(self) -> Dict[str, Any]:
        """
        Export optimization results for competition submission
        """
        return {
            "optimization_timestamp": int(time.time()),
            "total_strategies_tested": len(self.optimization_history),
            "best_overall_strategy": {
                "name": self.best_strategy.name if self.best_strategy else None,
                "performance_score": self.best_strategy.performance_score if self.best_strategy else 0,
                "parameters": self.best_strategy.params if self.best_strategy else {},
                "expected_roi": self.best_strategy.roi_percentage if self.best_strategy else 0
            },
            "optimization_history": [
                {
                    "name": s.name,
                    "performance_score": s.performance_score,
                    "roi_percentage": s.roi_percentage,
                    "win_rate": s.win_rate,
                    "sharpe_ratio": s.sharpe_ratio,
                    "max_drawdown": s.max_drawdown,
                    "parameters": s.params
                } for s in self.optimization_history
            ]
        }

if __name__ == "__main__":
    # Demo optimization engine
    optimizer = OptimizationEngine()
    
    # Generate historical data for backtesting
    optimizer.backtesting_engine.generate_historical_data(days=30)
    
    # Run multi-strategy optimization
    print("Starting comprehensive strategy optimization...")
    optimization_results = optimizer.multi_strategy_optimization()
    
    # Print summary
    print(optimization_results["optimization_summary"])
    
    # Export results
    export_data = optimizer.export_optimization_results()
    print(f"\\nOptimization completed with {export_data['total_strategies_tested']} strategy variations tested")
    
    # Demo adaptive optimization
    print("\\n=== Adaptive Optimization Demo ===")
    current_perf = {
        "roi_percentage": 3.2,
        "win_rate_percentage": 55,
        "gas_efficiency": {"avg_gas_per_trade": 22000}
    }
    
    adaptive_strategy = optimizer.adaptive_optimization(current_perf)
    print(f"Adaptive optimization complete: {adaptive_strategy.name}")
