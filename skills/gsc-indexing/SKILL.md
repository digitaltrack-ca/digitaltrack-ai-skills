---
name: gsc-indexing
description: Validate URL indexing readiness and submit sitemaps to Google Search Console — checks live status, sitemap membership, GSC verdict, and generates CSV + Markdown reports for any client property.
triggers:
  - "submit sitemap to Google"
  - "GSC sitemap"
  - "google sitemap submit"
  - "check indexing"
  - "url indexing report"
  - "are these pages indexed"
  - "GSC indexing report"
  - "sitemap submission google"
agents:
  - claude-code
  - codex
  - cursor
  - gemini-cli
  - any
---

# GSC Indexing Skill

AI-agnostic WAT skill for checking URL indexing readiness and submitting sitemaps to Google Search Console via the official GSC API.

**Script**: `skills/gsc-indexing/lib/gsc_indexing.py`
**Requirements**: Python 3.8+ (stdlib only). Optional: `google-auth` pip package for service account auth.
**Migrated from**: `C:\Users\Leo\OneDrive\Docs\...\codex\Skills\gsc-indexing-workflow\` (June 2026)

---

## What It Does

1. **URL validation** — for each URL in a list: checks HTTP status, redirects, sitemap membership, HTML detection, page title, meta description
2. **Sitemap submission** — submits the sitemap URL to Google Search Console via the official Sitemaps API (`--submit-sitemap`)
3. **URL Inspection** — calls the GSC URL Inspection API and adds index verdict, coverage state, last crawl time, and canonical data to each row (`--inspect-index`)
4. **Report output** — writes a CSV + Markdown checklist to the specified output directory

---

## IMPORTANT: Do Not Use Google Indexing API for Local SEO Pages

Restaurant pages, local service pages, location pages, menu pages, and blog posts are **not supported** by Google's Indexing API.

The Indexing API is for `JobPosting` and `BroadcastEvent` URLs only. Using it for regular pages is a terms-of-service grey area and Google may deprioritize those URLs.

**The correct Google path for local SEO clients:**
1. Ensure the page is live, useful, and internally linked
2. Add it to the sitemap with a truthful `<lastmod>` date
3. Submit or resubmit the sitemap via this skill (`--submit-sitemap`)
4. Use URL Inspection to monitor (`--inspect-index`)
5. Manually request indexing from GSC UI for the handful of highest-priority pages

For Bing: use the `indexnow` skill instead — it IS the right protocol for these pages.

---

## Auth Setup (One-Time)

### Option 1 — Service Account JSON (preferred for automation)

```powershell
# Requirements:
# - GCP project with "Google Search Console API" enabled
# - Service account created with a JSON key file downloaded
# - Service account email added as a verified owner in GSC for the property

# Store the JSON key at:
# C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\AI keys\gsc-service-account.json
# (Keep this out of any git repo — add to .gitignore)

# Install optional google-auth package for service account support:
pip install google-auth
```

### Option 2 — Bearer Token (quick, one-time use)

```powershell
# Get a fresh token via gcloud or Google OAuth playground
$env:GSC_ACCESS_TOKEN = "ya29.your-token-here"
```

---

## Core Usage

### Generate URL list from sitemap

```powershell
# Quick way to get a URL list from the sitemap:
python -c "
import urllib.request, re
data = urllib.request.urlopen('https://sabormexkitchen.com/sitemap.xml').read().decode()
urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', data)
open('urls.txt', 'w').write('\n'.join(urls))
print(f'Saved {len(urls)} URLs to urls.txt')
"
```

### Check indexing status only (no API calls)

```powershell
cd C:\Users\Leo\ai-skills
python skills/gsc-indexing/lib/gsc_indexing.py \
  --urls urls.txt \
  --site "sc-domain:sabormexkitchen.com" \
  --sitemap "https://sabormexkitchen.com/sitemap.xml" \
  --output-dir "C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Clients\Sabor Mex kitchen\website content\reports"
```

### Submit sitemap to Google + check indexing status

```powershell
python skills/gsc-indexing/lib/gsc_indexing.py \
  --urls urls.txt \
  --site "sc-domain:sabormexkitchen.com" \
  --sitemap "https://sabormexkitchen.com/sitemap.xml" \
  --submit-sitemap \
  --credentials "C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\AI keys\gsc-service-account.json" \
  --output-dir "C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Clients\Sabor Mex kitchen\website content\reports"
