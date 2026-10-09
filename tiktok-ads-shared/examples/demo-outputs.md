# Demo outputs

Synthetic samples only. Script blocks below are real runs against files in this directory.

## Creative Fatigue Detector

```bash
python3 tiktok-ads-shared/scripts/fatigue_scan.py tiktok-ads-shared/examples/data/fatigue_daily.csv
```

```text
Demo ad    7    7    3500    3500    5.00%    3.00%    1.00    1.25    fatigue_candidate
Thin ad    2    0    0    0    0.00%    0.00%    0.00    0.00    insufficient_window
```

T01 marks Demo ad as a candidate. Thin ad has no mature seven-day comparison.

## CPA Spike Diagnosis

```bash
python3 tiktok-ads-shared/scripts/cpa_decompose.py tiktok-ads-shared/examples/data/cpa_periods.csv
```

```text
baseline  1000.00  100000  500  20.00  10.00  0.50%  4.00%  50.00
current   1200.00  100000  500  12.00  12.00  0.50%  2.40%  100.00
cpa_change_pct: 100.0%
T04_verdict: escalate
```

Arithmetic points to a CVR movement. It does not assign a cause.

## Wasted Spend Finder

```bash
python3 tiktok-ads-shared/scripts/wasted_spend.py tiktok-ads-shared/examples/data/wasted_spend.csv --target-cpa 100 --conversion-lag-days 7
```

```text
High-intent demo  180.00  0.00  n/a  review_candidate  180.00
Too recent sample 220.00  0.00  n/a  excluded_recent   0.00
```

Recent spend is excluded by lag before a waste conclusion.

## GMV Max Profit Check

```bash
python3 tiktok-ads-shared/scripts/gmv_profit.py tiktok-ads-shared/examples/data/gmv_profit.csv
```

```text
Starter kit       1000.00 445.00 555.00 complete_cost_stack
Incomplete refill n/a     n/a    n/a    incomplete_cost_stack / needs_data affiliate_commission
```

Visible contribution is not profit. Blank fees stay missing.