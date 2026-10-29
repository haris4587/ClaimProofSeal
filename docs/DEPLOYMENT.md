# Verified deployment and Full Consensus

Completed 2026-10-28 using **GenLayer Studio's built-in account**, no external wallet. Public Studio sandbox / Studionet, chain ID **61999**, pinned GenVM runner **v0.2.16**. This is a test environment, not mainnet.

| Item | Verified value |
|---|---|
| Contract | [0xcD1E22b8B459b9A9d63A962538b7b332f420b908](https://explorer-studio.genlayer.com/address/0xcD1E22b8B459b9A9d63A962538b7b332f420b908) |
| Studio account | `0x647C6E2B4C62edFc774613d8B53d5f32e67edFFc` |
| Deployment | [0xb563fe1f1ae7374cc39ab46ae1d1dbc0222380ad50b2e74ca0f7a1d399817330](https://explorer-studio.genlayer.com/tx/0xb563fe1f1ae7374cc39ab46ae1d1dbc0222380ad50b2e74ca0f7a1d399817330) — FINALIZED, SUCCESS, Accepted |
| Registration | [0xf7186c2538da8aecfe98458e57b74cc6169176af952831e863a5dcb9effb63fa](https://explorer-studio.genlayer.com/tx/0xf7186c2538da8aecfe98458e57b74cc6169176af952831e863a5dcb9effb63fa) — FINALIZED, SUCCESS, Accepted |
| Semantic Full Consensus | [0x2f964d996fa85e092203615315bf3409bf1a36595fe0fbcceedc55d5c04d91b9](https://explorer-studio.genlayer.com/tx/0x2f964d996fa85e092203615315bf3409bf1a36595fe0fbcceedc55d5c04d91b9) — FINALIZED, SUCCESS, Accepted |
| Final source commit | [`25a2185b8e3d4746895566296b19ad76afdeb993`](https://github.com/haris4587/ClaimProofSeal/commit/25a2185b8e3d4746895566296b19ad76afdeb993) |
| Final source SHA-256 | `a52d1148e85d840d5beaf39aad508029d63b9628a707718f055e5c51a290b270` |
| Request ID | `c405c61e9c6b429787065f9d619d5b66458277cd38b37d46bf928082e580a9c1` |
| Package hash | `9d9bb51c431a34e7317d072d7f1e806eea89f65516f226eb27c89d6e70dd1de5` |
| Decision hash | `e3cf107521d8469d9d3ccd85cda1e2d8cfcc83b6aba6bc90c615c73174bfbf9a` |
| Stored verdict | **CONTRADICTED**, coverage VERIFIED, row (facet 0, source 0) REFUTE |

The final source was committed and pushed **before** deployment. Later documentation/evidence commits preserve these exact source bytes. The final documentation commit is supplied in the delivery message; the source commit above is the immutable deployment anchor.

## Meaningful real test

The immutable claim says the 48-hour battery endurance result for Lumen hardware revision A applies outdoors. The authenticated synthetic field addendum says outdoor testing measured **12 hours**, and explicitly states that the indoor 48-hour figure does not apply outdoors. The real validators retrieved that pinned file and reached documentary refutation. This is a real AI/web consensus test over synthetic evidence; no real product assertion is made.

Explorer showed **Normal** execution, five initially selected validators, **zero rotations**, and displayed votes **3 agree / 2 disagree**. It is majority consensus, not unanimity. Finalized at **2026-10-28 20:02:08 Asia/Colombo** (14:32:08 UTC). State was re-read with Studio's **Finalized** selector after finalization, rather than relying on accepted state or only the leader's return.

[Finalized request](../evidence/finalized-request.json) · [Finalized decision](../evidence/finalized-decision.json) · [Transaction observation](../evidence/full-consensus-finalized-observed.txt) · [Finalized state observation](../evidence/finalized-state-observed.txt) · [Vote observation](../evidence/consensus-votes-observed.txt) · [Screenshot](../evidence/full-consensus-finalized.jpg) · [Deployment/transaction list](../evidence/deployment-observed.txt) · [Machine record](../evidence/deployment.json)

## Exact source and receipt verification

Explorer's Code tab was read back into [deployed-source.py](../evidence/deployed-source.py), preserving original source bytes including final newline. `cmp` and SHA-256 match the final contract and the GitHub source at the source commit. `scripts/verify_live.py --remote` verifies request identity, package hash, receipt hash, history linkage, outcome, contract/chain binding, resolved quotations and deployed/source/GitHub byte equality. [Verification result](../evidence/verification.json).

58 actual-SDK direct-mode tests pass: [JUnit](../evidence/junit.xml), [summary](../evidence/test-results.json). GenVM AST lint, SDK validation and schema extraction pass: [lint/SDK result](../evidence/lint.json), [ABI](abi.json). Tests mock web/LLM I/O and explicitly execute validator closures; only the separate live transaction demonstrates network consensus. Prompt-injection offline tests verify guards/data flow and fail-closed paths, not empirical immunity across real models.

## Reproduction in Studio

1. Open https://studio.genlayer.com and use its built-in account.
2. Upload `contracts/claim_proof_seal.py`; select **Normal (Full Consensus)**.
3. Deploy with publisher `haris4587/ClaimProofSeal`; wait for finalized successful deployment.
4. Call `register` with the exact JSON in `examples/contradicted.json`. Wait for successful registration and copy its returned request ID (a different deployment produces a different ID).
5. Call `evaluate` with that ID. Verify FINALIZED, GenVM SUCCESS and Accepted consensus in Explorer.
6. Select **Finalized** for read methods; read `get_request(id)` and `get_decision(id, 1)`. Verify the exact receipt hashes with the supplied script.

No validator/provider settings were changed and Leader Only mode was never used for the live test.

## Failure retained and fixed

The initial source at [0xe334547fC224fdBFC231fc2b67799F4b99f28A78](https://explorer-studio.genlayer.com/address/0xe334547fC224fdBFC231fc2b67799F4b99f28A78), source commit `eba15498be62a588be29db17dc147e184cc022f7`, produced [UNDETERMINED](https://explorer-studio.genlayer.com/tx/0xfc03a4a8b4992288f25d2ec72a1572bc8516761f18bf429ab412f48fe26596b3) after rotations. One observed leader correctly identified REFUTE but marked coverage UNKNOWN because it conflated synthetic evidence with claim decomposition. No decision was stored. The final source clarifies that coverage is only claim/facet semantic equivalence, independent of truth/support/synthetic status, and adds bounded rejection diagnostics. It preserves every integrity, citation and independent-validation gate. This diagnosis does not claim to explain every dissenting validator. [Initial observed state](../evidence/initial-undetermined-observed.txt) and [initial source snapshot](../evidence/initial-deployed-source.py) remain available. Two deployments total; one semantic test on each. The initial run is not represented as a success.
