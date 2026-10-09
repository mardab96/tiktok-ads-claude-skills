---
name: landing-page-match-tiktok-ads
description: Compares a TikTok ad's spoken and on-screen promise with what a phone user sees on the first mobile screen after the tap, then checks in-app browser load friction and form or checkout friction, and writes a repair brief. Use when a TikTok media buyer says "CTR is fine but nobody buys", "the ad says one thing and the page says another", "check this landing page against our TikTok ad", "landing page views are way below clicks", "our TikTok lead form converts badly", or before scaling a winning TikTok creative onto a new page.
---

# Landing Page Match: TikTok Ads

## Use this skill when

An ad earns the tap and the page loses the visitor. TikTok traffic arrives inside an in-app browser, on a phone, seconds after a creator-style video. Whatever that video promised (product, price, bundle, code, result, audience) needs to be visible on the first mobile screen, load fast enough to be seen, and lead to a short path to the action. Work from screenshots, page text, and an ad script; a TikTok for Business connector in Claude is optional.

Typical requests:

- "Clicks look healthy, conversion rate on TikTok traffic is weak. Is it the page?"
- "Creator says 'two for one' and the page shows single-unit price."
- "Landing page views are far below clicks on this ad."
- "Our TikTok traffic bounces off the homepage."
- "Which page should our best TikTok ad point to?"

Do not use this skill when:

- Conversions may not be recorded. Run `pixel-events-api-check-tiktok-ads` first (T10), because an unmeasured page looks like a broken page.
- Hook or thumb-stop is the weak point and clicks are low. Run `hook-rate-scorer-tiktok-ads`.
- CPA moved and the page did not change. Run `cpa-spike-diagnosis-tiktok-ads` (T04).
- Viewers raise objections in comments that the page should answer. Run `comment-objection-miner-tiktok-ads`, then return here with the objection list.

## Required input

A match check needs three things: the ad promise, the page as a phone sees it, and funnel numbers per ad and URL. Fewer than three reduces the output to a generic page critique; say so.

Ad side:

- Video file or screen recording plus a transcript of the spoken opening, on-screen text, caption, CTA button label, and any discount code said or shown.
- Ad name, ad ID, and destination URL including parameters.

Page side (`landing_page`):

- Phone screenshots of the first screen as it loads from TikTok, then each scroll down to the primary CTA, the form, or the cart.
- A screen recording from tap to usable page inside the TikTok in-app browser, if possible. It shows popups, consent banners, and blank-screen time that a desktop audit misses.
- Page text or URL, plus the offer terms the business applies (price, bundle, code, shipping, guarantee).

Funnel side, Ads Manager export at ad level for the same dates, columns as labelled in your export: Ad name, Destination URL, Cost, Impressions, Clicks (destination), Landing page views or Page views if the account reports them, Conversions, Cost per conversion. Export from **Reporting** or the ad table and include the date range in the filename.

From the business: primary conversion action, conversion lag, and a dated release log for the page.

### Optional input

- Page speed report on mobile for the destination URL, or the site analytics load timing for TikTok sessions.
- Analytics export of TikTok sessions by landing page: sessions, engaged sessions, add to cart, checkout started, purchases or leads (`analytics_export`).
- Instant form setup screenshot when the campaign uses a TikTok lead form instead of a website.

## Before analysis

1. Confirm the conversion this page should produce: purchase, add to cart, lead, booking, or app install. Judge the page against that action only.
2. Confirm purchase or lead events are recorded on this URL. If T10 is met for the period, stop and route to `pixel-events-api-check-tiktok-ads`.
3. Open the destination URL exactly as the ad sends it, parameters included. A redirect to a homepage, a geo page, or a consent wall changes what the visitor sees first.
4. Check the release log. A page edit inside the comparison dates splits the period in two, and each half needs its own read.
5. Note whether the ad is a Spark Ad from a creator account. Visitors arrive expecting the creator's voice and product, so a polished brand page with a different look reads as a new conversation.

### TikTok instant forms

When a campaign uses a TikTok lead form instead of a website, apply the same promise map to the form intro screen and the questions. Check that the offer named in the video appears on the intro screen, that any fields the form fills in advance (where your form setup offers that) need only a confirm tap, and that each custom question changes how the lead is handled. Lead quality comes from the CRM, so instant form findings stay `possible` until qualified-lead data arrives.

## Analysis workflow

1. Extract the promise. From the transcript and on-screen text, list each promise element: product or variant shown, offer or price, code, outcome claimed, audience named ("for curly hair", "for landlords"), proof used (creator, review, demo), and CTA verb.
2. Read the first mobile screen. Record what sits above the fold on the supplied screenshot: headline, hero image, price, CTA button, and anything that covers them (cookie banner, email popup, app install bar, chat widget).
3. Match each promise element to the page and grade it: matched on first screen, matched below the fold, missing, or contradicted. Note the scroll depth where a below-fold match appears.
4. Check visual continuity. A creator-shot video landing on a studio-shot page with a different product colour or pack can break recognition even when the copy matches. Record it as a finding when the product shown differs.
5. Check load friction. Compare landing page views (or page views) with destination clicks per ad and URL, against other URLs in the same account and dates. A clearly weaker ratio on one URL, a blank or spinning first screen in the recording, or a redirect chain in the URL are load findings. No absolute speed threshold applies here; compare within the account.
6. Check form and checkout friction. Count required fields, flag fields the visitor cannot answer on a phone in the moment, forced account creation, a code that must be typed by hand, and shipping cost appearing only at the last step.
7. Separate observation from impact. Mismatch seen on a screenshot is `confirmed` as a mismatch. Its effect on conversion stays `possible` until funnel data per URL or a controlled page test supports it.
8. Write the repair brief: replacement first-screen headline, offer line, CTA label, what to remove from the first screen, form fields to cut or defer, and how to measure the change (same ad, same dates logic, conversion lag cleared).

