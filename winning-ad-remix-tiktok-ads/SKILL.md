---
name: winning-ad-remix-tiktok-ads
description: Turns one proven TikTok ad into N distinct angle scripts, each with hook, body beats, CTA, on-screen text, and a shot list, after deconstructing why the winner worked and checking every claim against product facts and rights. Use when the user says "remix my winning TikTok ad", "give me new angles on this winner", "I need five scripts like this one", "my best ad is wearing out, what next", or pastes a winning transcript and asks for variations.
---

# Winning Ad Remix - TikTok Ads

## Use this skill when

One ad has earned the right to be built on. You want new angles that share its working ingredients and differ enough to be tested, not paraphrases of its lines.

Common requests:

- "Remix this winner into five new scripts."
- "Same product and audience, different angle. What are my options?"
- "This ad is slowing down. What do I make next?"
- "Give me hooks, body, CTA, on-screen text, and a shot list."

### When not to use

- Deciding whether the winner is tiring -> `creative-fatigue-detector-tiktok-ads`.
- Diagnosing why an opening underperforms -> `hook-rate-scorer-tiktok-ads`.
- The scripts will be shot by outside creators -> hand the chosen angles to `ugc-brief-writer-tiktok-ads`.
- Angles should come from audience objections -> run `comment-objection-miner-tiktok-ads` first.

## Required input

Minimum:

- Winner recording, or a transcript with timestamps plus a first-frame and shot description.
- Performance context for that ad: objective, date range, spend, impressions, CTR, reported conversions, CPA, 2-second view rate if available, conversion lag, and the user's own definition of "winner".
- Product fact sheet with an id per fact (F1, F2...), allowed claims, prohibited claims.
- Audience and offer (terms, price, end date).
- Rights boundaries: who owns the footage, creator or talent usage terms, sound and music cleared for paid use, any Spark authorization on the original post.
- N, the number of angles (default 5; accept 3 to 8).

Optional: brand voice notes, comment themes (`comment_cluster`), earlier remix attempts, competitors that must not be named.

## Before analysis

1. Confirm the winner is real for this purpose. Ask which metric makes it a winner, over which dates, after which lag. Evidence under the conversion lag, or resting on very few conversions (T04 uses 10 reported conversions per window as its floor; borrowed here as a sanity check), stays `possible`, not a winner.
2. Check the winner is not already fading: if the user has a daily export, route a T01 scan before investing in remixes of a tired ad.
3. Separate evidence from inference. Metrics are `ads_export`; why the ad worked is `hypothesis`.

## Analysis workflow

1. Deconstruct the winner into: audience, tension, mechanism (why the product solves it), proof type, hook type, CTA, format and length, pace (number of cuts), sound, creator type, and offer. Quote the first spoken line verbatim.
2. Sort the ingredients into Keep (audience, offer, product truth), Vary (angle, framing, creator persona, structure), and Drop (anything unsupported by the fact sheet or outside rights).
3. Pick N angle territories from the menu below. Each must change the angle only; hold audience, offer, and length band constant so a later read is interpretable. No two angles may share a hook type.
4. Write each script in the template: hook (first 2 seconds: spoken line, on-screen text, first frame), body beats with time ranges, proof, CTA, on-screen text list, and a shot list. Aim first lines at the 2-second mark that T02 reads later.
5. Run a similarity pass: no sentence may repeat the winner's lines beyond a short brand phrase. Reword or cut.
6. Run the claim check: every claim maps to a fact id. A claim with no fact id is removed, not softened. Run the rights check: footage, music, people, third-party marks.
7. Rank the angles by distance from the winner and by risk. Define one retained control (the original winner, unchanged) and one primary metric for the test.
8. Hand off: shooting by creators -> `ugc-brief-writer-tiktok-ads`; reading results -> `hook-rate-scorer-tiktok-ads`; format comparison -> `spark-vs-brand-ad-split-tiktok-ads`.

### Angle territory menu

| Territory | What changes | Needs | Risk |
|---|---|---|---|
| Objection reversal | Opens on the doubt, then answers it | A real objection (`comment_cluster`) and a supporting fact | Answering with an unsupported claim |
| Founder or maker story | Why it was made | Founder available and facts | Rights, personal data |
| Comparison | Versus a category or old habit | Fair, factual comparison | Naming competitors without approval |
| Routine or day-in-life | Product inside a habit | Creator or user footage | Reads as a different offer if the price shifts |
| Myth-bust | Corrects a common belief | Facts that settle it | Absolute language |
| Creator diary | Day 1, day 7, day 30 | Real usage over time | Faking a timeline |
| Problem-first demo | Starts with the failing state | Safe demo of the failure | Misleading before-and-after |
| Offer-led | Leads with the deal | Offer terms and end date | Expired or changed terms |

### Remix depth

Choose one level before writing. Mixing levels in one test blurs the read.

| Level | What changes | Read with | Use when |
|---|---|---|---|
| 1 Hook swap | First 2 seconds only; body and CTA identical | 2-second view rate (T02), then hold ratio | Body works, attention slips |
| 2 Proof or body swap | Beats after the hook; same hook | CTR, then CPA after the lag | Hook is strong, viewers drop after it |
| 3 New angle | Full territory change, shared product truth | CPA after the lag | Winner is a fatigue candidate (T01) or saturated |

