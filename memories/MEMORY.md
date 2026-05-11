Browser: Chrome with CDP remote debugging at ws://localhost:9222. Bug fixed in session_search: the condition `resolved_sid == current_lineage_root` was incorrectly excluding the parent session when context compaction created a child session. Only `raw_sid == current_session_id` should be filtered. Patch applied to tools/session_search_tool.py lines 410-418. Config updated 2026-04-22: memory_char_limit=50000, user_char_limit=25000, compression.threshold=0.85, target_ratio=0.80, protect_last_n=50.
§
PolyAgent at /Users/momo/polyagent uses a project .venv with Python 3.11 because system /usr/bin/python3 is 3.9.6 and py-clob-client requires Python >=3.9.10. Use `.venv/bin/python` or `uv pip install --python .venv/bin/python ...` for live Polymarket dependencies.
§
ai4trade token: b_8sUiWfFDkCpPfbEJ2JRKv14rSc-GgrcnhVxXQ2Dx0 (agent_id: 5615, name: MomoTrades)
§
xurl (X/Twitter CLI) has no credentials — default app shows (no credentials). User needs to run auth manually: `xurl auth apps add` → `xurl auth oauth2 --app my-app` → `xurl auth default my-app`. Do NOT attempt to pass secrets inline.