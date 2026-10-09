---
name: attribution-gap-check-tiktok-ads
description: Reconciles TikTok Ads Manager conversions with GA4, Shopify, CRM, or app analytics using a baseline-ratio method, separating click-through from view-through credit, attribution window and timezone differences, and real tracking drift (T07). Use when a TikTok media buyer or client says "TikTok says 200 sales, Shopify says 90", "GA4 does not show our TikTok conversions", "TikTok ROAS looks too good", "the gap got bigger this month", or "which number do we report to the client".
---

# Attribution Gap Check: TikTok Ads

## Use this skill when

TikTok-reported results and an independent source disagree, and someone wants to know whether the gap is normal, has moved, or hides a measurement problem. TikTok and independent tools count different things on different clocks, so a gap alone proves nothing. Change in the gap against a documented baseline is the signal this skill reads. Work from pasted exports; a TikTok for Business connector in Claude is optional.

Typical requests:

- "TikTok shows 210 purchases this month and Shopify attributes 95 to TikTok. Who is right?"
- "GA4 barely shows TikTok. Is the pixel broken?"
- "The client's finance team does not trust TikTok ROAS."
- "TikTok numbers jumped after we changed something, and orders did not."
- "Which source should drive budget decisions?"

Do not use this skill when:

- Primary events dropped while clicks held. Run `pixel-events-api-check-tiktok-ads` first (T10).
- No baseline period exists with stable settings. Collect one, or run `account-triage-tiktok-ads` to scope what can be judged.
- Question concerns TikTok Shop fees and margin. Run `gmv-max-profit-check-tiktok-ads`.
- A CPA movement needs a cause and both sources moved together. Run `cpa-spike-diagnosis-tiktok-ads`.

## Required input

Two sources, one definition, one clock. Without those, the output is `needs_data`.

From TikTok Ads Manager, a daily export for the baseline and current windows with columns as labelled in your export: Date, Campaign name, Optimization event, Cost, Conversions, Total purchase value or conversion value. If your reporting offers click-through and view-through conversion columns, include both.

From TikTok, also capture:

- Attribution settings screenshot for the event (click-through window, view-through window, as labelled in your account).
- Ad account timezone and currency.
- Change log of attribution setting edits, Events API launches, or event remapping.

From the independent source, the same dates:

- GA4: Date, Session source / medium or Session campaign, Key events (or Purchases), Purchase revenue. Start in Reports > Acquisition > Traffic acquisition or an Exploration, as labelled in your property. Note the reporting attribution model.
- Shopify or order system: order date, order ID count, total, financial status, and the UTM or referrer field the store records. Exclude test, cancelled, and POS orders unless the business counts them.
- CRM: lead created date, source field, qualified flag, qualified date.
- App analytics: install or in-app event date, media source, event name.

From the business: event definition on each side, timezone of each source, deduplication status of each source, conversion lag, and the baseline period they consider normal.

### Optional input

- Total backend orders or leads per day, regardless of source. It supports a share-of-total ratio when UTM tagging is unreliable.
- Spend split by objective or campaign type for both windows, to explain view-through mix shifts.
- Consent banner change dates and regions.

## Before analysis

1. Pick a baseline period the team agrees was normal: settings unchanged, no tracking launches, no major promotion that changed buyer behaviour. Use several full weeks so one odd week cannot set the ratio, and record the exact dates.
2. Check that UTM parameters on TikTok ads are present and consistent for both windows; a changed UTM template moves the independent side on its own.
3. For lead generation, agree which CRM stage counts and how long it takes to reach it, then extend the lag to match.
4. For app campaigns, confirm which measurement partner or app analytics source is the independent side and whether it deduplicates installs across channels.

## Analysis workflow

1. Write both definitions side by side: TikTok event name and what fires it; independent conversion and what counts it. Mark `needs_data` if one side is undefined.
2. Align the clock. Same dates, same timezone, same currency. Record whether each source dates a conversion by ad interaction or by conversion time, as stated in its own settings or documentation; if unknown, mark `needs_data` and prefer weekly windows so edge days matter less.
3. Align attribution. Record TikTok click-through and view-through windows, GA4 model, and Shopify or CRM source logic. GA4 and order systems cannot see a view without a click, so view-through credit only exists on the TikTok side.
4. Choose the ratio and keep it fixed: TikTok conversions divided by independent TikTok-attributed conversions, or TikTok conversions divided by total backend conversions when tagging is weak. State which one.
5. Compute the baseline ratio over the documented baseline period with settings unchanged, then the current ratio over a mature current window with lag days removed.
6. Compute relative movement: current ratio divided by baseline ratio, minus one. Apply T07: escalate when the ratio moves at least 20% in either direction after dates, timezone, event definition, and attribution setup match.
7. If click and view columns exist, recompute the ratio on click-through conversions only. A total ratio that crosses T07 while the click-only ratio stays inside it points at a view-through mix shift as the first explanation to test, ahead of tracking.
8. Check change log and spend mix for explanations: attribution window edits, Events API launch, consent change, UTM template change, checkout domain move, spend shift toward reach-oriented campaigns.
9. Assign a governing source per decision type and write it into the output, so the client knows which number answers which question.

