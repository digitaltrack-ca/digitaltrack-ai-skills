---
name: wat
description: Scaffold a new WAT skill from scratch using the 6-step framework (Name/Trigger, Goal, Process, References, Rules, Self-Improvement). Use when asked to build a new skill, add a skill to the repo, or structure a workflow for a repeatable task.
metadata:
  short-description: Scaffold a new WAT skill using the 6-step framework — outputs a ready-to-use SKILL.md
---

# WAT Skill Builder — WAT Skill

## Trigger

Natural language: "build a new skill", "scaffold a skill", "add a skill to the repo", "help me write a skill",
"create a WAT skill for X", "WAT framework", "turn this into a skill", "make a skill that does X"

Slash command: `/wat`

## Goal

Guide Leo through the 6-step WAT skill framework and output a complete, deployable `SKILL.md` in
`C:\Users\Leo\ai-skills\skills\<name>\SKILL.md`, plus register it in `AGENTS.md`.

## The WAT Framework

WAT = **Workflows + Agent + Tools**

- **Workflows** = `SKILL.md` files — plain-language SOPs that tell the agent what to do and in what order
- **Agent** = Claude Code (or Codex) — reads the workflow, decides which tools to call, executes, self-corrects
- **Tools** = `lib/*.py` scripts or MCP tools — deterministic execution layer; never ad-hoc inline API calls

**Why this structure works:** AI is probabilistic; scripts are deterministic. Keep reasoning in the workflow, keep execution in tools. If each step is 90% accurate and you chain 5, you're at 59%. Offloading to deterministic scripts keeps the agent at full strength for orchestration.

## Step-by-Step Process

### Phase 1 — Gather inputs (ask Leo these if not already provided)

1. **What is the task?** — describe it in one sentence as if briefing a new hire
2. **What triggers it?** — what would you type or say to invoke this? (slash command and/or natural language)
3. **What does it produce?** — one sentence on the end output (file, CRM record, report, etc.)
4. **What would you do manually, step by step?** — walk through the process out loud
5. **What context does it need?** — brand rules, client data, API keys, file paths, templates
6. **What could go wrong?** — common failure modes, guardrails, things to never do

### Phase 2 — Draft the skill

Use the 6-step WAT skill building framework:

| Step | Section in SKILL.md | Purpose |
|------|---------------------|---------|
| 1 | Name & Trigger | How the agent knows to invoke this |
| 2 | Goal | One-sentence output definition |
| 3 | Step-by-Step Process | The SOP — ordered, specific |
| 4 | Reference Files | Paths to brand docs, templates, data |
| 5 | Rules & Guardrails | What can go wrong; hard constraints |
| 6 | Self-Improvement Loop | How to iterate after each run |

### Phase 3 — Write and register

1. Create `C:\Users\Leo\ai-skills\skills\<name>\SKILL.md` using the standard frontmatter format
2. Create `lib/` subdirectory and placeholder scripts only if the skill needs deterministic tools
3. Add a row to the **Skills Registry** table in `C:\Users\Leo\ai-skills\AGENTS.md`
4. If the skill should be available in Codex, add `skills\<name>\agents\openai.yaml`
5. Confirm with Leo before writing — show the draft SKILL.md first

### Phase 4 — Test and iterate

- Invoke the new skill once with a real task
- Watch where the agent searches, hesitates, or guesses — those are gaps to fill in
- Update the SKILL.md after the first 2–3 runs
- After 10–20 runs the skill should be stable

## Progressive Context Loading

Skills use a 3-level load system — keep this in mind when writing:

- **Level 1** (~100 tokens): only `name` + `description` frontmatter — this is what gets scanned across all skills
- **Level 2** (full SKILL.md): loaded when the skill matches — keep under 500 lines
- **Level 3** (reference files): only loaded when a step explicitly needs them — put heavy context here, not inline

**Optimization tips:**
- Hardcode IDs, paths, and known values rather than having the agent search for them every run
- Pre-load reference docs the skill needs frequently (e.g., a pricing schema, brand rules path)
- Delegate sub-tasks to other existing skills rather than duplicating their logic

## Standard Frontmatter Format

```markdown
---
name: skill-kebab-case
description: Full sentence describing what the skill does and when to use it. This is the Level 1 scan text — make it match the user's natural language.
metadata:
  short-description: 10-word version for registries and Codex display
---
```

## Codex openai.yaml Format

```yaml
name: skill-name
description: "Same description as SKILL.md frontmatter"
trigger_phrases:
  - "natural language trigger 1"
  - "natural language trigger 2"
skill_file: "skills/skill-name/SKILL.md"
```

## Reference Files

- WAT framework source: `C:\Users\Leo\OneDrive\Docs\Education\AI Automation Society\7 Day AIS Challenge\The WAT Framework.txt`
- Skill anatomy source: `C:\Users\Leo\OneDrive\Docs\Education\AI Automation Society\7 Day AIS Challenge\Skill Anatomy.txt`
- WAT CLAUDE.md template: `C:\Users\Leo\OneDrive\Docs\Education\AI Automation Society\7 Day AIS Challenge\WAT CLAUDE.md`
- Existing skills for format reference: `C:\Users\Leo\ai-skills\skills\salesflare\SKILL.md`, `skills\youtube-transcript\SKILL.md`
- Skills registry: `C:\Users\Leo\ai-skills\AGENTS.md`

## Rules & Guardrails

- **Always show Leo a draft before writing files** — confirm the skill name, trigger phrases, and goal first
- **Never overwrite an existing skill** without Leo's explicit approval — check `skills/` first
- **Keep SKILL.md under 500 lines** — move detailed reference material to `references/` subdirectory
- **Do not invent API calls inline** — if the skill needs an API, scaffold a `lib/` script for it
- **Skills are portable** — they work across Claude Code, Codex, and other markdown-reading agents; don't hardcode Claude-specific syntax
- **Register every new skill** in `AGENTS.md` Skills Registry immediately — unregistered skills don't get invoked
- **Do not create `references/` files preemptively** — only add them when the skill actually needs them on a real run

## Self-Improvement Loop

After scaffolding each new skill:
1. Did Leo ask for changes to the draft? Note which section was weak — tighten that section's guidance above.
2. Did the agent correctly infer the trigger from natural language without `/wat`? If not, add that phrase to the Trigger section.
3. Did any existing skill already cover this task partially? Note the overlap and add a cross-reference.
4. After 3 new skills built with this framework, review the Step-by-Step Process for any steps that always get skipped or always require clarification.
