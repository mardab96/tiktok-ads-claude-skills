---
name: budget-scaling-planner-tiktok-ads
description: Builds a staged TikTok budget plan with entry gates, one change per observation window, stop rules, and a recorded rollback, using T04, T05, T06, and T10 from the shared register. Use when someone types "can we scale this TikTok campaign", "double the budget on the winner", "how fast can I raise the daily budget", "scale before the sale", or "plan the budget increase for next week".
---

# Budget Scaling Planner

## Use this skill when

A campaign or ad group looks healthy and someone wants more spend. This skill decides whether the account has earned a raise, sets the step size and spacing, writes the stop rules before any money moves, and records the rollback. It never executes a change.

Common requests:

- "This ad group hit target CPA. Can we double budget?"
- "What is a safe step size on TikTok?"
- "Plan the raise for the sale on the 15th."
- "Budget is capped every day by noon. What now?"
- "We scaled last week and CPA went up. Roll back or hold?"

Do not use this skill for these jobs:

- Choosing or changing a bid strategy: `bid-strategy-check-tiktok-ads`.
- Edits while learning is in progress: `learning-phase-guard-tiktok-ads`.
- CPA already up with no clear cause: `cpa-spike-diagnosis-tiktok-ads`.
- Shop profit under GMV Max: `gmv-max-profit-check-tiktok-ads`.
- Exhausted creative: `creative-fatigue-detector-tiktok-ads`.

## Required input

Work from pasted exports and screenshots. Claude's TikTok for Business MCP connector is optional.

### Required

- Daily export at ad group or campaign level with columns `date`, `campaign`, `ad group`, `budget`, `spend`, `impressions`, `clicks`, `reported conversions`, `CPA`.
- Target CPA and where it came from (margin, lead value, owner statement).
- Bid strategy label and learning status, screenshotted as labelled in your Ads Manager.
- Dated change log for the last 14 days.
- Events Manager diagnostics capture.
- Capacity statement from the owner: stock, fulfilment, sales or call handling, landing page limits.
- Conversion lag in days and attribution setting.

### Optional

- Independent order or lead report for the same dates.
- Creative inventory with launch dates.
- Promo calendar with fixed dates.
- Budget type (daily or lifetime) at each level.

Export route: ad group table with date breakdown and the budget column visible. See `../tiktok-ads-shared/references/getting-your-data.md`.

## Before analysis

1. Confirm the budget type per level. TikTok's About Budget page (July 2026) says a live campaign or ad group cannot switch between daily and lifetime, and a campaign budget should not sit below its ad group budget.
2. Identify the entity to raise and the one metric that proves it is working, normally CPA on the primary event.
3. Read the current per-adjustment ceiling and spacing on TikTok's About Budget page. Record the figure and the date as [platform guidance]. T06 is the planned size in the register and stays at or under any ceiling TikTok shows.
4. Exclude days inside the conversion lag from every CPA you use.
5. Count mature conversions per window. T04 needs at least 10 per window to judge CPA movement.

## Analysis workflow

1. Check the gates in order (see Decision rules): tracking clean (T10), learning cleared (T05), CPA at or under target on mature rows (T04 floor), strategy label confirmed, capacity confirmed. Any failed gate ends the plan with its verdict.
2. Read pacing. Compare `spend` to `budget` across mature days. An entity that does not spend its budget has a delivery constraint, so a bigger budget changes nothing; route to `bid-strategy-check-tiktok-ads`.
3. Set the baseline: mature CPA, results per day, and CPM for the window before the first step.
4. Draft the ladder. Step size follows T06: 20% per step after learning, one budget action per observation window. An observation window is at least the conversion lag and must hold at least 10 conversions to judge CPA. Compounding applies, so three steps from 100 give 120, 144, and 172.80.
5. Name the owner of each step and the date it may be applied. Put promo dates in the calendar so no step lands inside a spike window.
6. Write stop rules before the first step: T04 against the pre-step baseline, T10 pattern, learning re-entry, capacity breach, pacing failure.
7. Write the rollback per step: the exact prior budget, who restores it, and the trigger. State that restoring the budget does not promise the prior CPA returns.
8. If TikTok guidance suggests it for the label in use, consider adding a stabiliser. TikTok says Target Cost per Result can help control volatility while budget rises; confirm the strategy with `bid-strategy-check-tiktok-ads` first, since a strategy switch is its own edit.
9. Output the plan and the approval request.

## Decision rules

Gates:

| Gate | Pass condition | If failed | Verdict |
|---|---|---|---|
| Tracking | No T10 pattern, diagnostics clean | Stop; fix events first | `hold` |
| Learning | Past about 25 results or 7 days, status cleared on screen (T05) | Wait; route to guard | `hold` |
| Efficiency | Mature CPA at or under target with at least 10 conversions (T04 floor) | No raise | `hold` or `needs_data` |
| Strategy | Label confirmed by screenshot | Ask for it | `needs_data` |
| Capacity | Owner confirms stock, handling, page can carry more | Do not plan | `hold` |
| Independent check | Independent report agrees directionally (T07) | Explain gap first | `needs_data` |

