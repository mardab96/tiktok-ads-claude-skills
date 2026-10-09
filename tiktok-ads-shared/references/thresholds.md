# Threshold register

This file owns every numeric decision threshold in the pack. These thresholds are decision aids, not performance promises. A skill cites its T-ID instead of copying its number.

## TikTok platform guidance

- **T01, Creative Fatigue Detector:** Review an ad only after both seven-day windows have at least 3,000 impressions. Flag a fatigue candidate when frequency rises at least 20% and CTR falls at least 20% [heuristic]. A larger floor reduces false calls caused by a small delivery sample.
- **T02, Hook Rate Scorer:** Review a hook when its 2-second view rate is at least 25% below the comparable account median after at least 3,000 impressions [heuristic]. Compare like objective, audience, and format.
- **T03, Wasted Spend Finder:** Review a mature row when spend reaches at least 1.5 times target CPA, reported conversions are zero, and the row has cleared the documented conversion lag [heuristic].
- **T04, CPA Spike Diagnosis:** Escalate a mature CPA movement when current CPA is at least 30% above a comparable baseline and each window has at least 10 reported conversions [heuristic].
- **T05, Learning Phase Guard:** Treat a conversions campaign or ad group as learning-sensitive until about 25 campaign results or 7 days since entry, whichever gives the account its available platform evidence [platform guidance]. Source: [TikTok Learning Phase](https://ads.tiktok.com/help/article/learning-phase?lang=en), June 2026.
- **T06, Budget Scaling Planner:** For post-learning Maximum Results campaigns, TikTok says to increase ad-group budget by at least 20% at a time and reassess cost volatility [platform guidance]. Keep one documented budget action per observation window as a pack heuristic. Source: [TikTok bidding best practices](https://ads.tiktok.com/help/article/best-practices-for-bidding-strategies), August 2026.
- **T07, Attribution Gap Check:** Escalate reconciliation when the TikTok-to-independent conversion ratio moves at least 20% relative to a documented baseline ratio, after dates, timezone, event definition, and attribution setup match [heuristic]. It is a change-from-baseline signal, not an absolute source difference.
- **T08, Placement Review:** Review a placement after at least 3,000 impressions when its CPA is at least 30% above the campaign average and the conversion lag has passed [heuristic]. A higher floor makes a placement comparison less fragile.
- **T09, GMV Max Profit Check:** Treat the cost stack as incomplete when revenue, refunds, affiliate commission, coupons, referral fees, or ad spend is absent or unparseable [heuristic]. COGS and seller-borne shipping are additional required inputs for a profit claim.
- **T10, Pixel and Events API Check:** Escalate a tracking investigation when a primary event falls at least 30% while clicks stay within 10% of baseline over comparable seven-day windows [heuristic].

## Current naming for bid strategy

TikTok’s September 2026 help page lists **Maximum Results** and **Target Cost per Result** as its two available bidding strategies. Older account language such as Maximum Delivery, Lowest Cost, Cost Cap, Bid Cap, Target ROAS, or Minimum ROAS may appear in historical exports or user requests, so skills preserve it only as a trigger and ask for an account screenshot before mapping it. Source: [Available bidding strategies](https://ads.tiktok.com/help/article/bidding-strategies), September 2026.