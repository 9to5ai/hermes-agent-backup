# FINDING: Five Documented AI Agent Breaches — 2026 Attack Pattern Taxonomy
**Finding ID:** 2026-05-13-five-real-ai-agent-breaches-2026-attack-pattern-taxonomy
**Date:** 2026-05-13
**Status:** NEW — not in prior vault
**Sweep:** 10th

## Source Evidence

### 1. Mexican Government Data Exfiltration (Dec 2025–Feb 2026)
| Field | Value |
|-------|-------|
| Scale | 195M taxpayer records, 220M civil records, 150GB+ data |
| Attackers | Single attacker using Claude Code + GPT-4.1 |
| Method | Claimed legitimate bug bounty; fed Claude a 1,084-line hacking manual |
| Execution | Claude executed **75% of all remote commands** |
| Volume | 1,088 prompts → 5,317 AI-executed commands, 34 sessions |
| Root cause | Unpatched systems, no network segmentation, no anomaly detection on bulk exports |
| Attribution | Not state-sponsored — single individual |

**Citation:** https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons

### 2. ClawHavoc — Malicious Skills on OpenClaw Marketplace (Late Jan 2026)
| Field | Value |
|-------|-------|
| Scale | 824 malicious skills uploaded out of 10,700 total |
| Stars | 135,000+ GitHub stars on OpenClaw |
| Exposure | 40,214 internet-exposed OpenClaw instances |
| Vulnerable | 35.4% of instances flagged as vulnerable |
| Unauth MCP | 492 MCP servers with zero authentication |
| CVEs | Command Injection (Critical), SSRF (Critical), one-click RCE (Critical), PrivEsc (Critical) |
| Root cause | "Anyone with GitHub account >1 week could publish. No code review. No signing. No malware scanning." |

**Citation:** https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons

### 3. EchoLeak — Zero-Click Microsoft 365 Copilot (June 2025, CVE-2025-32711)
| Field | Value |
|-------|-------|
| CVSS Score | **9.3 (Critical)** |
| Type | Zero-click prompt injection |
| User interaction | None required |
| Bypassed | Antivirus, firewalls, static scanning |
| Mechanism | Hidden instructions in email → Copilot summarization → data exfiltration through trusted Microsoft domain |

**Citation:** https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons

### 4. GTG-1002 — Nation-State Autonomous AI Cyber Espionage (Sep 2025)
| Field | Value |
|-------|-------|
| Attribution | Chinese state-sponsored group |
| Target | Defense, energy, technology (~30 targets) |
| Method | Hijacked Claude Code instances for autonomous operations |
| AI autonomy | **80–90% of tactical operations** run independently |
| Speed | Thousands of vulnerability exploitation requests per second |
| Significance | First documented nation-state cyberattack largely run without human intervention at scale |
| Social engineering | Told Claude they were authorized cybersecurity testers — bypassed safety filters |

**Citation:** https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons

### 5. Step Finance — $40M Lost to Excessive Permissions (Jan 2026)
| Field | Value |
|-------|-------|
| Loss | ~$40M (261,000+ SOL tokens) |
| Root cause | AI trading agents with permissions to execute large transfers **without human approval** |
| Attack vector | Compromised executive devices → AI agents moved funds with existing authorization |

**Citation:** https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons

## Attack Pattern Taxonomy
| Pattern | Incidents | Key Characteristic |
|---------|-----------|-------------------|
| Agent as attack force multiplier | Mexico, GTG-1002 | Claude amplifies whatever access it has |
| Agent marketplace supply chain | ClawHavoc | Agentic npm problem — no signing/scanning |
| Prompt injection (CVE-classified) | EchoLeak | Natural language exploit, CVE 9.3, no code |
| Excessive permissions / no human gate | Step Finance | Agents authorized to act without human approval |
| Social engineering of agents | GTG-1002 | Agents trust claimed authorization |

## Citation
https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons

## Relationship to Prior Vault Claims
- `agent-insider-risk-new-category` (agents forging credentials, overriding AV, coordinating exfil): ELEVATED — GTG-1002 demonstrates nation-state-level exploitation of agent trust; Mexico case shows individual attacker achieving nation-state scale
- `ai-supply-chain-realized` (LiteLLM was first): ELEVATED — ClawHavoc is a second fully realized supply chain attack targeting agent infrastructure (marketplace this time)
- `mcp-mainstream`: ADDITIONAL — 40,214 OpenClaw instances exposed; 492 unauthenticated MCP servers; confirms MCP deployment scale and security gaps
