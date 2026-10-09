---
name: bid-strategy-check-tiktok-ads
description: Checks whether a TikTok ad group's bidding strategy fits its goal, budget, and conversion volume using the labels TikTok currently lists (Maximum Results, Target Cost per Result, value options as shown in the account) and asks for a screenshot before mapping any legacy name. Use when someone types "Maximum Results or Target Cost per Result", "Cost Cap vs Lowest Cost on TikTok", "our target CPA is too low and delivery died", "bid strategy check", or "should we use hybrid bidding".
---

# Bid Strategy Check

## Use this skill when

A buyer needs to know whether the current bidding setup suits the business constraint, or which of TikTok's two listed strategies to test next. Skill starts from the label on screen, checks the inputs the strategy depends on, reads delivery evidence, and ends with one approval-ready test.

Common requests:

- "Should this ad group run Maximum Results or Target Cost per Result?"
- "Delivery collapsed after we set a target CPA. Why?"
- "Export says Lowest Cost. What is that now?"
- "Is hybrid bidding right for the sale week?"
- "CPA swings every day. Is the strategy the problem?"

Do not use this skill for these jobs:

- Edits that must wait for learning: `learning-phase-guard-tiktok-ads`.
- Sizing a budget increase: `budget-scaling-planner-tiktok-ads`.
- TikTok Shop profit under GMV Max: `gmv-max-profit-check-tiktok-ads`.
- A CPA jump with unknown cause: `cpa-spike-diagnosis-tiktok-ads`.

## Required input

Work from pasted exports and screenshots. Claude's TikTok for Business MCP connector is optional.

### Required

- Screenshot of the ad group **Bidding and optimization** section, with the strategy label, target or bid, and any suggested bid shown, as labelled in your Ads Manager.
- Objective and optimization goal (for example Conversion or a value option as shown in the account).
- Ad group export with columns `ad group`, `date`, `spend`, `budget`, `results` or `reported conversions`, `CPA`, `impressions`, `CPM`, plus the strategy label column if the export has one.
- Daily budget, target CPA or bid, and the business constraint: maximum affordable CPA, margin, promo window, or volume goal.
- Learning status and entry date, conversion lag, primary event, attribution setting.
- Any legacy strategy names found in exports or briefs.

### Optional

- Conversion value data and how it is passed.
- Margin per order or lead value, to derive a CPA ceiling.
- Independent order or lead report for the same dates.

Export route: ad group table with date breakdown, plus a screenshot of the edit page. See `../tiktok-ads-shared/references/getting-your-data.md`.

## Before analysis

1. Copy the strategy label exactly as it appears on screen. Do not retype it from memory.
2. Check against the current list in `../tiktok-ads-shared/references/thresholds.md`: TikTok's September 2026 help page lists Maximum Results and Target Cost per Result as the two available strategies.
3. Legacy names (Maximum Delivery, Lowest Cost, Cost Cap, Bid Cap, Target ROAS, Minimum ROAS) may sit in old exports or briefs. Keep them as a trigger and ask for a current screenshot before mapping them to anything.
4. Confirm the objective supports the strategy. TikTok's page says Target Cost per Result is available for Conversions campaigns only when the optimization goal is Conversion.
5. Confirm tracking is not the real issue. A T10 pattern outranks any strategy change.

## Analysis workflow

1. Record the on-screen label, objective, optimization goal, target or bid, budget, and learning state.
2. Map the label. Maximum Results and Target Cost per Result map with a screenshot. Any other label is `needs_data`. Value options are recorded exactly as shown in the account and not translated into ROAS terms.
3. State the business constraint in numbers: CPA ceiling, volume goal, or both, and where the ceiling came from.
4. Compare freedom to constraint. Maximum Results spends the budget toward the most results, with CPA volatility expected. Target Cost per Result steers toward an average cost per result, which can run slightly above or below the target.
5. Check strategy inputs. Under Target Cost per Result, compare budget to bid using TikTok's recommended bid-to-budget ratio and the suggested bid shown in your Ads Manager. Under Maximum Results, check that budget is realistic against recent CPA. Read the current ratio on TikTok's bidding best-practices page (August 2026) and record it with its date.
6. Read delivery evidence on mature rows: spend versus budget, CPM, CPA range, results per day. Note that TikTok says Conversions campaigns often see fluctuation and higher CPM before passing learning (T05).
7. Check value inputs when a value option is in use: is value passed on the event, does it match the independent report, and does the event pass T10 diagnostics.
8. Check switching options. Hybrid bidding lets an actively spending ad group switch between the two strategies on its edit page. TikTok lists exceptions: TikTok Shop and Value Based Optimization are not supported, and one Ad Network configuration is not supported.
9. Recommend one setting and one approval test with a stated read date.

## Decision rules

