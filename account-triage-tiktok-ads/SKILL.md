---
name: account-triage-tiktok-ads
description: Runs an ordered, layer-by-layer triage of an unfamiliar TikTok Ads account (tracking, structure, learning, creative, bidding, landing page) and hands the first blocker to one named sibling skill. Use when the user inherits a TikTok account, onboards a client, asks where to start, says TikTok results dropped with no known cause, asks whether an account is ready to scale, or says "audit this TikTok account" without naming a problem.
---

# Account Triage - TikTok Ads

## Use this skill when

Users of this skill need orientation, not a deep dive. Triage decides what to check first, what can wait, and which sibling skill owns the first blocker. It sequences problems; it does not solve them.

Common requests:

- "We just took over this TikTok account. Where do I start?"
- "Audit this account." (no narrower scope given)
- "TikTok results dropped last week and nobody knows why."
- "Is this account ready to scale or does it need fixing first?"
- "Client onboarding: what do I look at in the first hour?"

### When not to use

If the user already named the problem, run that skill instead: CPA jumped -> `cpa-spike-diagnosis-tiktok-ads`; spend with no results -> `wasted-spend-finder-tiktok-ads`; tracking doubt -> `pixel-events-api-check-tiktok-ads`; TikTok and Shopify disagree -> `attribution-gap-check-tiktok-ads`; a weekly client write-up -> `weekly-client-report-tiktok-ads`.

## Required input

Context (ask for it; never assume it):

- Business goal and target (CPA, ROAS, lead volume, or Shop revenue), primary event, currency, timezone.
- Attribution setting and conversion lag in days. Without a lag, no recent row counts as mature.
- Vertical: ecommerce, TikTok Shop, lead generation, or app. It changes which evidence counts.
- Date range: 30 days minimum; 14 distinct daily dates per ad if creative is in scope.

Exports, in priority order. Column labels vary by account and interface, so keep names as labelled in your Ads Manager and map them in the first reply.

1. **Ads Manager Reporting, ad level, daily breakdown.** Columns: `date`, `campaign name`, `ad group name`, `ad name`, `ad id`, `objective`, `spend`, `impressions`, `clicks`, `CTR`, `CPM`, `CPC`, `reported conversions`, `CPA`, `conversion value`, `frequency`, plus video-view columns if available. Keep the date range in the filename.
2. **Campaign table screenshot or export.** Campaign type (standard, Smart+, GMV Max, Search Ads Campaign), status, budget, bidding strategy as labelled, optimization event, placements.
3. **Events Manager captures.** Overview, event list, diagnostics, connection or matching status, test-event view. Screenshots are enough.
4. **Change history or an operator-written dated change log.**
5. **Independent report for the same dates** (Shopify, GA4, CRM, app analytics) with its conversion definition and timezone.

Optional: creative previews, a mobile landing page screenshot, TikTok Shop Seller Center exports, a prior agency handover note. A TikTok for Business MCP connector may supply tables, but every layer below works from pasted files.

## Before analysis

1. Write the goal you are triaging against at the top of the output. If you assumed it, label it `hypothesis`.
2. Reconcile spend: ad-level total must match the campaign table total for the same dates. A gap means a missing level, a currency mismatch, or a date mismatch. Record it as `needs_data` and do not proceed on inflated or deflated totals.
3. Split the export by objective before comparing CPA or value. Reach, video-view, traffic, and conversion campaigns do not share a CPA.
4. Exclude rows inside the conversion lag from any performance judgement.
5. Read the change log before blaming the market. An unexplained drop usually has a dated edit nearby; a chart alone is not a change event.

## Analysis workflow

Work in this order. A failed layer lowers the confidence of every layer below it. Name the first failed layer as the blocker, route it, and list the rest as a queue.

