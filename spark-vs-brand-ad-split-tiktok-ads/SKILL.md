---
name: spark-vs-brand-ad-split-tiktok-ads
description: Compares TikTok Spark Ads with brand-handle ads like-for-like by matching objective, optimization event, audience, offer, placements, bidding label, dates, and concept before any metric is read, then records authorization status and designs a matched test when no clean pair exists. Use when the user asks "do Spark ads perform better than our brand ads", "Spark vs non-Spark", "should we boost creator posts", "why is the creator ad cheaper", or pastes ad-level data with a format column and wants a verdict.
---

# Spark vs Brand Ad Split - TikTok Ads

## Use this skill when

A team sees different results from Spark Ads (an existing creator post run as an ad) and brand-handle ads and wants to know whether format is the reason. Format is unproven by default, because the two usually differ in creator, concept, offer, and age. This skill checks that before comparing anything.

Common requests:

- "Do Spark ads beat our brand-handle ads?"
- "Our creator ad has half the CPA. Is that Spark or the creative?"
- "Should we move budget to boosted creator posts?"
- "Set up a fair test between the two formats."

### When not to use

- A single ad's opening is weak -> `hook-rate-scorer-tiktok-ads`.
- An ad is tiring over time -> `creative-fatigue-detector-tiktok-ads`.
- A creator brief or rights wording is needed -> `ugc-brief-writer-tiktok-ads`.
- CPA moved in the whole account -> `cpa-spike-diagnosis-tiktok-ads`.

## Required input

Ad-level export from Ads Manager **Reporting** for a stated date range, one row per ad. Column labels vary; keep them as labelled in your Ads Manager and map them in the first reply.

| Field | Note |
|---|---|
| `ad id`, `ad name` | Never infer format from the name |
| Format (Spark or brand-handle) and ad identity or post source | From ad metadata or a screenshot of the ad detail |
| Creator, for Spark ads | As shown on the identity |
| `campaign name`, `ad group name`, `objective`, optimization event | Matching keys |
| Audience summary, placements, bidding strategy as labelled, daily budget | Matching keys |
| Offer per ad (user-stated), concept, length | Matching keys |
| `start date`, `end date` or `date` | Matching keys |
| `spend`, `impressions`, `clicks`, `CTR`, `CPM`, `CPC` | Delivery |
| `reported conversions`, `CPA`, `conversion value`, `frequency` | Outcome |
| `2-second video views`, `6-second video views` | Optional, for the hook read |

Also needed: the conversion lag, attribution setting, and a screenshot of each Spark ad's authorization status and expiry as shown in your account. Optional: engagement columns (likes, comments, shares) if the export carries them, creative previews, change log.

## Analysis workflow

1. Confirm format per ad from metadata. No metadata means `needs_data` for that ad, and it stays out of the comparison.
2. Normalise the window: same dates, same currency and timezone, same attribution setting. Drop rows inside the conversion lag.
3. Build candidate pairs. A pair is two ads, one per format, matched on all eight dimensions in the table below.
4. Compute for each arm: spend, impressions, CPM, CTR, CPC, conversion rate (reported conversions / clicks), CPA, frequency, 2-second view rate where present. Always print the sample next to the metric.
5. Apply floors: 3,000 impressions per arm before any hook or CTR read (T02); 10 reported conversions per arm before any CPA read (the floor T04 uses for its windows, borrowed here as a pack heuristic); exclude arms inside about 25 results or 7 days of entry (T05); check T01 if either ad is old.
6. Run the confounder pass: creator versus brand concept, offer, audience size, ad age, budget skew, social proof visible on the ad, view-versus-click attribution.
7. Assign a verdict per pair. If no pair is clean, list the mismatches and design the matched test below.
8. Record authorization per Spark ad: status, scope, expiry, owner. Unknown is `needs_data`.

### Matching dimensions

| Dimension | Must match | If it does not |
|---|---|---|
| Objective and optimization event | Identical | Not comparable; stop |
| Audience | Same targeting summary and size band | Label mismatch; verdict capped at `possible` |
| Offer | Same price, discount, and end date | Offer becomes the explanation |
| Placements | Same set | Placement mix can drive CPM |
| Bidding strategy label and budget scale | Same label, similar daily budget | Spend skew changes the sample |
| Dates | Overlapping window, same lag treatment | Seasonality and promo timing leak in |
| Concept and length | Same script and cut, or documented difference | Creative is the confounder, not format |
| Age and learning stage | Similar days live, both past T05 | Younger ad carries learning noise |

## Matched test design

When no clean pair exists, propose one variable: format. Use the same video: the creator's post as the Spark ad, and the identical footage uploaded as the brand-handle ad. Keep objective, optimization event, audience, placements, bidding label, offer, and schedule identical, with equal budgets, in separate ad groups. Read after both arms pass about 25 results or 7 days (T05) and the lag has cleared. State the limits: two ad groups with the same targeting can compete in the same auctions, and the Spark post may carry engagement history the upload lacks. Starting it requires approval.

## Reading metrics across formats

Some gaps come from how the two formats are built, so read them as questions, not as results.