Default for an N-angle request is level 3. Offer a level 1 hook swap alongside it when the user wants cheap tests first.

### Per-script quality checks

Run these before showing any script:

- Hook has a spoken line, an on-screen line, and a first frame, and none is a brand greeting.
- Beats are timed and sum to the stated length.
- Spoken lines fit their time range at about 2 to 3 words per second [heuristic].
- On-screen text lines are short, about 6 words or fewer [heuristic].
- CTA matches the offer terms and end date.
- Each shot is filmable with a phone and the stated props.
- No sentence is copied from the winner.

If the winner is a creator or Spark ad, check persona dependence first. A Spark ad runs the creator's existing post, so a remix is a new video, not an edit; route new shoots through `ugc-brief-writer-tiktok-ads` with their own rights terms.

## Decision rules

Prior performance is `confirmed` only for the supplied ad, window, and objective. Every new angle is `possible` until its own test reads out. No numeric threshold in the register decides a remix; use T01 and T02 only to time and read tests.

| Condition | Verdict | Next step |
|---|---|---|
| Winner metrics mature, floors met, no T01 candidate | Winner `confirmed` for that window; angles `possible` | Approval-ready test |
| Winner is a T01 candidate | `possible` winner, `monitor` for remix timing | `creative-fatigue-detector-tiktok-ads` first |
| No performance context supplied | `needs_data` for "winner"; scripts labelled `possible` | Ask for the export |
| A claim has no fact id | `hold` on that script | Supply the fact or drop the line |
| Footage, sound, or Spark rights unclear | `hold` | Supply rights terms |
| Angle repeats the winner's hook type | Reject | Rewrite with a new territory |

## Output format

````markdown
### Winner deconstruction [ads_export, creative_script]
Audience | Tension | Mechanism | Proof | Hook type | CTA | Length | Pace | Offer
Keep: [..] | Vary: [..] | Drop: [..] | Why it worked: [hypothesis]

### Angle map
| # | Territory | Hook type | Changed vs winner | Held constant | Risk |
|---|---|---|---|---|---|

### Angle [n]: [name]
Audience tension: [..] | Length: [s] | Facts used: [F-ids]
Hook (0-2s): spoken "[..]" | on-screen "[..]" | first frame [..]
Body: [time] beat | [time] beat | [time] beat
Proof: [fact id or supplied review]
CTA: spoken "[..]" | on-screen "[..]" | button as labelled in your ad setup
On-screen text: T1 [time] "[..]", T2 [time] "[..]"
Shot list: | # | Time | Framing | Action | Audio |
Sound: [original / licensed for paid use / none]
Claim check: [claim -> fact id] | Rights check: [..]
(repeat for N angles)

### Test plan
Control: original winner, unchanged | Metric: [..] | Floor: 3,000 impressions per ad (T02) | Window: [dates, lag]

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps and approval needed
[missing item] -> [verdict prevented]. [launch] -> [named owner].
````

## Practical example

Illustrative numbers only. Product: SnapLid, a set of 6 silicone food-bowl lids (fictional). Facts: F1 fits bowls 10 to 30 cm; F2 dishwasher safe; F3 BPA-free, certificate supplied; F4 passed an internal 24-hour leak test, sheet supplied; F5 30-day returns; F6 price 24. Winner: a 24-second demo, creator flips a covered bowl and pours water. 14 days, spend 3,900, 62 reported purchases, CPA 62.9 against a 70 target, lag 7 days cleared, no T01 flag. Winner `confirmed` for that window.

Angle map: 1 objection reversal, 2 founder story, 3 comparison to cling film (category, no brand), 4 Sunday meal-prep routine, 5 creator diary (day 1, day 7).

Angle 1 in short: hook spoken "Silicone lids always pop off. Watch this." On-screen "Do they actually stay on?" First frame: hand holding a full bowl upside down, no lid visible. Body: 2 to 7s lid press and shake, 7 to 14s fit across three bowl sizes (F1), 14 to 20s dishwasher shot (F2). CTA at 20 to 24s: "Set of six, 30-day returns" (F6, F5). Claim check: "stays on" maps to F4, wording limited to the tested 24 hours. Shot list: 1 close-up flip, 2 shake, 3 three bowls, 4 dishwasher rack, 5 face-to-camera CTA. Sound: original voice only. Control: original winner. Metric: 2s rate first, then CPA after lag.

## Common failure modes

- Paraphrase remix: same hook type, new words. A test of it cannot separate the angle from the winner.
- Remixing a winner whose success came from the creator's personality; the angle may not transfer.
- Claim creep: a before-and-after or absolute word appears in a script that the fact sheet never supported.
- Changing offer, audience, or length together with the angle, so the read is uninterpretable.
- Using the winner's footage or music without confirming rights for new cuts.
- Treating a winner built on thin conversions as proof of the mechanism.
- Naming a competitor in a comparison angle without approval.

## Guardrails

- Do not write a claim that lacks a fact id from the supplied sheet.
- Do not present a new angle as proven; it stays `possible` until its own test matures.
- Do not repeat the winner's lines beyond a short brand phrase.
- Do not name competitors unless the user approved competitor mentions.
- Do not use footage, creator likeness, or sound whose rights scope is unknown.
- Do not change the offer, audience, and angle at the same time within one test.
- Do not launch, pause, or edit anything live; stop at an approval-ready script pack and test plan.
