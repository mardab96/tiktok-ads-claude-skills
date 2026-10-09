---
name: wasted-spend-finder-tiktok-ads
description: Finds mature TikTok campaigns, ad groups, and ads that spent past a CPA-based floor with zero reported conversions, after excluding rows still inside the conversion lag, using the wasted_spend.py helper. Use when someone types "where is the wasted spend on TikTok", "which ad groups burn budget with no conversions", "what can we cut before we scale", "zero conversion ads", or "clean this account before the client call".
---

# Wasted Spend Finder

## Use this skill when

A buyer needs a defensible list of rows that look like wasted spend, with recent data kept out of the verdict and every candidate tied to a reversible action. Output is a review list and an estimated reducible scenario, never a saving.

Common requests:

- "Find the wasted spend in this TikTok account."
- "Which ad groups spent twice our CPA with nothing to show?"
- "What do we trim before raising budget?"
- "Client says CPA is high. Where is the leak?"
- "Run the waste check with a seven day lag."

Do not use this skill for these jobs:

- Search term level cleanup: `search-ads-keyword-review-tiktok-ads`.
- Placement comparisons: `placement-review-tiktok-ads`.
- A CPA that jumped and needs a cause: `cpa-spike-diagnosis-tiktok-ads`.
- Zero conversions that might be a tracking fault: `pixel-events-api-check-tiktok-ads` first.
- Ranking creatives for refresh: `creative-fatigue-detector-tiktok-ads`.

## Required input

Work from pasted exports. Claude's TikTok for Business MCP connector is optional.

### Required

- Export with exactly these columns for the script: `date`, `level`, `name`, `spend`, `conversions`. Dates in ISO form `YYYY-MM-DD`. Extra columns are ignored.
- Target CPA for the primary event, in the account currency.
- Conversion lag in days, from the buyer or from the account's own history. It is required, with no default.
- Primary event name and attribution setting.
- Events Manager diagnostics capture, and a note on any ad group that is a deliberate test.

### Optional

- `campaign`, `ad group`, `objective`, `impressions`, `clicks` per row for context.
- Learning status per ad group (screenshot).
- Independent order or lead report for the same dates.
- Margin or lead value, when the target CPA was derived rather than given.

Export route: **Reporting** or the campaign table at the level you need, spend and reported conversions columns on, date range in the filename. See `../tiktok-ads-shared/references/getting-your-data.md`.

## Before analysis

1. Pick one level per run (campaign, ad group, ad, or placement). A child row rolls into its parent, so mixed levels double count.
2. Decide how to shape rows. Each row is judged on its own, so one row per entity over a mature window works, while daily rows would each need to cross the floor in a single day. Date each aggregated row with the last day of its window.
3. Keep a block of recent rows, daily or aggregated, with the export's real last date. Recency is measured from the newest date in the file, and the helper has no way to see today.
4. Check how the export attributes conversions to dates (click or impression date versus conversion date), as labelled in your Ads Manager. If it is unknown, the lag treatment is `needs_data`.
5. Reconcile: sum of `spend` per level should match the Ads Manager total for the same dates. Cells the script cannot parse count as zero.
6. Exclude non-conversion objectives such as Reach or Video views from a CPA floor.

## Analysis workflow

1. Confirm the primary event, target CPA, lag, level, and window. Missing target CPA or lag means `needs_data` and no run.
2. Clean the CSV: remove currency symbols other than `$`, fill blank `conversions` with a real value or drop the row, and keep tab characters out of names.
3. Run the helper from the skill folder:
   `python3 ../tiktok-ads-shared/scripts/wasted_spend.py waste.csv --target-cpa 40 --conversion-lag-days 7`
4. Read the tab separated output (see Decision rules) and set aside `excluded_recent` rows as `needs_data`.
5. For each `review_candidate`, check diagnostics, test purpose, learning status (T05), and Smart+ allocation before any verdict.
6. Review converting rows by hand. No row with conversions is flagged by the helper, so weak but converting rows need a manual pass against target CPA.
7. Group candidates by reversible action, least disruptive first: tighten exclusions or negatives, swap creative, trim budget, pause only when confidence is high and the ad group is past learning.
8. Compute reducible scenarios per level and per confidence tier. Do not sum across levels or tiers.
9. Write the approval queue with an owner and a re-check date after the lag.

## Decision rules

Script contract: arguments are the CSV path, `--target-cpa` (number), and `--conversion-lag-days` (integer), both required. Cutoff is the newest date in the file minus the lag. A row dated after the cutoff is `excluded_recent`; a row dated exactly on the cutoff is judged. A judged row with spend at or above 1.5 times target CPA and zero conversions is `review_candidate` (T03). Everything else judged is `not_flagged`. Output columns: `level`, `name`, `spend`, `conversions`, `cpa` (`n/a` when conversions are zero, otherwise an unrounded number), `classification`, `estimated_reducible_spend` (equals spend for a candidate, otherwise 0.00). Errors print to stderr and exit 2: missing columns, non ISO dates, unreadable file.

