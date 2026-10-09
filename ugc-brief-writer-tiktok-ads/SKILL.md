---
name: ugc-brief-writer-tiktok-ads
description: Writes a complete creator-facing UGC brief for TikTok ads, with viewer situation, one message, three hook options, scene structure, claims allowed and forbidden, do and don't lists, disclosure, usage rights, and a Spark authorization note, plus an internal approval checklist. Use when the user says "write a UGC brief for TikTok", "brief a creator", "I need a creator script with approved claims", "what rights do I need to run this creator video as an ad", or has product facts and needs something a creator can film from.
---

# UGC Brief Writer - TikTok Ads

## Use this skill when

A creator will film a video that a brand may run as a paid TikTok ad, and the brief must protect factual claims and usage rights without killing the creator's voice. Output has two parts: a creator-facing brief in plain language and an internal approval checklist the creator never sees.

Common requests:

- "Write a UGC brief for this product."
- "Brief three creators on the same message with different hooks."
- "What claims can the creator make and what is off limits?"
- "Do we have the rights to run this as a Spark ad?"

### When not to use

- Scripting inside the brand's own team, from a winning ad -> `winning-ad-remix-tiktok-ads`.
- Mining comments for what to address -> `comment-objection-miner-tiktok-ads` first, then feed the clusters in here.
- Judging whether a finished video hooks -> `hook-rate-scorer-tiktok-ads`.
- Comparing the creator's post as a Spark ad against a brand-handle upload -> `spark-vs-brand-ad-split-tiktok-ads`.

## Required input

Minimum, or the brief stays a draft:

- Product fact sheet with ids (F1, F2...): what it is, who it is for, price, variants, offer and end date.
- Claims: allowed verbatim, allowed with a qualifier, prohibited. Sensitive categories need a human reviewer named.
- Viewer situation: who watches, what they want, what stops them.
- Deliverables: number of videos, length range, delivery date, review rounds.
- Disclosure rules for the creator's market, confirmed by the named approval owner.
- Usage rights scope: organic posting, paid use as a brand-handle ad, Spark authorization, duration, territories, edits, raw files.
- Approval owner (a named person) and the contact the creator replies to.

Optional: prior creative notes, comment clusters (`comment_cluster`), a winner transcript for tone, competitors not to name, brand do and don't, reference videos.

Performance history may shape direction ("problem-first openings have been tested") as a `hypothesis`. It is never a promise to the creator about results.

## Analysis workflow

1. State the creator job in one line (show X, say Y, to viewer Z) and the viewer situation in one line.
2. Convert every fact into a showable proof moment: what is on camera, what is said. A fact that cannot be shown or said safely is internal-only.
3. Build the claims ladder: allowed verbatim, allowed with a qualifier, never say. Each entry cites a fact id or an approver name.
4. Draft the structure as scenes with time ranges: hook (first 2 seconds), problem, proof, use, CTA. Mark each beat Mandatory or Creator-owned.
5. Ask for three distinct hook options per creator, each with a first line and a first frame. Later reads use T02 (2-second view rate after 3,000 impressions).
6. Write do and don't lists for filming (vertical, phone, light, sound, captions, safe zone, logos, other brands, minors, personal data in frame).
7. Fill the rights and disclosure block field by field. Every field is Yes, No, or `needs_data`; none stays blank.
8. Add the Spark authorization note and the review loop (rounds, what can be corrected, what is creator-owned).
9. Run the approval checklist. Any unchecked item is a `hold` on sending the brief.
10. State the measurement plan: which hooks, which metric (`hook-rate-scorer-tiktok-ads`), and which format comparison, if any.

## Spark authorization note

Spark Ads run an existing post from the creator's handle as an ad. That depends on a permission the creator grants, as labelled in the TikTok app and your Ads Manager. It is separate from content usage rights: a signed paid-usage clause does not by itself record Spark authorization. Record four things in writing: whether Spark is intended, the scope and duration the creator agreed, who at the brand holds the authorization, and how the creator can revoke it. This skill records the agreement; it never grants or approves a permission, and the exact authorization steps are as labelled in your Ads Manager.

## Claims ladder

Fill this before writing scenes. Every row cites a fact id or a named approver.

| Tier | Meaning | Illustrative skincare example | Source |
|---|---|---|---|
| Verbatim | Creator may say it exactly | "Fragrance-free" | F1 |
| Qualified | Allowed only with stated wording or a true condition | "Works for my routine", from real use | Creator's own use |
| Never | Forbidden in every context | "Clears acne", "dermatologist approved" | Prohibited list |
| Internal only | True but not for the video | Margin, supplier name | Fact sheet |

## Review loop and creator freedom

| Item | Brand may request a change | Creator-owned |
|---|---|---|
| Facts, claims, and numbers on screen | Yes | No |
| Disclosure and rights fields | Yes | No |
| Offer wording and end date | Yes | No |
| Voice, humour, outfit, setting | Only for a brand-safety issue | Yes |
| Hook wording | Only if a claim breaks | Yes, within the three-option rule |

Agree the number of revision rounds in the snapshot. A change request names the claim or field it protects; "make it more polished" is not a reason in a native-style ad.

### Writing rules for the creator-facing part