## Decision rules

| Condition | Evidence | Verdict | Next step |
|---|---|---|---|
| Core offer or price said in the ad is absent from the first screen or contradicted | `creative_script` + `landing_page` | `confirmed` mismatch | Repair brief; `approval_needed` from page owner |
| Product or variant shown in video differs from page hero | `creative_script` + `landing_page` | `confirmed` mismatch | Swap hero or point ad to the variant page |
| Promise matched only after several scrolls | `landing_page` | `likely` friction | Move the matching element into first screen |
| Landing page views to clicks ratio clearly weaker than sibling URLs, same dates | `ads_export` | `likely` load friction | Request in-app recording; developer check of redirects and heavy assets |
| Overlay covers headline or CTA on first screen in TikTok browser | `screenshot` | `confirmed` | Suppress the overlay for TikTok traffic, owner decision |
| Required fields or steps the visitor cannot complete on a phone | `landing_page` | `confirmed` friction | Defer or remove the field; note qualification cost |
| Match looks good, conversion rate still weak, tracking unverified | `ads_export` | `needs_data` | Route to `pixel-events-api-check-tiktok-ads` (T10) |
| Conversion change claimed after a page edit, lag not cleared | `ads_export` + `change_log` | `hold` | Wait for lag, then compare |

## Output format

```markdown
## Landing Page Match: [ad name] to [URL], [dates]

**Verdict:** [page is primary bottleneck / contributing / not the issue / needs_data] because [strongest evidence]

### Promise map
| Promise element | In ad (quote + timestamp) | On page | Location (first screen / scroll depth / absent) | Match status | Evidence |
|---|---|---|---|---|---|

### First-screen read (phone, TikTok in-app browser)
- Visible: [headline, price, CTA, image]
- Covered by: [overlay or none]
- Load observation: [from recording or ratio]

### Friction list
| Step | Friction | Evidence | Fix |
|---|---|---|---|

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Repair brief
- First-screen headline: [current] -> [replacement]
- Offer line: [current] -> [replacement]
- CTA label: [current] -> [replacement]
- Remove from first screen: [...]
- Form or checkout change: [...]
- Measure by: [metric, URL, window after lag]

### Data gaps
- [missing item]: blocks [conclusion]
```

## Practical example

Illustrative numbers for a fictional brand, not a benchmark. A pet supplement brand runs a creator video: "Two tubs for the price of one, code CHEW at checkout, for dogs over seven." Over 14 days the ad drives 6,800 destination clicks and 41 purchases to a product page. A duplicate of the same video in the same ad group, pointed at the brand's bundle page, records 5,900 clicks and 88 purchases in the same dates.

Phone screenshots show the product page first screen: single-tub price, a hero shot of the puppy formula, and an email popup that covers the add-to-cart button after load. Bundle offer appears at the third scroll. Code field sits in a collapsed section at the last checkout step. Landing page views to clicks look similar across both URLs, so load is not singled out.

Output: offer mismatch `confirmed`, variant mismatch `confirmed` (puppy formula shown for a senior-dog promise), overlay `confirmed`. Conversion impact `likely`, supported by the same account's bundle page converting at a higher rate on comparable traffic. Repair brief: point the ad to the senior bundle page, headline "Senior dog chews: 2 tubs for the price of 1", auto-apply the code from the URL parameter if the store supports it, suppress the popup for TikTok traffic. Measurement: same ad, new URL, compared after the conversion lag clears.

## Common misreads

- Auditing the page on a desktop browser. TikTok traffic sees a phone screen inside the in-app browser, often with an extra top bar.
- Sending a winning creator ad to the homepage and blaming the creative.
- Treating "code in video" as matched while the visitor must remember and type it at the last step.
- Calling a low conversion rate a page problem while purchase events fail T10.
- Reading a page-speed score as the cause without a load observation from TikTok traffic itself.
- Fixing copy while the product shown in the video differs from the page hero.
- Changing the page and the ad in the same week, which leaves no way to tell which change moved the result.
- Comparing conversion rates between URLs that receive different ads, audiences, or offers and calling the gap a page effect.

## Route to next

- Weak tap-through before anyone reaches the page: `hook-rate-scorer-tiktok-ads`.
- Questions in comments the page never answers: `comment-objection-miner-tiktok-ads`.
- New creative needed to match the fixed page: `ugc-brief-writer-tiktok-ads`.
- Events missing on the page after a release: `pixel-events-api-check-tiktok-ads` (T10).

## Guardrails

- Do not score a page you have only seen described; ask for screenshots or page text.
- Do not edit or publish page changes. Output stops at an approval-ready repair brief.
- Do not present a projected conversion lift as a promise; frame it against the account's own baseline as a hypothesis.
- Do not recommend removing a lead qualification field without stating what qualification is lost.
- Do not judge load speed against a generic benchmark; compare URLs within the same account and dates.
