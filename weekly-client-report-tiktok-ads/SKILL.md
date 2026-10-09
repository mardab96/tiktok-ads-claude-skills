---
name: weekly-client-report-tiktok-ads
description: Writes the weekly TikTok Ads client report as a plain-language narrative, a scorecard against the client goal, and next-week decisions with owners and approvals, after an integrity check on tracking, lag, and learning status (T04, T05, T07, T10). Use when an agency or freelance TikTok media buyer says "write the weekly TikTok report", "client update is due", "explain this week's TikTok results to the client", "what do we tell the client about CPA going up", or "set up a repeatable TikTok report format".
---

# Weekly Client Report: TikTok Ads

## Use this skill when

An agency owes a client a weekly update that a non-specialist can read in two minutes and act on. Report job: say whether TikTok is on track against the client's goal, explain what moved in words the client uses, and list the decisions for next week with who owns each one. Investigation belongs to specialist skills; this report routes to them. Work from pasted exports; a TikTok for Business connector in Claude is optional.

Typical requests:

- "Weekly TikTok report for the client, same format as last week."
- "CPA went up. How do I explain it without panicking them?"
- "Turn this export into a client email."
- "We need the client to approve new creators this week. Build it into the report."
- "Monthly roll-up from the last four weekly reports."

Do not use this skill when:

- A single problem needs diagnosis. Run the owner: `cpa-spike-diagnosis-tiktok-ads` (T04), `attribution-gap-check-tiktok-ads` (T07), `pixel-events-api-check-tiktok-ads` (T10), `creative-fatigue-detector-tiktok-ads` (T01).
- Account is new to the agency. Run `account-triage-tiktok-ads` first, then start weekly reporting.
- TikTok Shop margin is the client's question. Run `gmv-max-profit-check-tiktok-ads` and attach its ledger.

## Required input

A weekly report is only comparable if inputs and definitions stay the same each week. Ask once, then reuse.

Ads Manager export from **Reporting**, campaign level, daily rows for the reporting week and the prior week, columns as labelled in your export: Date, Campaign name, Objective, Optimization event, Cost, Impressions, CPM, Clicks (destination), CTR (destination), Conversions, Cost per conversion, Total purchase value or conversion value, 2-second video views, 6-second video views.

Also required:

- Reporting week dates, comparison week dates, ad account timezone.
- Client goal in their terms: cost per sale or lead target, ROAS target, monthly volume, or budget cap.
- Primary event and attribution setting, plus conversion lag in days.
- Change log for the week: budget edits, bid or target edits, new ads, paused ads, new ad groups, page or offer changes.
- Learning status of any campaign or ad group edited this week (screenshot or status column).

### Optional input

- Independent results for the same dates from Shopify, GA4, or CRM (`analytics_export` or `shop_export`), with last week's TikTok-to-independent ratio.
- Events Manager diagnostics status (`events_diagnostics`).
- Creative notes: which videos launched, which creators, which hooks.
- Last week's decisions with their status, so the report carries a running record.

## Before analysis

1. Confirm who reads the report and which decision they make from it: approve budget, approve creative, or simply stay informed. Write the "In short" section for that reader.
2. Confirm the client's goal number and whether it is judged on TikTok-reported results or on store or CRM results. Report against that number every week.
3. Pull last week's report and decisions so carried-forward items keep their wording and owners.
4. Agree the week cut-off once (for example Monday to Sunday in the ad account timezone) and keep it fixed.

### Client language rules

- One idea per sentence, in the words the client uses for their own business (orders, bookings, leads).
- Every number carries its unit and the goal it is judged against.
- Good news and bad news get the same plain wording; neither gets hedged into silence.
- Uncertainty is stated as a check with a date ("we will know by Tuesday"), never as a forecast.

## Analysis workflow

1. Lock definitions: same week cut-off, same timezone, same primary event, same attribution setting as last week. Announce any change at the top of the report.
2. Run the integrity check before any performance sentence. If the primary event fell at least 30% while clicks stayed within 10% of baseline (T10), lead with measurement and label every result below it as unreliable. If the TikTok-to-independent ratio moved at least 20% against its baseline (T07), say so and route.
3. Mark immature days. Days inside the conversion lag are reported separately as "still counting", never as a result.
4. Build the scorecard: spend, reach cost (CPM), tap rate (CTR), results, cost per result, value, and the client's target. Show absolute numbers next to every percentage change.
5. Flag small samples. When either week has fewer than 10 reported conversions, call the cost-per-result change too small to read, in line with the T04 volume floor.
6. Explain each material movement with a cause and a confidence label from the shared vocabulary: deliberate change from the log, learning phase after an edit (T05), creative launch or fatigue, mix shift between campaigns, measurement, or unexplained. "Unexplained so far" is an acceptable answer.
7. Route escalations: CPA up at least 30% with enough conversions (T04) to `cpa-spike-diagnosis-tiktok-ads`; ratio movement (T07) to `attribution-gap-check-tiktok-ads`; event drop (T10) to `pixel-events-api-check-tiktok-ads`; fatigue candidates (T01) to `creative-fatigue-detector-tiktok-ads`; budget moves to `learning-phase-guard-tiktok-ads` and `budget-scaling-planner-tiktok-ads`.
8. Choose up to three decisions for next week. Each has an owner, a reason, an approval flag, and a check date. Carry last week's decisions forward with status.
9. Translate into client language using the glossary below, then reread the narrative for any promise of future results and remove it.

