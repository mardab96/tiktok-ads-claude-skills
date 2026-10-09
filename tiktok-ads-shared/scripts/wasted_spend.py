#!/usr/bin/env python3
"""Wasted Spend Finder helper.
Input columns: date, level, name, spend, conversions. Requires a conversion-lag-days value; rows newer than the latest date minus that lag are excluded from T03 review.
"""
import argparse,csv,sys,math
from datetime import date,timedelta
def n(v):
 value=float(str(v or '').strip().replace('$',''))
 if not math.isfinite(value) or value<0:raise ValueError('finite non-negative number required')
 return value
def main():
 p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--target-cpa',required=True,type=float);p.add_argument('--conversion-lag-days',required=True,type=int);a=p.parse_args()
 try:
  with open(a.csv_file,newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 except OSError as e:print('ERROR:',e,file=sys.stderr);return 2
 need={'date','level','name','spend','conversions'}
 if not rows or not need<=set(rows[0]):print('ERROR: required columns: date, level, name, spend, conversions',file=sys.stderr);return 2
 try:
  for r in rows:
   n(r['spend']);n(r['conversions'])
 except ValueError:print('ERROR: needs_data: invalid or missing spend/conversions',file=sys.stderr);return 2
 try:latest=max(date.fromisoformat(r['date'][:10]) for r in rows)
 except ValueError:print('ERROR: date must be ISO YYYY-MM-DD',file=sys.stderr);return 2
 cutoff=latest-timedelta(days=a.conversion_lag_days);print('level	name	spend	conversions	cpa	classification	estimated_reducible_spend')
 for r in rows:
  spend,cv=n(r['spend']),n(r['conversions']);rowdate=date.fromisoformat(r['date'][:10]);cpa=spend/cv if cv else None
  if rowdate>cutoff: label='excluded_recent';red=0
  elif spend>=1.5*a.target_cpa and cv==0:label='review_candidate';red=spend
  else:label='not_flagged';red=0
  print(f"{r['level']}	{r['name']}	{spend:.2f}	{cv:.2f}	{cpa if cpa is not None else 'n/a'}	{label}	{red:.2f}")
 return 0
if __name__=='__main__':sys.exit(main())
