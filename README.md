# mrpkk — AI Agents, Telegram Bots & DeFi Systems

I build production systems that run 24/7. From idea to working product — no mockups, no "let's see how it goes". Only working code that delivers results.

## Projects

| Project | Live Demo | Presentation | Stack |
|---|---|---|---|
| **Telegram AI Bot** | [Demo](demos/telegram-bot.html) | [Deck](decks/telegram-ai-bot.html) | Python · FastAPI · Mistral AI · aiogram 3.x · RAG · Streamlit · ChromaDB |
| **RAG Corp Bot** | [Demo](demos/agent-dashboard.html) | [Deck](decks/rag-corp-bot.html) | Python · FastAPI · Mistral AI · BM25 · Vector Search |
| **DeFi One** | — | [Deck](decks/defi-one.html) | React · FastAPI · WalletConnect · Mistral AI |
| **Solidity Portfolio** | — | [Deck](decks/solidity-portfolio.html) | Solidity · Foundry · OpenZeppelin · React |
| **Crypto MCP Server** | [Demo](demos/crypto-mcp.html) | [Deck](decks/crypto-mcp-server.html) | Python · MCP SDK · CoinGecko · DeFiLlama |
| **On-Chain AI Agent** | [Demo](demos/onchain-agent.html) | [Deck](decks/onchain-ai-agent.html) | Solidity · Python · FastAPI · Docker |
| **AIRealty** | — | [Deck](decks/airealty.html) | React · FastAPI · Mistral AI · Monte Carlo |
| **AIBiz** | — | [Deck](decks/aibiz.html) | React · FastAPI · Mistral AI · Recharts |
| **AILegal** | — | [Deck](decks/ailegal.html) | React · FastAPI · Mistral AI · Framer Motion |
| **attest** | [Demo](demos/attest/) · [live](https://mrpkk.github.io/portfolio/demos/attest/) | — | Python · Web Crypto (HMAC-SHA-256) · JSON Schema · Apache-2.0 |

### attest — the live demo is checkable, not just clickable

Paste a tool artifact, get a verdict: schema contract, 23 context-poisoning signatures, signed
provenance. The engine runs in the browser — zero requests to a server.

```bash
# 1) assets are live
curl -s -o /dev/null -w '%{http_code}\n' https://mrpkk.github.io/portfolio/demos/attest/engine.js

# 2) the form answers: clean → ACCEPT, injection → REJECT, forged signature → rejected
bash scripts/attest_live_smoke.sh

# 3) browser engine is 1:1 with the Python service — 38/38 fixtures identical
python3 scripts/attest_conformance.py
```

The signature has a working negative control: change the record after signing and verification fails.
A demo that only prints "PASS" would prove nothing.

## Links

- 🌐 [Portfolio](https://mrpkk.github.io/portfolio/)
- 📧 [maxim.pkk@gmail.com](mailto:maxim.pkk@gmail.com)
- 🐙 [GitHub](https://github.com/mrpkk)
- 💬 Telegram: @mrpkk

## How I Work

1. Analysis of your task — free
2. Contract and 50% prepayment
3. Development with transparent reporting
4. Launch + remaining 50% after acceptance

Self-employed (samozanyatost) status, official receipts provided.
