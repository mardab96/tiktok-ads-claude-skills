# TikTok Ads shared scripts

All helpers use Python 3 standard library, make no network calls, and leave input files unchanged.

| Script | Skill | Required guard |
|---|---|---|
| `fatigue_scan.py` | Creative Fatigue Detector | fourteen distinct dates per ad |
| `cpa_decompose.py` | CPA Spike Diagnosis | baseline/current impressions, clicks, and conversions |
| `wasted_spend.py` | Wasted Spend Finder | target CPA and conversion lag days |
| `gmv_profit.py` | GMV Max Profit Check | every visible cost cell parseable |

Run the source checks with `python3 validate-skills.py` and `python3 selftest.py`. Install checks use `sh verify_install.sh <repo-url-or-local-path> <count>`.