| Script label or condition | Extra check | Verdict | Next step |
|---|---|---|---|
| `review_candidate`, diagnostics clean, no documented test, ad group past learning | None open | `likely` waste | `approval_needed`: trim or exclude, pause only at high confidence |
| `review_candidate` but event diagnostics show a drop (T10) | Tracking suspect | `hold` | `pixel-events-api-check-tiktok-ads` |
| `review_candidate` inside learning (T05) | Learning-sensitive | `monitor` | Re-run after about 25 results or 7 days since entry |
| `review_candidate` for a documented exploration cell | Strategic role | `monitor` | Record test end date and exit rule |
| `review_candidate` for a lead account with late CRM quality | Offline value unseen | `possible` | Ask for CRM-qualified outcomes before cutting |
| `excluded_recent` | Inside the lag | `needs_data` | Re-run after the lag clears |
| `not_flagged`, conversions above zero, CPA far above target | Manual review | `possible` | Compare against T04 style baseline before acting |
| `not_flagged`, spend under the floor | Too little spend | `monitor` | No action, keep the row in the next export |
| Target CPA missing or derived without margin | Floor unreliable | `needs_data` | Obtain target before any run |

`not_flagged` is not proof of efficiency. It means no zero-conversion floor breach on mature data.

Manual scenario for weak converters, outside the script and a house heuristic: spend minus conversions times target CPA, floored at zero. Report it as a separate line from the script total.

Value-optimized campaigns judged on return rather than CPA need a CPA equivalent from margin. Without it the T03 floor is `needs_data`.

## Output format

Fill this template.

```markdown
## Waste review: [account], [level], window [start to end], [currency], [timezone]
Target CPA: [value] | T03 floor: [1.5 x target] | Lag: [days] | Latest date in file: [date] | Cutoff: [date]
Command run: [exact command]  Rows: [n judged], [n excluded_recent], [n flagged]

### Waste review ledger
| Level | Name | Window end | Maturity | Spend | Conv | CPA | Diagnostic status | Strategic role | Verdict | Reducible scenario | Approval owner |
|---|---|---|---|---|---|---|---|---|---|---|---|

### Reducible scenario (not a saving)
High confidence: [sum] | Review tier: [sum] | Not summed across levels

### Findings
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Re-check plan
[date after lag, metric, rollback if conversions appear late]

### Data gaps
[missing diagnostics, attribution detail, target source, and the verdict each would firm up]
```

## Practical example

Illustrative numbers only. Target CPA 40 USD, lag 7 days, so the T03 floor is 60 USD. Ad group rows are aggregated over a mature window and dated with its last day.

```text
level     name                  spend    conv   cpa               classification    reducible
ad_group  Broad interest 25-34  95.00    0.00   n/a               review_candidate  95.00
ad_group  Lookalike purchasers  410.00   9.00   45.55555555555556 not_flagged       0.00
ad_group  Retargeting 7d        55.00    0.00   n/a               not_flagged       0.00
ad_group  New UGC test          120.00   0.00   n/a               excluded_recent   0.00
ad        Hook B v2             78.00    0.00   n/a               review_candidate  78.00
campaign  Autumn sale           1020.00  24.00  42.5              excluded_recent   0.00
```

Reading: the newest date in the file is 2026-09-20, so the cutoff is 2026-09-13. `Broad interest 25-34` spent 95 USD with no conversions and is `likely` waste once diagnostics are clean, medium severity, spend impact. `Retargeting 7d` spent 55 USD, under the floor, so it stays `monitor`. `New UGC test` has no verdict yet because its spend is recent. `Hook B v2` is an ad level row and its 78 USD is not added to the ad group total, so the reducible scenario is 95 USD at ad group level and 78 USD at ad level, reported apart. `Autumn sale` has a healthy-looking 42.50 CPA but is also recent, so it is `needs_data` rather than cleared.

Lookalike purchasers converts at 45.56, above target but with conversions, so it is a manual `possible` item, not a script finding.

## Common failure modes

- Feeding daily rows and expecting cumulative detection. Each row needs to cross the floor alone.
- Aggregating everything to the export's last date. Every row then falls inside the lag and the run flags nothing.
- Pasting spend with symbols other than `$`. A cell parses as zero, which hides spend and can invent zero-conversion rows when `conversions` is blank.
- Summing campaign, ad group, and ad scenarios into one headline.
- Cutting an ad group that is still inside learning. Pausing an ad group is itself something TikTok lists as affecting the learning phase.
- Calling zero conversions waste when the event stopped firing. Check diagnostics first.
- Cutting a Smart+ ad that TikTok already starved or paused. Allocation is automated, so route to `smart-plus-audit-tiktok-ads`.
- Treating the reducible scenario as a forecast or a guaranteed saving.

## Route to next

Search terms: `search-ads-keyword-review-tiktok-ads`. Placements: `placement-review-tiktok-ads`. Tracking suspicion: `pixel-events-api-check-tiktok-ads`. CPA movement: `cpa-spike-diagnosis-tiktok-ads`. Moving freed budget: `budget-scaling-planner-tiktok-ads`. Unmapped account: `account-triage-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not label a row waste while it sits inside the conversion lag.
- Do not recommend a pause where a trim or exclusion reaches the same goal.
- Do not call a `review_candidate` waste before diagnostics, test purpose, and learning status are checked.
- Do not sum reducible scenarios across levels or confidence tiers.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim a result before a controlled measurement exists.
