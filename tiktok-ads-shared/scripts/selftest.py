#!/usr/bin/env python3
"""Regression checks for TikTok analysis helpers."""
import csv,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; DATA=HERE.parent/'examples'/'data'
def run(s,*a): return subprocess.run([sys.executable,str(HERE/s),*map(str,a)],capture_output=True,text=True)
def check(name,ok): print(('pass' if ok else 'FAIL'),name); return ok
def main():
 bad=[]
 cases=[('fatigue_scan.py',[DATA/'fatigue_daily.csv'],'fatigue_candidate'),('cpa_decompose.py',[DATA/'cpa_periods.csv'],'T04_verdict:	escalate'),('wasted_spend.py',[DATA/'wasted_spend.csv','--target-cpa','100','--conversion-lag-days','7'],'excluded_recent'),('gmv_profit.py',[DATA/'gmv_profit.csv'],'incomplete_cost_stack / needs_data')]
 for s,a,n in cases:
  r=run(s,*a)
  if not check(s,r.returncode==0 and n in r.stdout):bad.append(s)
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'zero.csv';p.write_text('period,cost,impressions,clicks,conversions\nbaseline,100,1000,50,10\ncurrent,100,1000,50,0\n')
  r=run('cpa_decompose.py',p)
  if not check('zero conversions prints n/a', 'cpa_change_pct:\tn/a' in r.stdout and 'check_tracking' in r.stdout):bad.append('zero CPA')
  p=Path(d)/'blank.csv';p.write_text('product,revenue,refunds,affiliate_commission,coupons,referral_fees,ad_spend\nx,100,,,,,10\n')
  r=run('gmv_profit.py',p)
  if not check('blank fee is missing', 'affiliate_commission' in r.stdout and 'incomplete_cost_stack' in r.stdout):bad.append('blank fee')
  edge_cases=[
   ('wasted_spend.py','date,level,name,spend,conversions\n2026-10-01,ad,A,100,--\n',['--target-cpa','20','--conversion-lag-days','0'],2,'needs_data'),
   ('cpa_decompose.py','period,cost,impressions,clicks,conversions\nbaseline,0,1000,100,20\ncurrent,100,1000,100,20\n',[],0,'T04_verdict:\tneeds_data'),
   ('fatigue_scan.py','date,ad,impressions,clicks,frequency\n2026-10-01,A,1000,n/a,1\n',[],2,'needs_data'),
   ('gmv_profit.py','product,revenue,refunds,affiliate_commission,coupons,referral_fees,ad_spend\nx,100,0,NaN,0,0,10\n',[],0,'incomplete_cost_stack'),
  ]
  for s,data,args,code,expected in edge_cases:
   p=Path(d)/'edge.csv';p.write_text(data);r=run(s,p,*args)
   if not check(s+' missing/undefined input',r.returncode==code and expected in r.stdout+r.stderr):bad.append(s+' edge')
 if bad: print('FAIL:',', '.join(bad));return 1
 print('OK: every documented guarantee holds');return 0
if __name__=='__main__':sys.exit(main())
