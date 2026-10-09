#!/usr/bin/env python3
"""Validate TikTok skill structure and copy safety."""
import argparse,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REQ=['## Use this skill when','## Required input','## Analysis workflow','## Decision rules','## Output format','## Practical example','## Guardrails']
def body(t,h):
 m=re.search(r'^## '+re.escape(h)+r'\n(.*?)(?=^## |\Z)',t,re.M|re.S);return m.group(1) if m else ''
def check(p):
 t=p.read_text();e=[]
 for h in REQ:
  if h not in t:e.append('missing '+h)
 if 'TikTok' not in t.split('---',2)[1] if t.startswith('---') else True:e.append('description missing TikTok')
 if 'Use when' not in t.split('---',2)[1] if t.startswith('---') else True:e.append('description missing activation')
 if len(re.findall(r'^\d+\. ',body(t,'Analysis workflow'),re.M))<5:e.append('workflow needs 5 steps')
 if len(t.split())<280:e.append('under 280 words')
 if re.search(r'\b(\w+)\s+\1\b',t,re.I):e.append('doubled word')
 if re.search(r'(^|[.!?]\s+|\n)The\s',t):e.append('sentence starts with The')
 if '\u2014' in t or '\u2013' in t:e.append('forbidden dash')
 return e
def main():
 a=argparse.ArgumentParser();a.add_argument('--selftest',action='store_true');x=a.parse_args();files=sorted(ROOT.glob('*tiktok-ads/SKILL.md'))
 if x.selftest:
  sample=files[0].read_text();bad=check_text(sample.replace('Do not make','Do not'+' not make',1))
  print('OK: selftest caught doubled word' if any('doubled word' in q for q in bad) else 'FAIL: doubled word escaped');return 0 if any('doubled word' in q for q in bad) else 1
 errs=[]
 for p in files:
  for q in check(p):errs.append(p.parent.name+': '+q)
 if errs:print('\n'.join(errs));return 1
 print(f'OK: {len(files)} skills passed validation');return 0
def check_text(t):
 p=ROOT/'__x__';p.write_text(t);x=check(p);p.unlink();return x
if __name__=='__main__':sys.exit(main())
