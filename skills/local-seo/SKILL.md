---
name: local-seo
description: DigitalTrack's full Local SEO system — pre-sales audit through monthly maintenance. Covers website SEO, GBP category/service silo gaps, map ranking analysis, citations/NAP, SERP intent, rank-grid prioritization, page planning, content production, QA, and ongoing maintenance. Use for any local service business at any stage of the engagement.
---

# Skill: local-seo

**Purpose:** Run DigitalTrack's Local SEO system from first prospect review through active monthly maintenance. Covers every stage: pre-sales audit, intake, compliance, strategy, research, content planning, production, QA, and ongoing maintenance.

**Usage:**
```
/local-seo "Client Name" "C:\path\to\client\folder"
```

Run a specific stage directly:
```
/local-seo audit "Client Name" "C:\path\to\folder"
/local-seo intake "Client Name" "C:\path\to\folder"
/local-seo research "Client Name" "C:\path\to\folder"
/local-seo page-plan "Client Name" "C:\path\to\folder"
/local-seo content "Client Name" "C:\path\to\folder"
/local-seo qa "Client Name" "C:\path\to\folder"
/local-seo maintenance "Client Name" "C:\path\to\folder"
```

---

## Operating Rules

- Use provided files and facts as source of truth. Do not invent rankings, review counts, URLs, addresses, phone numbers, or categories.
- If live SERP, GBP, citation, or competitor data is needed, browse and cite sources.
- Ask for missing inputs only when the analysis would require guessing. For partial data, clearly mark what could not be verified.
- All output files are Markdown (.md). Never produce Word docs (.docx) from this skill.
- Keep output practical and direct. No filler. Every finding must include: what it is, why it matters, and what to do.
- Do not produce client-facing files with internal pricing, margin notes, raw tool exports, or private transcript text verbatim.

**DigitalTrack internal template references:**
- Client Brief: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Client Brief Template.md`
- Research Pack: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Research Pack Template.md`
- Page Plan: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Page Plan Template.md`
- Launch Checklist: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Launch Checklist Template.md`
- Monthly Tracker: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Monthly Tracker Template.md`
- Audit prompt reference: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\local seo audit prompt.txt`
- Process map: `C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\digitaltrack-local-seo-process-map.md`
- Brand rules: `C:\Users\Leo\.claude\rules\digitaltrack-brand.md`

---

## Step 1 — Read the client folder first

Before doing anything else:

1. List all files in the client folder
2. Read every file — prioritize: GBP exports, rank-grid data, SEO crawl exports, competitor notes, screenshots, meeting notes, prospect briefs
3. Identify which stages have already been completed based on the files present
4. Determine the engagement stage:

| Stage | Signs |
|---|---|
| Pre-sales | No intake, only audit screenshots or GBP data |
| Onboarding | Intake notes exist, no page plan yet |
| In-build | Page plan or content spreadsheet exists |
| Live + Maintenance | Website is live, tracking or reporting files present |

5. Report the stage and what was found. Unless a specific stage was passed in the command, confirm with Leo which stage(s) to run.

---

## Stage 1: Local SEO Audit

### Run when: No `audit-summary.md` exists yet, or Leo passes `audit` argument.

### Intake checklist — gather before starting

Collect what is available. If something is missing, proceed and label the gap clearly.

**Business facts:**
- Business name (legal and DBA if different)
- Website URL
- Canonical address, phone, email
- Any old names, old addresses, old phones, or suite variants
- License number (if applicable)
- Target service area (cities, priority order)
- Primary services and money services
- Business type: storefront / service-area / hybrid

**Data inputs:**
- GBP export (GMBEverywhere, BrightLocal, or screenshot) — categories, services, reviews, photos, posts, service areas
- Website crawl or SEO checker export — internal URLs, title tags, meta descriptions, H1s, word counts, issues
- Rank-grid CSV or screenshot — keyword, geographic distribution, rank positions
- Competitor data — GBP categories, review counts, website URLs
- Citation/NAP report — BrightLocal, Whitespark, or manual list
- Social profile links

