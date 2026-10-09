---
name: search-ads-keyword-review-tiktok-ads
description: Reviews TikTok Search Ads search terms and keywords and decides what to add as a keyword, add as a negative, or watch, with match handling as labelled in the account and a lag-aware waste floor. Use when someone types "review our TikTok search terms", "negative keyword list for TikTok Search Ads", "which queries should become keywords", "broad match is bringing junk", or "Search Ads spend with zero conversions".
---

# Search Ads Keyword Review

## Use this skill when

Search term data exists and the buyer must turn it into three lists: terms to add as keywords, terms to block as negatives, and terms to watch. Read search terms first, keywords second, and never treat a single thin term as proof.

Common requests:

- "Here is the Search Terms report. What do we block?"
- "Broad match is pulling irrelevant queries. Narrow it?"
- "Which converting queries deserve their own keyword?"
- "We spend on search with no conversions. Waste or just early?"
- "Build the negative list with the right match types."

Do not use this skill for these jobs:

- Non-search waste across ad groups, ads, or placements: `wasted-spend-finder-tiktok-ads`.
- A page that fails the query promise: `landing-page-match-tiktok-ads`.
- Event or tracking doubts: `pixel-events-api-check-tiktok-ads`.
- CPA moved and the cause is unknown: `cpa-spike-diagnosis-tiktok-ads`.

## Required input

Work from pasted exports and screenshots. Claude's TikTok for Business MCP connector is optional.

### Required

- Search terms export with columns `search term`, `keyword` (the entered keyword that matched), `match type` where present, `campaign`, `ad group`, `date`, `spend`, `clicks`, `conversions`. Rename the account's own column labels to these names when you paste.
- Current keyword list with match types, and the current negative list with its scope (ad group or account level, as labelled in your Ads Manager).
- Target CPA, currency, timezone, primary event, conversion lag in days.
- The offer: products or services sold, brand terms, competitor policy, landing page URL or text.

### Optional

- `impressions` and `CTR` per term, which help with intent reading.
- Ad copy or the in-feed video the search ad reuses.
- Independent order or lead report for the same dates.

Export route: the **Search Terms** section and **Custom reports** are the documented places in TikTok help pages for search reporting. See `../tiktok-ads-shared/references/getting-your-data.md` and save screenshots when a column cannot be exported.

## Before analysis

1. Identify which surface produced the data. A Search Ads Campaign is keyword based, with keywords set at ad group level. Automatic Search Placement (formerly Search Ads Toggle) extends an in-feed video campaign to the search results page, has no keywords to edit, and still shows a search terms report and accepts negatives.
2. Confirm the primary event and the conversion lag. Rows newer than the lag are `needs_data`.
3. Collect the brand and competitor policy. A competitor or brand term is a business decision, not a waste finding.
4. Check the change log for keyword, match, or budget edits in the window. Learning-sensitive ad groups (T05) get `hold` on match narrowing.

## Analysis workflow

1. Join every search term to the keyword and match type that served it. Terms with no keyword (Automatic Search Placement) go in a separate block.
2. Classify intent per term with the offer list in hand: brand, competitor, product specific, category or problem, research, free or DIY, unrelated. Ambiguous intent is `hypothesis`.
3. Keep mature rows only. Aggregate each term across the window and compute spend, clicks, conversions, CPA, CVR against the ad group average. Optionally run `../tiktok-ads-shared/scripts/wasted_spend.py` on term rows (columns `date`, `level` set to `search_term`, `name`, `spend`, `conversions`) with `--target-cpa` and `--conversion-lag-days`. It judges each row on its own, so aggregate first and strip currency symbols other than `$`.
4. Apply T03 to zero-conversion terms. Pass T03, then check intent. Pass both and the term enters the negative proposal.
5. For converting terms at or under target CPA on mature rows, check whether an equivalent keyword already exists and what match type serves it. Propose an add only where it gives control, for example a phrase or exact keyword for a term currently served by a broad keyword.
6. Choose negative match type from the blocking level TikTok documents: broad blocks most, phrase blocks medium, exact blocks least. Run a collision check: would this negative block any converting term or any active keyword.
7. Add variants. Negatives do not block plurals, misspellings, or synonyms, so each variant is its own entry. Casing is covered automatically.
8. Review keyword match types. TikTok help suggests broad match for reach and learning at launch, and says match types can be adjusted mid-flight, for example after learning. Propose narrowing only when off-intent terms dominate a keyword and the ad group is past T05.
9. Check overlap: the same term served by several ad groups or keywords. Propose one owner and negatives elsewhere.
10. Send adjacent terms (right audience, weak page) to `landing-page-match-tiktok-ads`. Return the approval queue.

## Decision rules

Match syntax as TikTok documents it (confirm in your account): broad is the plain keyword, phrase uses quotation marks, exact uses square brackets. For negatives, broad blocks a query that contains every word in any order, phrase blocks the words in order with extra words allowed around them, exact blocks only the identical query.

