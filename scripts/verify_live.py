"""Verify the saved finalized reads, receipt chain and exact deployed-source snapshot.
Read-only and offline by default; --remote also verifies the committed source on GitHub.
The observed Explorer snapshots separately establish transaction status and consensus.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)
def digest(v):return hashlib.sha256(canonical(v).encode()).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--remote',action='store_true');args=a.parse_args()
meta=json.loads((ROOT/'evidence/deployment.json').read_text())
r=json.loads((ROOT/'evidence/finalized-request.json').read_text())
d=json.loads((ROOT/'evidence/finalized-decision.json').read_text())
assert digest(r['binding'])==meta['request_id']==d['decision']['request_id']
assert digest(r['binding']['package'])==r['package_hash']==d['decision']['package_hash']
assert digest(d['decision'])==d['decision_hash']==r['head']==meta['decision_hash']
assert r['binding']['contract']==meta['contract'] and r['binding']['chain_id']==meta['chain_id']
assert r['status']==d['decision']['result']['outcome']==meta['outcome']=='CONTRADICTED'
assert d['decision']['attempt']==r['attempts']==1 and d['decision']['previous']==''
source=(ROOT/'contracts/claim_proof_seal.py').read_bytes()
assert source==(ROOT/'evidence/deployed-source.py').read_bytes()
assert hashlib.sha256(source).hexdigest()==meta['source_sha256']
p=r['binding']['package']
for row,quotes in zip(d['decision']['result']['rows'],d['decision']['result']['citations'],strict=True):
    s=p['sources'][row['source']]
    body=(ROOT/'fixtures'/s['url'].split('/')[-1]).read_bytes()
    assert len(body)==s['bytes'] and hashlib.sha256(body).hexdigest()==s['sha256']
    assert [body.decode().splitlines()[i] for i in row['lines']]==quotes
if args.remote:
    url=f"https://raw.githubusercontent.com/haris4587/ClaimProofSeal/{meta['source_commit']}/contracts/claim_proof_seal.py"
    with urllib.request.urlopen(url,timeout=30) as response:assert response.status==200 and response.read()==source
print(json.dumps({'verified':True,'request_id':meta['request_id'],'outcome':r['status'],'decision_hash':r['head'],'source_sha256':meta['source_sha256'],'source_matches_deployed':True,'github_source_checked':args.remote},indent=2))