---

### Audit sections

Run all sections. Use evidence from provided files. If data is missing, label the gap and continue.

#### A. Brand and NAP consistency

- Compare business name across GBP, website header/footer, social profiles, and directories
- Identify address variants (suite numbers, alternate addresses, old locations)
- Identify phone number variants
- Flag domain confusion (multiple active domains, email domain vs website domain)
- Confirm one canonical name/address/phone to use going forward
- Flag name conflicts with similarly named businesses in the same market

#### B. Website on-page and local SEO

Evaluate the homepage:
- Does the headline clearly state what they do and where?
- Are the top services visible above the fold?
- Are trust signals (reviews, badges, license, years in business, awards) near the top?
- Is the CTA clear and specific?
- Is a local phone number visible without scrolling?

Evaluate service pages:
- Does a dedicated URL exist for each primary service?
- Required title tag pattern: `[Service] [City, State] | [Brand]`
- Does each service page have 400+ words of unique content?
- Are trust elements present on each service page?

Evaluate location/city pages:
- Does a dedicated URL exist for each priority city?
- Required title tag pattern: `[Primary Service] [City, CA] | [Brand]`
- Does each city page have 400+ words of unique content with local proof?
- Are city pages linked from the homepage and relevant service pages?

CTA evaluation:
- Is the primary CTA (call / form / booking) consistent across key pages?
- Is the contact form or estimate form accessible without excessive clicks?
- Does the homepage link to each secondary category page?

#### C. Technical SEO

Using crawl exports or SEO checker data, identify:

| Issue type | Check |
|---|---|
| Indexation | Noindex tags, canonical conflicts, blocked pages |
| Response codes | 4xx broken pages, 5xx errors, redirect chains or loops |
| Title tags | Missing, duplicate, or over 60 characters |
| Meta descriptions | Missing, duplicate, or over 155 characters |
| H1 tags | Missing, empty, duplicate, or multiple H1s per page |
| Thin content | Pages under 300 words on pages that should have real content |
| Duplicate content | Pages with near-identical content sharing separate URLs |
| Page speed | Flag pages loading over 3 seconds |
| Internal links | Orphaned pages, key pages with few inbound internal links |
| URL structure | Query parameters being indexed, excessively long URLs |

Quick technical wins first (high impact / low effort), then architecture fixes.

#### D. GBP category and service silo gap check

This is a strict check. Run it for every GBP category and every GBP service.

**For each GBP category (primary and secondary):**
- Does a dedicated URL exist on the website?
- Does the page title follow the pattern: `[GBP Category] [City] | [Brand]`?
- Does the homepage mention this category in body copy?
- Does the homepage internally link to this category page?

**For each GBP service:**
- Does a dedicated URL exist on the website?
- Does the page title include the exact service and the target city?
- Is this service mapped to the most relevant GBP category?
- Does the relevant category page link to this service page?

**Output — Silo Gap Table:**

| GBP Category | Dedicated URL exists | Title tag correct | Homepage mention | Homepage link | Services mapped | Missing links |
|---|---|---|---|---|---|---|
| [category] | Yes / No | Yes / No / Fix needed | Yes / No | Yes / No | [list] | [list] |

#### E. Map visibility and rank-grid analysis

If rank-grid CSV or screenshot data is provided:

- Identify geographic areas with weak ranking (outside top 3)
- Group weak coordinates into neighborhoods or service areas when location context allows
- Prioritize neighborhoods by: ease of ranking + traffic or revenue value
- Recommend 3 keyword variations per priority neighborhood
- Propose content, internal links, and GBP post ideas tied to weak areas
- Score each neighborhood 1–10 for prioritization

If no rank-grid data, document the current map pack position for the primary keyword and city.

#### F. SERP intent review

