---
name: cpa-spike-diagnosis-tiktok-ads
description: Diagnoses a TikTok CPA jump by splitting it into CPM, CTR, and CVR movement between a baseline and a current window with the cpa_decompose.py helper, then checking tracking, changes, mix, creative, and landing page in that order. Use when someone types "TikTok CPA doubled", "cost per purchase is up 40%", "why did CPA spike", "CVR dropped but clicks are fine", or "the client wants to know what broke".
---

# CPA Spike Diagnosis

## Use this skill when

CPA moved and the buyer needs arithmetic before a story. This skill decomposes the move into delivery cost (CPM), click appeal (CTR), and post-click conversion (CVR), applies T04 as a triage label, and then works the causes in dependency order. It never names a cause from the arithmetic alone.

Common requests:

- "CPA doubled week over week. What happened?"
- "Cost per lead is up 45%. Tracking, creative, or market?"
- "CPM is fine, CTR is fine, CVR collapsed. Now what?"
- "Zero conversions today on a campaign that always converts."
- "Client asks why TikTok got expensive. Need an answer today."

Do not use this skill for these jobs:

- Event or Pixel setup review with no CPA question: `pixel-events-api-check-tiktok-ads`.
- Reported versus independent counts: `attribution-gap-check-tiktok-ads`.
- Ranking waste rows: `wasted-spend-finder-tiktok-ads`.
- Unmapped account: `account-triage-tiktok-ads`.

## Required input

Work from pasted exports and screenshots. Claude's TikTok for Business MCP connector is optional.

### Required

- CSV with columns `period`, `cost`, `impressions`, `clicks`, `conversions`. `period` must read exactly `baseline` or `current` in lower case. Several rows per period (for example daily rows) are summed by the script.
- Two mature windows of equal length with a similar weekday mix, both ending after the conversion lag has passed.
- Primary event name, attribution setting, timezone, currency, target CPA.
- Dated change log covering the baseline and the current window.
- Events Manager diagnostics capture.
- Landing page and site release dates.

### Optional

- The same export split by campaign, ad group, or ad, for the mix check.
- `frequency`, creative launch dates, audience edits.
- Independent order or lead report for the same dates.

Export route: **Reporting** at campaign, ad group, or ad level with date breakdown, then change history or campaign activity history. See `../tiktok-ads-shared/references/getting-your-data.md`. Never infer a change event from a chart alone.

## Before analysis

1. Establish that the spike is real. Each window needs at least 10 reported conversions for T04 to escalate; below that the script prints `insufficient_volume`.
2. Confirm both windows use the same primary event, objective, and attribution setting. A changed definition makes the two CPAs incomparable.
3. Drop days inside the conversion lag and any partial day. A recent window that is still collecting conversions is the commonest false spike.
4. Mark ad groups launched inside the current window. They are learning-sensitive (T05) and can lift CPA without any decay elsewhere.
5. Use the click column consistently across both windows, since CTR and CVR both depend on which click count is exported.

## Analysis workflow

1. State both windows with dates and lengths. If they are unequal or inside the lag, stop with `needs_data`.
2. Run the helper from the skill folder:
   `python3 ../tiktok-ads-shared/scripts/cpa_decompose.py cpa.csv`
3. Read the identity. CPA equals CPM divided by 1000, divided by CTR times CVR. CVR here is conversions divided by clicks. Compute current over baseline for CPM, for CTR (inverted), and for CVR (inverted); the three multiply to the CPA ratio.
4. Express each factor as a share of the CPA move: natural log of the factor ratio divided by natural log of the CPA ratio. Shares can be negative when a factor offsets the rise, and they describe arithmetic only.
5. Read the T04 label the script prints (see Decision rules).
6. Check tracking first: T10 pattern, diagnostics, event changes, site releases. A uniform drop across campaigns points at measurement before delivery.
7. Check the change log against the date the move began: budget, bid strategy, audience, creative, and event edits, and whether the effect sits in the edited entities.
8. Check mix using conversion yield, never an arithmetic spend-weighted mean of CPA. Let w_i be segment i's baseline share of spend and y_i its current conversions divided by current spend. Counterfactual CPA = 1 / sum(w_i * y_i). A segment with spend and zero conversions has y_i = 0; a segment with no current spend has no observable yield, so request comparable data. If total weighted yield is zero, CPA is undefined and needs tracking review. Compare this fixed-mix CPA with baseline and actual current CPA: near baseline suggests a mix shift; near current suggests within-segment deterioration. Illustrative example: unchanged segment CPAs 20 and 80, baseline spend 800/800 and current spend 400/1600 give baseline CPA 32, current CPA 50, fixed-mix CPA 32, so the rise comes from mix.
9. Check creative (CTR led move) then landing page (CVR led move with steady CTR), then auction (CPM led move). Use Smart+ allocation notes when the campaign is automated.
10. State the unexplained residual and the ordered action list with what to hold.

## Decision rules

Script contract: the only argument is the CSV path. It prints one line per window with `cost`, `impressions`, `clicks`, `conversions`, `cpm`, `ctr`, `cvr`, `cpa`, then `cpa_change_pct`, `T04_verdict`, and a read line. Rows with other `period` values are ignored. A missing `baseline` or `current` window exits with an error. Exit code 2 covers unreadable files and missing columns.

