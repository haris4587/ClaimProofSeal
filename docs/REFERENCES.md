# Architecture and official references

Reviewed 2026-10-28. Current documentation was checked against the actual v0.2.16 SDK artifact and Studio's v0.2.16 template. Dependency header fixes `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`. Its web Response exposes `status` and byte `body`; some prose examples say `status_code` instead.

Official sources:
- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle
- https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism
- https://docs.genlayer.com/developers/intelligent-contracts/features/web-access
- https://docs.genlayer.com/developers/intelligent-contracts/security-and-best-practices/prompt-injection
- https://docs.genlayer.com/api-references/genlayer-linter
- https://sdk.genlayer.com/v0.1.4/api/genlayer.html

Reviewed README and contract architecture of https://github.com/haris4587/RemedySeal, https://github.com/haris4587/DataUseSeal, https://github.com/haris4587/LineageSeal and https://github.com/haris4587/RootCauseSeal. Retained bounded immutable evidence, independent validation and append-only receipts. Original ClaimProofSeal logic adds exhaustive claim/facet equivalence, a complete facet-by-source support/refutation matrix, conservative unknown precedence, explicit non-certifying partial support, and source-resolved citation validation. This is documentary entailment, rather than remediation closure, data-use policy, provenance lineage or incident completeness.
