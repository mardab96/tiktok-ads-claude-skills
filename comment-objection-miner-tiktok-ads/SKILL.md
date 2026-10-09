---
name: comment-objection-miner-tiktok-ads
description: Strips personal data from TikTok ad comments, clusters them into objections, questions, proof requests, and noise with counts, links each cluster to product facts, and drafts reply options and hook ideas for approval. Use when the user pastes TikTok comments and asks "what are people objecting to", "mine the comments for hooks", "draft replies to these comments", "what do viewers keep asking", or wants an FAQ and creative briefs built from comment themes.
---

# Comment Objection Miner - TikTok Ads

## Use this skill when

Comments on a TikTok ad or Spark post hold the doubts that stop a viewer from buying. Sort them into clusters with counts, match each to what the product facts can honestly answer, and turn them into reply drafts, hook ideas, and FAQ candidates. Personal data is removed first, every time.

Common requests:

- "What are people objecting to under this ad?"
- "Mine these comments for hooks."
- "Draft replies to the top questions."
- "What should the next creator brief address?"

### When not to use

- The user wants full scripts from a winner -> `winning-ad-remix-tiktok-ads`.
- The user wants a creator brief -> `ugc-brief-writer-tiktok-ads` (feed the clusters in).
- The comments point at the page ("is this legit", "where is the price") -> confirm with `landing-page-match-tiktok-ads`.
- A customer-service complaint needs resolving -> the brand's support owner; this skill only flags it.

## Required input

- The comment corpus: pasted or exported text from the ad or Spark post comments, as available in your account. Fields: `comment text`, `date`, `ad id` or `post id`. Optional: `like count`, `reply count`, whether the comment is a reply. Remove handles and names before pasting if you can; the skill strips any that remain.
- Source and size: which ad, date range, and the total comment count versus the count supplied. A sample is a sample; say how it was picked.
- Product fact sheet with ids (F1, F2...), existing FAQ or support macros, claim restrictions, reply tone, market and language.
- Offer and price at the time of the comments, so objections can be read in context.

Optional: landing page text, creator brief, earlier clusters for comparison.

## Before analysis: PII strip

Do this first and report a redaction log with categories and counts only, never the removed values.

1. Remove @mentions, usernames, display names, profile links, emails, phone numbers, order or tracking numbers, street addresses, and locations finer than a country or region.
2. Assign neutral ids (C001, C002...). Never keep a field that could point back to a person.
3. Generalise sensitive personal disclosures. A comment about a personal health condition becomes a theme such as "skin sensitivity concern"; do not quote it.
4. Exclude comments that indicate a minor.
5. Quote only anonymised fragments of about 15 words or fewer [heuristic], or paraphrase. Never present a commenter's wording as a testimonial or reuse it in an ad without permission.
6. Do not attempt to match a comment to a person, order, or customer record.

## Analysis workflow

1. Run the PII strip and write the redaction log. Count comments before and after exclusion.
2. Assign each comment one primary cluster from the taxonomy below, plus an optional secondary. One comment is one count.
3. Count per cluster and show two denominators: share of the supplied corpus, and share of classifiable comments (corpus minus noise). Treat clusters of two or fewer comments as anecdote [heuristic].
4. Link each cluster to a fact id or mark it `needs_data` when no fact answers it. A cluster with no supporting fact is a gap, not a license to improvise.
5. Check for claim risk: comments where viewers assert outcomes or medical effects. These are `hold`; the brand must not echo them.
6. Draft the creative response per cluster: a public reply option, a hook idea, and an FAQ or page change where relevant.
7. Flag escalations: safety complaints, delivery disputes, legal threats, minors, personal data. These go to a named human, with no public reply drafted.
8. Mark which items are requests the product cannot meet and which are misunderstandings the ad can fix.

### Cluster taxonomy

| Cluster | What it looks like | Typical route |
|---|---|---|
| Price or value | "Is it worth that?" | Fact on price, returns |
| Efficacy | "Does it actually work?" | Demo, allowed proof only |
| Fit or compatibility | "Will it work for my X?" | Fact or `needs_data` |
| Safety or ingredients | Questions on materials, ingredients | Fact sheet, reviewer |
| Trust or legitimacy | "Is this a scam?" | Page trust signals |
| Shipping or availability | Delivery time, where to buy | FAQ, page |
| How to use | Setup, routine questions | Creator demo |
| Comparison | "How is it different from Y?" | Comparison angle, no unapproved names |
| Proof request | Asks for reviews, demos, results | Allowed proof only |
| Post-purchase complaint | Order or quality issue | Support owner |
| Praise | Positive statements | Do not reuse without permission |
| Tag-a-friend, spam, off-topic | Noise | Excluded from shares |

