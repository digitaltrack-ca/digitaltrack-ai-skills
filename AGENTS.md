# DigitalTrack AI Skills — Agent Instructions

This repository is the **single source of truth** for all DigitalTrack AI agent skills.
It follows the WAT framework: **Workflows + Agent + Tools**.

- **Workflows** = `skills/<name>/SKILL.md` — step-by-step SOPs in plain language
- **Agent** = Claude Code, Codex, or any supported coding agent reading this file
- **Tools** = `skills/<name>/lib/*.py` — deterministic Python scripts that do the actual API/data work

## Repository Layout

```
ai-skills/
├── AGENTS.md                              # This file — universal agent instructions (you are here)
├── CLAUDE.md                              # @AGENTS.md import + Claude Code-specific notes
├── skills/
│   ├── salesflare/
│   │   ├── SKILL.md                       # WAT workflow SOP
│   │   ├── agents/openai.yaml             # Codex display config
│   │   └── lib/salesflare_client.py       # Canonical Salesflare API library
│   ├── local-seo/SKILL.md                 # Full Local SEO system (12 modules)
│   ├── digitaltrack-prospect-presentation/SKILL.md
│   ├── proposal-builder/
│   │   ├── SKILL.md
│   │   └── references/                    # section-copy.md, pricing-schema.md
│   ├── sales-enablement/SKILL.md
│   ├── email-sequence/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── evals/
│   ├── video/SKILL.md
│   ├── youtube-transcript/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── lib/get_transcript.py
│   ├── outreach/SKILL.md
│   ├── lovable/SKILL.md
│   ├── gws-cli/SKILL.md
│   ├── google-search-console/
│   │   ├── SKILL.md                       # GSC WAT skill — quick wins, compare, decay, roll-up
│   │   └── agents/openai.yaml
│   └── wat/
│       └── SKILL.md                       # WAT skill builder — scaffold new skills via 6-step framework
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
| `local-seo` | "local SEO", "GBP audit", "map ranking", "run SEO for" | Full DigitalTrack Local SEO system — audit through monthly maintenance |
| `digitaltrack-prospect-presentation` | "build prospect deck", "prospect presentation" | Build branded interactive prospect deck from audit/transcript/research files |
| `proposal-builder` | "build a proposal", "propuesta", "sales proposal page" | Build/update DigitalTrack sales proposal in Lovable — 9-section bilingual structure |
| `sales-enablement` | "pitch deck", "one-pager", "objection handling", "sales deck" | Create sales collateral — decks, one-pagers, objection docs, demo scripts |
| `email-sequence` | "email sequence", "drip campaign", "nurture sequence" | Design and build email sequences, drip campaigns, automated lifecycle flows |
| `video` | "video pipeline", "social video", "content video" | Leo content pipeline — ElevenLabs voice + JSON2Video/Remotion production |
| `youtube-transcript` | "get YouTube transcript", "extract transcript from YouTube", "pull captions from this video", "transcribe this YouTube episode" | Extract transcript from any YouTube video using auto-generated captions — free, instant, no HappyScribe credits |
| `outreach` | "/outreach <company>", "networking outreach" | Daily networking outreach workflow — overdue follow-ups, drafted messages, send |
| `lovable` | "push to Lovable", "update Lovable project", "build in Lovable" | Send prompts to any Lovable project via MCP without leaving Claude Code |
| `gws-cli` | "Google Drive", "Gmail", "Calendar", "gws" | Google Workspace CLI — Drive, Gmail, Calendar, Sheets, Docs, Slides operations |
| `pacifiklive-content-router` | "which folder for pacifiklive", "route this content", "pacifiklive originals", "where does this go", "file this article", "category for paci" | Route PacifikLive content to correct Originals category folder, create article subfolder with draft + images/, confirm with Leo before writing |
| `chcc-awards-scoring` | "score CHCC nominees", "chcc awards", "score the nominations", "awards review committee" | Score CHCC award nominees using official rubric — reads nomination PDFs, applies strict scoring rules, proposes scores for Leo to approve, updates Excel sheet |
| `google-search-console` | "GSC", "search console", "quick wins", "traffic dropped", "gsc report", "gsc audit", "monthly GSC", "keyword ranking" | Pull and analyze Google Search Console data — quick wins, monthly compare, traffic drops, cannibalization, content decay, cross-client roll-ups via local SQLite cache |
| `wat` | "build a new skill", "scaffold a skill", "add a skill to the repo", "WAT framework", "turn this into a skill", "create a WAT skill for X" | Scaffold a new WAT skill using the 6-step framework — outputs ready-to-use SKILL.md and registers it in AGENTS.md |

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

**GitHub remote**: https://github.com/digitaltrack-ca/digitaltrack-ai-skills (private)
Push changes with `git push origin master` to keep the remote in sync.
