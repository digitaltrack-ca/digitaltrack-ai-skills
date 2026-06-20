# DigitalTrack AI Skills — Agent Instructions

This repository is the **single source of truth** for all DigitalTrack AI agent skills.
It follows the WAT framework: **Workflows + Agent + Tools**.

- **Workflows** = `skills/<name>/SKILL.md` — step-by-step SOPs in plain language
- **Agent** = Claude Code, Codex, or any supported coding agent reading this file
- **Tools** = `skills/<name>/lib/*.py` — deterministic Python scripts that do the actual API/data work

## Repository Layout

```
ai-skills/
├── AGENTS.md                     # This file — universal agent instructions (you are here)
├── CLAUDE.md                     # @AGENTS.md import + Claude Code-specific notes
├── skills/
│   └── salesflare/
│       ├── SKILL.md              # WAT workflow SOP — invoke with /salesflare or natural language
│       ├── agents/openai.yaml    # Codex display config (ignored by Claude Code)
│       └── lib/
│           └── salesflare_client.py  # Canonical Salesflare API library (no CSV)
└── README.md
```

## How to Use Skills

- **Claude Code**: invoke with `/salesflare` or natural language ("add this contact to Salesflare")
- **Codex**: skills registered as the `digitaltrack` local plugin; invoke via natural language
- **Other agents**: read the relevant `SKILL.md` file directly for step-by-step instructions

## Skills Registry

| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `salesflare` | "add to CRM", "new prospect", "look up in Salesflare" | Create/update accounts, contacts, opportunities, tasks via API — no CSV |

## Operating Rules for All Agents

1. **Check `skills/` before doing anything manually** — if a skill exists for the task, use it
2. **Use `lib/` scripts for API calls** — never invent ad-hoc API calls inline; use the canonical library
3. **API key**: Salesflare API key is stored in `$env:SALESFLARE_API_KEY` (Windows registry) or `SALESFLARE_API_KEY` env var
4. **No CSV files** — this skill system replaces the CSV import workflow entirely for single records; CSV intake is only for bulk (10+ records from events/mixers)
5. **No one-off scripts per client** — update the canonical skill instead of creating `salesflare_setup_<client>.py` files
6. **Update skills when you learn something new** — if an API call fails and you fix it, update the SKILL.md with what you learned

## Adding New Skills

Follow the 6-step WAT skill framework:
1. Name & Trigger — what is it called, what natural language fires it?
2. Goal — one sentence: what does it produce?
3. Step-by-Step Process — what would you do manually, in order?
4. Reference Files — what context does it need?
5. Rules — what could go wrong? Add guardrails.
6. Self-Improvement Loop — how will you test and iterate?

Create `skills/<name>/SKILL.md` following the format in existing skills.
Add a row to the Skills Registry table above.
Add the Codex display config at `skills/<name>/agents/openai.yaml`.

## Sync Note

This folder is the canonical source. Changes here must be reflected in:
- `~/.claude/skills/` if Claude Code has local copies (prefer `@import` over copies)
- `~/.codex/plugins/digitaltrack/skills/` for Codex (keep in sync or symlink when possible)

**GitHub repo (Phase 2)**: push to `digitaltrack-ai-skills` (private) for version control and cross-machine sync.
