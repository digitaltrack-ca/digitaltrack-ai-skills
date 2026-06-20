---
name: proposal-builder
description: Build or update a DigitalTrack sales proposal page for any prospect. Triggers on "build a proposal", "propuesta", "new prospect proposal", "sales proposal page", "add proposal to [project]". Collects prospect data, assembles the 9-section structure, and sends the full prompt to the correct Lovable project.
triggers:
  - "build a proposal"
  - "propuesta"
  - "new prospect proposal"
  - "sales proposal page"
  - "add proposal"
  - "proposal page"
  - "proposal for"
---

# Proposal Builder

Build an interactive, single-scroll Spanish sales proposal in the DigitalTrack voice. The **content and narrative are the asset** — reuse them. The **visual design is flexible** and may be reinvented each time, as long as the section order, the bilingual/honest tone, and the "no inflated promises" framing stay intact.

The canonical reference implementation lives in the Hair Day Growth Lovable project (`bfe1d383-2ef0-4f6a-81b8-5b2252b2dcc7`) at route `/propuesta` — source in `src/components/proposal/*`.

Section copy templates live in `references/section-copy.md`. Pricing schema and math rules live in `references/pricing-schema.md`.

---

## Step-by-step workflow

### 1. Identify the target Lovable project

Check if the prospect already has a Lovable presentation project. If yes, add `/propuesta` as a new route in that project. If no, create a new project first.

Known prospect project IDs (update as new projects are created):

| Prospect | Lovable Project ID |
|---|---|
| JD Remodel Services | `eb27d094-8859-4358-8808-abb0a26ed49c` |
| Hair Day Beauty Salon (canonical) | `bfe1d383-2ef0-4f6a-81b8-5b2252b2dcc7` |

### 2. Collect per-prospect inputs

Ask Leo for whatever is missing:

1. **Identity** — business name, owner name, address, phone, license (if any), meeting date
2. **Conversación (4 cards)** — shared read of the moment: what's already working + what's holding them back
3. **Bien vs Frena** — strengths list + friction/pain list (2 columns)
4. **Prioridades Fase 1** — 4 ordered steps with short rationale each
5. **Pricing** — which fixed packages apply + any custom scope

### 3. Assemble the Lovable prompt

Use the section flow below and the copy templates in `references/section-copy.md`. Fill placeholders with prospect data. Mark fixed sections clearly so the Lovable agent doesn't change them.

Reference the `proposal-builder` workspace skill in the prompt (`Use the proposal-builder workspace skill`).

### 4. Send via Lovable MCP

Call `mcp__lovable__send_message` with `wait: false` (the build takes 2–4 minutes). Report the message_id and preview URL to Leo.

### 5. Add "VER PROPUESTA →" to the presentation nav

If the project has a sticky presentation nav, add a CTA button top-right linking to `/propuesta`. Match the Hair Day nav style (cyan accent button).

---

## Section flow (the spine — keep this order)

```
01 Hero            — promise + meeting reference + two CTAs
02 Conversación    — shared read of the current moment (4 cards)
03 Bien vs Frena   — strengths vs friction (2 columns)
04 Google + IA     — how Google/AI surface businesses [FIXED]
05 Prioridades     — Fase 1 ordered roadmap (4 steps)
06 Nosotros        — DigitalTrack: CRECE values + CRECER process [FIXED]
07 Opciones        — fixed packages + custom card
08 Calculadora     — interactive presets + modular builder
09 Cierre          — next-step CTA + contact block
```

## Fixed — do NOT change per prospect

- DigitalTrack brand tokens, logo, and contact block
- CRECE values and the CRECER process (Section 06 Nosotros)
- The Google + IA discovery explainer (Section 04) — only change the city reference
- Pricing math rules: annual agreement, 10% paid-in-full discount, 20% down payment, 11 installments

## Pricing packages (canonical)

- **Starter** — $1,500/año
- **Local Visibility Foundation** *(anchor / más recomendada)* — $4,200/año
  - Pago de contado: $3,780 (10% desc.)
  - Enganche 20%: $840 + 11 mensualidades ~$305

Per-prospect: adjust which packages to show and any custom scope items. Never change the fixed package prices without Leo's explicit instruction.

---

## Design rules

- Route: `src/routes/propuesta.tsx`
- Sticky scroll-spy section nav (IntersectionObserver), driven by `{ id, label }` array
- DigitalTrack design tokens: `dt-navy` / `dt-cyan` / `dt-gray` / `dt-surface` (or equivalent CSS vars already in the project)
- Reuse logo asset already in `src/assets/`
- All copy in Spanish; tone: warm, honest, direct — no inflated promises, no "posición #1" guarantees
