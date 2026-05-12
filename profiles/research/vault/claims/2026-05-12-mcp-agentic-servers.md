# CLAIM — MCP Agentic Servers: MCP Is Now a Multi-Agent Orchestration Layer
**Date:** 2026-05-12T18:00:00Z
**Source:** MCP Blog one-year anniversary (modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/), November 2025 release
**Status:** NEW — CONFIRMED

## Claim
MCP has evolved from a tool-interface protocol (client calls tools on server) to a full multi-agent orchestration layer. With Sampling with Tools (SEP 1577) and Task-based Workflows (SEP 1686), MCP servers can now run autonomous agent loops, spawn sub-agents, and coordinate multi-agent work — all within the MCP protocol. This is architecturally equivalent to the multi-agent orchestration layer described in the Hermes multi-agent workflow.

## Evidence
- SEP 1577: MCP servers run agentic loops using client LLM tokens; explicit tool calling in sampling requests; server-side multi-step reasoning
- SEP 1686: Task-based workflows with explicit state machine (working/input_required/completed/failed/cancelled); session-based task isolation; multi-agent concurrent systems listed as explicit use case
- Nov 2025 release: Authorization extensions (SEP-1046 m2m OAuth, SEP-990 cross-app SSO) — addresses authentication but not prompt integrity
- Anthropic donated MCP to Linux Foundation / AAIF Dec 9 2025 — governance transferred to neutral body; co-founded with Block and OpenAI
- 17,000+ community servers, 97M monthly SDK downloads, production at Salesforce/Replit/Sourcegraph/Apollo
- Multi-vendor: Claude (native), OpenAI (Sep 2025), Google Gemini (Apr 2025), Cursor/Windsurf/Sourcegraph

## Implication
If MCP servers can run agentic loops, then MCP servers are agents. An MCP server compromise is equivalent to an agent compromise. The writable system prompt vulnerability (McKinsey Lilli) applies to MCP servers — not just end-user AI platforms.

## Routing Relevance
- `subc`: MCP agentic servers = deployment pattern validation. Recovery implication: MCP server-as-agent means recovery must operate at the MCP layer, not just the agent layer.
- `coder`: MCP = validated substrate for Hermes multi-agent coordination. Use SEP 1577/1686 as the API design reference for inter-agent task coordination.
