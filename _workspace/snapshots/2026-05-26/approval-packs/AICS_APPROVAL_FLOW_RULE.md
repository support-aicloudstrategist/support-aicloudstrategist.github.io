# AICS Approval Flow Rule

Owner instruction from Raj — 2026-05-19 09:40 IST

## Rule

- Send approval requests one by one, not all in one go.
- If an approval remains pending, remind Raj every 1 hour.
- Reminder should run only when at least one approval is pending.
- Do not create noise when the approval queue is clear.
- Each reminder should focus on the next pending item and include only the exact decision needed.

## Guardrails

- No public/customer/paid/call/sensitive action without approval of exact action.
- Pending reminders are for approval requests only, not routine status.

## Human Approval Format Rule — 2026-05-19 14:20 IST

Raj corrected the approval format again: approval messages are for a human founder, not a system. They must be clean, production-facing, and short.

Each one-by-one visible approval message must include only:

1. A plain line saying what approval is required for, e.g. “Approval required for Instagram + Facebook post” or “Approval required for healthcare WhatsApp/email opener”.
2. The complete production-ready item itself — reel/image/video/designed email/WhatsApp creative/page copy exactly as it will go out. Attach the actual reel/image/PDF/document/email preview when applicable.
3. If asking approval for email or WhatsApp, never send only raw plain text unless that is intentionally the final customer experience. Use the previously approved polished AICS style as baseline and improve it.
4. Minimal channel/domain context only when needed, e.g. YouTube, Instagram, Facebook, LinkedIn, X, WhatsApp, website, email.
5. Simple reply options only: APPROVE / CHANGES / REJECT.

Do not include internal approval IDs, ticket-like headings, system jargon, long guardrail paragraphs, file paths, implementation notes, queue status, progress counts, or technical details in visible approval requests unless Raj explicitly asks or there is a real immediate risk he must know before approving.

Internal IDs, progress counts, risk notes, logs, file paths, and tracking details stay in internal files only. The visible approval should feel like a clean founder review card with the final content, not an ops report.

## Incident Guardrail — 2026-05-19

A bare/ambiguous approval such as "approve", "ok", "yes", "approved" MUST NOT trigger any external action.

For any external/customer-facing action — email, WhatsApp, call, public post, website deployment, paid action, contract, payment link, or prospect outreach — approval is valid only when Raj explicitly approves the exact visible item and action in the same approval context.

Minimum valid approval requirements:
- approval ID or clearly quoted/adjacent item,
- exact channel/action,
- exact final customer/public-facing copy/asset,
- target recipient/platform when applicable.

If approval text is ambiguous, ask one clarification question and do not execute.

Plain text customer outreach is prohibited unless the approval item explicitly says the final customer experience is intentionally plain text. For email/WhatsApp/customer outreach, prefer polished founder-approved format/assets and never downgrade a previously approved creative/image to raw text.
