---
name: contact-goat
description: LinkedIn research and prospecting CLI — find who Leo knows at target companies, map warm intro paths, and build lead lists for SendPilot campaigns. Covers job search (FinTech/SaaS roles), DigitalTrack lead gen (local business owners), and contact enrichment. Uses LinkedIn (free/browser session), Happenstance (free 14 searches/month), and optionally Deepline (paid email enrichment).
triggers:
  - "contact goat"
  - "who do I know at"
  - "warm intro"
  - "coverage"
  - "find contacts at"
  - "prospect linkedin"
  - "linkedin research"
  - "map my network"
  - "who can introduce me"
  - "enrich contact"
  - "find leads linkedin"
agents:
  - claude-code
  - codex
  - cursor
  - gemini-cli
  - any
---

# Contact Goat Skill

LinkedIn research and warm-intro mapping for job search and lead gen. Feeds quality, pre-researched contacts into SendPilot for outreach and Salesflare for CRM.

**Binary**: `contact-goat-pp-cli`
**Source**: [printingpress.dev/library/sales-and-crm/contact-goat](https://printingpress.dev/library/sales-and-crm/contact-goat)
**Install**: `npx -y @mvanhorn/printing-press-library install contact-goat`

---

## 1. Auth Setup (One-Time Per Machine)

Contact Goat uses three sources. Each is optional — the CLI runs with whichever are configured.

| Source | Auth Method | Cost | Priority |
|--------|-------------|------|----------|
| **LinkedIn** | Browser session via `uvx` | **Free** — no limit | Start here |
| **Happenstance** | Chrome cookies | **Free** — 14 searches/month | Second |
| **Deepline** | `DEEPLINE_API_KEY` env var | **Paid** — credit-based | Optional only |

### LinkedIn (Free — Do First)
```powershell
# One-time login — opens browser, sign in to LinkedIn
uvx linkedin-scraper-mcp@latest --login
```
Uses Leo's own LinkedIn browser session. No API key, no credit burn.

### Happenstance (Free Tier — 14 searches/month)
```powershell
# macOS/Linux:
contact-goat-pp-cli auth login --chrome --service happenstance

# Windows (manual): set env var instead
$env:HAPPENSTANCE_WEB_APP_COOKIE_AUTH = "<paste cookie value>"
```
To get the cookie: log in to happenstance.ai in Chrome → DevTools → Application → Cookies → copy the session cookie value.

Free tier renews monthly. Check remaining quota:
```powershell
contact-goat-pp-cli user get-limits --json
```

### Deepline (Optional — Only for Email Enrichment)
```powershell
$env:DEEPLINE_API_KEY = "dlp_..."   # get from code.deepline.com
```
Only needed for `waterfall`, `dossier --enrich-email`, and `prospect --deepline`. Skip until email enrichment is needed.

### Verify Setup
```powershell
contact-goat-pp-cli doctor
```
WARN rows are fine — they just mean that source isn't wired up yet.

---

## 2. Usage

```
/contact-goat job-search <company>
/contact-goat lead-gen <niche> [location]
/contact-goat intro <person-name-or-linkedin-url>
/contact-goat enrich <linkedin-url>
/contact-goat status
```

Examples:
- `/contact-goat job-search stripe`
- `/contact-goat lead-gen restaurant "Fairfield CA"`
- `/contact-goat intro "Patrick Collison"`
- `/contact-goat enrich https://linkedin.com/in/someone`
- `/contact-goat status`

---

## 3. Branch 1 — Job Search Research

**Trigger:** `/contact-goat job-search <company>`

**Goal**: Before adding contacts to SendPilot, know who Leo already has a path to at the target company. Prioritize warm intros over cold outreach. Preserve Happenstance quota for key targets.

### Step 1 — Company Coverage Check
```powershell
# Who does Leo already know at this company? (LinkedIn 1st-degree)
contact-goat-pp-cli coverage "<Company>" --source li --json

# Add Happenstance layer (costs 1 Happenstance search — use only for priority companies)
contact-goat-pp-cli coverage "<Company>" --json
```

Output: ranked list of contacts by relationship strength. Anyone here = skip SendPilot, reach out manually first.

### Step 2 — Find Warm Intro Paths
```powershell
# Find who in Leo's network can introduce him to a target person
contact-goat-pp-cli warm-intro "<Target Person Name>" --json --limit 5
```

If warm intro exists → use the `/outreach` skill to reach the mutual connection first, not SendPilot.

### Step 3 — Build Dossier on Target Person
```powershell
# Unified profile from LinkedIn + Happenstance
contact-goat-pp-cli dossier "https://www.linkedin.com/in/<slug>" --json --compact
```

Use the dossier output to personalize the SendPilot connection note. Pull: current role, recent activity, shared connections.

### Step 4 — Prospect Search (When No Warm Intro Exists)
```powershell
# Find implementation/CS/solutions contacts at the target company — LinkedIn only (free)
contact-goat-pp-cli prospect "<Company> implementation OR 'customer success' OR 'solutions engineer'" --limit 30 --json
```

Priority roles for job search (in order):
1. Implementation / Professional Services
2. Customer Success
3. Solutions Architect / Solutions Engineer
4. HR / Technical Recruiting
5. Partnerships, Program Mgmt
6. Sales / GTM

### Step 5 — Feed into SendPilot
- Export the contact list from Step 4
- Pass to `/sendpilot job-search <company>` to build the campaign
- **Do not add anyone from Steps 1-2 to SendPilot** — those are warm paths, handle manually

### Step 6 — Update Tracker
Log coverage results in `C:\Users\Leo\OneDrive\Docs\resume\Networking\<Company>\` tracker:
- Mark contacts with warm intros as `warm-path` (bypass SendPilot)
- Mark cold contacts as `sendpilot-queued`

---

## 4. Branch 2 — DigitalTrack Lead Gen

**Trigger:** `/contact-goat lead-gen <niche> [location]`

**Goal**: Find local business decision-makers to feed into SendPilot lead gen campaigns. Contact Goat does the research; SendPilot does the outreach.

### Step 1 — Prospect Search
```powershell
# Find local business owners matching the ICP
contact-goat-pp-cli prospect "<niche> owner OR founder OR 'general manager'" --limit 50 --json

# With location filter (uses Happenstance — check quota first)
contact-goat-pp-cli prospect "<niche> owner OR founder" --source li --limit 50 --json
```

**Default ICP for DigitalTrack**:
| Field | Value |
|-------|-------|
| Target titles | Owner, Founder, General Manager, Marketing Manager |
| Industries | Restaurant, Home Services, Contractor, Retail, Auto, Medical/Dental |
| Location | Fairfield CA, Solano County, Sacramento, Bay Area |
| Company size | 1–50 employees |
| Exclude | Chains, franchises, companies already in Salesflare |

### Step 2 — Dedup Against Salesflare
Before adding to SendPilot, check if they're already in CRM:
- Use `/salesflare` skill: search contacts by name or company
- Remove anyone already in Salesflare pipeline (stage: Outreach → Closed Won/Lost)

### Step 3 — Export to SendPilot
- Export prospect list as CSV (LinkedIn URLs + names)
- Pass to `/sendpilot lead-gen <niche> <location>` to build the campaign
- Campaign naming: `DT-LeadGen-[Niche]-[YYYY-MM]`

### Step 4 — Warm Path Check (Optional, Uses Happenstance Quota)
For high-value targets (e.g., a specific restaurant chain owner):
```powershell
contact-goat-pp-cli warm-intro "<Target Name>" --json
```
If mutual connection found → `/outreach` skill, not SendPilot.

---

## 5. Branch 3 — Single Contact Intro

**Trigger:** `/contact-goat intro <person-name-or-linkedin-url>`

For one-off warm intro research — e.g., before a specific job application or prospect call.

```powershell
# Find who can introduce Leo to this person
contact-goat-pp-cli warm-intro "<Person Name>" --json --limit 5

# See people in BOTH LinkedIn 1st-degree AND Happenstance (strongest signals)
contact-goat-pp-cli intersect --json | grep -i "<Company>"
```

Output will show mutual connections ranked by strength. Pick the strongest one and use `/outreach` to reach them.

---

## 6. Branch 4 — Contact Enrichment

**Trigger:** `/contact-goat enrich <linkedin-url>`

Build a full dossier on a known contact before a call, interview, or personalized message.

```powershell
# Full profile from all configured sources
contact-goat-pp-cli dossier "<https://linkedin.com/in/slug>" --json

# Progressive enrichment: LinkedIn → Happenstance → Deepline (cheapest first)
# Only use --deepline if email is needed and budget allows
contact-goat-pp-cli waterfall "<https://linkedin.com/in/slug>" --max-cost 2 --json
```

Use the dossier to:
- Personalize SendPilot connection note (pull recent post, mutual connection)
- Prep for NSA conversation (Golden Question context)
- Qualify before adding to Salesflare

---

## 7. Branch 5 — Status / Quota Check

**Trigger:** `/contact-goat status`

```powershell
# Check Happenstance searches remaining this month
contact-goat-pp-cli user get-limits --json

# Check Deepline spend (if configured)
contact-goat-pp-cli budget --json

# Check CLI health and all auth sources
contact-goat-pp-cli doctor
```

Report:
- Happenstance searches used / remaining (resets monthly)
- Deepline credits used this month (if configured)
- LinkedIn auth status (valid/expired)

---

## 8. Integration Map

```
Contact Goat (Research)
       │
       ├── warm intro found ──────────► /outreach skill (manual email/LinkedIn)
       │
       ├── cold contacts found ────────► /sendpilot skill (LinkedIn automation)
       │
       └── hot lead responds ──────────► /salesflare skill (add to CRM pipeline)
```

**Never add a warm-path contact to SendPilot automation** — it degrades the relationship signal.

---

## 9. Quota Management

Happenstance free tier = **14 searches/month**. Budget deliberately:

| Use Case | Cost | Monthly Allocation |
|----------|------|-------------------|
| Job search (priority companies) | 1/search | 6 searches |
| DigitalTrack lead gen (high-value targets) | 1/search | 4 searches |
| Warm intro checks | 1/search | 4 searches |
| **Total** | | **14 max** |

When quota is low:
- Use `--source li` flag to force LinkedIn-only (free, no Happenstance cost)
- Reserve remaining Happenstance searches for highest-priority warm intro lookups

---

## 10. Rules & Guardrails

1. **LinkedIn first, always** — always try `--source li` before using Happenstance quota
2. **Deepline requires explicit budget** — never run `waterfall` or `prospect --deepline` without `--budget N --yes`
3. **Don't mix job search and lead gen contacts** — keep them in separate SendPilot campaigns
4. **Warm intros bypass SendPilot** — anyone with a mutual connection gets manual outreach via `/outreach`, not automation
5. **Dedup before SendPilot** — always check Salesflare first for lead gen targets
6. **Never store API keys in skill files or git** — auth via env vars or config.toml only
7. **LinkedIn account health** — Contact Goat reads from Leo's own session; don't run aggressive scrapes (stay under 100 profile lookups/day)

---

## 11. Self-Improvement Loop

- After each job search company: add coverage result to the company tracker
- After any new workflow that works: add it as a Cookbook example below
- If a command fails or returns empty: check `contact-goat-pp-cli doctor`, note the fix here
- Monthly: run `user get-limits` to reset planning for Happenstance quota

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| Auth error (exit 4) | Run `contact-goat-pp-cli doctor` to see which source failed |
| LinkedIn not logged in | `uvx linkedin-scraper-mcp@latest --login` |
| Happenstance returns empty | Cookies may have expired — re-import with `auth login --chrome --service happenstance` |
| Happenstance quota exhausted | Switch to `--source li` for the rest of the month |
| Deepline credit error | Add `--budget N --yes` flags, or skip Deepline entirely |
| `uvx` not found | Install uv: `pip install uv` or `winget install astral-sh.uv` |
| Rate limited (exit 7) | CLI auto-retries with backoff; wait 60 seconds and retry |
