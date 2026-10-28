# Evidence and reproducibility

All fixtures are **synthetic**, fictional Lumen revision-A battery tests. They assert no actual product performance.

- `launch-record.txt`: 48 hours indoors, limited operating range, no outdoor certification.
- `field-addendum.txt`: actual synthetic outdoor trial is 12 hours; explicitly says the indoor 48-hour figure does not apply outdoors.
- `ambiguous.txt`: missing hardware revision and conditions; must not certify scope.
- `injection.txt`: hostile verdict instructions amid documentary text; offline guard/data-flow test only, not a claimed live injection-resistance proof.

Immutable evidence commit: `5fe675fa9887570ee3b39245ff8f4f9a3847d5d5`. Exact URLs, byte counts and SHA-256 values are in [fixture-manifest.json](../evidence/fixture-manifest.json). [contradicted.json](../examples/contradicted.json) is the live request package. Line numbers are zero-based Python `splitlines()` indexes, explicitly supplied with every line in the audit prompt. Exact selected lines are resolved deterministically into `citations` in the accepted result; these are not model-generated quotations.

## Input bounds

Package UTF-8 JSON <=14,000 bytes; exact keys `claim`, `facets`, `sources`. Claim 1–2,000 characters; 1–6 unique nonempty facets, each <=500 characters. 1–4 unique source URLs, each <=350 characters. Each source has exact keys `url`, `sha256`, `bytes`; each document 1–10,000 bytes, all documents <=24,000 bytes, <=200 lines each. Cited lines must be nonempty/NUL-free and <=600 characters. No HTML rendering, PDFs, binary files or large dataset downloads. Output audits <=24,000 serialized bytes; one row per ordered facet/source pair, <=3 unique citation indexes per row.

Publisher constructor is one `owner/repository` location. Source form:
`https://raw.githubusercontent.com/OWNER/REPO/FULL_40_HEX_COMMIT/PATH`.
Commit binds version; SHA-256 and byte length bind the exact retrieved representation. Publisher and chain/contract/caller are bound into request identity.

## Hashes

`canonical(v) = json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)`; `digest(v)` is SHA-256 of its UTF-8 bytes. No floats enter accepted schemas. Request ID is digest of stored `binding`; package hash is digest of `binding.package`. Each receipt is `{decision, decision_hash}` where `decision_hash = digest(decision)`. `decision.previous` is the preceding decision hash, or empty string initially. Hashes cover full accepted reasons and quotations as well as exact classifications; different accepted explanations therefore intentionally produce different decision hashes.

Use `python scripts/verify_evidence.py` for fixture and source digests; `--remote` also GETs pinned fixtures and requires byte identity. Live state receipts and transaction status must be checked separately. A mocked unit test cannot prove model consensus.
