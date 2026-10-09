---
name: creative-fatigue-detector-tiktok-ads
description: Detects whether a TikTok ad is tiring by comparing the last seven distinct dates with the preceding seven for frequency and CTR, using the bundled fatigue_scan.py script and a 14-date rule, then builds a control-versus-refresh queue. Use when the user asks "is this TikTok ad fatigued", says CTR is dropping while frequency climbs, wants to know when to refresh TikTok creative, or pastes a daily ad export and asks which ads to replace.
---

# Creative Fatigue Detector - TikTok Ads

## Use this skill when

You have daily ad-level data and want to know whether delivery is repeating on the same viewers while engagement slides. Deliver a ranked refresh queue with a retained control, not a pause list.

Common requests:

- "Is this ad fatigued or is it just a bad week?"
- "CTR keeps falling and frequency is up. Do I refresh?"
- "Which of these ads should I replace first?"
- "How often should I rotate creative on this account?"

### When not to use

- A new ad never got attention in its first seconds -> `hook-rate-scorer-tiktok-ads`.
- CPA rose and the cause is unknown -> `cpa-spike-diagnosis-tiktok-ads`.
- The ad group was edited or is still inside about 25 results or 7 days (T05) -> `learning-phase-guard-tiktok-ads` first.
- The user wants new scripts after a verdict -> `winning-ad-remix-tiktok-ads` or `ugc-brief-writer-tiktok-ads`.

## Required input

One daily CSV at ad level. `fatigue_scan.py` needs exactly these columns, spelled as below (rename headers if your export differs):

| Column | Meaning |
|---|---|
| `date` | ISO format `YYYY-MM-DD` (a trailing time is ignored); other formats are skipped silently |
| `ad` | Ad ID or a unique ad name; two ads sharing a name merge into one |
| `impressions` | Daily impressions |
| `clicks` | Daily clicks; use one clicks column for the whole file |
| `frequency` | Frequency as the export labels it |

Also include `spend` and `conversions` for corroboration. Export from Ads Manager **Reporting** (or Analytics, as labelled in your Ads Manager): ad level, daily breakdown by date, one row per ad per day, widest range that is still one creative era, saved with the date range in the filename. Do not split rows by placement, ad group, or country unless you sum them back to one row per ad per day first.

Also ask for: a creative preview or first-seconds description, an audience and budget change log, and the conversion lag. TikTok for Business MCP data is optional; a pasted export is enough.

## Before analysis

1. Confirm one row per ad per day. Duplicates are summed by the script and double the weighting, so deduplicate first.
2. Confirm at least 14 distinct dates per ad. Fewer than 14 means the script prints `insufficient_window` and no verdict exists yet.
3. Confirm dates are consecutive. `fatigue_scan.py` takes the last 7 distinct dates and the 7 before them, so an ad paused for 5 days has windows spanning more than 14 calendar days. Flag any gap before trusting a status.
4. Note which `frequency` definition the export uses (daily or cumulative, as labelled in your Ads Manager). Frequency is weighted by impressions inside each window, so a cumulative figure rises by construction.

## Running the script

```bash
python3 ../tiktok-ads-shared/scripts/fatigue_scan.py ads_daily_2026-09-01_2026-09-14.csv
```

Installed form: `python3 ~/.claude/skills/tiktok-ads-shared/scripts/fatigue_scan.py <file.csv>`. It makes no network calls and does not modify the file. Exit code 2 plus an `ERROR:` line means the file is unreadable or a required column is missing.

Output is a tab-separated table:

`ad  prior_dates  current_dates  prior_impr  current_impr  prior_ctr  current_ctr  prior_freq  current_freq  status`

Reading it:

- `insufficient_window`: fewer than 14 distinct dates. `prior_dates` shows how many dates exist. Verdict `needs_data`.
- `fatigue_candidate`: both windows have at least 3,000 impressions, frequency rose at least 20%, and CTR fell at least 20% (T01).
- `monitor`: anything else, including thin impressions or a zero prior CTR. `monitor` here does not mean healthy; read `prior_impr` and `current_impr` yourself.
- An ad you expected is absent: every one of its dates failed to parse. Fix the date format and rerun.

Shared sample `../tiktok-ads-shared/examples/data/fatigue_daily.csv` returns one `fatigue_candidate` and one `insufficient_window` row; compare against `../tiktok-ads-shared/examples/demo-outputs.md`.

## Analysis workflow

