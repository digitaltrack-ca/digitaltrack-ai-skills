# Skill: digitaltrack-prospect-presentation

**Purpose:** Build or update a DigitalTrack-branded interactive prospect presentation based on audit files, research notes, transcripts, screenshots, and client meeting notes.

**Usage:**
```
/digitaltrack-prospect-presentation "C:\path\to\prospect\folder"
```

---

## What This Skill Does

When invoked, follow these steps in order:

### Step 1 — Inspect the prospect folder
- List all files in the provided prospect folder path
- Identify: transcripts, audit screenshots, notes, existing HTML files, competitor research, GBP data, website screenshots, social media data

### Step 2 — Read meeting transcripts first
- If any `.txt`, `.md`, `.docx`, or transcript files exist, read them first
- Extract: client name, business type, location, goals, pain points, what they liked/disliked, budget signals, timeline, services discussed
- Note any missing information

### Step 3 — Extract structured intelligence
Build a working summary with these fields:
- **Business goals** (what they want to achieve)
- **Pain points** (what is broken or frustrating now)
- **Services discussed / relevant** (what DigitalTrack can offer)
- **Opportunities** (quick wins, gaps competitors have, low-hanging fruit)
- **Missing info needed** (what you still need to complete the proposal)

### Step 4 — Inspect DigitalTrack brand guidelines and assets

**Brand rules file (always read this first):**
`C:\Users\Leo\.claude\rules\digitaltrack-brand.md`

**Brand asset locations:**
| Asset | Path |
|---|---|
| Logo (color, white BG) | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Logo source file\digital track with tagline(1).png` |
| Logo (white, dark BG) | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Logo source file\digital track with tagline for dark bg(2).png` |
| Brand identity overview | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Logo source file\brand identity.png` |
| Brand identity kit (JPG) | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Kit\digital track brand identity kit.JPG` |
| Brand identity kit (PNG) | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Kit\digital track brand identity kit png.PNG` |
| Brand guideline PDF | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Brand Guideline\PDF\Digital Track logo brand guideline.PDF` |
| Montserrat font folder | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Montserrat\` |
| Logo source files folder | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Logo source file\` |
| Brand guideline PNG sheets | `C:\Users\Leo\OneDrive\Pictures\Digitaltrack\Digital Track logo brand guideline\Brand Guideline\PNG\` |

**Quick brand reference (from brand rules):**
- Primary cyan: `#40D6E4` — use for headings, CTAs, borders, active states, icon accents
- Charcoal: `#606165` — body text, secondary headings
- Dark BG: `#000000` — cover/hero sections
- White: `#FFFFFF` — content section backgrounds
- Font: Montserrat (all weights) — Google Fonts CDN or local from Montserrat folder above
- Logo wordmark: "digital" in charcoal bold, "Track" in cyan bold, progress-bar icon below-left, "Digital Marketing" tagline
- Logo minimum width: 90px web / 1.25in print

Apply brand colors, typography, logo rules, and layout preferences to all output.

### Step 5 — Build or update the branded interactive presentation
Create or update `index.html` in the prospect folder:
- Single-file HTML with embedded CSS and JS (no external dependencies except Google Fonts)
- Montserrat font via Google Fonts CDN
- Brand colors: `#40D6E4` (cyan), `#606165` (charcoal), `#000000` (dark BG), `#FFFFFF` (white)
- Sections: Cover → About Client → Current State / Audit → Opportunities → Recommended Services → Proposed Strategy → Investment (placeholder) → Next Steps → CTA
- Cover: dark background, cyan headline, DigitalTrack logo text top-left
- Navigation: fixed top bar, logo left, section anchors right
- Every section scannable in under 10 seconds — short bullets, no walls of text
- Mobile responsive
- Suitable for screen recording / Loom walkthrough

### Step 6 — Create follow-up email drip content
Create `email-drip.md` in the prospect folder with:
- Email 1: Same-day follow-up (reference the meeting, attach/link the deck)
- Email 2: 3-day follow-up (one specific insight or opportunity from the audit)
- Email 3: 7-day follow-up (urgency / social proof / next step)
- All emails: direct, practical, no fluff, signed as Leo Callejas | DigitalTrack

### Step 7 — Create a video recording script
Create `video-script.md` in the prospect folder:
- 5–8 minute screen-recording script walking through the presentation
- Intro: who Leo is, why this deck was built for this specific client
- Walk each section with talking points
- Close: clear call to action, what happens next
- Tone: conversational, confident, specific to the prospect

### Step 8 — Create a recommendations summary
Create `recommendations-summary.md` in the prospect folder:
- Top 3–5 prioritized recommendations
- For each: what to fix, why it matters, estimated impact, effort level (Low/Med/High)
- One-page format suitable for a PDF export or printed leave-behind

### Step 9 — Create a missing-info file
Create `missing-info-needed.md` in the prospect folder:
- List every piece of information that is needed to complete or strengthen the proposal
- Flag anything that blocks deployment (e.g., no pricing approved, no logo from client, no website access)

### Step 10 — Prepare for Netlify deployment
- Confirm `index.html` is self-contained (no broken relative paths)
- Add a comment block at the top of index.html with: prospect name, creation date, DigitalTrack contact
- Confirm no internal pricing, private transcripts, or raw audit data is exposed in the HTML source

---

## Privacy Rules

- Do NOT embed internal pricing, margin notes, or raw audit tools output in the public HTML file
- Do NOT include private transcript text verbatim in the HTML — synthesize it into insights
- If uncertain whether something is safe to publish, add it to `missing-info-needed.md` and ask Leo

---

## Output Summary

After completing all steps, provide Leo with:
- Path to `index.html` (ready to drag into Netlify)
- Summary of what was extracted from the prospect folder
- List of what's complete vs. what needs Leo's input
- Any flags or blockers noted in `missing-info-needed.md`
