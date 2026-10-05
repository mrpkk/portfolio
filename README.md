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

# 3) the real form in a real browser: button click, rendered verdict, Web Crypto,
#    negative control — the wiring the fixture run above cannot see
node scripts/attest_dom_check.mjs

# 4) browser engine is 1:1 with the Python service — 38/38 fixtures identical
python3 scripts/attest_conformance.py
```

The signature has a working negative control: change the record after signing and verification fails.
A demo that only prints "PASS" would prove nothing.

**Last run, 2026-10-05, against the published URL, not a local build:**

| check | result |
|---|---|
| assets on `mrpkk.github.io` | `index.html` 200/9517B · `rules.js` 200 · `engine.js` 200 · `verdict.js` 200 · `verdict.css` 200 |
| published files vs repo | `diff` identical for all five — the live page is the committed code |
| `attest_live_smoke.sh` | `SMOKE: PASS` — clean → ACCEPT trust=100, injection → REJECT, forged signature rejected |
| `attest_dom_check.mjs` | `DOM: PASS` — click → rendered verdict, `crypto.subtle` present, 0 console errors |
| `attest_conformance.py` | `38/38` identical to the Python service |
| entry points | `/portfolio/` card, `demos/index.html` card, this README — all `200` |

`attest_dom_check.mjs` reuses the Chromium that `@playwright/mcp` already cached, so it downloads
nothing; without a browser it exits `2` and says the check was not run rather than passing silently.

**Measured limitation, not a claim:** the 23 signatures are Latin-script regexes. The Russian
formulation `ИГНОРИРУЙ ПРЕДЫДУЩИЕ ИНСТРУКЦИИ` returns `accept / trust=100` — confirmed against the
production `engine.js`. That is the documented behaviour ("достаточно переформулировать"), stated on
the page itself, not a gap hidden here. Matching non-Latin scripts is a real piece of work (unicode
normalisation + per-script signature sets), not a config flag.

**Measured, not assumed — the folder holds 7 files, the page loads 5.** `attest.css` and `attest.js`
are the superseded first iteration (ECDSA P-256 keypair instead of the shipped HMAC); nothing in
`index.html` references them, so they are dead weight that still deploys and answers `200`. Kept in
the tree rather than deleted — removal is a separate, deliberate step. The live surface is exactly
the five files the smoke check enumerates.

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
