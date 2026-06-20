# DigitalTrack AI Skills

Central skills repository for DigitalTrack AI agents (Claude Code, Codex, and others).
Follows the **WAT framework**: Workflows + Agent + Tools.

## Quick Start

- Claude Code: `/salesflare` or natural language ("add new prospect to Salesflare")
- Codex: registered as `digitaltrack` local plugin; use natural language

## Skills

| Skill | Description |
|-------|-------------|
| [salesflare](skills/salesflare/SKILL.md) | Salesflare CRM operations via API — no CSV |

## Adding Skills

See `AGENTS.md` for the 6-step WAT skill building framework.

## Sync

Edit skills here. Keep `~/.codex/plugins/digitaltrack/skills/` in sync (or symlink on Linux/Mac).
Phase 2: push to GitHub `digitaltrack-ai-skills` for version control + cross-machine access.