For the primary keyword and the 2–3 highest-value secondary keywords:

- Identify the dominant page type in top results (local service / informational / comparison)
- Is a map pack present? Who dominates it and why?
- What does the top organic result do above the fold?
- What goal-completion pattern do winners use?
- What are the most common weaknesses in competing pages?
- What is Google currently rewarding for this query?

Use live SERP data when available.

#### G. Citations and NAP audit

Search by: exact business name, phone variants, address variants, website URL, and city/state combinations. Capture exact listing URLs, not just root domains. Verify live page data.

| Directory | URL found | Name match | Address match | Phone match | Website match | Category match | Priority fix |
|---|---|---|---|---|---|---|---|
| [directory] | [url] | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No | High / Medium / Low |

Priority levels:
- **High:** Wrong phone, wrong city, wrong address, wrong name — these suppress rankings
- **Medium:** Suite/ZIP variance, outdated URL, secondary category mismatch
- **Low:** Punctuation, case, or spacing only

Flag duplicates within the same directory. Include claim URL or support contact path when available.

Include these directories at minimum: Google Business Profile, Apple Maps, Bing Places, Yelp, Facebook, BBB, Houzz, Thumbtack, Nextdoor, Angi, HomeAdvisor, and any relevant niche directories for the industry.

#### H. Social media baseline

For each active platform:
- Profile name, bio, category, link, and CTA button
- Post frequency and last post date
- Follower count if visible
- Whether GBP posts are active and recent

Flag gaps: no GBP posts, inactive Facebook/Instagram, profile bio doesn't state service + city.

#### I. Competitor comparison

For top 3–5 local competitors:
- Review count and rating
- GBP primary category and secondary categories
- Whether they have dedicated service pages and city pages
- Content depth (estimated)
- What they are doing that the client is not

---

### Audit output

Write `audit-summary.md` in the client folder. Structure:

1. **Engagement stage**
2. **Snapshot — what they have going for them** (3–5 bullets)
3. **Top visibility gaps** — ranked by impact, one section per gap:
   - What it is
   - Evidence
   - Why it matters
   - What to fix
4. **Map ranking baseline** — current position by keyword, competitor table
5. **Silo gap table** — GBP categories and services vs. website page coverage
6. **Technical SEO issues** — grouped by severity
7. **NAP and citation issues** — table with priority levels
8. **Competitor summary**
9. **Quick wins** — fixes that can be done in 1–2 weeks
10. **Bigger opportunities** — 30–90 day build items
11. **Compliance and risk notes** — only when a real risk is present
12. **What is still needed** — data gaps that would materially improve the audit

---

## Stage 2: Intake and Scope Lock

### Run when: Audit is done, no `client-brief.md` exists yet.

Use the Client Brief Template at:
`C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Client Brief Template.md`

If an intake call transcript or notes exist in the folder, read them and extract answers directly. If no intake exists, generate an `intake-script.md` Leo can use on the call.

### Capture these fields:

| Area | Questions to answer |
|---|---|
| Money services | Which services generate the most revenue? Highest margin? |
| Growth services | What services do they want more leads for? |
| Services to avoid | What do they offer but not want to promote? |
| Service area | Which specific cities do they actually serve — confirmed, not just claimed? |
| Capacity | Can they handle more leads in each service? Are there capacity limits? |
| Preferred CTA | Call / form / text / WhatsApp / booking link? |
| Lead handling | Who answers? Is voicemail professional? Do they text back promptly? |
| Sales process | Estimate flow, consult, booking, CRM, follow-up cadence |
| Proof assets | Reviews, photos, licenses, before/after, certifications, awards |
| Ideal job | Minimum project size, preferred customer type |
| Urgency | Why are they looking for help now? What happens if nothing changes? |
| Budget and readiness | Monthly investment range, timeline, expectations |

### Compliance checkpoint