```

### Full report — sitemap submit + URL inspection verdicts

```powershell
python skills/gsc-indexing/lib/gsc_indexing.py \
  --urls urls.txt \
  --site "sc-domain:sabormexkitchen.com" \
  --sitemap "https://sabormexkitchen.com/sitemap.xml" \
  --submit-sitemap \
  --inspect-index \
  --credentials "C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\AI keys\gsc-service-account.json" \
  --output-dir "C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Clients\Sabor Mex kitchen\website content\reports"
```

---

## Output Files

| File | Contents |
|------|----------|
| `gsc-indexing-report-YYYY-MM-DD.csv` | All URLs with HTTP status, sitemap membership, GSC verdict, coverage state, last crawl |
| `gsc-indexing-checklist-YYYY-MM-DD.md` | URLs grouped by recommended action — ready for review |

### Recommended Actions in the Report

| Action | Meaning |
|--------|---------|
| Ready for manual URL Inspection and request indexing | Page is live, in sitemap, no issues — go to GSC UI and request |
| Add final URL to sitemap, then resubmit sitemap | Page is live but missing from sitemap |
| Fix non-200 status before GSC request | Page has an error or redirect issue |
| Fix live URL error before GSC request | Page failed to load |
| Use final canonical URL for GSC inspection | URL is redirecting — use destination URL instead |

---

## Client Reference

| Client | GSC Property | Sitemap |
|--------|-------------|---------|
| Sabor-Mex Kitchen | `sc-domain:sabormexkitchen.com` | `https://sabormexkitchen.com/sitemap.xml` |
| MP Prime Cleaning | `sc-domain:mpprimecleaning.com` | `https://mpprimecleaning.com/sitemap.xml` |
| Nieto's Woodworking | `sc-domain:nietoswoodworking.com` | `https://nietoswoodworking.com/sitemap.xml` |
| Arroyo Drywall | `sc-domain:arroyodrywall.com` | `https://arroyodrywall.com/sitemap.xml` |
| DigitalTrack | `sc-domain:digitaltrack.co` | `https://digitaltrack.co/sitemap.xml` |

Add new clients by adding a row above. Full list in the `google-search-console` skill.

---

## Combined Submission Workflow (Bing + Google)

For a full "tell both search engines" push after a content update:

```powershell
cd C:\Users\Leo\ai-skills

# Step 1: Bing — IndexNow (real-time push)
python skills/indexnow/lib/indexnow_submit.py submit --domain sabormexkitchen.com

# Step 2: Google — GSC sitemap submission
python -c "import urllib.request, re; data=urllib.request.urlopen('https://sabormexkitchen.com/sitemap.xml').read().decode(); open('urls.txt','w').write('\n'.join(re.findall(r'<loc>\s*(.*?)\s*</loc>',data)))"
python skills/gsc-indexing/lib/gsc_indexing.py \
  --urls urls.txt \
  --site "sc-domain:sabormexkitchen.com" \
  --sitemap "https://sabormexkitchen.com/sitemap.xml" \
  --submit-sitemap \
  --credentials "C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\AI keys\gsc-service-account.json" \
  --output-dir "."
```

---

## Rules

1. **Never use this to submit URLs that aren't live and returning 200** — the report will flag them, fix first
2. **Bearer tokens expire in ~1 hour** — generate a fresh one before a long URL inspection run
3. **URL Inspection API limit**: 2,000 inspections/day per property — stay under that
4. **Sitemap submission is idempotent** — safe to run multiple times
5. **Do not git-commit service account JSON** — keep in OneDrive only, never in ai-skills repo
6. **Use `--inspect-index` sparingly** — it counts against the daily API quota; once per sprint is enough

---

## Self-Improvement Loop

- After each new client: add a row to the Client Reference table
- If a new GSC API endpoint becomes available (e.g., Google adds an IndexNow equivalent), update this skill
- If service account auth fails, check that the account has the `sc-domain:` property verified, not just a URL-prefix property
