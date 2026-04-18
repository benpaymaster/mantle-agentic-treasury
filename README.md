
# 🛡️ Mantle Agentic Treasury Guard
### *Autonomous DeFi Yield Optimization on Mantle Network*

**Mantle Agentic Treasury Guard** is a modular AI agent designed to automate the lifecycle of $MNT staking. Built during the 2026 "Agentic Summer," this tool leverages Mantle's high-performance modular rollup architecture to monitor, analyze, and execute staking strategies with minimal gas overhead and maximum capital efficiency.

---

## 🚀 The Vision
In a multi-chain world, manual treasury management is a bottleneck. This project moves away from "User-Initiated" DeFi toward **"Intent-Based" Autonomy**. The agent doesn't just wait for commands; it actively seeks the most efficient path to yield based on real-time on-chain data.

## 🧠 Core Intelligence
The agent operates via a three-tier modular architecture:

1. **The Sensor (`MantleClient`):** High-frequency polling of Mantle Mainnet RPCs for liquidity, gas prices, and wallet state.
2. **The Brain (`TreasuryGuard`):** A decision engine that calculates the "Staking ROI Threshold"---ensuring that the projected yield from $mETH significantly outweighs the transaction friction (gas).
3. **The Executor:** (In-Dev) Utilizing the **ERC-8183 Agent Standard** to interact with the Mantle LSP (Liquid Staking Protocol) autonomously.

---

## 🛠️ Technical Stack
- **Network:** Mantle Mainnet (Chain ID: 5000)
- **Language:** Python 3.12+
- **Blockchain Interface:** Web3.py
- **Standards:** ERC-8183 (Agentic Account Abstraction)
- **Infrastructure:** Mantle Modular DA & mETH Staking Protocol

---

## 🚦 Quick Start

### 1. Prerequisites
- Python 3.12+
- A Mantle RPC URL (Default: `https://rpc.mantle.xyz`)

### 2. Setup
```bash
git clone [https://github.com/benpaymaster/mantle-agentic-treasury.git](https://github.com/benpaymaster/mantle-agentic-treasury.git)
cd mantle-agentic-treasury
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 3\. Environment Configuration

Create a `.env` file in the root directory:

Plaintext

```
MANTLE_RPC_URL=[https://rpc.mantle.xyz](https://rpc.mantle.xyz)
PUBLIC_WALLET_ADDRESS=0x... # Your wallet address

```

### 4\. Run the Agent

```bash
python3 -m src.agents.treasury_guard

```

* * * * *

📈 Roadmap
----------

-   [x] **Phase 1:** Establish hardened connection to Mantle Mainnet.

-   [x] **Phase 2:** Implement "Watch-Only" decision logic and gas tracking.

-   [ ] **Phase 3:** Integrate LLM-driven market sentiment analysis (Gemini/GPT-4).

-   [ ] **Phase 4:** Secure transaction signing via encrypted local Vault.

* * * * *

🤝 Contributing
---------------

This project is part of the **benpaymaster** open-source initiative to simplify decentralized delivery of financial yield. Pull requests for new strategies are welcome.

**License:** MIT