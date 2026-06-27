# Google Search Console CLI — One-Time Auth Setup

## GCP Project to reuse
`gws-cli-dt-20260419` (already exists — just add the GSC API to it)

## Step 1 — Enable the API
1. Go to: https://console.cloud.google.com/
2. Make sure project `gws-cli-dt-20260419` is selected (top-left dropdown)
3. Left menu → **APIs & Services** → **Library**
4. Search: `Google Search Console API`
5. Click it → click **Enable**

## Step 2 — Create OAuth Client
1. Left menu → **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `gsc-cli` (or anything)
5. Click **Create**

## Step 3 — Copy the credentials (do NOT download JSON)
A dialog pops up showing:
- **Your Client ID** — looks like: `123456789-abc123.apps.googleusercontent.com`
- **Your Client Secret** — looks like: `GOCSPX-abc123xyz`

Copy each one. You don't need the JSON download button.

## Step 4 — Run these two commands in PowerShell
```powershell
google-search-console-pp-cli auth set-client YOUR_CLIENT_ID YOUR_CLIENT_SECRET
google-search-console-pp-cli auth login
```

`auth login` opens your browser. You'll see a Google sign-in page.
Sign in with `info@digitaltrack.co` → click **Allow**.

If you see "Google hasn't verified this app" → click **Advanced** → **Go to [app name] (unsafe)** → Allow.
That warning is normal for personal Desktop app OAuth clients.

## Step 5 — Verify it worked
```powershell
google-search-console-pp-cli doctor
google-search-console-pp-cli webmasters list-sites --json
```

`list-sites` shows all GSC properties the account has access to.

## Where credentials are stored (automatically)
`C:\Users\Leo\.config\google-search-console-pp-cli\config.toml`

You never touch this file directly. The CLI manages it. Tokens auto-refresh — you will never need to log in again.

## Add Test User (if auth login fails)
If Google blocks the login because the OAuth app is in Testing mode:
1. GCP Console → **APIs & Services** → **OAuth consent screen**
2. Click **Audience** tab → **+ Add Users**
3. Add: `info@digitaltrack.co`
4. Save → try `auth login` again
