---
name: hook-rate-scorer-tiktok-ads
description: Scores the opening seconds of TikTok ads by computing 2-second and 6-second view rates and a thumb-stop proxy from ad-level export columns, comparing them with like-for-like ads, and scoring the script opening on a five-point rubric. Use when the user asks "which TikTok hook is weak", "what's my hook rate", "why do people scroll past my ad", wants a hook test plan, or pastes a transcript of the first seconds next to video-view columns.
---

# Hook Rate Scorer - TikTok Ads

## Use this skill when

Use this when you want an attention read on how an ad opens before anyone writes new scripts. Two kinds of evidence are joined: export math (who watched past 2 and 6 seconds) and a read of the actual opening (what the viewer saw and heard).

Common requests:

- "What's my hook rate on these ads?"
- "Which of these openings is losing people?"
- "Score these three scripts before we shoot."
- "Write me a hook test plan for this winner."

### When not to use

- Delivery is repeating and CTR is sliding over weeks -> `creative-fatigue-detector-tiktok-ads`.
- Hook is fine but clicks do not convert -> `landing-page-match-tiktok-ads` or `cpa-spike-diagnosis-tiktok-ads`.
- The user wants full new scripts -> `winning-ad-remix-tiktok-ads`.

## Required input

Ad-level export, aggregated over the date range (daily rows are not required). Label the range in the filename. Use Ads Manager **Reporting**, ad level, and add the video-view columns; column labels vary, so keep them as labelled in your Ads Manager and map them in the first reply.

| Field | Why it is needed |
|---|---|
| `ad id`, `ad name` | Row identity |
| `campaign objective`, `ad group name` | Comparable-set grouping |
| Audience type (prospecting or retargeting), as stated by the user | Retargeting viewers open differently |
| Format: Spark or brand-handle, video length, placement | Comparable-set grouping |
| `impressions` | Denominator for both view rates |
| `2-second video views`, `6-second video views` | Hook and hold numerators |
| `clicks`, `spend` | Post-hook read |

Also needed: the exact first spoken line (word for word), the first frame described, any on-screen text in seconds 0 to 6, and the product facts the opening claims. Optional: other video-view columns your export carries (watch-time or completion columns, as labelled), creative previews, comments.

A generic `video views` column is not a 2-second column. If only that exists, mark T02 `needs_data` and say so.

## Metric definitions

All are calculated per ad from the same row, so they share one denominator. Label every one a proxy: TikTok does not publish a metric named "hook rate" in this pack's references.

| Metric | Formula | Reads as |
|---|---|---|
| 2s view rate | 2-second views / impressions | Thumb-stop proxy: share of impressions that held for 2 seconds |
| 6s view rate | 6-second views / impressions | Early interest proxy |
| 6s-to-2s ratio | 6-second views / 2-second views | Diagnostic ratio of differently defined metrics, never viewer retention; it may exceed 1 |
| Click per 6s view | clicks / 6-second views | Post-hook click intent proxy [heuristic] |

Autoplay, sound state, and placement change how a "view" is counted by viewers, so compare only inside a comparable set.

## Analysis workflow

1. Verify impressions and the exact exported metric definitions. TikTok 6-second views can include an early interaction or completion of a shorter video; 2-second views require two seconds of playback. A 6s count above 2s is therefore valid and must not stop analysis. See https://ads.tiktok.com/help/article/video-play?lang=en . Check missing denominators and incompatible report scopes instead.
2. Build the comparable set: same objective, same audience type, same format (T02). Drop ads under 3,000 impressions from the set (T02). State the set size. A median over two or three ads is fragile; cap the verdict at `possible` and say why.
3. Compute each ad's 2s rate, 6s rate, diagnostic 6s-to-2s ratio, and click per 6s view. Mark zero denominators undefined. Take the median 2s rate across the comparable set.
4. Apply T02: flag an ad when its 2s rate is at least 25% below the comparable median, after at least 3,000 impressions. Gap = (median - ad rate) / median.
5. Score the opening with the rubric below, from the transcript and first-frame description, not from the metrics. Score blind to the metrics where possible, then compare.
6. Cross the two reads using the quadrant table in Decision rules.
7. Check delivery differences before blaming the script: audience type, placement mix, ad age, learning window (T05), budget skew, sound-on share if known.
8. Write a controlled hook test: one ad, 3 openings, everything after second 2 identical.

### Opening rubric (house heuristic, not a predictor)

Score each 0 absent, 1 partial, 2 clear. Maximum 10.

| # | Criterion | Clear means |
|---|---|---|
| C1 | Subject in first frame | Product, problem, or person visible at frame 1; no logo card, fade, or black frame |
| C2 | Tension line | A spoken or on-screen line states a problem, question, claim, or surprise |
| C3 | Speed | The tension line lands before second 2; count words (about 2 to 3 spoken words per second [heuristic]) |
| C4 | Visual change | A cut, motion, or hand action inside the first 2 seconds |
| C5 | Sound-off read | On-screen text carries the point, sits inside the safe area, readable on a small screen |

Bands: 0 to 4 weak, 5 to 7 workable, 8 to 10 strong [heuristic]. Separate claim check: every claim in the opening must trace to a supplied product fact, else `hold` on reusing that hook.

## Scoring scripts that have not run yet

When no export exists (pre-shoot, or a brand-new ad), run the rubric alone. Each candidate needs its first spoken line, first frame, and any on-screen text from seconds 0 to 6. Tag the evidence `creative_script`.

