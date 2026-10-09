#!/usr/bin/env python3
"""CPA Spike Diagnosis helper.
Input columns: period, cost, impressions, clicks, conversions. Reads baseline/current and prints the CPM, CTR, CVR, and CPA identity. T04 output is a triage label, not a cause.
"""
import argparse,csv,sys,math
def n(v):
 value=float(str(v or '').strip().replace('$',''))
 if not math.isfinite(value) or value<0:raise ValueError('finite non-negative number required')
 return value
def f(v,fmt):return fmt.format(v) if v is not None else 'n/a'
def main():
 p=argparse.ArgumentParser();p.add_argument('csv_file');a=p.parse_args()
 try:
  with open(a.csv_file,newline='',encoding='utf-8-sig') as h:rows=list(csv.DictReader(h))
 except OSError as e:print('ERROR:',e,file=sys.stderr);return 2
 need={'period','cost','impressions','clicks','conversions'}
 if not rows or not need<=set(rows[0]):print('ERROR: required columns: period, cost, impressions, clicks, conversions',file=sys.stderr);return 2
 try:
  for r in rows:
   for key in ('cost','impressions','clicks','conversions'):n(r[key])
 except ValueError:print('ERROR: needs_data: invalid or missing numeric input',file=sys.stderr);return 2
 d={}
 for r in rows:
  x=d.setdefault(r['period'],[0,0,0,0]);x[0]+=n(r['cost']);x[1]+=n(r['impressions']);x[2]+=n(r['clicks']);x[3]+=n(r['conversions'])
 if not {'baseline','current'}<=set(d):print('ERROR: periods must include baseline and current',file=sys.stderr);return 2
 vals={};print('period	cost	impressions	clicks	conversions	cpm	ctr	cvr	cpa')
 for k in ('baseline','current'):
  cost,im,cl,cv=d[k];v=(cost/im*1000 if im else None,cl/im if im else None,cv/cl if cl else None,cost/cv if cv else None);vals[k]=v
  print(f'{k}	{cost:.2f}	{im:.0f}	{cl:.0f}	{cv:.2f}	{f(v[0],"{:.2f}")}	{f(v[1],"{:.2%}")}	{f(v[2],"{:.2%}")}	{f(v[3],"{:.2f}")}')
 b,c=vals['baseline'],vals['current']
 change=(c[3]/b[3]-1) if b[3] and c[3] is not None else None
 if c[3] is None: verdict='check_tracking'
 elif d['baseline'][3]<10 or d['current'][3]<10: verdict='insufficient_volume'
 elif change is None: verdict='needs_data'
 elif change>=.30: verdict='escalate'
 else: verdict='below_rule'
 print('cpa_change_pct:	'+(f(change,'{:.1%}') if change is not None else 'n/a'))
 print('T04_verdict:	'+verdict)
 print('read:	Check tracking and change history before naming a cause.')
 return 0
if __name__=='__main__':sys.exit(main())