Run this only when a real risk is present. Triggers:
- Licensed trade (contractor, HVAC, plumber, electrician, etc.)
- Address or service area conflicts
- Name conflicts with another business
- Aggressive claims that need verification
- Client wants to advertise services in cities they may not actually serve

Checks:
- Business name matches GBP, website, and state filings
- License or certification claims verified (CSLB for California contractors: CSLB.ca.gov)
- All listed services are actually provided
- All targeted cities are actually served
- No guaranteed rankings, guaranteed leads, or false "near me" promises

Add a short compliance note inside `client-brief.md` or create a separate `compliance-notes.md` if the issues are significant.

### Output: `client-brief.md` in the client folder

---

## Stage 3: Strategy, Research, and Page Plan

### Run when: Audit and intake are complete. No page plan exists yet.

Use the Research Pack and Page Plan Templates at:
`C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Research Pack Template.md`
`C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Page Plan Template.md`

### Core decisions Leo must lock before drafting begins:

- Which services get pages first (money services + growth services)
- Which cities matter first (top 3 by revenue potential and realistic ranking ability)
- Which GBP categories and services need matching URLs built
- Which pages are Now / Next / Later / Skip
- What proof is available per priority page

### Page priority labels:

| Label | Meaning |
|---|---|
| Now | Highest revenue value, strongest intent, GBP-aligned, client can support and wants more leads |
| Next | Important but not part of the first sprint |
| Later | Worth building after first wins are live |
| Skip | Not supported, not wanted, too thin, or no local relevance |

### Research — required before drafting any Now page

Complete a Research Pack for each Now page before drafting begins.

For each priority page, collect:

1. **GBP silo check** — does the matching category/service URL already exist? What is missing?
2. **SERP intent** — what is Google rewarding for the target keyword in this city?
3. **Top result patterns** — what do the top 3 results have in common? What should not be copied blindly?
4. **People Also Ask gaps** — what questions are not being answered well?
5. **Competitor review language** — what exact phrases do customers use when describing this service in reviews?
6. **Client GBP gaps** — missing Q&A, missing photos, missing service descriptions that could inform page content
7. **Local language** — Reddit, local Facebook groups, or Nextdoor if available
8. **Proof inventory** — what reviews, photos, certifications, or local examples are available for this page?
9. **Internal link requirements** — what pages should this link to and receive links from?

Rule: Find the gap, not the consensus. Do not produce pages that repeat what the top results already say.

### Page plan output

Write `page-plan.md` in the client folder using the template structure. Include:

| Priority | Page type | Page name | Target keyword | City | GBP match | Research done | Slug | CTA | Trust asset needed | Status |
|---|---|---|---|---|---|---|---|---|---|---|

Page types:
- Homepage
- Category page (tied to GBP primary or secondary category)
- Service page (specific buyer-intent service)
- Location/city page
- Supporting article / FAQ
- Case study / project page

### Title tag patterns to follow:

- Category page: `[GBP Category] [City, CA] | [Brand]`
- Service page: `[Service] [City, CA] | [Brand]`
- Location page: `HVAC Services in [City, CA] | [Brand]` or service-specific variant
- Homepage: `[Primary Service] in [City, CA] | [Brand Name]`
- All titles under 60 characters

### Content architecture rules:

- Homepage mentions each secondary GBP category and links to the corresponding category page
- Each category page links to its relevant service pages
- Each service page links to related location pages and the contact/CTA page
- No orphaned pages — every page receives at least one internal link from a higher-level page
- No thin location pages — each must have unique proof (a local review, a job in that city, a local reference)

### Output: `research-pack-[page-name].md` per Now page + `page-plan.md`

---

## Stage 4: Content Production

### Run when: A page in the page plan is marked Now / drafting, and Leo requests a draft.

### Rules

