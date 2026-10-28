# Security model

The deployment permanently trusts one public GitHub owner/repository as an evidence publication location. There is no setter, privileged reviewer, upgrade, delete or evidence replacement API. Anyone may register; only the recorded request creator may trigger its expensive assessments/retries. Independent requests have no global slot/capacity contention.

## Guarantees enforced by code

- Full 40-lowercase-hex commit URL; exact host/publisher prefix and conservative path alphabet. No credentials, ports, query, fragments, mutable branches/tags, encoded traversal or custom endpoints.
- HTTP 200, exact raw byte length, SHA-256, strict UTF-8, nonempty/NUL-free text and bounded line count. A mismatch aborts semantic evaluation with INCONCLUSIVE.
- Bounded package, documents, facets, matrix, reasons and citations. Unknown/malformed model output has one bounded retry, then INCONCLUSIVE. Validator citation judgment gets no retry.
- Full ordered facet/source matrix; no omitted cells. Semantic coverage must confirm every exact claim qualifier survives decomposition. Any UNKNOWN prevents positive certification; any explicit refutation prevents either support verdict.
- Validators independently fetch/authenticate and assess before comparing exact critical fields. Leader status, schema, derived verdict and exact resolved quotations are revalidated. A second grounded model judgment rejects misleading but literal quotations and material explanation differences. Errors and non-return VM results cannot masquerade as successful assessments.
- Canonical sorted compact ASCII-escaped JSON, SHA-256 request/package/decision bindings, append-only decision keys and previous hashes. Request hash includes caller, contract and chain, preventing cross-context receipt reuse.
- Only accepted attempts spend the three-attempt budget. Conclusive assessments are terminal. Revised evidence requires a new content-addressed request.

## Trust limits

Byte authentication does not prove publisher legal identity, honesty, authorship, real-world events or completeness. Commit pins preserve bytes; hashes are integrity commitments, not digital signatures from an independent authority. Choose and independently verify the deployment's publisher. GitHub/TLS and network retrieval availability remain dependencies. Identical dishonest documents may yield documentary support for false real-world assertions. Omitted external contradictory evidence cannot be discovered: validators assess the locked universe only.

PARTIALLY_SUPPORTED is explicitly non-certifying. Applications should accept only SUPPORTED and separately inspect claim, publisher, submitter, source identities and finalized transaction success. No probabilistic confidence score changes the rules. No logical aggregation across separate partial sources upgrades a facet to full support: at least one source must fully entail that facet. Split facets faithfully when separate sources establish separate assertions; coverage still checks the exact original claim.

Prompt guards, data separation, indexed citations, independent assessments and citation review reduce injection risk; they do not guarantee immunity or remove correlated model errors. Submitted facets and documents can contain malicious instructions; they never define contract policy. User-provided JSON duplicate keys are rejected; when a provider has already decoded JSON, discarded duplicate keys cannot be recovered. Model classifications remain semantic judgments, not a mathematical truth proof.

The SDK may follow HTTP redirects; any returned bytes must still match the locked SHA-256 and exact length. HTTP failures, provider outages, ambiguous records, malformed output or validator disagreement can prevent a verdict. Network disagreement can leave a transaction undetermined with unchanged state; it is not converted into a fabricated INCONCLUSIVE receipt.

Public sources and claims are public on-chain data. Do not submit secrets. No contract value transfers or third-party tool calls are requested. Untrusted evidence is never executed.