- Plain language, one short paragraph per field. No jargon such as ROAS, CPA, or learning phase.
- Do not share spend, targets, internal CPA goals, or the internal checklist with the creator.
- Briefing several creators: keep the message and claims ladder identical, vary the hook and setting per creator, so later reads can separate message from persona.
- Give reference videos as feel, not as shots to copy.

## Decision rules

| Condition | Verdict | Next step |
|---|---|---|
| Fact sheet missing or facts conflict | `needs_data`, `hold` on sending | Supply the sheet |
| Claims list missing for a sensitive category | `hold` | Named reviewer approves claims |
| Rights scope blank (paid use, duration, territory) | `needs_data`, `hold` on paid use | Fill the rights block |
| Spark intended, authorization scope or duration not recorded | `hold` on Spark; organic use may proceed if rights allow | Record it in writing |
| Disclosure wording unconfirmed | `hold` | Approval owner confirms |
| Fewer than 3 hook options requested | Revise brief | Restore the hook block |
| All checklist items pass | `approval_needed` | Named owner approves sending |

Thresholds belong to measurement, not to the brief: T02 reads hooks after 3,000 impressions; T05 treats about 25 results or 7 days as learning-sensitive when the finished video later runs.

## Output format

````markdown
## Creator brief (share this part)
**Snapshot:** brand [..] | product [..] | deliverables [n videos, length range, 9:16] | due [date] | reply to [name] | review rounds [n]
**Who you are talking to:** [viewer situation, one paragraph]
**One message:** [one sentence the viewer should leave with]
**Hook options (give 3):** each with first line and first frame, inside the first 2 seconds. Start on the thing, not on a greeting.
**Scenes:**
| Time | Beat | What the camera shows | Say it your way or say exactly | Mandatory / yours |
**Show on camera:** [proof moments from facts]
**You can say (verbatim):** [..]  **You can say with this qualifier:** [..]  **Never say:** [..]
**Do:** [..]  **Don't:** [..]
**Look and feel:** native phone video, your own voice, real setting; reference [..]
**Disclosure:** [wording and label, as required in your market and as shown in the TikTok app]
**Rights:**
| Item | Agreed (Yes / No / needs_data) | Scope, duration, territory |
|---|---|---|
| Organic post on your handle | | |
| Paid use as a brand-handle ad | | |
| Spark authorization | | |
| Edits, cutdowns, captions, translations | | |
| Raw files delivered to the brand | | |
| Music or sound in the video | | |
| Exclusivity or category limits | | |
**Spark authorization:** [intended or not; what you agree to; how you can revoke it]
**Delivery and review:** [draft date, rounds, what we may ask to fix: facts, claims, disclosure; yours: voice, humour, setting]

## Internal approval checklist (do not share)
[ ] Each claim maps to a fact id or approver [ ] Disclosure confirmed [ ] Rights block complete [ ] Spark scope recorded or marked not intended [ ] 3 hook options requested [ ] Sensitive-category reviewer named [ ] Measurement plan set

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps and approval needed
[missing item] -> [verdict prevented]. [sending the brief] -> [named owner].
````

## Practical example

Illustrative content only. Product: a fragrance-free gel cleanser (fictional). Facts: F1 fragrance-free, ingredient list supplied; F2 120 ml; F3 used morning and evening per the label; F4 price 18; F5 30-day returns. Prohibited: treating or curing any skin condition, any "dermatologist" wording without written approval, results in a number of days, before-and-after skin photos. Reviewer for skincare claims: named in the checklist.

This brief asks a creator for a 20 to 30 second morning routine, phone-shot at a bathroom sink. Message: a simple cleanser with no added fragrance. Hooks to request: (1) first frame is the bottle on the sink, line "Three products out, one in"; (2) on-screen text "Fragrance-free and I can tell" over a pump-and-lather shot; (3) a question to camera about what is in the shower caddy. Verbatim allowed: "fragrance-free" (F1). Qualifier: "works for my routine" only as personal experience, and only if the creator actually used it. Disclosure wording confirmed by the approval owner. Rights: organic post Yes; paid use as a brand-handle ad, 6 months, one territory; Spark authorization intended, scope and duration to be recorded before boosting; raw files delivered.

Check: Spark scope still blank, so verdict is `hold` on Spark use, `needs_data` for the field, while the organic use may proceed. Everything else passes, severity `medium`, business impact `brand_safety`. Next step: the brand's rights owner fills the Spark row.

## Common failure modes

- Scripting every word; creators lose their voice, and the video reads as an ad in the first second.
- A claim list that says what is allowed but not what is forbidden, so the creator improvises a medical-sounding line.
- Treating a paid-usage clause as Spark authorization.
- Missing raw-file rights, so cutdowns, captions, and translations cannot be made later.
- Gifted product treated as no disclosure needed; disclosure rules depend on the market, not on payment form alone.
- Briefing one hook and calling it a test.
- Quoting a creator's earlier hit and implying the same result is expected.
- Copy that mentions an offer after its end date.

## Guardrails

- Do not put a claim in the brief that lacks a fact id or a named approver.
- Do not ask a creator to state an experience they have not had; personal statements must be true.
- Do not treat usage rights and Spark authorization as one permission; record them separately.
- Do not promise performance, earnings, or results to a creator or the brand.
- Do not leave rights, disclosure, or approval-owner fields blank; mark them `needs_data`.
- Do not name competitors or show third-party logos unless approved.
- Do not approve, grant, or change any permission or live ad; stop at a brief awaiting a named approver.