| Metric | What a gap may reflect | How to check |
|---|---|---|
| CPM | Audience, placement mix, and competition at the time | Same audience band and placements (matching dimensions) |
| CTR | Creative and creator pull, plus the profile and engagement surface a post carries | Compare only with CPA and conversion rate beside it |
| Conversion rate and CPA | Offer, landing page, creator trust | Same landing page and offer, lag cleared |
| Likes, comments, shares on a Spark post | Organic history of the post, not only paid delivery | Do not treat as an ad-quality score |

A cheaper CTR with a worse CPA points at a landing or offer problem, not at the format. Route that to `landing-page-match-tiktok-ads`.

## Authorization status watch

Record status as shown in the account, as labelled in your Ads Manager. This skill never approves or extends it.

| Status | Verdict | Next step |
|---|---|---|
| Recorded, scope covers the run, expiry after the test ends | Proceed with the comparison | Note the expiry date in the record |
| Recorded, expiry inside the test window | `monitor` | Owner decides on extension before the read |
| Not recorded or unreadable | `needs_data`, `hold` on budget moves toward Spark | Owner records it in writing |
| Revoked or lapsed during the test | `hold` | Stop the comparison; mark the arm incomplete |

## Decision rules

| Condition | Verdict | Next step |
|---|---|---|
| Format not confirmed from metadata | `needs_data` | Supply ad detail screenshots |
| Pair unmatched on one or more dimensions | Format effect `possible`; mismatch itself `confirmed` | Matched test |
| Matched, floors met, CPA and CTR agree in direction in one window | `possible` | Repeat in a second non-overlapping window |
| Same, agreeing across two non-overlapping windows [pack heuristic] | `likely` | Matched test before shifting budget |
| Matched test result with both arms past T05 and lag | `confirmed` for that test | `approval_needed` for a budget decision |
| Either arm under the impression or conversion floor | `monitor` | Wait or widen |
| Either arm inside a learning window (T05) | `hold` | `learning-phase-guard-tiktok-ads` |
| Authorization missing, unknown, or near expiry | `hold` on extending Spark spend; `needs_data` | Owner records status |

## Output format

````markdown
### Format map
| Ad id | Format (from metadata) | Creator or identity | Evidence | Authorization status |
|---|---|---|---|---|

### Matched split table
| Pair | Dimension matches (8) | Arm | Spend | Impr | CPM | CTR | CPA | Conv | Confounder | Verdict | Next controlled test |
|---|---|---|---|---|---|---|---|---|---|---|---|

### Authorization record
| Spark ad | Scope | Expiry | Owner | Status |
|---|---|---|---|---|
(as shown in the account; not approved by this skill)

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps and approval needed
[missing item] -> [verdict prevented]. [budget move or Spark extension] -> [named owner].
````

## Practical example

Illustrative numbers only. 14 days, lag 7 days cleared, purchase objective, same audience band and placements.

Pair 1 (unmatched): Spark creator ad, spend 1,240, impressions 210,000, CPM 5.90, clicks 2,310 (CTR 1.10%), 31 conversions, CPA 40.0, carries a 15% code. Brand-handle ad, spend 1,180, impressions 148,000, CPM 7.97, clicks 1,030 (CTR 0.70%), 19 conversions, CPA 62.1, no code. Different offer and different concept. Verdict: format `possible`, offer mismatch `confirmed`, severity `medium`, impact `spend`.

Pair 2 (matched on all eight): Spark spend 620, impressions 98,000, clicks 735 (CTR 0.75%), 9 conversions, CPA 68.9. Brand spend 600, impressions 91,000, clicks 664 (CTR 0.73%), 9 conversions, CPA 66.7. Impressions clear 3,000, but 9 conversions is under 10 per arm, so the CPA read is `monitor`; the CTR gap is negligible.

Conclusion: the headline gap in pair 1 is offer and concept, not format. Next: the matched test with one video in both formats. Authorization: the Spark ad expires within the next window; owner status `needs_data`, so extending Spark spend is `hold`.

## Common failure modes

- Reading a Spark ad's lower CPA as a format effect when it carries a different offer.
- Comparing arms with different learning stages or ad ages.
- Pooling many unmatched ads into a format average that hides one outlier.
- Inferring format from the ad name.
- Letting social proof or comments on the creator post explain results without labelling it.
- Comparing before the conversion lag clears, so recent spend looks worse.
- Running both arms as ad groups with identical audiences and ignoring auction overlap.
- Extending Spark spend after the authorization has lapsed or was never recorded.

## Guardrails

- Do not declare a format winner from unmatched pairs; format stays `possible` until the eight dimensions match.
- Do not infer Spark or brand-handle status from an ad name.
- Do not compare CPA with fewer than 10 reported conversions per arm or hook metrics under 3,000 impressions.
- Do not mix offers, audiences, or bidding labels inside one pair without naming the mismatch.
- Do not approve, extend, or request a Spark permission; record status only.
- Do not recommend a budget shift before a controlled test; stop at an approval-ready proposal.
- Do not hide the conversion lag, attribution setting, or date window.