## Decision rules

| Condition | Evidence | Verdict | Next step |
|---|---|---|---|
| Dates, timezone, definition, or attribution differ between windows or sources | `ads_export` + `analytics_export` | `needs_data` | Realign, then recompute; no comparison verdict |
| Ratio movement below 20% relative to baseline (T07) | both exports | `monitor` | Report gap as stable; keep baseline |
| Ratio up at least 20% (T07), click-only ratio stable | export with click/view split | `likely` view-through mix shift | Explain to client; no tracking escalation |
| Ratio up at least 20% (T07), Events API or event change in log | `change_log` + exports | `likely` double counting | Route to `pixel-events-api-check-tiktok-ads` |
| Ratio down at least 20% (T07), backend volume stable | exports + `shop_export` | `likely` TikTok signal loss | Route to `pixel-events-api-check-tiktok-ads`; `hold` budget cuts |
| Ratio down at least 20% (T07), UTM or redirect change in log | `change_log` | `possible` independent-side gain or loss | Check UTM template and landing redirects |
| Ratio moved, no explanation found after checks | all sources | `possible` | Escalate reconciliation with owner and date |
| No documented baseline | none | `needs_data` | Collect a stable baseline period |

Governing source by decision, as a house heuristic:

| Decision | Governing source | Reason |
|---|---|---|
| Creative or ad group comparison inside TikTok | TikTok Ads Manager | Same attribution rules across rows |
| Channel budget split, client revenue reporting | Shopify, CRM, or backend | Deduplicated across channels |
| Lead quality | CRM qualified stage | Platform leads include unqualified ones |

## Output format

```markdown
## Attribution Gap Check: [account], [baseline dates] vs [current dates], [timezone]

**Verdict:** [shared verdict label] because [strongest evidence]
**Ratio used:** [TikTok / independent TikTok-attributed] or [TikTok / total backend]

### Source definitions
| Source | Conversion definition | Timezone | Attribution | Deduplicated | Lag |
|---|---|---|---|---|---|

### Ratio table
| Window | TikTok conversions | Independent conversions | Ratio | Click-only ratio |
|---|---|---|---|---|
| Baseline | | | | |
| Current | | | | |
Relative change: [x%] | T07: [met / not met / needs_data]

### Explanations checked
- [setting edit / Events API / consent / UTM / mix shift]: [found or not found, evidence tag]

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Which number answers which question
- [decision]: [source]

### Data gaps
- [missing item]: blocks [conclusion]
```

## Practical example

Illustrative numbers for a fictional brand, not a benchmark. Baseline (four weeks, settings unchanged): TikTok reports 420 purchases, Shopify attributes 300 orders to TikTok by UTM. Baseline ratio 1.40. Current week: TikTok 118, Shopify 64. Current ratio 1.84, a 31.7% rise. T07 is met on totals.

Dates, timezone, and purchase definition match; attribution settings did not change. Export offers a click and view split. Baseline: 344 click-through and 76 view-through. Current: 78 click-through and 40 view-through. Click-only ratio moves from 1.15 to 1.22, a 6.3% rise, inside T07. Spend data shows a reach-oriented campaign launched this week.

Output: gap growth is `likely` a view-through mix shift, severity low, impact `client_trust`. No pixel escalation. Client note explains that TikTok credits views the store cannot see, and that budget decisions keep using Shopify-attributed orders. Baseline stays; reach campaign spend gets its own ratio line next week.

## Common misreads

- Treating any gap as a tracking bug. A stable gap is expected; only movement against baseline (T07) escalates.
- Comparing TikTok totals with GA4 last-click TikTok sessions and forgetting view-through.
- Mixing an ad account in one timezone with a store in another, which shifts late-night orders across dates.
- Rebuilding the baseline after a setting change without saying so, which hides the change.
- Counting cancelled, test, or refunded orders on the store side but not on the TikTok side, or the reverse.
- Reading a GA4 drop after a consent or UTM change as a TikTok performance drop.
- Comparing platform leads with CRM qualified leads without lag; qualified status arrives later.

## Route to next

- Ratio fell and TikTok events dropped against clicks: `pixel-events-api-check-tiktok-ads` (T10).
- Ratio stable, CPA up on both sides: `cpa-spike-diagnosis-tiktok-ads` (T04).
- Shop orders and fees in question: `gmv-max-profit-check-tiktok-ads` (T09).
- Client-facing explanation of the gap: `weekly-client-report-tiktok-ads`, with the governing-source table attached.

## Guardrails

- Do not compare sources whose dates, timezone, definition, or attribution setup do not match; return `needs_data`.
- Do not call one source correct and the other wrong; assign each to the decision it governs.
- Do not change attribution settings, UTM templates, or tracking. Output stops at a recommendation.
- Do not present TikTok view-through conversions as incremental sales without a controlled test.
- Do not reset a baseline silently; record the reason and date.
