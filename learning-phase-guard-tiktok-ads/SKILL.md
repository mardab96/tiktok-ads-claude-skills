---
name: learning-phase-guard-tiktok-ads
description: Sequences planned TikTok edits around the learning phase, separating urgent repairs from optimisation, naming which edits TikTok itself labels as affecting learning, and ordering one observable action at a time with rollback. Use when someone types "can I edit this ad group during learning", "will this reset the learning phase", "campaign is in learning, what can we change", "sequence these changes", or "the client wants five edits this week".
---

# Learning Phase Guard

## Use this skill when

A conversions campaign or ad group is new, recently changed, or still showing a learning status, and several edits are waiting. This skill decides what goes first, what waits, and what evidence clears each gate. It sits between diagnosis and any live proposal.

Common requests:

- "Ad group is in learning. Can we raise budget today?"
- "Does swapping creative reset learning?"
- "Client sent five edits. What order do we use?"
- "Is it safe to pause the weak ad group?"
- "How do we know learning is over?"

Do not use this skill for these jobs:

- Picking a bid strategy: `bid-strategy-check-tiktok-ads`.
- Sizing and staging a budget increase: `budget-scaling-planner-tiktok-ads`.
- Fixing events: `pixel-events-api-check-tiktok-ads`.
- Finding why CPA moved: `cpa-spike-diagnosis-tiktok-ads`.

## Required input

Work from pasted exports and screenshots. Claude's TikTok for Business MCP connector is optional.

### Required

- Planned edits, one line each: what, level (campaign, ad group, ad), why, who asked, urgency claim.
- Screenshots of the campaign and ad group tables showing learning status, results count, and budget, as labelled in your Ads Manager.
- Learning entry date for each ad group. Take it from change history or campaign activity history.
- Objective, optimization goal, bid strategy label, daily budget, target CPA.
- Dated change log for the last 14 days and the conversion lag in days.
- Events Manager diagnostics capture.

### Optional

- Smart+ flag per campaign.
- Promo or launch calendar with fixed dates.
- Results export by ad group with `date`, `spend`, `reported conversions`, `CPA`.

Export route: campaign table, ad group table, and change history. See `../tiktok-ads-shared/references/getting-your-data.md`.

## Before analysis

1. Record the status shown on screen for each entity. Account status is stronger evidence than any assumed reset rule.
2. Count results since entry for each ad group, and days since entry. T05 treats a conversions entity as learning-sensitive until about 25 campaign results or 7 days since entry.
3. Note that TikTok pages disagree on the count. A June 2026 Learning Phase page says volatility tends to decline after about 25 campaign results or 7 days. A Learning Phase FAQ dated February 2025 and a Smart+ page cite 50 conversions. Record which page you relied on and trust the account status when it differs.
4. Check whether duplicate or misfiring events inflated the results count. A count built on double-firing is not progress.
5. List edits already made since entry. Earlier edits may already be spending the observation window.

## Analysis workflow

1. List each proposed edit with level and type: budget, bid or strategy, target, audience, schedule, creative, conversion event, status change, name.
2. Record learning evidence per entity and label it with T05: learning-sensitive or cleared, with the page or screen relied on.
3. Split urgent repairs from optimisation. Urgent means broken event delivery, a rejected or non-compliant ad, a wrong price or claim, a brand safety issue, or an offer that ended. Everything else is optimisation.
4. Classify each edit by TikTok labelling (see Decision rules). Where TikTok publishes no label, the class is unlabelled and the verdict is `needs_data`.
5. Check conflicts: two edits to one variable, edits that stack on one day so the read is impossible, and edits that fight Smart+ automation.
6. Sequence: Slot 0 holds the smallest urgent repair set. Each later slot holds one optimisation action, opens only after the observation window closes (at least the conversion lag), and needs evidence that the prior action is readable (T04 floor of 10 reported conversions per window when you compare CPA).
7. Allow parallel actions only on independent entities that share no budget, audience, or event.
8. Write rollback, owner, and check date per slot. A rollback restores the recorded prior value. It does not promise the prior CPA returns.
9. Produce the change ledger and the hold list. Live edits stop at `approval_needed`.

## Decision rules

TikTok labelling, from its own help pages (confirm current wording in your Ads Manager):

| Class | What TikTok says | Source and date |
|---|---|---|
| Named as affecting learning | Pausing campaigns or ad groups; edits that retrigger learning status; unreasonable budget or creative volume | Learning Phase page, June 2026 |
| Reset by TikTok's wording | Changing the conversion event at campaign level resets existing ad groups and ads information | Edit ad settings page, November 2025 |
| Named in context | In the first 7 days of a Smart+ Web campaign, bid, audience, and creative edits may impact learning | Smart+ Web best practices, April 2025 |
| Review only | Some edits put an ad or ad group back under review while delivery continues | Edit ad settings page, November 2025 |
| Unlabelled | Any other edit, including strategy switches and schedule changes | No label found; ask for an in-product notice screenshot |

TikTok does not list on the Learning Phase page which edits retrigger learning. Do not fill that gap from memory.

Editability, per the same edit page: campaign level allows name and budget; ad group level allows name, audience targeting, budget and schedule, and bidding and optimization; ad level allows all settings. Other settings need a new campaign or ad group, which starts its own learning.