## Decision rules

Comment frequency is `confirmed` only for the supplied corpus and window. Selection bias applies: commenters are not buyers and not a random sample.

| Condition | Verdict | Next step |
|---|---|---|
| Cluster counted in the supplied corpus | Count `confirmed` for that corpus | Report with both denominators |
| Cluster claimed to suppress conversions | `possible` | Test a response in creative, read via `hook-rate-scorer-tiktok-ads` |
| Cluster has a supporting fact | Response ready | Draft reply and hook; `approval_needed` |
| Cluster has no fact | `needs_data` | Owner supplies the fact or the cluster stays unanswered |
| Commenters assert medical or outcome claims | `hold` | Do not echo; reviewer decides |
| Complaint, safety, or personal-data content | Escalate | Named human; no public reply drafted |
| Corpus is small or one-sided | `monitor` | Collect more comments |
| Product change requested | `possible` | Brand owner decides |

No numeric register threshold applies to comments. If a later read of a hook built from a cluster is needed, T02 sets the floor (3,000 impressions).

## Output format

````markdown
### Redaction log
Comments in: [n] | Excluded: [n] (reasons by category) | Fields removed: [categories and counts] | Window: [dates] | Source: [ad or post id] [comment_cluster]

### Objection bank
| Theme | Anonymized wording | Count | Share of corpus | Share of classifiable | Fact support | Creative response | Verdict |
|---|---|---|---|---|---|---|---|

### Reply drafts (approval_needed)
| Cluster | Reply option (1 to 2 sentences, facts only, no tags, no personal data) | Fact id | Do not say |
|---|---|---|---|

### Hook ideas
| Cluster | First line | First frame | Answers with (fact id) | Feeds |
|---|---|---|---|---|
(Feeds = `winning-ad-remix-tiktok-ads` or `ugc-brief-writer-tiktok-ads`)

### FAQ and page candidates
[question] -> [answer from fact id] -> [where it goes]

### Escalations
[category] -> [named human]. No reply drafted.

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Data gaps and approval needed
[missing item] -> [verdict prevented]. [publishing a reply] -> [named owner].
````

## Practical example

Illustrative numbers only. A hair-styling tool ad: 143 comments supplied, 3 excluded as possibly from minors, 140 analysed. Redaction log: handles and mentions removed from most comments.

Cluster counts (primary, share of 140): price or value 31 (22.1%), fit for thick or curly hair 27 (19.3%), shipping 14 (10.0%), trust or legitimacy 12 (8.6%), proof request 9 (6.4%), praise 22 (15.7%), tag-a-friend 17 (12.1%), spam 8 (5.7%). Classifiable comments: 140 minus 25 noise = 115, so price is 27.0% of classifiable.

Facts: F1 ceramic plates; F2 three heat settings; F3 price 59 with 30-day returns; F4 ships within 2 business days. No fact covers thick or curly hair, so that cluster is `needs_data`, severity `medium`, impact `conversion`.

Reply (price, F3): "It is 59 and comes with a 30-day return window, details are on our page." Hook for price: first line "Is it really 59? Here is what is in the box", first frame the open box, feeds `ugc-brief-writer-tiktok-ads`. Hook for fit: held until the owner supplies a tested-hair-type fact. Escalation: none. Verdict: the counts are `confirmed` for this corpus; price as a barrier is `possible`, to be tested in creative.

## Common failure modes

- Treating the loudest comment as a theme; count first.
- Reading comments as buyer research; commenters self-select.
- Answering an unsupported fit or efficacy question with a confident reply.
- Echoing a viewer's outcome or medical claim in a brand reply.
- Using praise comments as testimonials without permission.
- Mixing comments from several ads or dates into one count without saying so.
- Forgetting that a Spark post carries comments from before the ad ran; date the corpus.
- Replying publicly to a support complaint with order details.

## Guardrails

- Do not output, quote, or retain handles, names, links, contact details, or order data; log redaction by category and count only.
- Do not quote more than a short anonymised fragment, and never as a testimonial.
- Do not draft a reply or hook that makes a claim without a fact id.
- Do not reply to or amplify comments that assert medical or outcome claims.
- Do not treat comment counts as audience-wide or as proof that an objection suppresses conversions.
- Do not post, reply to, hide, or moderate any comment; stop at drafts awaiting a named approver.
- Do not draft public replies for safety, legal, minor, or personal-data cases; escalate them.
