# TreasuryGuard Deployment Guide
## Mantle Turing Test Hackathon 2026 - Phase 1: ClawHack

### 🚀 Quick Start for Competition

Once you're whitelisted and have your $MNT deposit, follow these steps:

### Step 1: Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Verify all dependencies are installed
pip install -r requirements.txt

# Test basic connectivity
python3 -m src.agents.treasury_guard
```

### Step 2: Strategy Optimization (Pre-Deployment)
```bash
# Run strategy optimization to find best parameters
python3 -c "
from src.agents.treasury_guard import TreasuryGuard
guard = TreasuryGuard()
results = guard.optimize_strategy_parameters()
print(f'Best strategy: {results[\"overall_best\"][\"name\"]}')
"
```

### Step 3: Backtesting Validation
```bash
# Test your strategy with historical data
python3 -c "
from src.agents.treasury_guard import TreasuryGuard
guard = TreasuryGuard()
backtest = guard.run_backtesting_analysis(days=30)
print(f'Expected ROI: {backtest[\"best_strategy\"][\"total_roi_percentage\"]:.2f}%')
"
```

### Step 4: RealClaw Platform Deployment
1. **Navigate to RealClaw Platform**: [https://claw.byreal.io](https://claw.byreal.io)
2. **Connect Your Wallet**: Use the wallet with your $MNT deposit
3. **Upload Agent Strategy**: Import optimized parameters from Step 2
4. **Set Competition Parameters**:
   - Minimum trade amount: $10 equivalent
   - Gas limit: 15-25 Gwei (adjust based on APR)
   - Strategy mode: AGGRESSIVE (if APR ≥ 5%) else CONSERVATIVE

### Step 5: Competition Monitoring
```bash
# Generate real-time performance dashboard
python3 -c "
from src.agents.treasury_guard import TreasuryGuard
guard = TreasuryGuard()
dashboard = guard.generate_competition_dashboard()
print(f'Current ROI: {dashboard[\"current_performance\"][\"total_roi\"]:.2f}%')
print(f'Projected Rank: #{dashboard[\"leaderboard_projection\"][\"giga_claw_projected_rank\"]}')
"
```

## 🎯 Competition Strategy

### Giga Claw (Volume Focus)
- **Target**: $50,000+ daily trading volume
- **Method**: High-frequency, low-margin trades
- **Protocols**: Rotate between MerchantMoe, Fluxion, Agnidex
- **Gas Optimization**: Trade when gas < 15 Gwei

### Sharp Claw (ROI Focus)  
- **Target**: 15-25% ROI over competition period
- **Method**: Momentum + mean reversion hybrid
- **APR Threshold**: Aggressive when mETH APR ≥ 5%
- **Risk Management**: Dynamic position sizing

### Wild Claw (Innovation)
- **ERC-8004 Identity**: ✅ Implemented
- **On-Chain Logging**: ✅ Every decision recorded
- **Dynamic Strategy**: ✅ APR-based adaptation
- **Advanced Analytics**: ✅ Real-time dashboard

## 📊 Key Metrics to Monitor

### Primary KPIs
- **Total Trading Volume**: Giga Claw ranking
- **ROI Percentage**: Sharp Claw ranking  
- **Reputation Score**: ERC-8004 on-chain reputation
- **Gas Efficiency**: Average gas per trade
- **Win Rate**: Percentage of profitable trades

### Alert Thresholds
- **Volume Alert**: < $10,000 daily volume
- **ROI Alert**: < 5% weekly performance
- **Gas Alert**: > 20 Gwei average
- **Reputation Alert**: < 0.5 score

## 🔧 Advanced Features

### Strategy Optimization Engine
- **Multi-Strategy Testing**: Conservative, Aggressive, Balanced, Hybrid
- **Parameter Tuning**: Automatic optimization based on backtesting
- **Adaptive Adjustment**: Real-time strategy switching
- **Performance Scoring**: Composite ROI + risk metrics

### Performance Dashboard
- **Real-time Analytics**: Portfolio value, ROI trends
- **Competition Metrics**: Live leaderboard projections
- **Visualization Data**: Export-ready charts
- **Historical Tracking**: Complete performance history

### Backtesting System
- **Historical Simulation**: 30+ days of market data
- **Strategy Comparison**: Automated ranking system
- **Risk Metrics**: Sharpe ratio, max drawdown
- **Parameter Optimization**: Grid search + random sampling

## 🏆 Winning Formula

### Technical Excellence (40%)
1. ERC-8004 Compliance ✅
2. On-Chain Transparency ✅
3. Gas Optimization ✅
4. Advanced Analytics ✅

### Strategic Performance (40%)
1. Volume Generation ✅
2. ROI Optimization ✅
3. Risk Management ✅
4. Adaptation Speed ✅

### Innovation (20%)
1. Dynamic APR Strategy ✅
2. Multi-Protocol Trading ✅
3. Real-Time Optimization ✅
4. Comprehensive Analytics ✅

## 📞 Support & Troubleshooting

### Common Issues
- **Connection Failed**: Check RPC URL in `.env`
- **Low Balance**: Ensure ≥ $100 in eligible tokens
- **High Gas**: Wait for gas prices < 15 Gwei
- **Strategy Not Executing**: Verify APR threshold logic

### Debug Commands
```bash
# Test individual components
python3 -m src.blockchain.mantle_client
python3 -m src.blockchain.meth_apr_fetcher
python3 -m src.strategy.backtesting_engine
python3 -m src.analytics.performance_dashboard
```

### Export Competition Data
```bash
# Generate complete competition package
python3 -c "
from src.agents.treasury_guard import TreasuryGuard
guard = TreasuryGuard()
package = guard.export_competition_package()
import json
with open('competition_package.json', 'w') as f:
    json.dump(package, f, indent=2)
print('Competition package exported to competition_package.json')
"
```

## 🎁 Submission Package

When ready to submit, include:
1. **Source Code**: Complete repository
2. **Performance Data**: `competition_package.json`
3. **Strategy Report**: Optimization results
4. **Innovation Docs**: ERC-8004 implementation
5. **Demo Video**: Live trading session (optional)

---

**Good luck in the Mantle Turing Test Hackathon! 🚀**

*Built for the Agent Economy. Powered by Mantle.*