| T04 label printed | Meaning | Verdict | Next step |
|---|---|---|---|
| `escalate` | Current CPA at least 30% above baseline, each window at least 10 conversions (T04) | `likely` real move, cause unknown | Work tracking, change log, mix, creative, page in order |
| `below_rule` | Move under 30%, or CPA fell | `monitor` | Keep windows, re-run next period |
| `insufficient_volume` | A window has under 10 conversions | `needs_data` | Widen windows, never diagnose |
| `check_tracking` | Current conversions are zero, CPA prints `n/a` | `needs_data` | Capture Events Manager and diagnostics; no tracking claim from CPA alone |

| Pattern in the factors | Area to test first | Verdict if evidence is missing | Next step |
|---|---|---|---|
| Conversions down at least 30% with clicks within 10% (T10) | Event delivery | `possible` | `pixel-events-api-check-tiktok-ads` |
| CVR led, CTR and CPM steady | Landing page, offer, checkout, event | `possible` | `landing-page-match-tiktok-ads` after tracking clears |
| CTR led, CVR steady | Creative engagement, audience | `possible` | `creative-fatigue-detector-tiktok-ads` (T01 floors), `hook-rate-scorer-tiktok-ads` |
| CPM led, CTR and CVR steady | Auction pressure, audience or placement mix | `possible` | `placement-review-tiktok-ads` (T08), seasonality check |
| Stable segment CPAs, shifted spend weights | Mix | `likely` once the reweight shows it | Budget or audience edits in the change log |
| Dated change within days before the move, effect in that entity | Deliberate edit | `confirmed` when the entry and the effect both appear | `learning-phase-guard-tiktok-ads` before reverting |
| New ad groups in the window | Learning (T05) | `monitor` | Hold optimization edits until learning clears |
| Reported moves, independent report flat | Attribution | `possible` | `attribution-gap-check-tiktok-ads` (T07) |

A statement of arithmetic is `confirmed` (for example CPM fell, so auction cost did not drive this rise). A statement of cause needs a dated entry, a diagnostics capture, or a release date; otherwise it stays `possible` or `likely`. Prefer a few confirmed causes with a labelled residual over a full list.

## Output format

Fill this template.

```markdown
## CPA diagnosis: [campaign or account], [currency], [timezone]
Baseline: [dates, n days] | Current: [dates, n days] | Lag cleared: [yes/no] | Event: [name]
Command run: [exact command]

### Arithmetic
| Period | Cost | Impr | Clicks | Conv | CPM | CTR | CVR | CPA |
|---|---|---|---|---|---|---|---|---|
T04 label: [label] | CPA change: [%] | Factor shares: CPM [%], CTR [%], CVR [%]

### Cause tree (ordered)
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Ruled out
[causes excluded and the evidence that excluded them]

### Residual
[what remains unexplained, never spread across causes]

### Ordered action and hold list
[fix order by dependency; edits that wait, with prerequisite]

### Data gaps
[missing diagnostics, change log, segment export, and the verdict each would firm up]
```

## Practical example

Illustrative numbers only. Two 7-day windows, target CPA 50 USD. Input rows: `baseline,4200,520000,5200,84` and `current,4500,600000,4800,56`.

```text
period    cost     impressions  clicks  conversions  cpm   ctr    cvr    cpa
baseline  4200.00  520000       5200    84.00        8.08  1.00%  1.62%  50.00
current   4500.00  600000       4800    56.00        7.50  0.80%  1.17%  80.36
cpa_change_pct:  60.7%
T04_verdict:     escalate
```

CPA rose 60.7%. Factor ratios: CPM 0.93, CTR 0.80, CVR 0.72. In log shares, CVR carries about 69% of the move, CTR about 47%, and cheaper CPM offsets about 16%. Shares can exceed 100% in total when one factor offsets another.

Cause tree: CPM fell, so auction cost is `confirmed` as not the driver. Conversions fell 33% while clicks fell 8%, which meets the T10 pattern, so event delivery is `possible`, high severity, measurement impact, and diagnostics are missing (`needs_data`). A product page template was released on day 3 of the current window and a new creative batch on day 1, so landing page is `possible` for the CVR share and creative is `possible` for the CTR share (frequency not exported).

Ordered action: capture Events Manager and run an event test first, split CVR by day around the release date, then run the T01 check on the new batch. Hold budget and bid edits until tracking is verified. Residual: not yet quantified because daily rows are missing.

## Common failure modes

- Reading `escalate` as a diagnosis. T04 is a triage label, not a cause.
- Comparing windows of different length or weekday mix.
- Including days inside the conversion lag, which inflates CPA.
- Calling tracking broken from CPA alone. T10 plus diagnostics are the evidence.
- Treating factor shares as additive causes. Several causes can sit behind one factor.
- Blaming the auction when CPM did not rise.
- Missing learning ad groups: new ad groups lift CPA while they explore (T05).
- Blaming Smart+ for a move that came from an event change. Check the event first.
- Reading platform conversions as sales without an independent comparison.

## Route to next

Event delivery: `pixel-events-api-check-tiktok-ads`. Reported versus independent gap: `attribution-gap-check-tiktok-ads`. Creative: `creative-fatigue-detector-tiktok-ads`, `hook-rate-scorer-tiktok-ads`. Page: `landing-page-match-tiktok-ads`. Placement: `placement-review-tiktok-ads`. Edits waiting on learning: `learning-phase-guard-tiktok-ads`. Waste rows: `wasted-spend-finder-tiktok-ads`. Automated campaign: `smart-plus-audit-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not diagnose a window that sits inside the conversion lag or holds under 10 conversions.
- Do not name a cause from the decomposition alone.
- Do not call tracking broken from CPA alone; ask for the Events Manager capture.
- Do not recommend bid or budget reactions to a CPA that tracking has not been shown to report correctly.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim a result before a controlled measurement exists.
