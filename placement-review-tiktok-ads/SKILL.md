---
name: placement-review-tiktok-ads
description: Reviews TikTok Ads delivery split between the TikTok placement and Pangle or TikTok Ad Network inventory (as labelled in your Ads Manager), testing CPA and downstream quality per placement against T08 and keeping brand safety and suitability as a separate question. Use when a TikTok media buyer says "should we turn off Pangle", "where is our TikTok spend actually going", "automatic placement is eating budget", "network traffic converts badly", "is our TikTok ad showing next to unsafe content", or when a client asks for a placement and brand safety readout.
---

# Placement Review: TikTok Ads

## Use this skill when

A buyer needs to know where spend lands across placements, whether one placement underperforms after enough delivery, and whether the brand safety setup matches the client's requirements. Performance and suitability are two separate questions here: a cheap CPA says nothing about adjacency, and a safety setting says nothing about efficiency. Work from a placement breakdown export and settings screenshots; a TikTok for Business connector in Claude is optional.

Typical requests:

- "Half our impressions go to Pangle. Is that wasted?"
- "Automatic placement or TikTok only for this conversion campaign?"
- "Network clicks look cheap and nothing converts."
- "Client legal wants proof we control where ads appear."
- "CPA by placement for the monthly report."

Do not use this skill when:

- Search results traffic and search terms are in question. Run `search-ads-keyword-review-tiktok-ads`.
- Placement looks fine and CPA moved account-wide. Run `cpa-spike-diagnosis-tiktok-ads` (T04).
- A Smart+ campaign controls placement automatically and the question is the whole automation. Run `smart-plus-audit-tiktok-ads`.
- Zero-conversion rows across many dimensions are the target. Run `wasted-spend-finder-tiktok-ads` (T03).

## Required input

Placement names, available controls, and safety tiers differ by account, objective, and market. Every setting claim needs a screenshot; otherwise it is `needs_data`.

Ads Manager export from **Reporting** or the campaign table, broken down by placement, columns as labelled in your export: Date, Campaign name, Ad group name, Ad name, Placement, Cost, Impressions, Clicks (destination), CTR (destination), Landing page views if reported, Conversions, Cost per conversion. Use at least 14 days plus the conversion lag so rows mature before T08 applies.

Screenshots (`screenshot`):

- Ad group placement setting: automatic or selected placements, and which apps or networks are ticked, as labelled.
- Brand safety or inventory filter setting for the TikTok placement, as labelled in your account.
- Any block list, app exclusion list, or category exclusion available for network inventory, if your account shows one.

From the business: target CPA or ROAS, conversion lag, and written brand safety requirements (excluded categories, sensitive topics, regions). If the client has no written requirement, record that as a data gap with an owner.

### Optional input

- Downstream quality per placement: CRM qualified rate, refund rate, or repeat purchase rate, by UTM or placement macro if the account passes one (`analytics_export`).
- Third-party verification or post-campaign suitability report, if the client buys one.
- Creative-to-placement mapping when ads differ in format (vertical video, horizontal, image).

## Before analysis

1. Confirm the objective and optimisation event per campaign. Placement CPA comparisons only hold inside one campaign with one event.
2. Confirm tracking is sound for the period. If T10 is met, route to `pixel-events-api-check-tiktok-ads` first, because missing events can hit one placement harder than another.
3. Record which ad groups were edited during the window and whether they re-entered learning (T05); a learning ad group can shift delivery between placements on its own.
4. Get the client's brand safety requirement in writing before reading any setting, so the check compares against a stated standard.

### Brand safety context by placement

TikTok placement delivers ads in the TikTok feed, next to user videos. Suitability here depends on the adjacent content, and the controls are the inventory or safety settings your account shows for that placement. Pangle or TikTok Ad Network (as labelled in your Ads Manager) delivers ads inside third-party apps, so context depends on which apps and app categories serve the ad, and the controls are whatever app exclusion or block list options your account shows. Treat these as two separate safety questions with two separate evidence sets. A setting screenshot for one placement says nothing about the other.

## Analysis workflow

1. Map placements and controls. List each placement in the export, the ad groups using automatic versus selected placement, and the safety settings shown in screenshots. Note campaign types where the setup screen shows no placement choice; record those as constraints.
2. Check row maturity. Drop days inside the conversion lag. A placement row needs at least 3,000 impressions before T08 applies.
3. Compute campaign-average CPA, then CPA per placement inside each campaign. Apply T08: review a placement when its CPA is at least 30% above the campaign average after the lag has passed.
4. Check click quality on network inventory. Compare CTR, landing page views per destination click, and conversion rate between the TikTok placement and Pangle or TikTok Ad Network rows. High CTR with weak landing page views points to accidental or low-intent taps as a hypothesis.
5. Check creative mix. List which ads carry each placement's impressions. If one placement ran mostly on a creative that underperforms everywhere, placement causation stays `possible`.
6. Check downstream quality when supplied. A placement with acceptable platform CPA and poor CRM qualification or high refunds belongs in the decision table, since platform CPA alone hides it.
7. Review brand safety separately. Compare the settings shown with the client's written requirements. Flag any gap between required and configured protection, and any placement where the account offers no control the client asked for.
8. Propose a reversible action: a time-boxed split with a selected-placement ad group against the current setup, an exclusion list update, or a hold. Every action is `approval_needed` with a named owner and a check date after lag.

