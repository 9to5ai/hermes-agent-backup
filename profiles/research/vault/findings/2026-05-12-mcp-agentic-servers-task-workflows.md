# FINDING — MCP Agentic Servers: Server-as-Agent Pattern and Task Workflows
**Date:** 2026-05-12T18:00:00Z
**Source:** MCP Blog one-year anniversary (modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
**Confidence:** HIGH

## Evidence
MCP's November 2025 release introduces two architectural upgrades that shift MCP from tool interface protocol to multi-agent orchestration layer:

**1. Task-based Workflows (SEP 1686 — Experimental)**
New abstraction tracking work with states: `working → input_required → completed → failed → cancelled`
- Active polling for status checks
- Result retrieval after completion
- Task isolation with session-based access control
- Use cases explicitly include: multi-agent concurrent systems, internal agent spawning (deep research tools)

**2. Sampling with Tools: Agentic Servers (SEP 1577)**
Allows MCP servers to run agentic loops using the client's LLM tokens:
- Tool calling in sampling requests
- Server-side agent loops for multi-step reasoning
- Parallel tool calls
- Explicit capability declarations
- **Key:** A research MCP server can now spawn multiple agents internally, coordinate work, and deliver coherent results using standard MCP primitives — without exiting the MCP stack.

**3. Authorization Extensions**
- SEP-1046: OAuth client credentials for machine-to-machine
- SEP-990: Enterprise IdP policy controls (Cross App Access) — single sign-on to all authorized MCP servers

**4. URL Mode Elicitation**
Secure out-of-band credential flow: browser-based OAuth, API keys never transit through MCP client.

## Key Takeaway
MCP is no longer a client-to-server tool protocol. With agentic servers (servers that run agent loops) and task-based workflows, MCP now describes a multi-agent system architecture where the boundary between "client" and "server" dissolves — both are agents, both can spawn sub-agents, both use standard primitives for coordination. This is the same architecture Graeme's multi-agent Hermes work describes.

## Architectural Implication
If MCP servers can run agentic loops, then an MCP server IS a control plane for its subdomain. The question becomes: who controls the MCP server? MCP authorization extensions (SEP-1046, SEP-990) address authentication but not the writable-system-prompts problem (see McKinsey Lilli finding). The agentic server can operate autonomously within its authorized scope — exactly the conditions for the PocketOS-style data destruction scenario, but within the MCP stack.

## Routing Relevance
- `dossier`: Updates MCP entry from "tool interface protocol" to "multi-agent orchestration layer"
- `coder`: MCP = viable substrate for multi-agent Hermes coordination; agentic servers = production pattern to model
- `subc`: MCP now has server-as-agent pattern. Recovery implications: if MCP server is agentic, and MCP server is authorized, the same data-destruction scenario applies to MCP servers, not just end-user agents.
