#!/usr/bin/env python3
"""Creative Fatigue Detector helper.
Requires daily rows and compares the last seven distinct calendar dates with the preceding seven dates for every ad. T01 is evaluated only with complete 14-day coverage.
"""
import argparse,csv,sys,math
from collections import defaultdict
from datetime import date,timedelta

def n(v):
 value=float(str(v or '').strip().replace('$',''))
 if not math.isfinite(value) or value<0:raise ValueError('finite non-negative number required')
 return value
def main():
 p=argparse.ArgumentParser();p.add_argument('csv_file');a=p.parse_args()
 try:
  with open(a.csv_file,newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 except OSError as e:print('ERROR:',e,file=sys.stderr);return 2
 need={'date','ad','impressions','clicks','frequency'}
 if not rows or not need<=set(rows[0]):print('ERROR: required columns: date, ad, impressions, clicks, frequency',file=sys.stderr);return 2
 try:
  for r in rows:
   for key in ('impressions','clicks','frequency'):n(r[key])
 except ValueError:print('ERROR: needs_data: invalid or missing numeric input',file=sys.stderr);return 2
 groups=defaultdict(list)
 for r in rows:
  try:r['_date']=date.fromisoformat(r['date'][:10]);groups[r['ad']].append(r)
  except ValueError:print('ERROR: needs_data: invalid date',file=sys.stderr);return 2
 print('ad	prior_dates	current_dates	prior_impr	current_impr	prior_ctr	current_ctr	prior_freq	current_freq	status')
 for ad,rs in sorted(groups.items()):
  days=sorted({r['_date'] for r in rs})
  if len(days)<14 or days[-1]-days[-14]!=timedelta(days=13):
   print(f'{ad}	{len(days)}	0	0	0	0.00%	0.00%	0.00	0.00	insufficient_window');continue
  current=days[-7:]; prior=days[-14:-7]
  def agg(ds):
   part=[r for r in rs if r['_date'] in ds];im=sum(n(r['impressions']) for r in part);cl=sum(n(r['clicks']) for r in part);fr=sum(n(r['frequency'])*n(r['impressions']) for r in part)/im if im else 0
   return im,cl/im if im else 0,fr
  oi,oc,of=agg(prior);ni,nc,nf=agg(current)
  status='fatigue_candidate' if oi>=3000 and ni>=3000 and of and oc and nf>=of*1.2 and nc<=oc*.8 else 'monitor'
  print(f'{ad}	7	7	{oi:.0f}	{ni:.0f}	{oc:.2%}	{nc:.2%}	{of:.2f}	{nf:.2f}	{status}')
 return 0
if __name__=='__main__':sys.exit(main())