1. **Tracking.** Confirm the primary event is named and firing. Compare the primary event trend against clicks over comparable seven-day windows: event down at least 30% while clicks stay within 10% is a tracking-shaped signal (T10). Compare TikTok conversions to the independent source; a ratio that moved at least 20% against a documented baseline, after dates, timezone, and event definition match, needs reconciliation (T07). Check diagnostics for browser and server events counted twice. Hand off: `pixel-events-api-check-tiktok-ads`, then `attribution-gap-check-tiktok-ads`.
2. **Structure.** Map campaigns by type, objective, budget, and ad-group count. Flag budget split across many ad groups when each cannot approach about 25 results in 7 days (T05). Flag overlapping audiences competing in the same auctions, stacked campaign types chasing one product, and Smart+ or GMV Max campaigns whose inputs are not visible in the export. Hand off: `smart-plus-audit-tiktok-ads`, `gmv-max-profit-check-tiktok-ads`, `search-ads-keyword-review-tiktok-ads`, or `placement-review-tiktok-ads` by campaign type.
3. **Learning.** Mark every conversions ad group as learning-sensitive until about 25 results or 7 days since entry (T05). Cross-check the change log: an edit inside that window means `hold` on further live changes and on any "this does not work" verdict. Hand off: `learning-phase-guard-tiktok-ads`.
4. **Creative.** Count active ads per ad group and the share of spend on the top ad. Run `creative-fatigue-detector-tiktok-ads` when an ad has 14 distinct dates and both seven-day windows reach 3,000 impressions (T01). Run `hook-rate-scorer-tiktok-ads` when 2-second view columns exist and comparable ads have at least 3,000 impressions (T02). A single ad carrying nearly all spend is a structural creative risk even when it performs.
5. **Bidding.** Record the strategy as shown in the account: Maximum Results or Target Cost per Result. If the export or user says Lowest Cost, Cost Cap, Bid Cap, or ROAS, ask for a screenshot before mapping it. Compare target CPA to actual CPA, and daily budget to target CPA: an ad group whose budget affords fewer than about 3.6 results a day cannot reach 25 results in 7 days, by arithmetic (25 divided by 7). Hand off: `bid-strategy-check-tiktok-ads`. If current CPA is at least 30% above a baseline with 10 or more reported conversions in each window, add `cpa-spike-diagnosis-tiktok-ads` (T04).
6. **Landing page.** Compare the ad promise (first line, offer, price) with the mobile page. A mismatch can masquerade as a CPA problem. Hand off: `landing-page-match-tiktok-ads`.
7. **Waste and headroom.** Only after layers 1 to 3 pass: scan for mature rows that spent at least 1.5 times target CPA with zero conversions (T03) via `wasted-spend-finder-tiktok-ads`, and route a scale question to `budget-scaling-planner-tiktok-ads` (T06).

## Decision rules

Thresholds are decision aids from `../tiktok-ads-shared/references/thresholds.md`, not performance promises. Cite the T-id beside every number. Tags and verdict labels come from `../tiktok-ads-shared/references/output-standard.md`.

| Condition | Verdict | Next step |
|---|---|---|
| Primary event undefined, diagnostics unseen, or conversion definition missing | `needs_data` | Pixel and Events API Check; every layer below stays `hold` |
| Event down at least 30% with clicks within 10% (T10) | `likely` tracking issue, severity `high` | `pixel-events-api-check-tiktok-ads` |
| TikTok-to-independent ratio moved at least 20% from documented baseline (T07) | `possible` until sources match | `attribution-gap-check-tiktok-ads` |
| Ad group inside about 25 results or 7 days of entry (T05) | `hold` on live changes | `learning-phase-guard-tiktok-ads` |
| Fatigue-shaped candidate (T01) or weak 2-second view rate (T02) | `possible` | Creative Fatigue Detector or Hook Rate Scorer |
| CPA at least 30% above baseline, 10 or more conversions per window (T04) | `confirmed` as a movement, cause `needs_data` | `cpa-spike-diagnosis-tiktok-ads` |
| Layers 1 to 3 clear, no named blocker above | `monitor` | Hand scale or waste questions to the owning skill as `approval_needed` |

First blocker = the lowest-numbered layer whose verdict is not `monitor`. Name exactly one sibling for it. A missing goal produces `needs_data` for the whole triage.

### What a pass looks like, by layer