Step and stop rules:

| Condition | Verdict | Next step |
|---|---|---|
| All gates pass, step window clear | `approval_needed` | Apply one step of 20% (T06) and open the next window |
| Step window CPA at least 30% above pre-step baseline, both windows at least 10 conversions (T04) | `likely` stop | Roll back to the prior budget, then diagnose |
| Step window has under 10 conversions | `needs_data` | Extend the window, apply no second step |
| T10 pattern appears after a step | `hold` | `pixel-events-api-check-tiktok-ads`, freeze ladder |
| Ad group re-enters learning (status on screen) | `hold` | `learning-phase-guard-tiktok-ads`, freeze ladder |
| Spend stays well under budget across mature days | `possible` bid constraint | `bid-strategy-check-tiktok-ads`, no budget raise |
| Planned step above the ceiling TikTok shows | `hold` | Reduce to the ceiling and extend the ladder |
| Client asks to double in one action | `hold` | Offer staged steps; never skip windows |
| Campaign budget below ad group budget | `hold` | Correct the pair before any raise |
| Creative frequency or T01 signals worsening | `possible` | Add creative supply before the next step |
| Independent report diverges from reported conversions (T07) | `needs_data` | `attribution-gap-check-tiktok-ads` |

TikTok's Maximum Results guidance is that a higher budget often raises cost per result after learning. Plan for CPA to move, and decide the acceptable ceiling before step one.

## Output format

Fill this template.

```markdown
## Scaling plan: [campaign / ad group], [currency], [timezone]
Strategy label: [as labelled] | Learning: [status] | Lag: [days] | Target CPA: [value, source]
TikTok ceiling read: [figure, page, date] | T06 step used: [20%]

### Gate check
| Gate | Evidence | Pass or fail | Verdict |
|---|---|---|---|

### Baseline (mature window, [dates])
Spend/day: [..] | Conversions: [..] | CPA: [..] | CPM: [..] | Budget used: [..]

### Ladder
| Step | Earliest date | Budget from | Budget to | Observe until | Stop rule | Rollback value | Owner |
|---|---|---|---|---|---|---|---|

### Findings
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Stop and rollback rules
[each rule, its trigger, and the exact restore action]

### Data gaps
[missing diagnostics, capacity, independent report, and the verdict each would firm up]
```

## Practical example

Illustrative numbers only. Maximum Results ad group, daily budget 100 USD, target CPA 40 USD, lag 7 days. Mature 14 day window: 52 reported conversions, CPA 38 USD, budget fully spent on most days. Learning status cleared on screen. Events diagnostics clean. Owner confirms stock and handling can carry roughly double volume. Independent orders sit within a few percent of reported.

Gates all pass, so the plan is `approval_needed`. Client asks to double to 200 USD at once. That is `hold` for a single action; stage it instead.

| Step | Budget from | Budget to | Observe |
|---|---|---|---|
| 1 | 100.00 | 120.00 | 7 days, at least 10 conversions |
| 2 | 120.00 | 144.00 | 7 days, at least 10 conversions |
| 3 | 144.00 | 172.80 | 7 days, at least 10 conversions |

Stop rule: CPA in an observation window at or above 30% over the 38 USD baseline, which is 49.40 USD, rolls the budget back to the prior step (T04). Any T10 pattern or a learning re-entry freezes the ladder. Rollback for step 2 restores 120.00. If a step window shows only 7 conversions, the answer is `needs_data` and the window extends before step 3.

## Common failure modes

- Applying step 2 before the first window closes and holds enough conversions.
- Scaling on a window that still sits inside the conversion lag.
- Raising budget on an entity that does not spend its current one. Delivery is constrained, so look at the bid.
- Raising budget and bid together, then having no clean read.
- Scaling through a sale or holiday spike and reading the spike as the effect.
- Putting a campaign budget below its ad group budget.
- Trusting in-platform CPA when the independent report disagrees.
- Scaling a Smart+ campaign without reading its own run guidance, which carries separate limits.
- Treating rollback as a guarantee. Restoring the budget does not return the prior audience pool or CPA.
- Letting creative supply lag the budget until frequency climbs.

## Route to next

Timing against learning: `learning-phase-guard-tiktok-ads`. Strategy mismatch: `bid-strategy-check-tiktok-ads`. Event doubts: `pixel-events-api-check-tiktok-ads`. CPA rising: `cpa-spike-diagnosis-tiktok-ads`. Creative: `creative-fatigue-detector-tiktok-ads`, `winning-ad-remix-tiktok-ads`. Automated campaign: `smart-plus-audit-tiktok-ads`. Client update: `weekly-client-report-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not plan a raise while any gate is failed or unverified.
- Do not stage more than one budget action per observation window.
- Do not exceed the per-adjustment ceiling shown on TikTok's budget page.
- Do not start a stop rule clock inside the conversion lag.
- Do not promise that CPA, volume, or return will hold at a higher budget.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim a result before a controlled measurement exists.
