"""Read-only fixture/source verification. No wallet or transaction writes."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--remote',action='store_true')
args=parser.parse_args()
for entry in json.loads((ROOT/'evidence/fixture-manifest.json').read_text()):
    body=(ROOT/'fixtures'/entry['url'].split('/')[-1]).read_bytes()
    assert len(body)==entry['bytes']
    assert hashlib.sha256(body).hexdigest()==entry['sha256']
    if args.remote:
        with urllib.request.urlopen(entry['url'],timeout=30) as r:
            assert r.status==200 and r.read()==body
    print(entry['sha256'],len(body),entry['url'])
source=ROOT/'contracts/claim_proof_seal.py'
print('contract SHA-256',hashlib.sha256(source.read_bytes()).hexdigest())