1. Validate the file and run the script as above. Quote the raw output rows in the reply.
2. Re-check floors by hand: both `prior_impr` and `current_impr` must reach 3,000 (T01). If not, the verdict is `needs_data` or `monitor`, never a fatigue call.
3. Compute the two relative changes: frequency change = current_freq / prior_freq - 1; CTR change = current_ctr / prior_ctr - 1. T01 needs at least +20% and at most -20%.
4. Locate the scope. Run the same two ratios on sibling ads in the same ad group. If most siblings fell together, suspect audience, season, auction, or tracking before the creative.
5. Check alternates against the change log: audience or budget edits, a new ad splitting delivery, a bid change, learning re-entry (T05), a landing page change, a promo ending, a placement mix shift (`placement-review-tiktok-ads`).
6. Corroborate with direction only: CPM up, CPA up, or conversions per click down in the current window. No threshold exists for these; treat them as support, not proof.
7. Read the creative: how many seconds before the offer, whether the hook is a trend format, whether comments repeat the same objection (`comment-objection-miner-tiktok-ads`).
8. Build the refresh queue: one retained control per ad group, one replacement concept per candidate, and one metric per test.

## Decision rules

T01 is a heuristic, not a TikTok rule. It flags candidates; the verdict comes from the checks that follow.

| Condition | Verdict | Next step |
|---|---|---|
| Fewer than 14 distinct dates | `needs_data` | Re-export a wider range |
| Either window under 3,000 impressions (T01) | `needs_data` | Wait or widen; no fatigue call |
| Floors met, no candidate | `monitor` | Rescan after the next full week |
| Candidate, alternates unchecked or open | `possible` | Close the alternate checks |
| Candidate, siblings stable, no edits in either window, floors met | `likely` | Approval-ready refresh test |
| Candidate, siblings fell too | `possible` audience or auction issue | Route to `placement-review-tiktok-ads` or `cpa-spike-diagnosis-tiktok-ads` |
| Candidate inside a learning window (T05) | `hold` | `learning-phase-guard-tiktok-ads` |

Never mark fatigue `confirmed` from delivery data alone. `confirmed` belongs to the result of a controlled refresh test.

## Output format

````markdown
### Fatigue scan
Window: [prior dates] vs [current dates] | Clicks column: [label] | Frequency definition: [..] [ads_export]

| Ad | Prior / current impr | CTR change | Freq change | Script status | Verdict | Alternate explanation checked |
|---|---|---|---|---|---|---|

### Refresh queue
| Rank | Ad | T01 status | Control to retain | Replacement concept | Metric and window | Route |
|---|---|---|---|---|---|---|

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps
[missing item] -> [verdict it prevented]

### Approval needed
[refresh or swap] -> [named owner]. No ad was changed.
````

## Practical example

Illustrative numbers only. Daily export for three ads in one ad group: 16 distinct dates for the first two, 9 for the third. Lag 7 days, no edits in the change log.

| ad | prior_dates | current_dates | prior_impr | current_impr | prior_ctr | current_ctr | prior_freq | current_freq | status |
|---|---|---|---|---|---|---|---|---|---|
| UGC-demo-01 | 7 | 7 | 41200 | 38900 | 1.10% | 0.82% | 1.80 | 2.30 | fatigue_candidate |
| UGC-demo-02 | 7 | 7 | 40100 | 39300 | 1.05% | 1.02% | 1.70 | 1.74 | monitor |
| Static-offer-03 | 9 | 0 | 0 | 0 | 0.00% | 0.00% | 0.00 | 0.00 | insufficient_window |

Raw script output is tab-separated; the table above is the same data reformatted.

- UGC-demo-01: frequency +27.8%, CTR -25.5%, floors met (T01). Sibling UGC-demo-02 in the same ad group held, and no edits are logged. Verdict `likely`, severity `medium`, impact `conversion`. Refresh: keep UGC-demo-01 as control, test a new first-2-seconds variant plus one new angle against it.
- UGC-demo-02: `monitor`.
- Static-offer-03: 9 dates, `needs_data`.

## Common failure modes

- Reading `monitor` as healthy when the window was thin.
- Calling fatigue when every ad in the ad group fell together; that points at audience, season, or auction.
- Comparing frequency definitions across exports: a cumulative figure rises by construction.
- Running a gap-ridden file; the windows silently stretch past 14 calendar days.
- Letting a budget cut or audience narrowing explain a frequency rise, then blaming the creative.
- Pausing the control in the same step as launching the replacement, which removes the comparison.
- Merging two ads that share a name, so one row blends two creatives.

## Guardrails

- Do not call fatigue from fewer than 14 distinct dates or from either window under 3,000 impressions (T01).
- Do not call a `monitor` row healthy; state the impressions that produced it.
- Do not invent a rotation cadence or a lifespan for creative; only the supplied data can justify a refresh.
- Do not promise that a refresh will recover CTR or CPA.
- Do not recommend pausing the control; propose a retained control and a matched replacement.
- Do not hide the conversion lag, the clicks column used, or the frequency definition.
- Do not change any live ad, budget, bid, or audience; stop at an approval-ready refresh queue.
