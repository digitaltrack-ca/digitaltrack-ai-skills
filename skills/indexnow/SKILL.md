---
name: indexnow
description: Submit client website URLs to Bing/IndexNow for fast crawl prioritization — from sitemap or individual URL. Works for Lovable, Builderall, and any custom domain.
triggers:
  - "indexnow"
  - "submit to Bing"
  - "submit URLs"
  - "fast indexing"
  - "IndexNow"
  - "Bing indexing"
  - "notify Bing"
  - "reindex"
agents:
  - claude-code
  - codex
  - cursor
  - gemini-cli
  - any
---

# IndexNow URL Submission Skill

AI-agnostic WAT skill for submitting client website URLs to Bing/IndexNow — either from the sitemap (all pages) or as a single URL after a content update. Replaces manual "Submit URL" clicks in Bing Webmaster Tools.

**Script**: `skills/indexnow/lib/indexnow_submit.py`
**Config**: `skills/indexnow/config/keys.json` (keys stored per domain)
**Endpoint**: `https://api.indexnow.org/indexnow`
**Requirements**: Python 3.8+ (stdlib only — no pip installs)

---

## When to Use

- After publishing or updating pages on any client site
- After adding new local SEO landing pages to a Lovable site
- When a client says "why isn't my page showing in Bing?"
- Monthly maintenance: resubmit full sitemap to keep Bing crawl fresh
- After a site migration or domain change

---

## 1. First-Time Domain Setup

```powershell
cd C:\Users\Leo\ai-skills
python skills/indexnow/lib/indexnow_submit.py setup --domain sabormexkitchen.com
```

The script will:
1. Generate a 32-char hex key unique to the domain
2. Save it to `config/keys.json`
3. Print exact hosting instructions for the key `.txt` file

### Key File Hosting by Platform

**Lovable sites** — send a Lovable message (via /lovable skill):
> "Add a static text file at the root of the site: `/{key}.txt`
> The file must return plain text content: `{key}`
> No HTML — raw UTF-8 text only. This is needed for Bing IndexNow verification."

**Builderall** — upload the `.txt` file via Builderall File Manager to the root public folder.

**Any platform** — verify the file is live before submitting:
```powershell
curl https://sabormexkitchen.com/{key}.txt
# Must return the key as plain text
```

---

## 2. Submit Full Sitemap

```powershell
cd C:\Users\Leo\ai-skills
python skills/indexnow/lib/indexnow_submit.py submit --domain sabormexkitchen.com
```

Fetches `https://<domain>/sitemap.xml`, parses all `<loc>` URLs, POSTs them to IndexNow in one batch.
Handles nested sitemap indexes automatically.
Max 10,000 URLs per POST (IndexNow limit).

---

## 3. Submit a Single URL (After Content Update)

```powershell
python skills/indexnow/lib/indexnow_submit.py submit --domain sabormexkitchen.com --url https://sabormexkitchen.com/menu
```

Use this when you just updated one page and want Bing to re-crawl it immediately.

---

## 4. Custom Sitemap URL

```powershell
python skills/indexnow/lib/indexnow_submit.py submit --domain sabormexkitchen.com --sitemap https://sabormexkitchen.com/sitemap_index.xml
```

---

## 5. List All Configured Domains

```powershell
python skills/indexnow/lib/indexnow_submit.py list
```

---

## Response Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200  | Success | Done |
| 202  | Accepted, key pending | Normal on first submission — wait ~1 hr, resubmit |
| 400  | Bad request | Check URL format |
| 403  | Key not found | Host the key `.txt` file at domain root |
| 422  | URL/host mismatch | URLs must belong to the declared host |
| 429  | Rate limited | Wait 1 hour and retry |

---

## Configured Domains

| Domain | Platform | Key file hosted? |
|--------|----------|-----------------|
| sabormexkitchen.com | Lovable | Pending — see Step 1 |

Add new domains by running `setup --domain <domain>`. Keys are stored in `config/keys.json`.

---

## Rules

1. **Never submit URLs for a domain not in `keys.json`** — run `setup` first
2. **Key file must be live before submitting** — 403 means the file isn't hosted yet
3. **Submit only current/live URLs** — no URLs from old domains or redirected pages
4. **One submission per content push is enough** — don't spam; 429 = rate limited
5. **202 is normal on first submission** — Bing is validating your key; try again in 1 hour if needed
6. **Track in Bing Webmaster Tools** — go to URL Inspection or Submission History to verify

---

## Adding a New Client Domain

```powershell
python skills/indexnow/lib/indexnow_submit.py setup --domain clientdomain.com
```

Then manually add the `"platform"` field to `config/keys.json`:
```json
{
  "clientdomain.com": {
    "key": "<generated>",
    "platform": "lovable",
    "sitemap": "https://clientdomain.com/sitemap.xml"
  }
}
```

Then host the key file per Step 1 instructions for that platform.

---

## Self-Improvement Loop

- If a submit gets 403 repeatedly, confirm the key file is served as raw text (not HTML)
- If Bing Webmaster Tools shows no submission history after 24h, check the key file and resubmit
- If sitemap parsing fails, check for sitemap index format (nested sitemaps) — the script handles these automatically
- Update this SKILL.md with any platform-specific gotchas discovered
