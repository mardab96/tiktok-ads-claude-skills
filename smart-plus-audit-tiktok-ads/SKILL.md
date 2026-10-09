---
name: smart-plus-audit-tiktok-ads
description: Audits a TikTok Smart+ campaign by mapping what Smart+ automates against what the media buyer still controls (creative supply, audience exclusions, conversion event, budget, bidding), then ranks the risks. Use when someone types "audit our Smart+ campaign", "what does Smart+ actually control", "Smart+ vs manual", "Smart+ spend is up but results are flat", or "can we trust Smart+ with this budget".
---

# Smart+ Audit

## Use this skill when

A Smart+ campaign is live or about to launch and the buyer needs a clear line between what TikTok automates and what still needs a human. Smart+ hides many knobs, so an audit starts from what is visible in screenshots and reporting, not from what the automation is assumed to do.

Common requests:

- "Audit our Smart+ Web campaign before we move more budget into it."
- "What does Smart+ decide, and what is still on us?"
- "Smart+ is spending but CPA is flat. Where do we look?"
- "Client asks if Smart+ beats our manual setup."
- "Which inputs should we feed Smart+ so it does not drift?"

Do not use this skill for these jobs:

- Tracking health or missing events: run `pixel-events-api-check-tiktok-ads` first.
- One ad losing steam: `creative-fatigue-detector-tiktok-ads`.
- Where impressions landed: `placement-review-tiktok-ads`.
- TikTok Shop GMV Max profit: `gmv-max-profit-check-tiktok-ads`.
- Unfamiliar account with no map: `account-triage-tiktok-ads`.

## Required input

Work from pasted exports and screenshots. Claude's TikTok for Business MCP connector may supply the same tables, but this skill never requires it.

### Required

- Screenshots of the Smart+ setup or edit pages: objective, destination, optimization goal, bidding and optimization, budget, audience (location, language, exclusions), creative section including any AI creative toggles, catalog section if present, placement text.
- Results export at campaign and ad level with these columns where available: `date`, `campaign`, `ad group`, `ad`, `spend`, `impressions`, `clicks`, `CTR`, `CPM`, `reported conversions`, `CPA`, `conversion value`, `frequency`.
- Primary event name and what it counts, plus an Events Manager capture (overview and diagnostics).
- Dated change log.
- Goal, target CPA or value target, currency, timezone, attribution setting, conversion lag.

### Optional

- A comparable manual campaign export for the same dates.
- Result of any split test the buyer ran.
- Asset list with source per asset (UGC, brand studio, Spark, AI generated).
- Independent order or lead report for the same dates.

Export route: campaign table or **Reporting** for the tables, screenshots for settings pages. See `../tiktok-ads-shared/references/getting-your-data.md`. Label names move between accounts, so write "as labelled in your Ads Manager" for any label you could not confirm.

## Before analysis

1. Confirm the campaign is Smart+ from a screenshot of the Smart+ toggle or the campaign type label. Record the flavor shown (Web, App, Lead Generation, Traffic, Catalog).
2. Confirm the primary event and optimization goal. No event definition means `needs_data` and no performance claim.
3. Fix two comparable mature windows after the conversion lag (see T04 for the floor of 10 reported conversions per window).
4. Read the change log for edits inside the first learning window. If edits stack up, run `learning-phase-guard-tiktok-ads` before judging results (T05).
5. Note features that depend on market or advertiser, such as gender targeting, multilingual tooling, and some placements. Treat them as "as labelled in your Ads Manager".

## Analysis workflow

1. Inventory every visible setting and tag it `screenshot`. Anything not visible is `needs_data`, never assumed.
2. Fill the boundary map in Decision rules, one row per input, naming the manual owner.
3. Audit creative supply: asset count, format mix, source mix, age, Spark versus non-Spark mix, and which ads actually received spend. Smart+ can shift budget and pause weak creatives itself, so uneven spend is expected and is not proof of quality.
4. Audit exclusions: audience exclusions applied (existing customers, converters, employees where relevant), geography and language scope, catalog scope if any.
5. Audit the event: does the optimization goal match the business outcome, is value passed when value optimization is used, and do diagnostics show a T10 pattern.
6. Audit budget and bidding against the strategy label shown on screen. Route label questions to `bid-strategy-check-tiktok-ads` and budget moves to `budget-scaling-planner-tiktok-ads`.
7. Read delivery outcomes: spend share by ad, CPA by ad on mature rows, trend against the manual comparison if supplied. Flag reporting you cannot split (for example placement or audience detail that the campaign type does not expose).
8. Write the review cadence and the approval queue. Live changes stop at `approval_needed`.

## Decision rules

### Boundary map

| Input | What Smart+ automates (per TikTok help pages) | What stays with the buyer | Audit check |
|---|---|---|---|
| Campaign and audience targeting | Targeting and audience expansion inside the limits you set | Location, language, gender where offered, audience exclusions | Exclusions present, scope matches the market served |
| Optimization | Delivery optimization toward the chosen goal | Choice of optimization goal and primary event | Event matches business outcome, diagnostics clean (T10) |
| Creative combinations | Combines assets, CTAs, and format variations, detects ad group fatigue, auto-refreshes | Supply of source assets, claims, brand rules, music and licensing | Count, variety, age, claim approval, AI creative toggles |
| Budget between creatives | May shift budget to stronger creatives and pause weak ones | Campaign budget and schedule | Spend share by ad, no manual pause fights |
| Placements | Automatic selection in Smart+ Web as documented in March 2026 | Choosing a non-Smart+ campaign if exact placement control is required | Placement report if the account exposes one |
| Bidding | Delivers inside the strategy you pick | Strategy label, target value, budget level | Label confirmed by screenshot, learning state (T05) |
| Paid and organic link | May add an organic anchor link to select posts | Whether organic posts are brand safe and on offer | Check posts that carry the link |
| Measurement | Nothing automated | Pixel, Events API, attribution setting, split test design | T10, T07, test hygiene |

