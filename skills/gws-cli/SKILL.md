---
name: gws-cli
description: Use the Google Workspace CLI on Leo's Windows machine for Drive, Gmail, Calendar, Sheets, Docs, Slides, and workflow tasks, including safe auth checks, schema discovery, searches, summaries, and cautious write operations.
---

# gws CLI

Use this skill when a task should be handled through the local `gws` Google Workspace CLI on Leo's machine.

## Environment

- Working notes live at `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\AI instructions\gws cli\GWS_CLI_Quickstart.md`.
- `gws` is installed and authenticated for `info@digitaltrack.co`.
- OAuth client path: `C:\Users\Leo\.config\gws\client_secret.json`.
- Encrypted credentials path: `C:\Users\Leo\.config\gws\credentials.enc`.
- GCP project: `gws-cli-dt-20260419`.
- Google Cloud SDK is installed at `C:\Users\Leo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin`.
- In a fresh PowerShell session, prepend Cloud SDK to `PATH` if `gcloud` is needed:

```powershell
$env:PATH="$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin;$env:PATH"
```

## Core Workflow

1. Start with a read-only status or discovery command when the target API shape is unfamiliar.
2. Use `gws schema <service.resource.method>` before write commands or unusual methods.
3. Prefer Gmail/Drive/Calendar native search parameters over broad list-all scans.
4. Use small `pageSize` values while exploring; use `--page-all --page-limit <N>` only when the task needs pagination.
5. Summarize proposed write, send, delete, archive, label, invite, or calendar-change actions before executing them.
6. Never print OAuth secrets, full credential files, access tokens, refresh tokens, or downloaded client secrets.

## Safe Smoke Tests

```powershell
gws auth status
gws drive files list --params '{"pageSize":1,"fields":"files(id,name,mimeType),nextPageToken"}'
gws gmail users messages list --params '{"userId":"me","maxResults":5}'
gws calendar events list --params '{"calendarId":"primary","maxResults":5,"singleEvents":true,"orderBy":"startTime","timeMin":"2026-04-20T00:00:00-07:00"}'
```

## Command Patterns

General shape:

```powershell
gws <service> <resource> [sub-resource] <method> [flags]
```

Common examples:

```powershell
gws drive files list --params '{"pageSize":10}'
gws gmail users messages list --params '{"userId":"me","q":"in:inbox newer_than:7d","maxResults":10}'
gws calendar events list --params '{"calendarId":"primary","singleEvents":true,"orderBy":"startTime","timeMin":"2026-04-20T00:00:00-07:00"}'
gws sheets spreadsheets get --params '{"spreadsheetId":"SPREADSHEET_ID"}'
gws docs documents get --params '{"documentId":"DOCUMENT_ID"}'
gws slides presentations get --params '{"presentationId":"PRESENTATION_ID"}'
```

Schema discovery:

```powershell
gws schema drive.files.list
gws schema gmail.users.messages.list
gws schema calendar.events.list
```

## Gmail Guidance

- Use Gmail query syntax in `q`.
- For cleanup, shortlist candidates first and distinguish marketing messages from operational messages.
- Moving messages to Trash is done through Gmail delete behavior; treat it as a write action.
- Examples:

```powershell
gws gmail users messages list --params '{"userId":"me","q":"from:business@yelp.com category:promotions","maxResults":20}'
gws gmail users messages list --params '{"userId":"me","q":"from:(messaging.yelp.com) subject:\"Message from\"","maxResults":20}'
```

## Drive Guidance

- Use `fields` to keep responses small.
- Use MIME filters for Google Docs, Sheets, Slides, PDFs, and folders.
- Examples:

```powershell
gws drive files list --params '{"pageSize":10,"fields":"files(id,name,mimeType,modifiedTime)"}'
gws drive files list --params '{"pageSize":10,"q":"mimeType='\''application/vnd.google-apps.document'\''","fields":"files(id,name,modifiedTime)"}'
```

## Calendar Guidance

- Always use explicit ISO datetimes with timezone offsets for bounded searches.
- Confirm before creating, updating, deleting, inviting attendees, or changing RSVP state.

## Safety Rules

- Confirm before sending email, modifying Drive files, deleting or trashing messages/files, inviting attendees, or changing calendar events.
- Prefer `--dry-run` when a helper supports it.
- Keep JSON arguments in single quotes in PowerShell so embedded double quotes survive.
- If auth fails, check `gws auth status` first. Do not rerun OAuth setup unless credentials are missing or invalid.
