#!/usr/bin/env python3
"""GMV Max Profit Check helper.
Blank or unparseable fee and refund cells remain missing. They are never treated as zero and force incomplete_cost_stack / needs_data.
"""
import argparse,csv,sys,math
COST=('refunds','affiliate_commission','coupons','referral_fees','ad_spend')
def parse(v):
 s=str(v or '').strip().replace('$','')
 if ',' in s:return None
 if not s:return None
 try:
  value=float(s)
  return value if math.isfinite(value) else None
 except ValueError:return None
def main():
 p=argparse.ArgumentParser();p.add_argument('csv_file');a=p.parse_args()
 try:
  with open(a.csv_file,newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 except OSError as e:print('ERROR:',e,file=sys.stderr);return 2
 need={'product','revenue',*COST}
 if not rows or not need<=set(rows[0]):print('ERROR: required columns: '+', '.join(sorted(need)),file=sys.stderr);return 2
 print('product	revenue	cost_stack	contribution_before_cogs	status	missing_columns')
 for r in rows:
  rev=parse(r['revenue']);missing=[k for k in COST if parse(r[k]) is None]
  if rev is None: missing=['revenue',*missing]
  if missing: print(f"{r['product']}	n/a	n/a	n/a	incomplete_cost_stack / needs_data	{','.join(missing)}");continue
  cost=sum(abs(parse(r[k])) for k in COST);print(f"{r['product']}	{rev:.2f}	{cost:.2f}	{rev-cost:.2f}	complete_cost_stack	")
 return 0
if __name__=='__main__':sys.exit(main())