- Score every candidate side by side, 0 to 10, and count the spoken words before second 2.
- The score orders ideas to test. It is not evidence of performance, so the verdict ceiling is `possible`.
- Recommend the top two plus one deliberately different opening, so the test spans a spread instead of three near-copies.

Illustrative candidates for a silicone food-lid set (fictional):

| Candidate | First line | First frame | C1-C5 | Score | Note |
|---|---|---|---|---|---|
| A | "Hi, we're Lumo Home" | Logo card | 0,0,0,1,1 | 2 | Greeting before the problem |
| B | "Silicone lids always pop off." | Bowl held upside down | 2,2,2,2,1 | 9 | Tension in 5 words |
| C | On-screen only: "Do these stay on?" | Hand pressing a lid | 2,1,1,2,2 | 8 | Works with sound off |

### Partial exports

| What you have | What you can compute | Verdict ceiling |
|---|---|---|
| Impressions, 2-second views | 2s rate, T02 gap | `possible` on cause, gap `confirmed` |
| Impressions, 2s and 6s views | Adds diagnostic 6s-to-2s ratio, not retention | Same |
| Only a generic `video views` column | Nothing for T02 | `needs_data` |
| Impressions and clicks only | CTR, not a hook read | `needs_data` for the hook |

## Decision rules

T02 flags a gap in attention. It never supports a purchase conclusion.

| Condition | Verdict | Next step |
|---|---|---|
| Gap at least 25% (T02), 3,000 or more impressions, rubric 0 to 4, set is like-for-like | Gap: `confirmed` for the supplied export. Opening as cause: `likely` | Hook test, then `winning-ad-remix-tiktok-ads` |
| Gap at least 25% (T02), rubric 8 to 10 | `possible` delivery or audience difference | Check placement, audience, sound, learning (T05) |
| 2s rate fine, diagnostic 6s-to-2s ratio below the set median | `possible` metric-definition, interaction or duration difference | Compare duration and interaction counts; inspect seconds 2 to 6 before proposing edits |
| 2s and diagnostic ratio comparable, click per 6s view low | `possible` CTA or offer mismatch | `landing-page-match-tiktok-ads` |
| 2s rate high, clicks and conversions weak | `possible` curiosity without payoff | Compare opening claim with page and offer |
| Under 3,000 impressions, or set too thin | `needs_data` or `monitor` | Wait or widen the set |
| 2-second column missing | `needs_data` | Re-export with the video-view columns |

## Output format

````markdown
### Comparable set
Objective: [..] | Audience: [..] | Format: [..] | Ads in set: [n] | Median 2s rate: [x%] | T02 line: [y%] [ads_export]

### Hook scorecard
| Ad | Impr | 2s rate | 6s rate | Diagnostic 6s-to-2s ratio | Gap vs median | First spoken line | First frame | Rubric C1-C5 | Verdict | Next hook |
|---|---|---|---|---|---|---|---|---|---|---|

### Hook test plan
Control: [ad, retained] | Variants: V1 [..], V2 [..], V3 [..] | Held constant: [body, CTA, audience, budget] | Read after: 3,000 impressions per variant (T02) | Metric: 2s rate; 6s-to-2s ratio as context, never retention

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps and approval needed
[missing item] -> [verdict prevented]. [live change] -> [named owner].
````

## Practical example

Illustrative numbers only. Prospecting purchase ads, in-feed vertical video, six ads each past 3,000 impressions. 2s rates: A 31%, B 28%, C 33%, D 30%, E 26%, F 19%. Sorted median = (28% + 30%) / 2 = 29%; T02 line = 29% x 0.75 = 21.75%.

Ad F: 12,400 impressions, 2,356 2-second views (19.0%), 1,178 6-second views (9.5%), diagnostic 6s-to-2s ratio 0.50 against a comparable-set median near 0.61, 112 clicks. This ratio does not measure retention. Gap = (29 - 19) / 29 = 34.5%, so F clears T02. Opening: a "Hi, we're Lumo Home" logo card for 1.5 seconds, greeting line, product appears at second 3. Rubric: C1 0, C2 0, C3 0, C4 1, C5 1 = 2 of 10, weak. Claim check passes.

Verdict: the gap is `confirmed` for this export; the opening as the cause is `likely`, severity `medium`, impact `conversion` only as an attention input. Hook test: V1 problem-first line over the product in frame 1; V2 on-screen question with a hand demo; V3 result shown first, then the line. Body and CTA identical.

## Common failure modes

- Comparing a retargeting ad with prospecting ads; warm audiences stop and watch for different reasons.
- Comparing a 9-second ad with a 45-second ad on 6s view rate.
- Reading a high 2s rate as a win when clicks and conversions are weak; the hook may promise something the offer does not.
- Mixing Spark and brand-handle ads in one set without saying so (`spark-vs-brand-ad-split-tiktok-ads`).
- Scoring a script from memory instead of from the first 2 seconds as filmed.
- Declaring a hook weak from an ad still in learning or under 3,000 impressions.
- Treating the rubric score as a forecast; it orders ideas to test, nothing more.

## Guardrails

- Do not score a hook from fewer than 3,000 impressions or from a median built on two or three ads without capping the verdict at `possible` (T02).
- Do not substitute a generic `video views` column for 2-second views.
- Do not compare across objective, audience type, or format without labelling the mismatch.
- Do not write a claim in a new hook that is absent from the supplied product facts.
- Do not present a hook gap as a conversion finding or a sales prediction.
- Do not change a live ad or budget; stop at a test plan awaiting approval.
- Do not present rubric bands or the diagnostic 6s-to-2s ratio as platform benchmarks or viewer retention.