| Layer | Pass | Fail |
|---|---|---|
| 1 Tracking | Primary event named, diagnostics show a healthy connection, event trend follows click trend, independent count within the documented baseline ratio | Event undefined, event falls while clicks hold (T10), ratio drifted from baseline (T07), duplicate events |
| 2 Structure | One objective per comparison, ad groups large enough to approach about 25 results (T05), campaign types have a stated job | Budget fragmented, overlapping audiences, unknown Smart+ or GMV Max inputs |
| 3 Learning | Ad groups past about 25 results or 7 days (T05), no edit inside the window | Recent entry or edit, results still below the evidence mark |
| 4 Creative | Several live ads per ad group, spend not concentrated on one ad, no unreviewed T01 or T02 flag | One ad holds nearly all spend, fatigue candidate, weak 2-second view rate |
| 5 Bidding | Strategy label verified, target CPA reachable on the daily budget | Unverified label, budget below the arithmetic floor for results |
| 6 Landing | Mobile page repeats the ad promise, offer, and price | Different offer, slow or confusing first screen, wrong product |
| 7 Waste | No mature zero-result row at 1.5 times target CPA (T03) | Mature row with spend and no results |

Layers 2 and 3 read settings and counts, not CPA, so they run even when layer 1 fails. Layers 4 to 7 that lean on reported conversions wait for layer 1.

### Vertical adjustments

- Ecommerce and TikTok Shop: a scale or profit claim needs refunds, fees, COGS, and shipping evidence (T09); route to `gmv-max-profit-check-tiktok-ads`.
- Lead generation: reported leads are not qualified leads; ask for CRM outcomes and use a longer lag.
- App: ask for the in-app event and release history; install volume alone does not satisfy layer 1.

## Output format

Keep triage short. Output that reads like a full audit defeats its purpose.

````markdown
### Goal and context
Goal: [target] | Primary event: [..] | Attribution: [..] | Lag: [n] days | Window: [dates] [evidence tag]

### First-read board
| Layer | Evidence | Verdict | Owner skill | Next input |
|---|---|---|---|---|
| 1 Tracking | ... | `...` | pixel-events-api-check-tiktok-ads | ... |
(one row per layer 1-7)

### First blocker
[layer] -> [one sibling skill] because [evidence]. Queue: [remaining layers in order].

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps
[missing item] -> [verdict it prevented]

### Approval needed
[live action] -> [named human owner]. Nothing here was changed in the account.
````

## Practical example

Illustrative numbers only. An agency inherits an ecommerce account: 30 days, 8,400 spend, 6 campaigns, stated goal CPA 35, lag 7 days, attribution as shown in the account.

- Reconcile: ad-level spend 8,400 equals campaign table. Pass.
- Layer 1: the purchase event has 5 days of flat clicks (about 2,100 a day) while reported purchases fell from 38 to 21 a day, a 45% drop; the Shopify order count did not fall. Clicks held within 10%, event down over 30% (T10), so tracking is `likely` the blocker, severity `high`, business impact `measurement`. Diagnostics screenshot is missing: `needs_data` for the cause.
- Layers 2 and 3: 14 ad groups in one campaign at roughly 3 results a day each. Structure `possible` fragmentation; learning `hold` because two ad groups were edited 3 days ago.
- Layer 4 onward: not judged. Reported CPA is untrustworthy until layer 1 clears.

Triage output: first blocker is Tracking, owner `pixel-events-api-check-tiktok-ads`, queue is `attribution-gap-check-tiktok-ads`, `learning-phase-guard-tiktok-ads`, `smart-plus-audit-tiktok-ads`. Deferred on purpose: the client's question "why is CPA up". Reported CPA is not trustworthy yet, so answering it now would hand the client an invented number.

## Common failure modes

- Judging CPA from rows inside the conversion lag; recent days look worse only because results have not arrived.
- Comparing a reach or video-view campaign's cost per result with a purchase campaign.
- Calling a Smart+ or GMV Max campaign weak from ad-group tables that do not describe how it delivers; ask for screenshots instead.
- Reading a frequency rise as fatigue before audience, budget, and change log are checked.
- Treating a platform-reported conversion as revenue or profit.
- Reading older bid labels such as Cost Cap as if they were current options.

## Guardrails

- Do not issue a performance verdict on top of unverified tracking. A tracking-shaped signal outranks every layer below it.
- Do not present triage as an audit. List the sequence and stop at the first blocker plus a queue.
- Do not scale, pause, rebid, or restructure anything. Output stops at an approval-ready action for a named human.
- Do not call tracking broken from CPA alone; require event and diagnostics evidence.
- Do not hide missing dates, lag, attribution setting, or conversion definition; mark each `needs_data`.
- Do not treat platform-reported conversions or GMV as profit without a supplied cost stack.
- Do not map retired or historical bid labels to current options without a screenshot.
- Do not name more than one owner skill for the first blocker.