| Condition | Verdict | Next step |
|---|---|---|
| Optimisation edit on an entity under about 25 results and 7 days (T05) | `hold` | Gate: T05 cleared and window closed |
| Urgent repair, entity in learning | `approval_needed` | Smallest fix first; recount results after (T05) |
| Pause of an ad group in learning, not urgent | `hold` | TikTok names pausing as affecting learning; keep running |
| Conversion event change at campaign level | `hold` | Treat as a rebuild; new campaign with a defined test |
| Budget increase while learning | `possible` impact | Stay within the per-adjustment ceiling on TikTok's budget page; T06 covers post-learning only |
| New or swapped creative in the first 7 days | `possible` impact | Add after T05 clears unless creative is the urgent repair |
| Edit with no TikTok label | `needs_data` | Treat as learning-sensitive until a notice or screenshot says otherwise |
| Several edits queued for one day | `hold` for all but Slot 0 | Re-slot one per window |
| Entity cleared (T05), CPA readable (T04 floor met) | `approval_needed` | One action per window; budget via `budget-scaling-planner-tiktok-ads` (T06) |
| Status on screen says learning, count says 25 or more | `monitor` | Trust the screen; re-check next window |
| Event diagnostics show a T10 pattern | `hold` on all optimisation | `pixel-events-api-check-tiktok-ads` |

## Output format

Fill this template.

```markdown
## Learning guard: [account or campaign], [timezone], [currency]
Strategy label: [as labelled] | Lag: [days] | T05 page relied on: [page, date]

### Learning evidence
| Entity | Status on screen | Results since entry | Days since entry | T05 state | Evidence tag |
|---|---|---|---|---|---|

### Change ledger
| Edit | Level | TikTok label class | Urgency | Verdict | Prerequisite | Rollback value | Owner | Earliest date |
|---|---|---|---|---|---|---|---|---|

### Sequence
| Slot | Date | Single action | Observe until | Gate to open next |
|---|---|---|---|---|

### Findings
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps
[missing status, entry date, notice screenshot, and the verdict each would firm up]
```

## Practical example

Illustrative numbers only. A conversions ad group `A` entered learning on 2026-09-14 and shows 11 results on 2026-09-18 (day 4). Lag is 7 days. Another ad group `B` in the same campaign shows 60 results. Client queues five edits.

1. Purchase event fires twice on the thank-you page. Urgent, measurement impact. Slot 0, `approval_needed`. After the fix, recount `A` results because 11 may include duplicates.
2. Raise `A` budget by 50%. `hold`: `A` is learning-sensitive (T05) and the size is above the T06 step. Re-plan through `budget-scaling-planner-tiktok-ads` after clearing.
3. Swap three creatives in `A`. `possible` impact on learning, optimisation, `hold` until T05 clears, then add new ads rather than swapping.
4. Narrow `A` audience. TikTok lists audience edits as editable, but publishes no reset label here, so the class is unlabelled, `needs_data`, `hold`.
5. Pause `B` for weak CPA. `B` is past learning, but it shares the campaign budget with `A`, so a pause may move budget into a learning ad group. `hold` until Slot 0 is read, then one action.

Sequence: Slot 0 event fix on 2026-09-18, observe 7 days, then Slot 1 one budget step if `A` has cleared and CPA is readable. Rollback for Slot 0 is the previous event configuration, owned by the tracking lead.

## Common failure modes

- Assuming a fixed list of resetting edits. TikTok's Learning Phase page does not publish one.
- Mixing up a review cycle with a learning reset. A review does not affect delivery per TikTok's edit page.
- Stacking budget, bid, and creative edits on one day, which makes the next read uninterpretable.
- Editing to chase early CPA noise. TikTok says performance may fluctuate during learning.
- Counting results that include duplicate event firing.
- Pausing and unpausing to restart learning. TikTok names pausing as an operation that can prevent exit.
- Duplicating an ad group to escape learning. A copy starts its own learning.
- Setting a budget too small for the CPA, then blaming the algorithm. TikTok names unreasonable budget setting as a blocker; route to `bid-strategy-check-tiktok-ads`.
- Treating a Smart+ campaign's learning status as a normal ad group status. Read its own screens.

## Route to next

Strategy and budget ratio: `bid-strategy-check-tiktok-ads`. Staged increase after clearing: `budget-scaling-planner-tiktok-ads`. Event repair: `pixel-events-api-check-tiktok-ads`. CPA movement: `cpa-spike-diagnosis-tiktok-ads`. Automated campaign: `smart-plus-audit-tiktok-ads`. Client communication of the hold: `weekly-client-report-tiktok-ads`.

## Guardrails

- Do not make a live account, budget, bid, placement, tracking, Shop, page, or creative change.
- Do not state that an edit does or does not reset learning unless a dated TikTok page or an in-product notice says so.
- Do not recommend pausing a learning ad group unless the reason is urgent.
- Do not queue more than one optimisation action per observation window on the same entity.
- Do not override the status shown on screen with a count or a rule of thumb.
- Do not present platform-reported conversions or GMV as profit without the supplied cost stack.
- Do not hide missing dates, lag, attribution settings, or conversion definitions.
- Do not claim a result before a controlled measurement exists.
