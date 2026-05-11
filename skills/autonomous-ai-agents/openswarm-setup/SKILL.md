---
name: openswarm-setup
description: Set up VRSEN/OpenSwarm (multi-agent AI team built on Agency Swarm) with MiniMax as the model provider. Covers venv creation, Node.js path quirks, litellm MiniMax routing, and API key configuration. Load when asked to set up, install, or configure OpenSwarm.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  homepage: https://github.com/VRSEN/OpenSwarm
  framework: Agency Swarm
  providers: [minimax, openai, anthropic]
---

# OpenSwarm Setup

[OpenSwarm](https://github.com/VRSEN/OpenSwarm) is a multi-agent AI team (8 agents: orchestrator, deep research, data analyst, slides, docs, image gen, video gen, virtual assistant) built on [Agency Swarm](https://github.com/VRSEN/agency-swarm).

## Quick Setup

```bash
# 1. Clone
git clone https://github.com/VRSEN/OpenSwarm ~/OpenSwarm

# 2. Create Python 3.12 venv (system Python may be too old)
#    Check: python3 --version → needs 3.10+
#    macOS homebrew Python path: /opt/homebrew/bin/python3.12
/opt/homebrew/bin/python3.12 -m venv ~/openswarm-venv --clear

# 3. Install Python deps
cd ~/OpenSwarm && ~/openswarm-venv/bin/pip install -e .

# 4. Install Node deps (homebrew node on macOS)
/opt/homebrew/bin/npm install
#   or if node not on PATH:
export PATH="/opt/homebrew/bin:$PATH" && npm install

# 5. Write .env with model config — use write_file tool, NOT heredoc
#    MiniMax-M2.7 is Jun's model; sk-cp-* is the API secret key format
write_file(path="/Users/momo/OpenSwarm/.env", content="""\
MINIMAX_API_KEY=sk-cp-YOUR_KEY_HERE
DEFAULT_MODEL=minimax/Minimax-M2.7
""")
```

## Running

```bash
cd ~/OpenSwarm && ~/openswarm-venv/bin/python swarm.py
```

## Model Configuration

OpenSwarm uses `config.py` which reads `DEFAULT_MODEL` from environment:

| DEFAULT_MODEL value | Provider used |
|---------------------|---------------|
| `gpt-4o` (no slash) | OpenAI direct |
| `minimax/Minimax-M2.7` | MiniMax via litellm (reasoning model) |
| `minimax/MiniMax-Text-01` | MiniMax via litellm (may not be available on all plans) |
| `anthropic/claude-sonnet-4` | Anthropic via litellm |

The `/` format routes through litellm. Any litellm-supported model works.

**MiniMax M2.7 is a reasoning model** — it outputs content with leading `\n\n` and the actual answer follows. This is normal, not an error. litellm strips the newlines when returning `choices[0].message.content`. Do not treat empty content as a failure — verify with `max_tokens=100` and `.strip()` on the response.

**MiniMax API base URL**: `https://api.minimax.io/v1` (global). China plan uses `https://api.minimaxi.com/v1`.

## API Key Setup for MiniMax

**Preferred: Get key directly from user.** MiniMax API keys are `sk-cp-*` format. Get the actual key string — do NOT use the masked `***` placeholder from Hermes `.env` display. If the user pastes the key in chat, use `write_file` tool (NOT heredoc/terminal) to write `~/OpenSwarm/.env`.

**If key is already configured in Hermes**, the `.hermes/.env` file masks it as `***` — it cannot be extracted from there. The running gateway process does have it in memory, but it uses encrypted storage. Just ask the user to paste the key.

**Write the .env with Python, not heredoc.** Heredocs via terminal mangled the API key (unintended hex encoding, `\n` escapes). Always write the file directly:
```python
write_file(path="/Users/momo/OpenSwarm/.env", content="MINIMAX_API_KEY=sk-cp-...\nDEFAULT_MODEL=minimax/Minimax-M2.7\n")
```

**Verify with curl before testing litellm.** If you get auth errors, check the model name:
```bash
curl -s -X POST https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"Minimax-M2.7","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```
Error `"model not support (2061)"` → the model name is wrong or not on your plan.
Error `"login fail: Please carry the API secret key" (1004)` → bad key or wrong base URL.

**`dotenv` loading requires `override=True`** in some contexts. When testing litellm from OpenSwarm, use:
```python
from dotenv import load_dotenv
load_dotenv('/Users/momo/OpenSwarm/.env', override=True)
os.environ['MINIMAX_API_KEY']  # verify it's set
```

## macOS-Specific Dependencies

```bash
# REQUIRED for docs agent (PDF rendering via pypango)
brew install pango   # version 1.57.1 on Jun's machine

# Without this: pango-related rendering failures in docs agent
# Error message references "pango" or "pangocairo" in the traceback
```

## Programmatic Usage (`agency.get_response_sync`)

`swarm.py` is a **TUI app** — it runs an interactive terminal UI and should NOT be used directly for automated tasks.

**For programmatic control**, import and use the Agency API directly:
```python
import sys
sys.path.insert(0, '/Users/momo/OpenSwarm')
from swarm import agency  # Agency instance defined in swarm.py

# Single prompt — synchronous
response = agency.get_response_sync("Your prompt here")
print(response)
```

This is how to test the swarm without the TUI. Use in scripts, tests, or when delegating via `delegate_task`.

## Complex Task Timeout Strategy

OpenSwarm's default run loop can time out (600s) on multi-step research + creation tasks (e.g., "research jurisdictions and produce a slide deck").

**Workaround: single focused subagent prompt**
Instead of a multi-agent parallel workflow, use one subagent with:
1. All research context pre-loaded in the prompt
2. A specific, narrow output directive ("create an HTML slide deck at path X")
3. No coordination overhead — it just produces the artifact

Example delegate prompt structure:
```
You are a slide deck generator. Research context: [all facts]. Task: create a beautiful HTML slide deck at /path/to/output.html with N slides covering [topics]. [Style guidance]. Return the file path when done.
```

This completed a full 18-slide research deck in ~246s vs 600s+ timeout on the multi-agent approach.

## Common Issues

- **Python version error**: Requires 3.10+. Use `pyenv` or homebrew Python 3.12+ on macOS. Do NOT use system Python 3.9 on macOS.
- **Node not found**: `/opt/homebrew/bin` may not be in PATH. Use absolute path to node/npm.
- **libpango missing**: macOS requires `brew install pango` for the docs agent's PDF rendering. Without it, pango/pangocairo errors appear in docs agent traces.
- **litellm MiniMax auth error**: Ensure key is the raw API secret key (starts with `sk-cp-`), not an OAuth token. MiniMax OAuth uses a different auth flow via `minimax-oauth` provider.
- **litellm returns empty content**: MiniMax-M2.7 is a reasoning model — content is in `message.content` but may have leading `\n\n` from reasoning output. litellm strips these. Use `max_tokens=100` and call `.strip()` on response. Empty content with 20 tokens may be a token limit issue, not an auth issue.
- **KEY shows as `***` in .env**: Hermes masks keys on display. The running gateway has the real key in memory but encrypted; just ask the user to paste the key — it's the fastest path.
- **Multi-agent task times out**: 600s default timeout is too short for research+creation chains. Use single focused subagent with pre-loaded context instead of multi-agent coordination.

## Optional Dependencies

```bash
# Composio (10k+ tool integrations)
/opt/homebrew/bin/npm install  # already done above

# For image/video agents
FAL_KEY=your_fal_key
GOOGLE_API_KEY=your_google_key

# For web search
SEARCH_API_KEY=your_search_key
```

## Architecture

- `swarm.py` — agency definition, agent wiring, communication flows
- `config.py` — model resolution, litellm routing
- `agents/` — one subfolder per agent (orchestrator, virtual_assistant, deep_research, data_analyst_agent, slides_agent, docs_agent, image_generation_agent, video_generation_agent)
- `shared_tools/` — composio-powered integrations available to all agents
- `shared_instructions.md` — system prompt shared across all agents
