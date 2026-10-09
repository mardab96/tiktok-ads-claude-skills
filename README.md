# 20 Claude Skills for TikTok Ads

A public, MIT-licensed pack for agency media buyers and paid-social specialists. Every skill works from pasted TikTok Ads exports, screenshots, creative scripts, comments, and independent reports. Live access and TikTok for Business MCP are optional.

## What's inside

Twenty TikTok skills cover account triage, creative fatigue, hook quality, remixes, UGC briefs, Spark comparison, Smart+ audit, Search Ads, waste, Pixel and Events API, attribution, CPA spikes, learning phase, bidding, scaling, comments, landing-page match, TikTok Shop GMV, placement, and weekly client reporting. Each folder ending in `-tiktok-ads` contains one `SKILL.md`.

## How to install

Copy the skills and the pack-specific shared directory together. This avoids collision with other packs that use generic `scripts`, `references`, or `examples` directories.

```bash
git clone https://github.com/mardab96/tiktok-ads-claude-skills.git
mkdir -p ~/.claude/skills
cp -r tiktok-ads-claude-skills/*tiktok-ads tiktok-ads-claude-skills/tiktok-ads-shared ~/.claude/skills/
```

Start a new Claude Code session. Every installed skill resolves helpers through `../tiktok-ads-shared/`.

## Start here by effort to feed

| What you have | Start with |
|---|---|
| Brief, screenshots, script | Account Triage, UGC Brief Writer, Landing Page Match |
| Daily Ads Manager export | Creative Fatigue Detector, Wasted Spend Finder, CPA Spike Diagnosis |
| Events Manager and another source | Pixel and Events API Check, Attribution Gap Check |
| TikTok Shop cost data | GMV Max Profit Check, then Budget Scaling Planner |

## Quick start packs

- **New account:** Account Triage -> Pixel and Events API Check -> CPA Spike Diagnosis.
- **Creative refresh:** Creative Fatigue Detector -> Hook Rate Scorer -> Winning Ad Remix -> UGC Brief Writer.
- **Scale decision:** Attribution Gap Check -> Learning Phase Guard -> Budget Scaling Planner.
- **Weekly agency read:** Weekly Client Report -> owning specialist skill.

## Bring your data

Use Ads Manager CSV exports, Events Manager diagnostics, TikTok Shop Seller Center reports, creative recordings, mobile page captures, redacted comments, GA4, Shopify, CRM, and dated change logs. See [`tiktok-ads-shared/references/getting-your-data.md`](tiktok-ads-shared/references/getting-your-data.md).

## Guardrails

Skills do not make live account changes. They preserve missing data, conversion lag, attribution settings, and cost gaps. Platform-reported results remain separate from profit.

## Output standard

Evidence tags, verdict labels, and decision-table fields live in [`tiktok-ads-shared/references/output-standard.md`](tiktok-ads-shared/references/output-standard.md). Numeric rules have one home in [`tiktok-ads-shared/references/thresholds.md`](tiktok-ads-shared/references/thresholds.md).

## Scripts

`fatigue_scan.py`, `cpa_decompose.py`, `wasted_spend.py`, and `gmv_profit.py` use Python standard library only. Run `python3 tiktok-ads-shared/scripts/validate-skills.py`, `python3 tiktok-ads-shared/scripts/selftest.py`, or `sh tiktok-ads-shared/scripts/verify_install.sh <repo-url-or-local-path> <count>`.

## Examples

Copy-paste prompts, demo output, and sample CSV files are in [`tiktok-ads-shared/examples/`](tiktok-ads-shared/examples/).

## License and attribution

MIT, see [`LICENSE`](LICENSE). Free to use, modify, and redistribute for personal and commercial work. If you ship something built on top of these skills, a credit is appreciated but not required.

Built and maintained by [AdLume](https://adlume.co) - performance marketing infrastructure for AI-native operators.