- Start from the approved Research Pack. Do not draft without it.
- Use only verified facts from the client brief and audit. Do not invent addresses, team names, reviews, licenses, or statistics.
- Place trust signals near the top of every priority page: reviews, ratings, license number, awards, years in business, certifications, or association memberships. Do not bury proof below the fold.
- Use the customer's actual language from review mining where it fits naturally.
- CTA must appear above the fold and repeat at the bottom.
- No guaranteed rankings, no fabricated customer names, no exaggerated claims.
- Each location page needs unique local proof — a named city, a local review, a specific job in that ZIP code.
- Internal links must be included in the draft.

### Output per page:

- Meta title (under 60 characters)
- Meta description (under 155 characters)
- H1
- Page body with section structure: intro, services, why choose us, service area, proof/trust, FAQ, CTA
- FAQ section (3–5 questions from Research Pack gaps)
- Internal link targets (specific URLs)
- Image/photo needs flagged

Produce a separate `implementation-brief-[page-name].md` for handoff to the developer/VA with:
- URL slug
- Meta title and meta description
- Full H1/H2/H3 structure
- Complete body content
- Image filenames and alt text
- CTA type (phone / form / booking)
- Internal link targets
- Schema type: LocalBusiness / Service / FAQPage as applicable
- Sitemap: include
- Notes for developer/VA

---

## Stage 5: Launch QA and Indexing

### Run when: Pages are live and Leo asks for QA.

Use the Launch Checklist Template at:
`C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Launch Checklist Template.md`

### QA check per page:

| Check | Pass / Fail / Note |
|---|---|
| Page is live at correct URL | |
| URL is clean (no query strings, no /index.html) | |
| Meta title is present and under 60 characters | |
| Meta description is present and under 155 characters | |
| One clear H1 exists | |
| H2/H3 structure is logical | |
| Internal links are present | |
| Page is not orphaned (at least one inbound link from another page) | |
| Images have descriptive alt text | |
| Schema is added where applicable | |
| Page is in the XML sitemap | |
| Sitemap submitted in Google Search Console | |
| URL inspected in GSC | |
| Indexing requested for priority pages | |
| Index status tracked with date | |
| Mobile rendering confirmed | |
| Main CTA works | |

### Indexing escalation — if a priority page is not indexed after 4–6 weeks, check:

1. Thin or duplicate content
2. Weak internal links (page not linked from other pages)
3. Noindex tag or canonical conflict
4. Sitemap or crawl budget issue
5. Page lacks unique local proof or local relevance
6. Domain authority too low — may need more links pointing to the page

### Output: `qa-checklist.md` in the client folder

---

## Stage 6: Monthly Maintenance

### Run when: Client is in an active retainer.

Use the Monthly Tracker Template at:
`C:\Users\Leo\OneDrive\Docs\Business\DigitalTrack\Operations\Processes\Local SEO\Monthly Tracker Template.md`

### Default monthly actions:

| Area | Action |
|---|---|
| GBP posts | Publish 4+ posts per month — offers, job photos, reviews, seasonal updates |
| GBP photos | Upload recent job photos, team photos, or location photos |
| Reviews | Confirm review request process is active; respond to all new reviews within 48 hours |
| Citations | Verify NAP accuracy on Apple Maps, Bing, Yelp, and niche directories |
| Rankings | Pull keyword + city ranking report; flag significant changes |
| Content | Identify one page per month to improve with better proof, stronger content, or better links |
| Indexing | Confirm new pages are indexed; escalate non-indexed priority pages |
| Reporting | Short client update from Leo: what we did, what changed, what we recommend next |

### Output: Update `maintenance-log.md` monthly + produce `report-[YYYY-MM].md` for client reporting

---

## Templates — copy/paste ready

### Review request — SMS version

Hi [First Name], it's [Your Name] from [Company]. Thank you for letting us handle your [service] — glad it went well. If you have a minute, an honest Google review would mean a lot to us: [Google Review Link]

