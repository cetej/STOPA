---
name: Polymarket CLI & Python SDK references
description: Key repos and contract addresses for Polymarket wallet setup and Phase 2 live trading
type: reference
---

## Repos
- **polymarket-cli** (Rust): https://github.com/Polymarket/polymarket-cli — wallet management, approvals, CLI trading. Uses `polymarket-client-sdk` Rust crate v0.4.
- **py-clob-client** (Python): https://github.com/Polymarket/py-clob-client — official Python SDK for CLOB trading. `pip install py-clob-client`.

## Contract Addresses (Polygon, chain ID 137)
| Asset/Contract | Address |
|---|---|
| USDC | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` |
| CTF tokens | `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045` |
| CTF Exchange | `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E` |
| Neg Risk Exchange | `0xC5d563A36AE78145C45a50134d48A1215220f80a` |
| Neg Risk Adapter | `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296` |

## Auth Model
- L0: No auth — read-only (current POLYBOT state)
- L1: Private key signing — can create API keys
- L2: API key + secret + passphrase — full trading (derived deterministically from PK)

## Wallet Setup Plan
Detailed plan in `docs/WALLET_SETUP_PLAN.md` in POLYBOT project.