### Verdicts

| Condition | Verdict | Next step |
|---|---|---|
| Primary event falls at least 30% while clicks stay within 10% of baseline over comparable seven-day windows (T10) | `hold` on every optimization claim | Run `pixel-events-api-check-tiktok-ads` |
| Campaign or ad group still learning-sensitive: under about 25 results or 7 days since entry (T05) | `hold` on edits, `monitor` on results | Run `learning-phase-guard-tiktok-ads` |
| CPA at least 30% above baseline with at least 10 conversions per window (T04) | `likely` problem, cause unknown | Run `cpa-spike-diagnosis-tiktok-ads` |
| One ad holds a clear majority of spend and its CTR is sliding (T01 floors apply) | `possible` supply problem | Run `creative-fatigue-detector-tiktok-ads`, plan new assets |
| Creative supply visibly thin: few assets, one source, one format | `likely` risk, `approval_needed` for new assets | Hand to `ugc-brief-writer-tiktok-ads` |
| Exclusions missing for existing customers or converters | `confirmed` gap if the screenshot shows none | `approval_needed` to add exclusions |
| Results look good, no controlled comparison exists | `possible` Smart+ benefit only | Design a split test, claim nothing yet |
| Settings or event screenshots missing | `needs_data` | Ask for the exact screen |

Confidence rule: `confirmed` applies only to what a screenshot or export shows. Statements about how the automation works are `hypothesis` unless a TikTok page is cited with its date.

## Output format

Fill this template. Keep it to one page for the buyer plus the table.

```markdown
## Smart+ audit: [campaign], [dates], [currency], [timezone]
Goal: [target]. Primary event: [name]. Lag: [days]. Attribution: [setting].
Smart+ flavor seen in screenshot: [Web | App | Lead Gen | Traffic | Catalog | needs_data]

### Boundary map
| Input | Automation shown | Manual owner | Evidence | Risk | Next review |
|---|---|---|---|---|---|

### Findings
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Creative supply snapshot
Assets: [n] | Formats: [list] | Sources: [list] | Spark mix: [yes/no] | Spend share top ad: [%]

### Review cadence
[who checks what, on which date, after the lag]

### Approval queue
[each live change with named approver, nothing applied]

### Data gaps
[missing screen or export, and the verdict it would firm up]
```

## Practical example

Illustrative numbers only. A Smart+ Web campaign for a home-fitness brand, target CPA 40 USD, 7 days of conversion lag, 28 days of data.

Screenshots show the Conversion goal on a Purchase event, a budget set, location and language chosen, no audience exclusion, and five video assets from one UGC creator. One ad has 61% of spend, while CTR slid from 1.1% to 0.8% across two mature weeks. Reported CPA sits at 44 USD, above target but under the T04 trigger.

Findings: the event is `confirmed` as Purchase (screenshot). An exclusion gap is `confirmed`, medium severity, spend impact. Thin creative supply from a single source is `likely`, medium, conversion impact. A top-ad slide is `possible` fatigue, because frequency was not exported and the T01 pairing cannot be checked. Whether Smart+ beats the old manual campaign is `possible` at best, since the manual campaign ran a different event and budget.

Approval queue: add a customer exclusion, brief three new assets from other creators, export frequency for T01, and run a split test with matched event and budget before anyone reports lift.

## Common failure modes

- Crediting Smart+ for results the Pixel or Events API reports. A tracking change moves reported conversions with no delivery change.
- Reading ad-level CPA as creative quality when Smart+ itself reallocated budget and paused ads.
- Comparing Smart+ with a manual campaign that has a different event, budget, or date range.
- Assuming "automated audience" means exclusions are unnecessary.
- Assuming placement control exists inside Smart+ Web. TikTok's March 2026 page says manual placement selection is not supported there.
- Letting AI generated or auto-refreshed creative carry claims nobody approved. Brand safety and claims are manual decisions.
- Calling the campaign out of learning because spend is steady. Use T05 and the status on screen.
- Presenting platform-reported conversions or value as profit.

## Route to next

Event problems: `pixel-events-api-check-tiktok-ads`. CPA movement: `cpa-spike-diagnosis-tiktok-ads`. Edits during learning: `learning-phase-guard-tiktok-ads`. Strategy label doubts: `bid-strategy-check-tiktok-ads`. Raising budget: `budget-scaling-planner-tiktok-ads`. Spark permissions: `spark-vs-brand-ad-split-tiktok-ads`. Reported versus independent numbers: `attribution-gap-check-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not mark a setting `confirmed` unless a screenshot or export shows it.
- Do not describe how Smart+ works beyond what a dated TikTok help page or the supplied screens state; label the rest `hypothesis`.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim Smart+ lift before a controlled comparison with matched event, budget, and dates exists.
- Do not read ad-level CPA as creative quality without noting that Smart+ may have shifted budget between ads.