## Decision rules

| Condition | Evidence | Verdict | Next step |
|---|---|---|---|
| Placement at least 3,000 impressions, CPA at least 30% above campaign average, lag passed (T08), creative mix comparable | `ads_export` | `likely` placement underperformance | `approval_needed` for a time-boxed selected-placement split |
| T08 met, placement driven by one weak creative | `ads_export` | `possible` | Route creative to `creative-fatigue-detector-tiktok-ads` or test the creative on TikTok placement first |
| Below 3,000 impressions or lag not passed (T08) | `ads_export` | `monitor` | Recheck at next window |
| Network CPA acceptable, downstream quality clearly worse | `ads_export` + `analytics_export` | `likely` low-quality conversions | Owner decision on exclusion test; record quality metric |
| Network CPA lower than TikTok placement, downstream quality not supplied | `ads_export` | `possible` | Request CRM or refund data before any budget shift toward network |
| High CTR, weak landing page views per click on network rows | `ads_export` | `possible` accidental taps | Check landing page views; route to `landing-page-match-tiktok-ads` if load suspected |
| Configured safety setting below client written requirement | `screenshot` + requirement doc | `confirmed` gap | `approval_needed` for setting change; impact `brand_safety` |
| No written safety requirement from client | none | `needs_data` | Request requirement from client owner |
| Setting or placement availability claimed without screenshot | none | `needs_data` | Request screenshot |

Severity is set by share of spend: a placement failing T08 on a small slice of campaign spend is `low` or `medium`; the same pattern on a large slice is `high`. A confirmed brand safety gap against a written client requirement is `high` or `critical` regardless of spend.

## Output format

```markdown
## Placement Review: [account / campaign], [dates], lag excluded: [days]

**Verdict:** [shared verdict label] because [strongest evidence]

### Placement map
| Ad group | Placement mode (automatic / selected) | Placements live | Safety setting shown | Evidence |
|---|---|---|---|---|

### Performance by placement
| Campaign | Placement | Impressions | Spend | Clicks | LP views per click | Conversions | CPA | vs campaign avg | T08 |
|---|---|---|---|---|---|---|---|---|---|

### Creative mix per placement
| Placement | Top ads by impressions | Share | Same ads on TikTok placement CPA |
|---|---|---|---|

### Brand safety check
| Client requirement | Configured control | Evidence | Gap |
|---|---|---|---|

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Proposed test or hold
- Action: [split / exclusion / hold] | owner: [name] | check date: [after lag] | success read: [metric]

### Data gaps
- [missing item]: blocks [conclusion]
```

## Practical example

Illustrative numbers for a fictional lead-gen account, not a benchmark. One campaign on automatic placement, 21 days, seven-day lag excluded. TikTok placement: 610,000 impressions, 3,800 spend, 100 leads, CPA 38.00. Pangle row (as labelled in that account): 240,000 impressions, 1,220 spend, 20 leads, CPA 61.00. Campaign average CPA 41.83, so Pangle sits about 46% above it. T08 is met.

Creative mix check: 70% of Pangle impressions went to a horizontal product demo. Same ad on the TikTok placement converts at CPA 55.00, already weak. CRM data shows 9 of 20 Pangle leads qualified against 61 of 100 TikTok leads. Landing page views per click on Pangle sit well below the TikTok placement.

Output: placement underperformance `likely`, creative contribution `possible`. Proposed test, `approval_needed`: duplicate the ad group on TikTok placement only for one lag-cleared window, retire the horizontal demo in both, compare qualified leads per spend. Brand safety: client asked for exclusion of gambling and dating adjacency in writing; the inventory filter screenshot shows a standard tier as labelled, and no network block list was supplied. Gap marked `needs_data` until the account owner confirms which network exclusions exist.

## Common misreads

- Judging placements on CTR. Network inventory can show high CTR with low intent.
- Pausing a placement after a week inside the conversion lag.
- Blaming the placement when the creative served there is the real weak point.
- Assuming a safety tier covers network inventory the same way it covers the TikTok placement; confirm from the screenshot.
- Comparing placement CPA across campaigns with different objectives.
- Treating placement savings as wasted spend removed without checking the volume lost.
- Reading a placement row with a different creative format mix as a like-for-like comparison.
- Treating automatic placement as a single setting when the export shows how spend actually split.

## Route to next

- Placement fine, creative weak across placements: `creative-fatigue-detector-tiktok-ads` (T01) or `hook-rate-scorer-tiktok-ads` (T02).
- Network clicks reach the page and drop off: `landing-page-match-tiktok-ads`.
- Proposed placement split touches a learning ad group: `learning-phase-guard-tiktok-ads` (T05).
- Client report needs a placement and safety summary: `weekly-client-report-tiktok-ads`.

## Guardrails

- Do not switch placements, change safety settings, or edit block lists. Output stops at an approval-ready action.
- Do not apply T08 before 3,000 impressions and lag clearance.
- Do not mix performance findings and brand safety findings in one verdict.
- Do not name a placement, app, safety tier, or control your screenshots do not show; quote labels as labelled in your Ads Manager.
- Do not claim adjacency incidents without a verification report or screenshot.
- Do not recommend shifting budget toward a cheaper placement without downstream quality evidence.