Fit criteria (read with the account's own numbers):

| Strategy as labelled | Fits when | Misfit signals |
|---|---|---|
| Maximum Results | Goal is volume inside a fixed budget, no hard CPA ceiling, promo or peak window, business can absorb CPA swings | CPA repeatedly above the ceiling, margin thin, budget tiny against CPA |
| Target Cost per Result | A CPA ceiling exists and is derived from margin, target sits near what the ad group has actually achieved, budget meets the bid-to-budget ratio | Spend far under budget, impressions collapse, target below achieved CPA and below the suggested bid |
| Value option as shown in account | Value is passed reliably and varies by order or lead, tracking is clean | Flat value, missing value, event diagnostics failing |
| Legacy label in an export | Never | `needs_data` until a current screenshot maps it |

| Condition | Verdict | Next step |
|---|---|---|
| Label is not Maximum Results or Target Cost per Result | `needs_data` | Ask for the current screenshot, do not map |
| Target Cost per Result, mature spend well under budget, target below achieved CPA | `likely` target too tight | `approval_needed`: test a target nearer the suggested bid or achieved CPA, one change |
| Target Cost per Result, budget below the recommended ratio to the bid | `likely` budget or bid mismatch | `approval_needed`: raise budget or lower the bid-to-budget gap, one change |
| Maximum Results, CPA above the ceiling for a mature window with at least 10 conversions (T04 floor) | `possible` strategy misfit | Test Target Cost per Result at the ceiling, or fix funnel first |
| Maximum Results, CPA swings but stays under the ceiling | `monitor` | Volatility is expected; no change |
| Ad group still learning (T05) | `hold` | Leave strategy alone; route to `learning-phase-guard-tiktok-ads` |
| Switch planned for a Shop or value-based ad group | `hold` | Hybrid bidding is not listed as supported for these |
| Event drop with steady clicks (T10) | `hold` | `pixel-events-api-check-tiktok-ads` |
| Budget increase planned after the check | `approval_needed` | `budget-scaling-planner-tiktok-ads` (T06) |
| Ceiling not stated | `needs_data` | Derive from margin or ask the owner |

Confidence rule: a strategy fit finding is `confirmed` only when the screenshot, the budget, and the delivery rows all agree. A single mature window gives `likely` at best.

## Output format

Fill this template.

```markdown
## Strategy fit: [campaign or ad group], [currency], [timezone]
Label on screen: [verbatim] | Mapped to: [Maximum Results | Target Cost per Result | value option as shown | needs_data]
Objective and goal: [..] | Budget: [..] | Target or bid: [..] | Suggested bid on screen: [..] | Learning: [status]

### Business constraint
CPA ceiling: [value, source] | Volume goal: [..] | Window: [promo or ongoing]

### Delivery evidence (mature rows)
Spend versus budget: [..] | CPA range: [..] | CPM: [..] | Results per day: [..]

### Findings
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Recommended setting and approval test
Change: [one] | Window: [days, at least the lag] | Read criteria set in advance: [..] | Rollback: [prior value or switch back] | Approver: [name]

### Data gaps
[missing screenshot, ceiling, value data, and the verdict each would firm up]
```

## Practical example

Illustrative numbers only. Two ad groups in one Conversions campaign, lag 7 days, ceiling 45 USD from a 60 USD contribution per order.

Ad group `One` appears in an old export as "Lowest Cost". Output: `needs_data`. Ask for a current bidding screenshot and do not map the label to Maximum Results.

Ad group `Two` shows Target Cost per Result with a 25 USD target. Suggested bid on screen reads 38 USD. Mature days show spend at about 38% of a 100 USD daily budget, achieved CPA near 41 USD, and falling impressions.

Findings: the target sits under both achieved CPA and the suggested bid, so under-delivery is `likely` caused by a tight target, medium severity, conversion impact. Approval test: change only the target to 40 USD, which stays under the 45 USD ceiling. Window: 7 days plus, read once at least 10 conversions sit in each window (T04 floor). Rollback: restore 25 USD. If volume rather than cost matters during the coming sale week, hybrid bidding is a candidate for `Two`, unless the ad group is Shop or value based.

## Common failure modes

- Translating legacy names by memory. Cost Cap, Bid Cap, Lowest Cost, and ROAS labels need a screenshot, because TikTok's current page lists two strategies.
- Treating Target Cost per Result as a cap on every conversion. TikTok says actual CPA can run slightly above or below the target.
- Setting the target at the margin ceiling. Give the target room below the ceiling because delivery can drift.
- Ignoring the bid-to-budget ratio and the suggested bid, then blaming delivery.
- Judging Maximum Results on CPA stability. TikTok says CPA fluctuation is expected there.
- Switching strategy while the ad group is still learning.
- Assuming hybrid bidding works everywhere. Shop and value based setups are listed as unsupported.
- Using a value option without verified value data on the event.
- Reading platform conversions as profit.

## Route to next

Timing a switch: `learning-phase-guard-tiktok-ads`. Budget increases: `budget-scaling-planner-tiktok-ads`. Value or event doubts: `pixel-events-api-check-tiktok-ads`. Shop economics: `gmv-max-profit-check-tiktok-ads`. Automated campaign: `smart-plus-audit-tiktok-ads`. Unexplained CPA move: `cpa-spike-diagnosis-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not map a legacy strategy name to a current label without a current screenshot.
- Do not invent strategy names, options, or menu paths; write "as labelled in your Ads Manager" when unsure.
- Do not recommend a switch while the ad group is learning-sensitive (T05).
- Do not recommend two strategy or budget changes in one test.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim a result before a controlled measurement exists.
