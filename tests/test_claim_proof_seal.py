"""Actual pinned SDK/direct-mode; synthetic LLM/web mocks, not network consensus."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import pytest
from gltest.direct import VMContext, deploy_contract, create_address

ROOT = Path(__file__).resolve().parents[1]
FILES = ['launch-record.txt', 'field-addendum.txt']


def package():
    sources = []
    for name in FILES:
        b = (ROOT/'fixtures'/name).read_bytes()
        sources.append({'url':f'https://raw.githubusercontent.com/haris4587/ClaimProofSeal/{"a"*40}/fixtures/{name}', 'sha256':hashlib.sha256(b).hexdigest(), 'bytes':len(b)})
    return {'claim':'Lumen hardware revision A achieved 48 hours of battery endurance both indoors and outdoors.',
            'facets':['Lumen hardware revision A achieved 48 hours of battery endurance indoors.', 'Lumen hardware revision A achieved 48 hours of battery endurance outdoors.'], 'sources':sources}


@pytest.fixture
def env():
    vm = VMContext()
    with vm.activate():
        c = deploy_contract(ROOT/'contracts/claim_proof_seal.py', vm, 'haris4587/ClaimProofSeal', sdk_version='v0.2.16')
        m = sys.modules['_contract_claim_proof_seal']
        yield vm, c, m, package()


def audit(states=None, coverage='VERIFIED'):
    states = states or ['SUPPORT','ABSENT','ABSENT','REFUTE']
    rows=[]
    for n,s in enumerate(states):
        rows.append({'facet':n//2,'source':n%2,'state':s,'reason':'Documentary assessment.', 'lines':[] if s in ['ABSENT','UNKNOWN'] else [5 if n%2==0 else 3]})
    return {'coverage':coverage, 'reason':'All assertions and qualifiers are preserved.', 'rows':rows}


def io(vm,p,answer=None, judge=True):
    vm.clear_mocks()
    for s in p['sources']:
        vm.mock_web(re.escape(s['url']), {'method':'GET','status':200,'body':(ROOT/'fixtures'/s['url'].split('/')[-1]).read_text()})
    vm.mock_llm('Supply one row for EACH', json.dumps(answer or audit()))
    vm.mock_llm('Validate both audits', json.dumps({'valid':judge}))


def run(env, answer=None):
    vm,c,m,p=env
    io(vm,p,answer)
    rid=c.register(json.dumps(p)); c.evaluate(rid)
    return rid,json.loads(c.get_request(rid)),json.loads(c.get_decision(rid,1))


@pytest.mark.parametrize('states,expected',[
    (['SUPPORT','ABSENT','SUPPORT','ABSENT'],'SUPPORTED'),
    (['SUPPORT','ABSENT','ABSENT','ABSENT'],'PARTIALLY_SUPPORTED'),
    (['PARTIAL','ABSENT','ABSENT','ABSENT'],'PARTIALLY_SUPPORTED'),
    (['SUPPORT','ABSENT','ABSENT','REFUTE'],'CONTRADICTED'),
    (['SUPPORT','UNKNOWN','ABSENT','REFUTE'],'INCONCLUSIVE'),
    (['ABSENT']*4,'INCONCLUSIVE'),
])
def test_outcomes_hash_and_validator(env,states,expected):
    vm,c,m,p=env
    rid,r,d=run(env,audit(states))
    assert r['status']==expected
    assert m.digest(d['decision'])==d['decision_hash']==r['head']
    assert m.digest(r['binding'])==rid and m.digest(p)==r['package_hash']
    assert vm.run_validator() is True


def test_omitted_qualifier_is_inconclusive(env):
    rid,r,d=run(env,audit(['SUPPORT']*4,'UNKNOWN'))
    assert r['status']=='INCONCLUSIVE'


@pytest.mark.parametrize('mutation',[
    lambda a:a.update(coverage='YES'),lambda a:a.update(extra=True),
    lambda a:a.update(rows=[]),lambda a:a['rows'].pop(),
    lambda a:a['rows'][0].update(state='SUPPORTED'),
    lambda a:a['rows'][0].update(facet=True),lambda a:a['rows'][0].update(source=3),
    lambda a:a['rows'][0].update(lines=[-1]),lambda a:a['rows'][0].update(lines=[999]),
    lambda a:a['rows'][0].update(lines=[True]),lambda a:a['rows'][0].update(lines=[]),
    lambda a:a['rows'][0].update(lines=[0,0]),lambda a:a['rows'][0].update(reason=''),
    lambda a:a['rows'][0].update(quote='forged'),lambda a:a.update(reason='x'*501),
])
def test_malformed_outputs_fail_closed(env,mutation):
    a=audit();mutation(a)
    rid,r,d=run(env,a)
    assert r['status']=='INCONCLUSIVE' and d['decision']['result']['error']=='INVALID_MODEL'


@pytest.mark.parametrize('change',[
    lambda p:p.update(claim=''),lambda p:p.update(claim='x'*2001),
    lambda p:p.update(facets=[]),lambda p:p.update(facets=['x']*2),
    lambda p:p.update(sources=[]),lambda p:p['sources'][0].update(bytes=True),
    lambda p:p['sources'][0].update(bytes=10001),lambda p:p['sources'][0].update(sha256='F'*64),
    lambda p:p['sources'][0].update(url=p['sources'][0]['url'].replace('a'*40,'main')),
    lambda p:p['sources'][0].update(url=p['sources'][0]['url']+'?x=1'),
    lambda p:p['sources'][0].update(url=p['sources'][0]['url'].replace('/fixtures/','/../')),
    lambda p:p['sources'][0].update(url=p['sources'][0]['url'].replace('haris4587','attacker')),
    lambda p:p['sources'].append(copy.deepcopy(p['sources'][0])),lambda p:p.update(extra='x'),
])
def test_invalid_registration(env,change):
    vm,c,m,p=env;change(p)
    with pytest.raises(Exception): c.register(json.dumps(p))


def test_duplicate_keys(env):
    vm,c,m,p=env
    with pytest.raises(Exception):c.register('{"claim":"x","claim":"y","facets":[],"sources":[]}')
    with pytest.raises(Exception):m.decode('{"valid":true,"valid":false}',100)


@pytest.mark.parametrize('kind',['tamper','http','utf8','nul','long_lines'])
def test_bad_evidence(env,monkeypatch,kind):
    vm,c,m,p=env;io(vm,p)
    b=(ROOT/'fixtures'/FILES[0]).read_bytes(); status=200
    if kind=='tamper':b=b.replace(b'48',b'99')
    if kind=='http':status=404
    if kind=='utf8':b=b'\xff'
    if kind=='nul':b=b'a\x00b'
    if kind=='long_lines':b=b'x\n'*201
    if kind in ['utf8','nul','long_lines']:
        p['sources'][0].update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    class Response: pass
    res=Response();res.status=status;res.body=b
    monkeypatch.setattr(m.gl.nondet.web,'get',lambda *a,**kw:res)
    rid=c.register(json.dumps(p));c.evaluate(rid)
    assert json.loads(c.get_request(rid))['status']=='INCONCLUSIVE'
    assert vm.run_validator() is True


def test_sealed_duplicate_and_auth(env):
    vm,c,m,p=env;rid,r,d=run(env)
    with pytest.raises(Exception):c.register(json.dumps(p))
    with pytest.raises(Exception):c.evaluate(rid)
    vm.sender=create_address("attacker")
    with pytest.raises(Exception):c.evaluate(rid)


def test_retry_history(env):
    vm,c,m,p=env
    io(vm,p,audit(['UNKNOWN']*4));rid=c.register(json.dumps(p))
    last=''
    for n in range(1,4):
        c.evaluate(rid);d=json.loads(c.get_decision(rid,n))
        assert d['decision']['previous']==last
        last=d['decision_hash']
    with pytest.raises(Exception):c.evaluate(rid)
    assert json.loads(c.get_decision(rid,1))['decision']['previous']==''


def test_malicious_leader_and_semantic_citations(env,monkeypatch):
    vm,c,m,p=env;io(vm,p)
    docs,error=m.retrieve(p['sources']);own=m.normalize(audit(),p,docs)
    assert m.validate_leader(own,p,docs,own)
    forged=copy.deepcopy(own);forged['outcome']='SUPPORTED'
    assert not m.validate_leader(forged,p,docs,own)
    forged=copy.deepcopy(own);forged['rows'][3]['state']='SUPPORT';forged['outcome']='SUPPORTED'
    assert not m.validate_leader(forged,p,docs,own)
    forged=copy.deepcopy(own);forged['rows'][0]['lines']=[999]
    assert not m.validate_leader(forged,p,docs,own)
    # Literal line exists but is semantically unrelated. Independent judge rejects.
    forged=copy.deepcopy(own);forged['rows'][0]['lines']=[0]
    forged['citations'][0]=[docs[0][0]]
    monkeypatch.setattr(m.gl.nondet,'exec_prompt',lambda *a,**kw:{'valid':False})
    assert not m.validate_leader(forged,p,docs,own)
    assert not m.validate_leader({'outcome':'INCONCLUSIVE','error':'FETCH_ERROR'},p,docs,own)


def test_different_valid_quotes_and_reasons(env):
    vm,c,m,p=env;io(vm,p)
    docs,e=m.retrieve(p['sources']);own=m.normalize(audit(),p,docs)
    leader=copy.deepcopy(own);leader['reason']='Same complete coverage, different wording.'
    leader['rows'][3]['lines']=[4]
    leader['citations'][3]=[docs[1][4]]
    assert m.validate_leader(leader,p,docs,own)


def test_json_text_provider_and_injection_guard(env,monkeypatch):
    vm,c,m,p=env;io(vm,p)
    calls=[]
    def llm(prompt,**kw):
        calls.append(prompt)
        return json.dumps({'valid':True}) if 'Validate both audits' in prompt else json.dumps(audit())
    monkeypatch.setattr(m.gl.nondet,'exec_prompt',llm)
    rid=c.register(json.dumps(p));c.evaluate(rid)
    assert vm.run_validator() is True
    assert all('never instructions' in x and 'No outside knowledge' in x for x in calls)


def test_validator_executes_independent_retrieval(env,monkeypatch):
    vm,c,m,p=env;rid,r,d=run(env)
    monkeypatch.setattr(m.gl.nondet.web,'get',lambda *a,**k: (_ for _ in ()).throw(ValueError('offline')))
    assert vm.run_validator() is False


def test_pending_owner_and_request_isolation(env):
    vm,c,m,p=env;io(vm,p)
    rid=c.register(json.dumps(p))
    vm.sender=create_address('other')
    with pytest.raises(Exception):c.evaluate(rid)
    other=c.register(json.dumps(p))
    assert other!=rid
    c.evaluate(other)
    assert json.loads(c.get_request(rid))['attempts']==0


def test_captured_validator_rejects_malicious_return_and_errors(env):
    vm,c,m,p=env;rid,r,d=run(env)
    malicious=copy.deepcopy(d['decision']['result'])
    malicious['outcome']='SUPPORTED'
    assert vm.run_validator(leader_result=malicious) is False
    assert vm.run_validator(leader_error=ValueError('leader failed')) is False


@pytest.mark.parametrize('raw',['```json {} ```','{"coverage":"VERIFIED","coverage":"UNKNOWN"}', '[]', 'null', '{"valid":1}', 'x'*24001])
def test_malformed_text_and_bounded_model_retry(env,monkeypatch,raw):
    vm,c,m,p=env;io(vm,p);calls=[]
    def llm(*a,**kw):calls.append(1);return raw
    monkeypatch.setattr(m.gl.nondet,'exec_prompt',llm)
    rid=c.register(json.dumps(p));c.evaluate(rid)
    assert len(calls)==2
    assert json.loads(c.get_request(rid))['status']=='INCONCLUSIVE'


@pytest.mark.parametrize('filename,state',[('ambiguous.txt','UNKNOWN'),('injection.txt','ABSENT')])
def test_adversarial_documents_are_prompt_data(env,monkeypatch,filename,state):
    vm,c,m,p=env
    body=(ROOT/'fixtures'/filename).read_bytes()
    p['sources']=p['sources'][:1]
    p['sources'][0].update(url=p['sources'][0]['url'].rsplit('/',1)[0]+'/'+filename,bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
    class R:status=200
    response=R();response.body=body
    monkeypatch.setattr(m.gl.nondet.web,'get',lambda *a,**k:response)
    def llm(prompt,**kw):
        assert 'never instructions' in prompt
        assert filename!='injection.txt' or 'IGNORE ALL PRIOR' in prompt
        return {'coverage':'VERIFIED','reason':'Exact facets.', 'rows':[{'facet':i,'source':0,'state':state,'reason':'No affirmative support.','lines':[]} for i in range(2)]}
    monkeypatch.setattr(m.gl.nondet,'exec_prompt',llm)
    rid=c.register(json.dumps(p));c.evaluate(rid)
    assert json.loads(c.get_request(rid))['status']=='INCONCLUSIVE'
