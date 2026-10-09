#!/bin/sh
set -eu
source=${1:?usage: verify_install.sh <repo-url-or-local-path> <count>}; expected=${2:?count}; tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
if [ -d "$source" ]; then cp -R "$source" "$tmp/tiktok-ads-claude-skills"; else git clone "$source" "$tmp/tiktok-ads-claude-skills"; fi
mkdir -p "$tmp/home/.claude/skills/references"; echo decoy > "$tmp/home/.claude/skills/references/thresholds.md"
(cd "$tmp" && HOME="$tmp/home" sh -c 'mkdir -p ~/.claude/skills; cp -r tiktok-ads-claude-skills/*tiktok-ads tiktok-ads-claude-skills/tiktok-ads-shared ~/.claude/skills/')
i="$tmp/home/.claude/skills"; count=$(find "$i" -mindepth 1 -maxdepth 1 -type d -name '*tiktok-ads' -exec test -f '{}/SKILL.md' \; -print | wc -l | tr -d ' '); [ "$count" = "$expected" ]
paths=0; for s in "$i"/*tiktok-ads/SKILL.md; do for r in $(grep -Eo '\.\./tiktok-ads-shared/(scripts|references)/[A-Za-z0-9_.-]+' "$s" | sort -u); do test -e "$(dirname "$s")/$r"; paths=$((paths+1)); done; done
! grep -R 'decoy' "$i/tiktok-ads-shared" >/dev/null
python3 "$i/tiktok-ads-shared/scripts/validate-skills.py"; python3 "$i/tiktok-ads-shared/scripts/selftest.py"; python3 "$i/tiktok-ads-shared/scripts/fatigue_scan.py" "$i/tiktok-ads-shared/examples/data/fatigue_daily.csv" >/dev/null; python3 "$i/tiktok-ads-shared/scripts/cpa_decompose.py" "$i/tiktok-ads-shared/examples/data/cpa_periods.csv" >/dev/null; python3 "$i/tiktok-ads-shared/scripts/wasted_spend.py" "$i/tiktok-ads-shared/examples/data/wasted_spend.csv" --target-cpa 100 --conversion-lag-days 7 >/dev/null; python3 "$i/tiktok-ads-shared/scripts/gmv_profit.py" "$i/tiktok-ads-shared/examples/data/gmv_profit.csv" >/dev/null
echo "PASS: installed $count skill folders; checked $paths TikTok-relative paths; decoy collision did not resolve; ran 4 installed analysis scripts"
