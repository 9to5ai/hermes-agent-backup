# Agentic Commerce Stack — Build Candidate Reference
*Research output from session — May 11, 2026*

## Source
Graeme's Substack: "The Agentic Commerce Stack: Trust + Payments + Composability (and the Risks)"  
URL: https://gkisokay.substack.com/p/the-agentic-commerce-stack-trust

## What It Describes

Three converging developments signal the autonomous agentic economy:

### 1. x402 Protocol (Payments)
- HTTP 402 repurposed as machine-readable paywall standard
- Agent requests → server returns 402 + payment requirements → agent retries with payment → server verifies → content + receipt
- Cloudflare already in production with Pay-Per-Crawl
- x402 generalizes beyond Cloudflare — any server can implement
- Assessment: high-value APIs, tool access, data endpoints could adopt — enough to start

### 2. ERC-8004 (Identity + Reputation)
- Onchain agent identity registry (ERC-721 NFT)
- Three registries: Identity, Reputation, Validation
- Portable (move between wallets), indexable, composable
- Enables agent discovery + trust across organizational boundaries without pre-existing trust
- Mainnet target: January 16 (from article date Jan 12)

### 3. xPortal Demo (Composability)
- Working loop: agent needs identity → ERC-8004 registration → gated by HTTP 402 → pays USDC → server verifies → agent now onchain
- Proves agents can bootstrap from nothing to "onchain participant" without human intervention

### Physical Counterpart: DeRobotics
- Robots paying for positioning data, mapping services, compute, task markets, verification
- Web analog: pay-per-crawl → pay-per-localization

## What This Means for the Multi-Agent System

Graeme's system already has the architecture (Research → Dreamer → Main → Coder → QA). 
This stack (x402 + ERC-8004) is a concrete domain the research agent could monitor and the Dreamer could signal builds against.

## Relevant Signals for Build Decisions

- x402 adoption path: APIs and tool endpoints first, not content sites
- ERC-8004 identity enables agent-to-agent trust without humans — large unlock
- The risk Graeme flags: reputation laundering (fake reviews / wash trading of agent quality)
- Physical agent payments (DeRobotics) is the longer-horizon version

## Build Candidates from This Research

| Candidate | Priority | Rationale |
|-----------|----------|-----------|
| Monitor ERC-8004 identity registry | Medium | New onchain signal for agent quality/trust |
| x402 paywall integration for agent APIs | Medium | Practical payment rail for agent tool access |
| Agent reputation tracker | Lower | Depends on ERC-8004 adoption rate |
| Recovery layer for multi-agent handoffs | High | Core system improvement (per 37-day results) |

## Note on Research Method

web_extract works on Substack. X posts require browser_navigate + browser_snapshot + browser_scroll.
X blocks web_extract entirely.