Plain-language glossary for the client sections:

| Ads term | Client wording |
|---|---|
| CPA / cost per conversion | cost per sale (or per lead) |
| CPM | cost to show the ads 1,000 times |
| CTR | share of viewers who tapped through |
| Learning phase | TikTok is still working out who to show the ads to after a change |
| Attribution | how TikTok decides which sales to credit to its ads |
| Conversion lag | sales that arrive days after someone saw the ad |

## Decision rules

| Condition | Evidence | Verdict | Report treatment |
|---|---|---|---|
| T10 met this week | `ads_export` + `events_diagnostics` | `likely` measurement issue | Lead with it; hold budget decisions; route to pixel check |
| T07 ratio movement | `ads_export` + `analytics_export` | `possible` | Note gap change; report independent number as the client figure |
| Fewer than 10 conversions in either week (T04 floor) | `ads_export` | `monitor` | Say "too small to read" in the scorecard |
| CPA up at least 30% with at least 10 conversions per week (T04) | `ads_export` | `likely` real movement | Explain known causes; route unknown ones |
| Campaign edited and still learning (T05) | `change_log` + status | `hold` | Tell the client results are settling; no further edits |
| Movement explained by a logged change | `change_log` | `confirmed` | One sentence, cause and owner |
| No cause found after log and mix check | all inputs | `possible` | Write "unexplained so far" and name the check |
| Spend or budget change proposed | any | `approval_needed` | Put in decisions with client approval flag |

## Output format

```markdown
# TikTok weekly report: [client], week of [dates] ([timezone])

## In short
[Three to five sentences in client language: on track or not against the goal, what moved most and why, what we do next week, what we need from you.]

## Scorecard
| Measure | This week | Last week | Change | Goal | Status |
|---|---|---|---|---|---|
| Spend | | | | | |
| Sales or leads (TikTok-reported) | | | | | |
| Cost per sale or lead | | | | | |
| Sales value | | | | | |
| Sales or leads (your store or CRM) | | | | | |
Status words: on track / watch / off track / too small to read / still counting

## What happened this week
- [Plain sentence]: [cause], confidence: [confirmed / likely / possible]

## Decisions for next week
| Decision | Why | Owner | Needs your approval | Check date |
|---|---|---|---|---|

## Last week's decisions
| Decision | Status | Result so far |
|---|---|---|

## Risks and open questions
- [risk or data gap in plain words]

## Operator appendix
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|
Routed to: [skill names]
Data gaps: [missing item: blocks conclusion]
```

## Practical example

Illustrative numbers for a fictional apparel client, not a benchmark. Goal: cost per sale at or under 45.00. This week: spend 6,200, 141 TikTok-reported purchases, cost per purchase 43.97. Last week: spend 5,900, 155 purchases, cost per purchase 38.06. Change: up 15.5%, below the T04 escalation line, with well over 10 conversions in both weeks. Shopify TikTok-tagged orders moved in line, so the TikTok-to-Shopify ratio is stable (T07 not met). Purchase events tracked clicks (T10 not met).

Change log: budget raised on two ad groups on Tuesday; both re-entered learning (T05). Four new creator videos launched Wednesday.

Client "In short" section: "TikTok stayed under your 45.00 cost-per-sale goal this week at 43.97, though it cost more per sale than last week. We raised budget on Tuesday, and TikTok is still adjusting who sees the ads after that change, so costs can swing while it settles. Four new creator videos went live Wednesday and are too new to judge. Next week we keep budgets flat while TikTok settles, and we need your approval for three new creator briefs by Thursday."

Decisions: keep budgets flat until learning clears (owner: agency, check Tuesday); approve three creator briefs (owner: client, approval needed); review new videos once each passes the T01 impression floor (owner: agency).

## Common misreads

- Opening with a CPA story while purchase events failed T10 that week.
- Reporting percentage swings on a handful of conversions.
- Calling the last two days a drop while they sit inside the conversion lag.
- Promising that next week will recover. Clients remember promises; report the plan and the check date instead.
- Using Ads Manager jargon in the summary. Keep terms for the operator appendix.
- Silently changing the week cut-off or attribution setting between reports.
- Reporting TikTok-reported sales as the client's revenue when their goal is judged on store or CRM numbers.

## Route to next

- Cost per result up past T04 with enough volume: `cpa-spike-diagnosis-tiktok-ads`.
- TikTok and store numbers drifting apart (T07): `attribution-gap-check-tiktok-ads`.
- Events dropped while clicks held (T10): `pixel-events-api-check-tiktok-ads`.
- Best ads slowing down (T01): `creative-fatigue-detector-tiktok-ads`, then `winning-ad-remix-tiktok-ads`.
- Client wants more budget: `budget-scaling-planner-tiktok-ads` (T06), checked by `learning-phase-guard-tiktok-ads` (T05).
- Shop client asking about margin: `gmv-max-profit-check-tiktok-ads` (T09).

## Guardrails

- Do not promise future results or recovery dates in client sections.
- Do not report a performance change on top of a tracking or definition change without saying so first.
- Do not invent a cause; write "unexplained so far" and name the check.
- Do not let the client summary contradict the operator appendix.
- Do not include budget, bid, or targeting changes as done; list them as decisions awaiting approval.
- Do not paste customer names, emails, or comments with identifiers into the report.