Optional prompts if they want help getting started:
- What service did we help with, and how did the process go?
- Was there anything about the communication or scheduling that stood out?
- What result or detail are you most happy with?

No script needed — just your honest experience in your own words. Thank you.

---

### Review request — email version

Subject: Quick favor — would you leave us a Google review?

Hi [First Name],

Thank you for choosing [Company] for your [service]. It was a pleasure working with you.

If you have 2 minutes, an honest review on Google helps other homeowners like you find us:
[Google Review Link]

A few optional prompts if they're helpful:
- What service did we complete and how did the process feel?
- How was communication and scheduling?
- What result or detail stood out?

Your honest words are what help us most. No obligation — but it really does make a difference.

Thanks again,
[Your Name]
[Company] | [Phone]

---

### GBP post templates (4-week repeating cycle)

**Week 1 — Job or project post:**
We just completed a [service] for a homeowner in [City]. [One sentence about the job or result.] If you're dealing with something similar, give us a call at [phone] — we're available [hours].

**Week 2 — Trust signal post:**
[Company] has been serving [City] and surrounding areas since [year]. We're [trust signals: Diamond Certified / BBB A+ / 4.9 on Google with X reviews]. When your [system] needs attention, we're ready. Call [phone] or request a quote at [website].

**Week 3 — Seasonal or timely post:**
[Seasonal tip relevant to the month — e.g., "Summer is here — when did you last service your AC?" or "Heating season is around the corner."]. Schedule your maintenance appointment now before our calendar fills up: [phone] or [website].

**Week 4 — Offer or Care Club / maintenance program post:**
Ask us about our [Care Club / maintenance membership / seasonal special]. [One sentence on what it includes.] Members get priority scheduling and discounts on repairs. Call [phone] or visit [website] to sign up.

---

## Silo Gap Table — blank template

Use this in the audit for the GBP silo check section:

| GBP Category | Dedicated URL exists | Title tag correct | Homepage mention | Homepage internal link | Services mapped | Category → service links | Action needed |
|---|---|---|---|---|---|---|---|
| [Primary category] | Yes / No | Yes / No | Yes / No | Yes / No | [list] | Yes / No | [fix] |
| [Secondary 1] | Yes / No | Yes / No | Yes / No | Yes / No | [list] | Yes / No | [fix] |
| [Secondary 2] | Yes / No | Yes / No | Yes / No | Yes / No | [list] | Yes / No | [fix] |

---

## Priority Action Plan format

Use P0 / P1 / P2 in the audit output for every recommended fix:

| Priority | Action | Why it matters | Expected impact | Effort | Exact next steps |
|---|---|---|---|---|---|
| P0 | [fix] | [reason] | [impact] | Low / Medium / High | [step-by-step] |
| P1 | [fix] | [reason] | [impact] | Low / Medium / High | [step-by-step] |
| P2 | [fix] | [reason] | [impact] | Low / Medium / High | [step-by-step] |

- **P0:** Do immediately. Actively hurting rankings or trust.
- **P1:** Do in the first sprint. High-value fix with clear upside.
- **P2:** Do after P0 and P1 are done. Worth doing but not urgent.

---

## 30 / 60 / 90 Day Plan format

Include this section at the end of the `audit-summary.md`:

**Days 1–30 (foundation):**
- [Quick wins from audit — NAP cleanup, H1 fixes, GBP phone, GBP posts, duplicate title fixes]

**Days 31–60 (build sprint 1):**
- [First set of Now pages from page plan — top 1–2 service + city combinations]
- [GBP silo gaps from the table that are missing category pages]

**Days 61–90 (build sprint 2):**
- [Next set of Now pages]
- [City page expansions]
- [First maintenance cycle — review request, citation updates, rank check]

---

## Output summary after any stage

After completing any stage, tell Leo:
- What files were produced (exact filenames and folder location)
- What is complete vs. what needs his input or approval
- Any flags, compliance risks, or data gaps
- The recommended next stage to run
