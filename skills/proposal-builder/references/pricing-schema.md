# Pricing Schema

Pricing is driven by a single JSON file (`src/data/proposalPricing.json`) plus
a small pure math helper. Per-prospect: change the numbers and selected items,
not the structure.

## Top-level keys

- `meta` — prospect_name, language ("es"), route, currency ("USD"), pricing_status_note
- `digitaltrack_contact` — company_name, email, phone, website, contact_url, consultation_url **[FIXED]**
- `page_copy` — headings + notes (pricing/builder headings, planning_note, agreement_note, custom_note)
- `calculation_rules` — see Math rules below
- `fixed_packages[]`, `preset_bundles[]`, `line_item_rules`, `line_items[]`
- `proposal_context` — conversation_summary, pain_points, opportunities (mirrors the findings sections)

## fixed_packages[]

Client-safe, fixed annual prices. Each:
`{ id, label, badge, recommended, pricing_mode: "fixed", annual_price,
short_description, included_ui_items[], notes?[] }`.

Recommended anchor package may add `official_payment_option`:
`{ headline, down_payment, remaining_total, monthly_payment_months_1_to_10,
monthly_payment_month_11, paid_in_full }`.

**Canonical packages (do not change prices without Leo's instruction):**
- **Starter** — $1,500/año fixed · GBP + directorio básico + soporte mensual
- **Local Visibility Foundation** *(Más recomendada)* — $4,200/año fixed
  - Pago de contado: $3,780 (10% desc.)
  - Enganche 20%: $840 + 11 mensualidades ~$305

## preset_bundles[]

Tabs in the calculator. Types:
- `fixed_package` — references a `package_id`
- `line_item_bundle` — has `selected_line_item_ids[]`, `bundle_discount_override`,
  and `precomputed_totals` `{ yearly_subtotal, bundle_discount, yearly_total,
  paid_in_full, down_payment, monthly_payment }`
- `custom` — free selection (Personalizada)

Each preset has a `rationale`. Canonical set: Starter, Recomendada, Personalizada.

## line_items[] and line_item_rules

Each item: `{ id, category, label, annual_price, short_description_es, price_status }`.

`line_item_rules`:
- `single_select_categories`: Branding, Website, Search Engine Optimization,
  Local Business Listings (pick one tier per category)
- `multi_select_categories`: Operations, Engagement, Advertising, Social

Modular rows are **planning-only** — for conversation/scoping, not a committed
quote until final scope is confirmed.

## Math rules (`calculation_rules` + helper)

- Annual agreement
- `paid_in_full_discount_pct`: 10 — paying the full year up front gets −10%
- `standard_down_payment_pct`: 20 — enganche is 20% of yearly total
- `remaining_installments`: 11

Helper (pure):
```
yearlyTotal   = max(0, yearlySubtotal - bundleDiscount)
paidInFull    = yearlyTotal * (1 - 0.10)
downPayment   = yearlyTotal * 0.20
monthly       = (yearlyTotal - downPayment) / 11
```

Display fields: Subtotal anual, Descuento de paquete, Total anual, Pago de
contado, Enganche, Pago mensual estimado. Format as USD with 2 decimals.
