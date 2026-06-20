---
name: lovable
description: Push prompts to any Lovable project via MCP. Use to build new pages, update existing pages, or send any instruction to the Lovable agent without leaving Claude Code.
---

# Skill: lovable

**Purpose:** Send a prompt to a Lovable project using the Lovable MCP server. Works from any project on this machine — the MCP connection is global (user scope).

---

## Usage

```
/lovable "[what to build or change]"
/lovable "[page or feature]" --project [project-id]
```

If no `--project` is given, look for the project ID in the current project's `CLAUDE.md` (search for `lovable.app` or `lovable.dev/projects/`).

---

## Step-by-step workflow

### 1. Resolve the project ID

Check the current project's `CLAUDE.md` for a Lovable project URL like:
```
https://lovable.dev/projects/e90a04a9-2f5d-4480-b09f-b17b50ace260
```
The UUID after `/projects/` is the project ID.

If no URL is in `CLAUDE.md`, ask Leo to confirm which Lovable project to target before proceeding.

### 2. Confirm the project is reachable

Call `mcp__lovable__get_project` with the project ID. If it returns project details, the connection is live. If it errors, tell Leo and stop — do not send a build prompt to a wrong or inaccessible project.

### 3. Prepare the prompt

Before calling `mcp__lovable__send_message`, assemble the full prompt:
- If a page-specific Lovable prompt file exists (e.g., `lovable-homepage-prompt.md`, `lovable-services-prompt.md`), read it and send its full contents as the message body.
- If no file exists and the user gave a short instruction, expand it using the project's brand constants, NAP, and page structure from the project skill (e.g., `/hair-day-lovable`) before sending.
- Never send a vague one-liner like "build the services page" — Lovable needs the full spec.

### 4. Send the message

Call `mcp__lovable__send_message` with:
- `projectId`: the UUID from step 1
- `message`: the full prompt text

### 5. Report back

After the call returns:
- Tell Leo what was sent and to which project.
- Note any diff or confirmation returned by the tool.
- If the prompt referenced placeholder values (domain, photo, GBP CID), flag those explicitly so Leo knows what still needs filling in on the live site.

---

## Known project IDs

| Client / Project        | Lovable Project ID                          | Live URL |
|-------------------------|---------------------------------------------|----------|
| IVR (Innovative Vision Realty) | `e90a04a9-2f5d-4480-b09f-b17b50ace260` | https://ivr-invest.lovable.app/ |
| Hair Day Beauty Salon   | `2c191394-440a-4caa-bccd-543663f742d9`      | TBD |
| JD Remodel Services (prospect deck) | `eb27d094-8859-4358-8808-abb0a26ed49c` | https://id-preview--eb27d094-8859-4358-8808-abb0a26ed49c.lovable.app |
| Studio LUNAREY (prospect deck) | `efe69f6c-15c7-4e1a-8155-9d3d492bdc38` | https://studiolunarey.lovable.app |
| Jarquin-Rose Law (prospect deck) | `743a77c7-6c99-4cdb-8cd8-e2404b2cd1e6` | https://jarquin-rose-law.lovable.app |

Update this table as new Lovable projects are created for other clients.

---

## Rules

- **Never send to the wrong project.** Always confirm the project ID from CLAUDE.md or an explicit user instruction before calling send_message.
- **Always send a complete prompt.** A partial or vague message wastes the Lovable agent's context — prep it fully first.
- **Never expose private data in prompts.** Prompts sent via MCP go to Lovable's servers — don't include client pricing, internal notes, or unapproved copy.
- **No IVR changes without Leo's explicit instruction.** The IVR site is live. Do not send messages to the IVR project unless Leo specifically asks.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `mcp__lovable__*` tools not in deferred list | Start a fresh Claude Code session — the Lovable MCP loads at session start |
| `get_project` returns auth error | Run `claude mcp list` — if lovable shows `! Needs authentication`, run `claude mcp add -s user --transport http lovable "https://mcp.lovable.dev"` again to re-trigger OAuth |
| Wrong project modified | Check CLAUDE.md for the correct UUID — don't rely on memory |
