# Copy-paste prompts

Run these after the documented install. Attach a file to Claude, or use an absolute installed path such as `~/.claude/skills/tiktok-ads-shared/examples/data/fatigue_daily.csv`. Paths written inside a `SKILL.md` are for that skill's own location, not for your shell working directory.

## Creative Fatigue Detector

```text
Use Creative Fatigue Detector for TikTok Ads.
Attached: daily export with date, ad, impressions, clicks, conversions, spend, frequency.
Context: objective, conversion lag, audience changes, and budget changes.
Run the attached file with ~/.claude/skills/tiktok-ads-shared/scripts/fatigue_scan.py if appropriate.
Return T01 status, alternate explanations, a retained control, and an approval-ready refresh queue.
```

## CPA Spike Diagnosis

```text
Use CPA Spike Diagnosis for TikTok Ads.
Attached: baseline/current CSV with period, cost, impressions, clicks, conversions; change log; Events Manager diagnostics.
Run ~/.claude/skills/tiktok-ads-shared/scripts/cpa_decompose.py where useful.
Return CPM, CTR, CVR, CPA, T04 verdict, ranked evidence, residual uncertainty, and what to hold.
```

## Wasted Spend Finder

```text
Use Wasted Spend Finder for TikTok Ads.
Target CPA: [currency and value]. Conversion lag: [days].
Attached: daily CSV with date, level, name, spend, conversions, plus diagnostics and test context.
Run ~/.claude/skills/tiktok-ads-shared/scripts/wasted_spend.py with --target-cpa and --conversion-lag-days.
Keep recent rows excluded and return review candidates, never automatic pauses.
```

## GMV Max Profit Check

```text
Use GMV Max Profit Check for TikTok Shop.
Attached: product CSV with revenue, refunds, affiliate commission, coupons, referral fees, ad spend, COGS, and seller shipping if available.
Run ~/.claude/skills/tiktok-ads-shared/scripts/gmv_profit.py.
Separate GMV, visible contribution before COGS, and profit. List every missing cost field.
```

## Weekly Client Report

```text
Use Weekly Client Report for TikTok Ads.
Week, comparison, timezone, primary event, attribution setting, and client goal: [paste].
Attached: Ads Manager export, change log, creative notes, diagnostics, and independent report if available.
Write client narrative, scorecard, material changes, three actions with owners, approvals, and data gaps.
```