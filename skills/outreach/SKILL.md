# /outreach — Company-Focused Networking Outreach

## Purpose
Run the daily networking outreach workflow for a specific company: show who needs contact today (overdue follow-ups first, then new contacts), display drafted messages, and send emails to the ones you pick.

## Usage
```
/outreach <company>
```
Examples: `/outreach block`, `/outreach adyen`, `/outreach plaid`

---

## Step 1 — List today's contacts for the company

Run this command via PowerShell and relay the full output to the user:

```powershell
python "C:\Users\Leo\OneDrive\Docs\resume\job applications\networking_outreach_triage.py" --company "<COMPANY>" --list-mode
```

Replace `<COMPANY>` with the company argument (lowercase, e.g. `block`).

The output will be a numbered list like:
```
[1] Jane Doe — Sr. PM | 14 days overdue | Email: jane@block.com
[2] John Smith — Lead | 9 days overdue | LinkedIn (manual)
[3] Alice Brown — Tech PM | Wave week1/A1 | LinkedIn (manual)
```
Each entry includes a draft message below it.

Display the full numbered list clearly to the user.

---

## Step 2 — Ask who to send to

After displaying the list, ask:

> "Which contacts should I send to? Say the numbers (e.g. '1 and 3') or names, or 'all' for everyone with an email address."

If the user says **"all"**: collect all contact names that have an email address (shown as `Email: ...` in the list), not LinkedIn contacts.

If the user says numbers or names: map the numbers to the full names shown in the list output.

LinkedIn contacts must be sent **manually** — the script will skip them and remind you.

---

## Step 3 — Send the selected emails

Build the comma-separated name list and run:

```powershell
python "C:\Users\Leo\OneDrive\Docs\resume\job applications\networking_outreach_triage.py" --company "<COMPANY>" --send-names "Full Name 1,Full Name 2"
```

The script will print per-contact results:
- `SENT  Jane Doe → jane@block.com`
- `SKIP (LinkedIn)  John Smith — copy draft manually`
- `FAIL  Alice Brown → ...  (error detail)`

Relay the results clearly. Remind the user to update the tracker CSV for any contacts reached.

---

## Edge cases

- **No contacts found**: If the company name doesn't match any tracker folder, suggest checking the exact folder name in `C:\Users\Leo\OneDrive\Docs\resume\Networking\`
- **All LinkedIn, no email contacts**: Tell the user all contacts require manual outreach — display the drafts so they can copy-paste them on LinkedIn
- **Credential not set up**: If the script fails with a credential error, tell the user to run: `python "...\networking_outreach_triage.py" --setup-credential`
- **Partial company match**: `--company block` matches any folder containing "block" (case-insensitive). If two companies match unexpectedly, suggest a more specific name.

---

## Script location
`C:\Users\Leo\OneDrive\Docs\resume\job applications\networking_outreach_triage.py`

## Tracker CSVs location
`C:\Users\Leo\OneDrive\Docs\resume\Networking\<Company>\*Tracker*.csv`
