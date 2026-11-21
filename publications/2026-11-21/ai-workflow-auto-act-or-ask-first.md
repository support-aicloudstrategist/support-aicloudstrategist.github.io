# AI Workflow Decision: Auto-Act or Ask First?

![AI Workflow Decision: Auto-Act or Ask First?](https://support-aicloudstrategist.github.io/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.png)

A five-check educational gate for deciding when an AI-assisted workflow may take a bounded action and when a human should review first.

1. **Scope.** AUTO-ACT: Bounded, approved and reversible ASK FIRST: Ambiguous, external-facing or high-impact
2. **Data.** AUTO-ACT: Approved, necessary and non-sensitive ASK FIRST: Secrets, personal data or restricted data
3. **Evidence.** AUTO-ACT: Rule matched and required evidence is available ASK FIRST: Evidence is missing, stale or conflicting
4. **Review.** AUTO-ACT: Action is logged and included in an approved review process ASK FIRST: Human approval is required before action
5. **Failure control.** AUTO-ACT: Tested stop or rollback path is ready ASK FIRST: No safe stop, rollback or accountable owner

**Decision rule:** AUTO-ACT only when every AUTO-ACT condition is true. Otherwise ASK FIRST.

Local policy and authorized human owners always override this educational gate.

Worksheet: https://support-aicloudstrategist.github.io/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.csv

**Proof boundary:** Educational workflow-design material only — not a security assessment, legal or compliance advice, production authorization, performance guarantee, client case study or customer result.

Public page: https://support-aicloudstrategist.github.io/publications/2026-11-21/ai-workflow-auto-act-or-ask-first.html
