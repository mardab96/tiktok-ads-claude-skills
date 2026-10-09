---
name: pixel-events-api-check-tiktok-ads
description: Checks TikTok Pixel and Events API health from Events Manager screenshots and an Ads Manager export, covering event match signals, event_id deduplication between browser and server events, parameter completeness on value events, and primary-event drops against stable clicks (T10). Use when a TikTok media buyer says "purchases dropped but clicks are flat", "check our TikTok pixel", "is Events API deduplicating", "Events Manager shows a diagnostic warning", "TikTok value does not match our orders", or before any bid, budget, or scale call that depends on TikTok conversion data.
---

# Pixel and Events API Check: TikTok Ads

## Use this skill when

A buyer needs to know whether TikTok receives the conversion signal it optimises toward, before anyone acts on CPA, ROAS, or learning-phase behaviour. Diagnosis runs from Events Manager screenshots plus an Ads Manager export. A TikTok for Business connector in Claude helps when present and is never required.

Typical requests:

- "Purchases in TikTok fell off a cliff yesterday but traffic looks normal."
- "We added Events API through our Shopify app. Are we double counting now?"
- "Events Manager shows a warning on CompletePayment. Does it matter?"
- "Purchase value in TikTok is far off our order totals."
- "Before we change bidding, confirm tracking is clean."

Do not use this skill when:

- TikTok and GA4, Shopify, or CRM disagree while each source looks internally healthy. Run `attribution-gap-check-tiktok-ads`.
- CPA rose and event counts still track clicks. Run `cpa-spike-diagnosis-tiktok-ads`.
- Event volume holds and conversion rate fell after a page or offer change. Run `landing-page-match-tiktok-ads`.
- A TikTok Shop order and fee question sits behind the request. Run `gmv-max-profit-check-tiktok-ads`.

## Required input

Tracking diagnosis needs both sides: what the site sent and what TikTok received. Screenshots are enough.

From Events Manager (start in **Assets** or **Events Manager**, as labelled in your account), select the data source and capture:

1. Overview: data source name, connection method (Pixel, Events API, or both), last received time.
2. Event list: each event name with volume for the last 14 days, plus the browser and server split where shown.
3. Diagnostics: every message with its date and the affected event, copied as text where possible.
4. Matching or event quality view for each primary event, as labelled in your Events Manager.
5. Event detail or parameter view for each primary event, showing which parameters arrive (value, currency, content_id, content_type).
6. Test Events view from one fresh test purchase or lead, if the team can run one safely.

From Ads Manager, a daily campaign-level export covering 28 days, with these columns as labelled in your export: Date, Campaign name, Optimization event, Cost, Impressions, Clicks (destination), Conversions, Cost per conversion, and Total purchase value or conversion value where relevant. Twenty-eight days gives a clean seven-day baseline and current window for T10 plus room for lag.

From the business:

- Site URL and platform (Shopify, WooCommerce, custom build, app).
- Events treated as primary, with the user action that should fire each one.
- Conversion lag in days for the primary event.
- Dated change log: theme, checkout, consent banner, tag manager, Events API partner or gateway changes.

Every missing item becomes `needs_data` in the output, named, together with the conclusion it blocks.

### Optional input

- Backend order or lead count per day for the same dates (`shop_export` or `analytics_export`). It separates a tracking loss from a real demand drop.
- Developer notes or payload samples showing how event_id is generated on browser and server.
- Consent banner configuration and the regions it applies to.

## Before analysis

1. Confirm which data source each campaign uses. Accounts with several pixels or a legacy pixel next to a new one often optimise toward a source nobody watches.
2. Confirm the primary event name per campaign from the ad group setup screenshot, since export column names can hide which event counts as a conversion.
3. Record the conversion lag and drop lag days from the current window before reading any trend.
4. Ask whether anyone ran test purchases or test leads in the period; those inflate small counts and belong in the notes.

## Analysis workflow

1. Build the event map. List every event the data source receives, mark which event each campaign optimises toward, and note whether it arrives from browser, server, or both. A campaign optimising toward an event the business does not treat as primary is a finding on its own.
2. Read diagnostics as dated evidence. Record each message, its date, and the affected event. Diagnostics confirm that an implementation signal exists; they never size lost revenue.
3. Run the T10 check. Compare the primary event and clicks across two comparable seven-day windows with lag days removed from the current window. Escalate when the event falls at least 30% while clicks stay within 10% of baseline (T10).
4. Check deduplication wherever Pixel and Events API send the same event. Both payloads need the same event name and the same event_id for one real action. Warning signs: reported events near double the backend count, event_id present on only one side, or an event_id built from a value generated twice (for example a timestamp created separately in browser and server).
5. Check event match signals. Read the matching or quality view for each primary event and list the customer parameters that arrive (hashed email, hashed phone, external_id, ttclid, IP, user agent, as labelled). A server event with few match parameters can arrive on time and still attribute poorly.
6. Check parameter completeness. Purchase-type events need value and currency on every event, a currency that matches the store, and a value that follows the order total definition the business uses (with or without tax and shipping). Catalog-linked events need content_id values that match catalog IDs.
7. Put the change log on the event timeline. A drop that starts on a deploy date is `likely` tied to it. Confirmation needs a Test Events failure, a matching diagnostic, or a developer check.
8. Cross-check backend counts when supplied. Backend orders stable while TikTok events fell points at tracking. Backend orders falling by a similar share points at demand, offer, or site, and routes away from this skill.
9. Write the handoff: what a developer checks, which media actions a buyer holds, and which counts will prove the fix.

