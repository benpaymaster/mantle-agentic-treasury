"""
Performance Dashboard for TreasuryGuard
Real-time analytics and visualization for hackathon competition
"""

import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

@dataclass
class PerformanceMetrics:
    timestamp: int
    portfolio_value: float
    roi_percentage: float
    gas_used: int
    reputation_score: float
    apr_rate: float
    strategy_mode: str

class PerformanceDashboard:
    """
    Advanced analytics dashboard for competition monitoring
    """
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.competition_start = int(time.time())
        self.initial_portfolio = 100.0  # $100 starting value
        
    def add_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Add new performance metrics to history
        """
        performance_data = PerformanceMetrics(
            timestamp=metrics.get("timestamp", int(time.time())),
            portfolio_value=metrics.get("portfolio_value", self.initial_portfolio),
            roi_percentage=metrics.get("roi_percentage", 0.0),
            gas_used=metrics.get("gas_used", 0),
            reputation_score=metrics.get("reputation_score", 0.0),
            apr_rate=metrics.get("apr_rate", 0.0),
            strategy_mode=metrics.get("strategy_mode", "CONSERVATIVE")
        )
        
        self.metrics_history.append(performance_data)
    
    def generate_competition_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive competition performance report
        """
        if not self.metrics_history:
            return {"error": "No performance data available"}
        
        current_metrics = self.metrics_history[-1]
        
        # Calculate time-based metrics
        competition_hours = (int(time.time()) - self.competition_start) / 3600
        trades_per_hour = len(self.metrics_history) / competition_hours if competition_hours > 0 else 0
        
        # Calculate performance trends
        roi_trend = self._calculate_roi_trend()
        gas_efficiency = self._calculate_gas_efficiency()
        reputation_growth = self._calculate_reputation_growth()
        
        # Competition positioning
        volume_score = self._calculate_volume_score()
        roi_score = self._calculate_roi_score()
        
        return {
            "report_timestamp": int(time.time()),
            "competition_hours": competition_hours,
            "current_performance": {
                "portfolio_value": current_metrics.portfolio_value,
                "total_roi": current_metrics.roi_percentage,
                "reputation_score": current_metrics.reputation_score,
                "current_apr": current_metrics.apr_rate,
                "strategy_mode": current_metrics.strategy_mode
            },
            "performance_trends": {
                "roi_trend": roi_trend,
                "gas_efficiency": gas_efficiency,
                "reputation_growth": reputation_growth,
                "trades_per_hour": trades_per_hour
            },
            "competition_metrics": {
                "giga_claw_volume_score": volume_score,
                "sharp_claw_roi_score": roi_score,
                "wild_claw_innovation_score": self._calculate_innovation_score()
            },
            "leaderboard_projection": self._project_leaderboard_position()
        }
    
    def _calculate_roi_trend(self) -> str:
        """
        Calculate ROI trend over last 10 periods
        """
        if len(self.metrics_history) < 10:
            return "insufficient_data"
        
        recent = self.metrics_history[-10:]
        roi_values = [m.roi_percentage for m in recent]
        
        # Simple trend calculation
        if roi_values[-1] > roi_values[0] * 1.05:
            return "strongly_increasing"
        elif roi_values[-1] > roi_values[0]:
            return "moderately_increasing"
        elif roi_values[-1] < roi_values[0] * 0.95:
            return "strongly_decreasing"
        else:
            return "stable"
    
    def _calculate_gas_efficiency(self) -> Dict[str, Any]:
        """
        Calculate gas efficiency metrics
        """
        if not self.metrics_history:
            return {"avg_gas_per_trade": 0, "gas_trend": "stable"}
        
        total_gas = sum(m.gas_used for m in self.metrics_history)
        avg_gas = total_gas / len(self.metrics_history)
        
        # Calculate gas trend
        if len(self.metrics_history) >= 10:
            recent_avg = sum(m.gas_used for m in self.metrics_history[-5:]) / 5
            older_avg = sum(m.gas_used for m in self.metrics_history[-10:-5]) / 5
            
            if recent_avg < older_avg * 0.9:
                gas_trend = "improving"
            elif recent_avg > older_avg * 1.1:
                gas_trend = "degrading"
            else:
                gas_trend = "stable"
        else:
            gas_trend = "stable"
        
        return {
            "avg_gas_per_trade": avg_gas,
            "total_gas_used": total_gas,
            "gas_trend": gas_trend
        }
    
    def _calculate_reputation_growth(self) -> float:
        """
        Calculate reputation growth rate
        """
        if len(self.metrics_history) < 2:
            return 0.0
        
        initial_rep = self.metrics_history[0].reputation_score
        current_rep = self.metrics_history[-1].reputation_score
        
        if initial_rep == 0:
            return current_rep
        
        return ((current_rep - initial_rep) / initial_rep) * 100
    
    def _calculate_volume_score(self) -> float:
        """
        Calculate volume score for Giga Claw competition
        """
        # Simulate volume based on trading activity
        total_trades = len(self.metrics_history)
        avg_gas_per_trade = sum(m.gas_used for m in self.metrics_history) / len(self.metrics_history) if self.metrics_history else 0
        
        # Volume score based on trade frequency and size
        volume_score = (total_trades * 100) + (avg_gas_per_trade * 0.001)
        return round(volume_score, 2)
    
    def _calculate_roi_score(self) -> float:
        """
        Calculate ROI score for Sharp Claw competition
        """
        if not self.metrics_history:
            return 0.0
        
        current_roi = self.metrics_history[-1].roi_percentage
        return round(current_roi, 2)
    
    def _calculate_innovation_score(self) -> float:
        """
        Calculate innovation score for Wild Claw competition
        """
        innovation_factors = {
            "erc8004_implementation": 25.0,
            "on_chain_logging": 20.0,
            "dynamic_apr_adjustment": 15.0,
            "gas_optimization": 15.0,
            "reputation_system": 10.0,
            "backtesting_engine": 10.0,
            "performance_dashboard": 5.0
        }
        
        return sum(innovation_factors.values())
    
    def _project_leaderboard_position(self) -> Dict[str, Any]:
        """
        Project potential leaderboard positions
        """
        volume_score = self._calculate_volume_score()
        roi_score = self._calculate_roi_score()
        
        # Simulate competition (these would be real in production)
        simulated_competitors = 500
        
        # Project positions based on scores
        volume_rank = max(1, int(simulated_competitors * (1 - volume_score / 10000)))
        roi_rank = max(1, int(simulated_competitors * (1 - roi_score / 50)))
        
        return {
            "giga_claw_projected_rank": volume_rank,
            "sharp_claw_projected_rank": roi_rank,
            "total_competitors": simulated_competitors,
            "qualification_probability": min(1.0, (volume_score / 5000) + (roi_score / 25))
        }
    
    def generate_visualization_data(self) -> Dict[str, Any]:
        """
        Generate data for visualization charts
        """
        if not self.metrics_history:
            return {"error": "No data for visualization"}
        
        timestamps = [datetime.fromtimestamp(m.timestamp) for m in self.metrics_history]
        portfolio_values = [m.portfolio_value for m in self.metrics_history]
        roi_values = [m.roi_percentage for m in self.metrics_history]
        gas_values = [m.gas_used for m in self.metrics_history]
        reputation_values = [m.reputation_score for m in self.metrics_history]
        
        return {
            "portfolio_chart": {
                "timestamps": [t.isoformat() for t in timestamps],
                "values": portfolio_values,
                "initial_value": self.initial_portfolio
            },
            "roi_chart": {
                "timestamps": [t.isoformat() for t in timestamps],
                "roi_percentages": roi_values
            },
            "gas_chart": {
                "timestamps": [t.isoformat() for t in timestamps],
                "gas_used": gas_values
            },
            "reputation_chart": {
                "timestamps": [t.isoformat() for t in timestamps],
                "reputation_scores": reputation_values
            },
            "strategy_modes": [
                {
                    "timestamp": m.timestamp,
                    "mode": m.strategy_mode
                } for m in self.metrics_history
            ]
        }
    
    def export_competition_data(self) -> Dict[str, Any]:
        """
        Export all competition data for submission
        """
        return {
            "agent_identity": {
                "name": "TreasuryGuard ClawTrader",
                "erc8004_compliant": True,
                "on_chain_logging": True
            },
            "competition_performance": self.generate_competition_report(),
            "visualization_data": self.generate_visualization_data(),
            "raw_metrics": [
                {
                    "timestamp": m.timestamp,
                    "portfolio_value": m.portfolio_value,
                    "roi_percentage": m.roi_percentage,
                    "gas_used": m.gas_used,
                    "reputation_score": m.reputation_score,
                    "apr_rate": m.apr_rate,
                    "strategy_mode": m.strategy_mode
                } for m in self.metrics_history
            ],
            "export_timestamp": int(time.time())
        }

