---
name: google-search-console
description: Pull and analyze Google Search Console data for any client property — quick wins, traffic drops, content decay, cannibalization, monthly reports — using the local SQLite-cached CLI.
triggers:
  - "GSC"
  - "Google Search Console"
  - "search console"
  - "quick wins"
  - "keyword ranking"
  - "traffic dropped"
  - "site traffic"
  - "gsc report"
  - "gsc audit"
  - "monthly GSC"
agents:
  - claude-code
  - codex
  - cursor
  - gemini-cli
  - any
---

# Google Search Console Skill

AI-agnostic WAT skill for pulling, caching, and analyzing Google Search Console data from the terminal.

**Binary**: `google-search-console-pp-cli`
**Source**: [printing-press-library/marketing/google-search-console](https://printingpress.dev/library/marketing/google-search-console)
**Install**: `npx -y @mvanhorn/printing-press-library install google-search-console` (requires Go)

---

## 1. Auth Setup (One-Time Per Machine)

### Prerequisites
- Go installed: `winget install GoLang.Go`
- GSC binary installed: `npx -y @mvanhorn/printing-press-library install google-search-console`
- GCP project with Search Console API enabled (reuse existing `gws-cli-dt-20260419` or create a new one)

### OAuth Setup Steps
```powershell
# 1. In Google Cloud Console: APIs & Services → Library → enable "Google Search Console API"
# 2. Create OAuth client: Credentials → Create Credentials → OAuth client ID → Desktop app
# 3. Copy Client ID and Client Secret, then:
google-search-console-pp-cli auth set-client <CLIENT_ID> <CLIENT_SECRET>
google-search-console-pp-cli auth login
# Opens browser → click Allow → done. Tokens auto-refresh forever.

# Verify everything works:
google-search-console-pp-cli doctor
```

**Config stored at**: `~/.config/google-search-console-pp-cli/config.toml`

### Write Scope (for sitemap submit / site add)
```powershell
google-search-console-pp-cli auth login --scope write
```

---

## 2. Property Format

GSC has two property types — always use the correct format:

| Type | Format | When to use |
|------|--------|-------------|
| Domain property | `sc-domain:example.com` | Modern preferred format, covers all subdomains |
| URL-prefix | `https://www.example.com/` | Older sites, must include trailing slash |

List all properties the token can see:
```powershell
google-search-console-pp-cli webmasters list-sites --json
```

---

## 3. First Run on a New Client Property

Run this sequence when onboarding a new client into the local cache:

```powershell
# Step 1: Confirm connectivity
google-search-console-pp-cli doctor

# Step 2: Verify the property is accessible
google-search-console-pp-cli webmasters list-sites --json

# Step 3: Sync 90 days into local SQLite (safe to re-run, idempotent)
google-search-console-pp-cli sync --site sc-domain:clientdomain.com --last 90d

# Step 4: Run the first quick-wins report (page-2 keywords with high impressions)
google-search-console-pp-cli quick-wins sc-domain:clientdomain.com --position 8-20 --min-imps 100 --json
```

---

## 4. Core Workflows

### Monthly SEO Report (run for each client on the 1st)
```powershell
# Period-over-period: last 28 days vs previous 28 days
google-search-console-pp-cli compare sc-domain:clientdomain.com --period 28d --vs prev-period --dim query --top 50

# Top pages this month vs last month
google-search-console-pp-cli compare sc-domain:clientdomain.com --period 28d --vs prev-period --dim page --top 20 --json

# New queries that emerged this month
google-search-console-pp-cli new-queries sc-domain:clientdomain.com --since 28d --min-imps 30 --top 50 --json
```

### Quick Wins (Page-2 Keywords to Prioritize)
The highest-leverage recommendation for local SEO clients — keywords already ranking 8-20 with real impressions.
```powershell
google-search-console-pp-cli quick-wins sc-domain:clientdomain.com --position 8-20 --min-imps 50 --json
```

### Traffic Drop Investigation
Run when a client says "traffic dropped" or you notice a dip:
```powershell
# 1. Find the exact day traffic dropped
google-search-console-pp-cli cliff sc-domain:clientdomain.com --metric clicks --threshold -20% --window 14d --json

# 2. See which queries moved in the affected period
google-search-console-pp-cli compare sc-domain:clientdomain.com --period 28d --vs prev-period --dim query --top 25 --agent

# 3. Check for indexing regressions (pages that got de-indexed)
google-search-console-pp-cli coverage-drift sc-domain:clientdomain.com --field indexingState --days 30 --json
```

### Keyword Cannibalization Audit
For clients where a service keyword ranks poorly because multiple pages compete:
```powershell
google-search-console-pp-cli cannibalization sc-domain:clientdomain.com --min-imps 30 --top 25 --json
```

### Title/Meta Description Rewrite Queue (CTR Outliers)
Find pages with abnormally low CTR for their ranking position — title or description needs work:
```powershell
google-search-console-pp-cli outliers sc-domain:clientdomain.com --metric ctr --sigma 2 --min-imps 100 --top 30 --json

# Export as CSV for the team
google-search-console-pp-cli outliers sc-domain:clientdomain.com --metric ctr --sigma 2 --min-imps 100 --top 30 --csv > rewrite-queue.csv
```

### Content Decay (Refresh Queue)
Pages with steady traffic decline — priority content update candidates:
```powershell
google-search-console-pp-cli decaying sc-domain:clientdomain.com --window 90d --min-imps 200 --top 20 --json
```

### Indexing & Sitemap Health
```powershell
# Check if specific URLs are indexed
google-search-console-pp-cli url-inspection inspect-url --site sc-domain:clientdomain.com --inspection-url https://clientdomain.com/service-page/ --json

# Sitemap status
google-search-console-pp-cli webmasters list-sitemaps --site sc-domain:clientdomain.com --json

# Detect sitemap regressions vs last week
google-search-console-pp-cli sitemap-watch sc-domain:clientdomain.com --since 7d --json
```

### Cross-Client Agency Roll-Up
One command across all client properties the token sees:
```powershell
# Top queries across all clients, last 28 days
google-search-console-pp-cli roll-up --metric clicks --group-by query --top 100 --last 28d --json

# Top pages across all clients
google-search-console-pp-cli roll-up --metric clicks --group-by page --top 50 --last 28d --json
```

### Raw Search Analytics Query (Custom)
When you need a custom breakdown not covered by the above:
```powershell
google-search-console-pp-cli webmasters query-search-analytics --site sc-domain:clientdomain.com \
  --params '{"startDate":"2026-05-01","endDate":"2026-05-31","dimensions":["query","page"],"rowLimit":100}' --json
```

---

## 5. Keeping the Cache Fresh

The local SQLite cache is the source of truth for `quick-wins`, `cannibalization`, `outliers`, `compare`, `historical`, `decaying`, and `new-queries`. Keep it updated:

```powershell
# Sync last 7 days (incremental, safe to run daily)
google-search-console-pp-cli sync --site sc-domain:clientdomain.com --last 7d

# Full 90-day refresh (run monthly)
google-search-console-pp-cli sync --site sc-domain:clientdomain.com --last 90d
```

**Tip**: Add to a weekly scheduled task or cron so reports always reflect fresh data.

---

## 6. DigitalTrack Client Reference

| Client | Property | Notes |
|--------|----------|-------|
| *(add clients here as you onboard them)* | | |

**To add a client**: run `webmasters list-sites --json` after auth, copy the `siteUrl` field, add a row above.

---

## 7. Output & Agent Flags

| Flag | Use case |
|------|----------|
| `--json` | Machine-readable output, pipe to files or agent |
| `--csv` | Export for Google Sheets / Excel |
| `--agent` | JSON + compact + no prompts (best for AI agent pipelines) |
| `--select field1,field2` | Trim JSON to only the fields you need (reduces tokens) |
| `--dry-run` | Preview the API request without sending |
| `--top N` | Limit rows returned |

Exit codes: `0` success · `2` usage error · `3` not found · `4` auth error · `5` API error · `7` rate limited · `10` config error

---

## 8. Rules & Guardrails

1. **Always run `sync` before analysis** — `quick-wins`, `compare`, and `outliers` work from the local cache; stale data = wrong recommendations.
2. **Use `--dry-run` before write commands** (sitemap submit, site add/delete).
3. **Don't share CLI output directly with clients** — extract insights, rewrite in plain language.
4. **Data lag**: GSC API lags 2-3 days. Use `--end-date` 3 days ago for stable numbers; add `--data-state all` if you want preliminary data.
5. **API rate limits**: URL inspection is capped at ~2,000/day per property. Use `inspect-batch --max-per-day 2000`.
6. **Domain property vs URL-prefix**: `sc-domain:` covers all subdomains. URL-prefix properties must have trailing slash. If in doubt, `list-sites` to confirm the exact format.
7. **Never commit OAuth tokens or config.toml** to repos.

---

## 9. Self-Improvement Loop

- After each new client onboard: add a row to the Client Reference table above.
- After any new workflow you run successfully: add it as a Cookbook recipe.
- If a command fails: note the fix here under Troubleshooting.
- Monthly: run `sync --last 90d` for all active clients to keep history growing.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| Auth error (exit 4) | Run `google-search-console-pp-cli auth status` then `auth login` to refresh |
| 401 Unauthorized | Token expired. Run `auth login` to get a new one (OAuth auto-refreshes; if using `GSC_ACCESS_TOKEN` env var, tokens last 1 hour) |
| Empty rows for last 1-2 days | GSC data lag — use `--data-state all` or set end date to 3 days ago |
| `sc-domain:` returns wrong data | Confirm property format with `list-sites --json` |
| `historical` returns nothing | Only returns data for date ranges that were previously synced |
| Binary not found | Re-run `npx -y @mvanhorn/printing-press-library install google-search-console` |
| Go required error | Install Go: `winget install GoLang.Go`, then restart terminal |