## Decision rules

| Condition | Evidence | Verdict | Next step |
|---|---|---|---|
| Primary event down at least 30% while clicks stay within 10% of baseline, mature windows (T10) | `ads_export` + `events_diagnostics` | `likely` tracking loss; `confirmed` only with a Test Events failure or matching diagnostic | Developer handoff; `hold` budget, bid, and creative kills on affected campaigns |
| T10 met and backend orders fell by a similar share | `ads_export` + `shop_export` | `possible` tracking issue, demand or site cause stronger | Route to `cpa-spike-diagnosis-tiktok-ads` or `landing-page-match-tiktok-ads` |
| Browser and server send one action without a shared event_id | `screenshot` of setup or payload | `confirmed` dedup gap | `approval_needed` from site owner for event_id fix before value-based bidding work |
| Reported-to-backend ratio jumps on the day Events API went live | `events_diagnostics` + `shop_export` + `change_log` | `likely` double counting | Same as above; remeasure one full week after fix |
| value or currency missing or wrong on purchase events | `events_diagnostics` or `screenshot` | `confirmed` | `hold` value-based bid decisions; route to `bid-strategy-check-tiktok-ads` after fix |
| Diagnostic warning present while events track clicks | `events_diagnostics` | `monitor` | Log it in the normal developer queue |
| Fewer match parameters than the implementation claims to send | `screenshot` of matching view | `possible` attribution loss | Developer check of advanced matching and server payload |
| Diagnostics capture or click export missing | none | `needs_data` | Request the named capture |

T10 opens an investigation. Revenue lost stays unsized unless a backend comparison supplies it.

## Output format

```markdown
## Pixel and Events API Check: [data source], [dates], [timezone]

**Verdict:** [shared verdict label] because [strongest evidence]
**Primary event(s):** [names] | **Connection:** [Pixel / Events API / both] | **Lag excluded:** [days]

### Event map
| Event | Source (browser / server / both) | Optimised by | Business meaning | Status |
|---|---|---|---|---|

### T10 window check
| Window | Dates | Clicks | Primary events | Change vs baseline |
|---|---|---|---|---|
| Baseline | | | | |
| Current | | | | |
T10 result: [met / not met / needs_data]

### Deduplication and parameters
- event_id on browser: [yes / no / unknown]; on server: [yes / no / unknown]; shared per action: [yes / no / unknown]
- value and currency on purchase events: [finding + evidence tag]
- content_id matches catalog: [finding + evidence tag]
- Match parameters seen: [list]

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Developer handoff
1. [check] | owner: [name] | verify by: [Test Events run or count comparison]

### Media actions on hold
- [campaign and action] held until [condition]

### Remeasurement plan
[windows, counts, and ratio that will show the fix worked]

### Data gaps
- [missing item]: blocks [conclusion]
```

## Practical example

Illustrative numbers for a fictional store, not a benchmark. A Shopify skincare brand optimises one campaign toward CompletePayment. Baseline week: 4,210 clicks and 162 CompletePayment events. Current week: 4,050 clicks (down 3.8%) and 88 events (down 45.7%). T10 is met. Shopify shows 151 orders in the current week against 158 in the baseline, so demand held.

Change log shows a new checkout extension deployed on day two of the current week. Events Manager lists a diagnostic on CompletePayment dated that same day. Event source view shows server events continuing while browser events stopped.

Output: tracking loss is `likely`, severity high, impact `measurement`. Developer handoff asks to confirm the browser purchase event fires on the new checkout and that browser and server share one event_id once restored, so the repair does not swing into double counting. Media actions on hold: no budget cut, no creative kills, and no bid change on that campaign, because its CPA for the affected days is inflated by missing events. Remeasurement: one full seven-day window after the fix, with the TikTok-to-Shopify ratio back inside its pre-change range.

## Common misreads

- Calling tracking broken from CPA alone. CPA rises for auction, creative, and page reasons; T10 needs the click comparison.
- Treating a diagnostics warning as proof of lost sales. Some warnings coexist with healthy volume.
- Celebrating a jump in conversions in the week Events API launched. A missing or mismatched event_id can double the count overnight.
- Expecting TikTok events to equal Shopify orders. Click and view windows make them differ; ratio stability over time is what matters, and that belongs to `attribution-gap-check-tiktok-ads`.
- Including lag days in the current window, which makes any week look like a drop.
- Missing a consent banner change in one region, which can cut browser events while server events continue.
- Reading website pixel events and TikTok Shop orders under GMV Max as one stream.

## Route to next

- Tracking confirmed healthy, CPA still up: `cpa-spike-diagnosis-tiktok-ads` (T04).
- Events healthy, gap with Shopify, GA4, or CRM moved: `attribution-gap-check-tiktok-ads` (T07).
- Fix shipped and campaigns need edits afterwards: `learning-phase-guard-tiktok-ads` (T05) before any live change.
- Value parameters repaired and the team wants a value-based bid change: `bid-strategy-check-tiktok-ads`.

## Guardrails

- Do not change pixel, Events API, consent, or site code. Output stops at a developer handoff.
- Do not label tracking `confirmed` broken without a Test Events failure, a diagnostic message, or a backend comparison.
- Do not estimate revenue lost from diagnostics alone.
- Do not recommend budget, bid, or creative changes on a campaign whose primary event met T10 until remeasurement is done.
- Do not ask for raw customer emails, phone numbers, or IP addresses; parameter coverage screenshots are enough.
- Do not invent Events Manager menu or metric names; quote what the screenshot shows.
