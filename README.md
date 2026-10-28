# ClaimProofSeal

**Does authenticated evidence actually support the exact claim?** A reusable GenLayer Intelligent Contract for documentary claim verification. No frontend, tokens, payments or external wallet required.

ClaimProofSeal locks an exact claim, an exhaustive ordered decomposition into factual facets, and commit-pinned source fingerprints. Every validator independently retrieves the bytes, authenticates them and assesses **every facet against every source**. A coverage check prevents a submitter from obtaining a seal by omitting an inconvenient qualifier. Deterministic code derives the result; the LLM cannot choose the final verdict.

| Outcome | Strict rule, in precedence order |
|---|---|
| INCONCLUSIVE | Retrieval/integrity/model failure; unverified facet coverage; or any UNKNOWN matrix cell |
| CONTRADICTED | No unknowns, coverage verified, and any source explicitly REFUTES any facet |
| SUPPORTED | No refutation/unknown; every facet fully supported by at least one source |
| PARTIALLY_SUPPORTED | No refutation/unknown; at least one partial/full supporting cell, but not all facets fully supported |
| INCONCLUSIVE | All cells ABSENT: missing support never certifies the claim |

Contradiction cannot be outvoted by supporting documents. PARTIALLY_SUPPORTED is a **non-certifying gap report**, never a positive seal for the complete claim. Only SUPPORTED certifies documentary entailment, within the locked evidence universe. Ambiguity conservatively dominates even an observed contradiction.

## Interface

Deploy `contracts/claim_proof_seal.py` with the immutable publication repository `haris4587/ClaimProofSeal`, or a repository your application trusts.

- `register(package_json) -> request_id`: anyone may lock a bounded package; request hash binds protocol version, chain, contract, caller, publisher and canonical package. Identical submissions by that caller are rejected.
- `evaluate(request_id) -> decision_hash`: request owner only; at most three accepted attempts, only following INCONCLUSIVE. Conclusive results seal permanently. Consensus failure reverts without consuming an attempt.
- `get_request(request_id)`, `get_decision(request_id, attempt)`, `get_config()`: canonical JSON views. Attempt numbers start at one.

[Example package](examples/contradicted.json) intentionally misapplies an indoor battery endurance figure outdoors. Synthetic field evidence explicitly refutes it. Full Consensus evidence and source matching are recorded in [DEPLOYMENT](docs/DEPLOYMENT.md).

## Why GenLayer

Real `gl.nondet.web.get`, `gl.nondet.exec_prompt` and `gl.vm.run_nondet_unsafe` execute inside the Equivalence Principle. Validators repeat retrieval and semantic assessment independently. Coverage, every ordered matrix classification and derived verdict must agree exactly. Leader citations are resolved from authenticated line indexes, checked byte-for-byte, and semantically judged against full documents. Valid explanations and quote selection may differ. A schema-only check never suffices.

The reusable output is a content-addressed request plus a hash-linked, append-only decision receipt containing coverage, the complete support/refutation matrix, exact citations, reasons and outcome. Other applications can consume finalized receipts without trusting an off-chain AI service to decide or overwrite results.

## Reproduce

Python 3.12+:

```sh
python -m pip install -r requirements-dev.txt
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -p gltest.direct.pytest_plugin -q tests
GENVM_VERSION=v0.2.16 genvm-lint check contracts/claim_proof_seal.py --json
GENVM_VERSION=v0.2.16 genvm-lint schema contracts/claim_proof_seal.py --json
python scripts/verify_evidence.py
```

Tests use the **actual pinned SDK** with mocked host web/LLM calls and explicitly invoke captured validator closures. These test deterministic protections and adversarial paths; they do not establish real model accuracy or network consensus. The separately recorded Studio run does.

[Security and trust limits](docs/SECURITY.md) · [Evidence specification](docs/EVIDENCE.md) · [Deployment](docs/DEPLOYMENT.md) · [Submission](docs/SUBMISSION.md) · [Official references and architectural review](docs/REFERENCES.md)

MIT licensed. Authentication establishes byte integrity at a configured publication location, not publisher honesty or universal factual truth.
