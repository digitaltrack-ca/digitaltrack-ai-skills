---
name: salesflare
description: Create or update accounts, contacts, opportunities, tasks, and notes in Salesflare via the REST API. Use for new prospect intake, contact lookup, deal creation, meeting logs, or any CRM update. Replaces the CSV import workflow for single records and small batches.
metadata:
  short-description: Direct Salesflare CRM operations via API — no CSV files
---

# Salesflare — WAT Skill

## Trigger
Natural language: "add this contact to Salesflare", "new prospect in CRM", "create account for [company]",
"log this meeting in Salesflare", "look up [name/company] in Salesflare", "update the opportunity for [company]",
"create a follow-up task for [contact]"

Slash command: `/salesflare`

## Goal
Perform Salesflare CRM operations (create/update accounts, contacts, opportunities, tasks, internal notes)
via the REST API — no CSV template, no file upload, no leftover import files.

## Environment Setup

```powershell
# API key must be set before running any lib/ script:
$env:SALESFLARE_API_KEY = "your_api_key_here"

# Or store permanently in Windows user environment (survives terminal restarts):
[System.Environment]::SetEnvironmentVariable("SALESFLARE_API_KEY", "your_key", "User")
```

API key location: Salesflare → Settings → API

## Step-by-Step Process

### For a single new prospect (most common)

1. **Gather the required info** — at minimum: company name OR domain, and contact name OR email
2. **Check if they already exist** — run `lib/salesflare_client.py` lookup before creating anything
3. **Create or update the account** — company/domain deduplication is handled automatically
4. **Create or update the contact** — linked to the account; email is the dedup key
5. **Create an opportunity** — use the likely service (`Local SEO Audit`, `Website Refresh`, `Digital Marketing`)
6. **Create a follow-up task** — specific next action (`Call owner`, `Send Loom audit`, `Follow up on proposal`)
7. **Add an internal note** — lead source, why they matter, exact pitch angle

### For lookup only (no creation)

Use `lib/salesflare_client.py` `find_account()` / `find_contact()` methods directly.
Pass company name, domain, or email. Returns existing Salesflare record or None.

### For bulk intake (10+ records from an event/mixer)

Use the CSV workflow at:
`C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Prospects\salesflare_import_leads.py`

This is the only case where the CSV route is appropriate.

## Using the Library

The canonical Python library lives at `lib/salesflare_client.py`.
It exposes `SalesflareClient` — no dependencies beyond Python stdlib.

```python
from lib.salesflare_client import SalesflareClient, get_salesflare_api_key

client = SalesflareClient(get_salesflare_api_key())

# Lookup
account = client.find_account({"domain": "acmeplumbing.com", "company_name": "Acme Plumbing", "website": "", "email": ""})
contact = client.find_contact({"email": "john@acmeplumbing.com", "contact_name": "John Smith"})

# Create account
account_id = client.record_id(
    client.request("POST", "/accounts", query={"update_if_exists": "true"}, payload={
        "name": "Acme Plumbing",
        "domain": "acmeplumbing.com",
        "website": "https://acmeplumbing.com",
        "tags": ["Prospect", "Local SEO"]
    })
)

# Create contact linked to account
contact_id = client.record_id(
    client.request("POST", "/contacts", query={"force": "true"}, payload={
        "name": "John Smith",
        "email": "john@acmeplumbing.com",
        "phone_number": "707-555-1234",
        "account": int(account_id),
        "position": {"role": "Owner", "organisation": "Acme Plumbing"},
        "tags": ["Prospect"]
    })
)

# Create opportunity
opp_id = client.record_id(
    client.request("POST", "/opportunities", payload={
        "account": int(account_id),
        "name": "Local SEO Audit",
        "value": 500,
        "stage": client.resolve_stage_id("Contacted"),
        "main_contact": int(contact_id),
        "tags": ["Local SEO"]
    })
)

# Create follow-up task
client.request("POST", "/tasks", payload={
    "account": int(account_id),
    "description": "Send Loom audit video",
    "reminder_date": "2026-06-25T09:00:00-07:00"
})

# Add internal note
client.request("POST", "/messages", payload={
    "account": int(account_id),
    "body": "Lead source: SBDC referral\nPitch angle: GBP ranking for 'plumber Fairfield CA'\nNote: Owner is open to monthly retainer if audit impresses."
})
```

## DigitalTrack Tags

Use these standard tags consistently:

| Tag | When to Apply |
|-----|--------------|
| `Prospect` | New lead, not yet qualified |
| `Local SEO` | Good fit for GBP, reviews, local rankings |
| `Website Audit` | Needs website review or Loom |
| `Needs Follow Up` | Clear next step identified |
| `Proposal Sent` | Has received pricing |
| `Warm Lead` | Has responded or shown intent |
| `Bad Fit` | Keep record, no active follow-up |

## Pipeline Stages (Common)

Use `client.resolve_stage_id("Stage Name")` to look up by name at runtime.
Common stages: `New Lead`, `Contacted`, `Audit Sent`, `Proposal Sent`, `Negotiation`, `Closed Won`, `Closed Lost`

## Rules & Guardrails

- **Never delete** accounts or contacts — use `Bad Fit` tag and close the opportunity instead
- **Always dedup first** — call `find_account()` and `find_contact()` before creating anything
- **Email is the contact dedup key** — if no email, use full name; duplicates can be merged in Salesflare UI
- **Domain is the account dedup key** — strip `www.`, lowercase, no `https://`
- **Dry-run before bulk ops** — for 5+ records, print what would happen before committing
- **Never store the API key in code** — always read from `$env:SALESFLARE_API_KEY`
- **Tasks need a due date** — format: `YYYY-MM-DDTHH:MM:SS-07:00` (Pacific time, 9am default)

## Self-Improvement Loop

After each use:
1. Did the dedup catch existing records correctly? If not, add edge case to Rules section.
2. Did a stage name fail to resolve? Add the exact Salesflare stage name to the Pipeline Stages section.
3. Did an API call fail with a specific error? Document the fix here under a `## Known Issues` section.
4. Did you hardcode something that should be dynamic? Move it to a reference section.

First 5-10 uses: watch each run and note what the agent searches for repeatedly — pre-load that data here.