if __name__ == "__main__":
    # Demo performance dashboard
    dashboard = PerformanceDashboard()
    
    # Simulate some performance data
    print("Simulating competition performance...")
    
    for i in range(20):
        metrics = {
            "timestamp": int(time.time()) - (20 - i) * 3600,  # Every hour
            "portfolio_value": 100 + (i * 2.5) + (i % 3),  # Growing portfolio
            "roi_percentage": (i * 0.5) + (i % 2) * 0.2,  # Growing ROI
            "gas_used": 20000 + (i % 5) * 2000,  # Variable gas usage
            "reputation_score": min(1.0, i * 0.05),  # Growing reputation
            "apr_rate": 4.0 + (i % 3) * 0.5,  # Variable APR
            "strategy_mode": "AGGRESSIVE" if i % 5 == 0 else "CONSERVATIVE"
        }
        
        dashboard.add_metrics(metrics)
    
    # Generate competition report
    report = dashboard.generate_competition_report()
    
    print("\\n=== Competition Performance Report ===")
    print(f"Current Portfolio: ${report['current_performance']['portfolio_value']:.2f}")
    print(f"Total ROI: {report['current_performance']['total_roi']:.2f}%")
    print(f"Reputation Score: {report['current_performance']['reputation_score']:.3f}")
    print(f"Strategy Mode: {report['current_performance']['strategy_mode']}")
    
    print(f"\\nROI Trend: {report['performance_trends']['roi_trend']}")
    print(f"Gas Efficiency: {report['performance_trends']['gas_efficiency']['gas_trend']}")
    print(f"Trades per Hour: {report['performance_trends']['trades_per_hour']:.1f}")
    
    print(f"\\nGiga Claw Volume Score: {report['competition_metrics']['giga_claw_volume_score']:.1f}")
    print(f"Sharp Claw ROI Score: {report['competition_metrics']['sharp_claw_roi_score']:.1f}")
    print(f"Wild Claw Innovation Score: {report['competition_metrics']['wild_claw_innovation_score']:.1f}")
    
    projection = report['leaderboard_projection']
    print(f"\\nProjected Giga Claw Rank: #{projection['giga_claw_projected_rank']}")
    print(f"Projected Sharp Claw Rank: #{projection['sharp_claw_projected_rank']}")
    print(f"Qualification Probability: {projection['qualification_probability']:.1%}")
    
    # Export data for submission
    export_data = dashboard.export_competition_data()
    print(f"\\nExported {len(export_data['raw_metrics'])} data points for competition submission")
