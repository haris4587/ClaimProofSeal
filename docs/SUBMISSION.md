# GenLayer Intelligent Contracts submission

**Title:** ClaimProofSeal

**One-line description:** A reusable GenLayer primitive that verifies exact factual claims against immutable, authenticated documentary evidence through independent validator consensus.

**Category:** Builder → Intelligent Contracts

## Notes / Description (968 characters)

ClaimProofSeal is a reusable GenLayer documentary-claim verification primitive. It locks the exact claim, exhaustive facets and commit-pinned evidence with SHA-256 and exact byte lengths. Validators independently retrieve/authenticate documents, assess every facet against every source, compare coverage and classifications exactly, and validate source-grounded citations while allowing different valid explanations. Deterministic rules return SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED or INCONCLUSIVE; ambiguity, missing support and integrity failures cannot certify a complete claim. Content-addressed requests, owner-only bounded retries and hash-linked immutable receipts make results reusable. 58 SDK tests plus GenVM lint/schema/SDK validation pass. Real Studio Full Consensus finalized CONTRADICTED for an indoor endurance figure misleadingly applied outdoors; deployed bytes match GitHub. Evidence is explicitly synthetic; partial support is non-certifying.

## Submission links and identifiers

| Field | Value |
|---|---|
| Repository | https://github.com/haris4587/ClaimProofSeal |
| Contract / Explorer | https://explorer-studio.genlayer.com/address/0xcD1E22b8B459b9A9d63A962538b7b332f420b908 |
| Deployment transaction | https://explorer-studio.genlayer.com/tx/0xb563fe1f1ae7374cc39ab46ae1d1dbc0222380ad50b2e74ca0f7a1d399817330 |
| Full Consensus transaction | https://explorer-studio.genlayer.com/tx/0x2f964d996fa85e092203615315bf3409bf1a36595fe0fbcceedc55d5c04d91b9 |
| Registration transaction | https://explorer-studio.genlayer.com/tx/0xf7186c2538da8aecfe98458e57b74cc6169176af952831e863a5dcb9effb63fa |
| Final contract source commit | `25a2185b8e3d4746895566296b19ad76afdeb993` |
| Source SHA-256 | `a52d1148e85d840d5beaf39aad508029d63b9628a707718f055e5c51a290b270` |
| Request ID | `c405c61e9c6b429787065f9d619d5b66458277cd38b37d46bf928082e580a9c1` |
| Decision hash | `e3cf107521d8469d9d3ccd85cda1e2d8cfcc83b6aba6bc90c615c73174bfbf9a` |
| Network | Public Studio sandbox / Studionet, chain ID 61999 |
| Real result | FINALIZED, SUCCESS, Accepted; stored **CONTRADICTED**; zero rotations |
| Validation | **58 passed**, zero failures/errors/skips; GenVM lint, SDK validation and ABI schema extraction passed |

The final source commit identifies the exact deployed code. Later documentation/evidence commits preserve its bytes. Repository HEAD is the completed submission package; the delivery message supplies that exact final documentation commit.

## Strong evidence URLs

- [Deployment, reproduction and failure investigation](https://github.com/haris4587/ClaimProofSeal/blob/main/docs/DEPLOYMENT.md)
- [Finalized stored decision](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/finalized-decision.json)
- [Finalized stored request](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/finalized-request.json)
- [Receipt/source verification](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/verification.json)
- [Exact source read back from Explorer](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/deployed-source.py)
- [Finalization observation](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/full-consensus-finalized-observed.txt)
- [Finalized state observation](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/finalized-state-observed.txt)
- [Validator vote observation](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/consensus-votes-observed.txt)
- [Finalized transaction screenshot](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/full-consensus-finalized.jpg)
- [All 58 test cases](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/junit.xml)
- [Test summary](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/test-results.json)
- [GenVM lint and SDK validation](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/lint.json)
- [ABI schema](https://github.com/haris4587/ClaimProofSeal/blob/main/docs/abi.json)
- [Pinned fixture fingerprints](https://github.com/haris4587/ClaimProofSeal/blob/main/evidence/fixture-manifest.json)
- [Actual pinned document used in Full Consensus](https://raw.githubusercontent.com/haris4587/ClaimProofSeal/5fe675fa9887570ee3b39245ff8f4f9a3847d5d5/fixtures/field-addendum.txt)

## Review scope

No frontend, tokens, payments, escrow, external wallet or provider reconfiguration. Real Full Consensus assessed synthetic evidence. Offline tests mock web/LLM host I/O and are distinct from the live run. Only SUPPORTED certifies documentary entailment; PARTIALLY_SUPPORTED is a non-certifying gap report. Authentication proves bytes at a configured publication location, not publisher honesty or universal real-world truth. The initial undetermined run is disclosed in deployment documentation.
