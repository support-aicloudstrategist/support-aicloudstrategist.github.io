# AI Workflow Decision: Auto-Act or Ask First?

Use this five-check educational gate before allowing an AI-assisted workflow to act.

| Check | AUTO-ACT lane | ASK-FIRST lane |
|---|---|---|
| Scope | Bounded, approved and reversible | Ambiguous, external-facing or high-impact |
| Data | Approved, necessary and non-sensitive | Secrets, personal data or restricted data |
| Evidence | Rule matched and required evidence is available | Evidence is missing, stale or conflicting |
| Review | Action is logged and included in an approved review process | Human approval is required before action |
| Failure control | Tested stop or rollback path is ready | No safe stop, rollback or accountable owner |

Decision rule: AUTO-ACT only when every AUTO-ACT condition is true. Otherwise ASK FIRST.

Local policy and authorized human owners always override this educational gate.

Proof boundary: Educational workflow-design material only — not a security assessment, legal or compliance advice, production authorization, performance guarantee, client case study or customer result.