| Condition on mature rows | Action | Verdict | Next step |
|---|---|---|---|
| Spend at least 1.5 times target CPA, zero conversions (T03), intent off-offer | Negative | `likely` | `approval_needed`, pick match type after the collision check |
| Same T03 pass, intent on-offer or ambiguous | Watch and page check | `possible` | `landing-page-match-tiktok-ads`, review again next window |
| Zero conversions, spend under the T03 floor | Watch | `monitor` | Re-export next window |
| Zero conversions, spend under the floor, intent clearly unrelated | Negative on intent alone | `possible`, confidence `low`, tag `hypothesis` | `approval_needed` if the operator accepts intent as evidence |
| Converted at or under target CPA, no matching keyword control | Add as keyword | `likely`, or `possible` if all conversions came on one date | `approval_needed` for match type |
| Converted, CPA above target | Watch | `monitor` | Do not negate a converter on CPA alone |
| Brand or competitor term | Policy decision | `approval_needed` | Owner decides, record the rule |
| Row inside the conversion lag | None | `needs_data` | Wait for the lag to clear |
| Primary event drop with steady clicks (T10) | Freeze all negatives | `hold` | `pixel-events-api-check-tiktok-ads` |
| Export has no keyword column (Automatic Search Placement) | Negatives only; adds are a test | `possible` | Consider a separate Search Ads Campaign, `approval_needed` |

Term clusters: single terms are thin. Group by pattern (for example all "free" variants), treat the cluster as one row, and label it `hypothesis` until a member converts or the cluster passes T03 as a whole.

## Output format

Fill this template.

```markdown
## Search review: [campaign], [dates], [currency], [timezone]
Surface: [Search Ads Campaign | Automatic Search Placement | needs_data]
Target CPA: [value]. T03 floor: [1.5 x target]. Lag: [days]. Rows excluded as recent: [n]

### Search action sheet
| Term | Keyword and match as labelled | Intent | Spend | Clicks | Conv | Lag status | Action | Verdict | Rationale |
|---|---|---|---|---|---|---|---|---|---|

### Negative proposals
| Entry with syntax | Scope | Blocks | Collision check | Variants to add |
|---|---|---|---|---|

### Keyword proposals
| Term | Proposed match | Why | Existing keyword it overlaps |
|---|---|---|---|

### Findings
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps
[missing column, lag, policy, or export and what it would firm up]
```

Keep negative proposals separate from live changes. Nothing is applied by this skill.

## Practical example

Illustrative numbers only. A sports-nutrition store, Search Ads Campaign, target CPA 30 USD, lag 7 days, so the T03 floor is 45 USD.

- "free protein samples": 62 USD, 48 clicks, 0 conversions, off-offer. Passes T03 and intent. Verdict `likely`. A broad negative `free` would also block "free shipping protein powder", which converted, so the collision check rejects it. Propose `[free protein samples]` plus `[free protein sample]`, since a singular form is not blocked.
- "whey protein isolate 2kg": 118 USD, 5 conversions, CPA 23.60, served by broad keyword `protein powder`. Verdict `likely`. Propose phrase keyword `"whey protein isolate"` and keep the broad keyword.
- "best protein powder reddit": 51 USD, 40 clicks, 0 conversions, research intent. Passes T03 but intent is ambiguous. Verdict `possible`, action watch, page check.
- "protein bar recipes": 18 USD, 0 conversions, unrelated. Below the floor. Verdict `possible`, confidence `low`, negative on intent alone if the owner agrees.
- "protein shaker bottle": spend inside the lag. Verdict `needs_data`.

Output: two negatives and one phrase keyword at `approval_needed`, one watch item with a page check, one recent row held back.

## Common failure modes

- Treating Automatic Search Placement terms as keywords you control. That surface extends in-feed video, so there is no keyword to add.
- Adding a broad negative that blocks a converting query because the words appear in a different order.
- Assuming a negative also covers plurals, misspellings, and synonyms. It does not.
- Negating a term after a few clicks. Per-term volume on search is often thin, so cluster before judging.
- Judging terms inside the conversion lag, which makes late converters look like waste.
- Narrowing match types while the ad group is still learning (T05).
- Importing intent classes from other search platforms. TikTok queries mix entertainment and shopping, so check every class against your own converting terms.
- Reading platform-reported term conversions as sales without an independent check.

## Route to next

Weak page after a good click: `landing-page-match-tiktok-ads`. Tracking doubt: `pixel-events-api-check-tiktok-ads`. Waste outside search: `wasted-spend-finder-tiktok-ads`. CPA movement: `cpa-spike-diagnosis-tiktok-ads`. Strategy fit for a Traffic or Conversions ad group: `bid-strategy-check-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not propose a negative from T03 alone; intent review comes first.
- Do not negate a converting term on CPA alone.
- Do not use a broad negative without a collision check against converting terms and active keywords.
- Do not treat rows inside the conversion lag as findings.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim a result before a controlled measurement exists.
