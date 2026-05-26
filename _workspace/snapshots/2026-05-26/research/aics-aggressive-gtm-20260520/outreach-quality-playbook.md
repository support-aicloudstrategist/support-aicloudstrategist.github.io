# AICloudStrategist Outreach Quality-Improvement Playbook

Created: 2026-05-20 22:15 IST  
Scope: AICS prospect/customer outreach quality control for email, WhatsApp, calls, social creatives, approval cards, and follow-ups.  
Status: Internal playbook only. No customer sends, public posts, calls, paid actions, or credential changes performed.

## 1. Why this exists

Recent outreach work improved speed, but quality risk is now the constraint. The DIAG-LAB-A lane showed the correct pattern for guarded, approval-gated category sends, while earlier diagnostics outreach exposed critical failures:

- Wrong WhatsApp number used externally: old `+91 78383 47711` instead of current `+91 87963 02608`.
- Wrong public identity used externally: Rajiv personal name instead of `Anushka Bhattacharya, Director, AICloudStrategist`.
- Earlier outreach used `support@aicloudstrategist.com` as a prospecting sender; this is now prohibited.
- Some approval cards are too operational and not founder-friendly.
- Some WhatsApp creatives are visually not send-ready even when the copy is compliant.

Current verified AICS public contact source checked live on 2026-05-20:

- Website: `https://aicloudstrategist.com/`
- Free review: `https://aicloudstrategist.com/free-business-review`
- Primary customer/prospect email: `contact@aicloudstrategist.com`
- Support reference only: `support@aicloudstrategist.com`
- WhatsApp Business: `+91 87963 02608`
- Voice line: `+91 80654 80898`
- Default public signature: `Anushka Bhattacharya, Director, AICloudStrategist`

## 2. Non-negotiable quality principle

Speed must never bypass source verification, visual QA, exact-item founder approval, or guarded execution.

If an operator cannot prove the final customer experience is exactly what Raj approved, the item is not send-ready.

## 3. Preflight checklist — required before any approval request

Complete this before sending an approval card to Raj or routing a rendered approval email.

### Source-of-truth checks

- [ ] Fetch `https://aicloudstrategist.com/contact-channels.json` or use the local website repo fallback if live fetch fails.
- [ ] Confirm WhatsApp is `+91 87963 02608` and no asset contains `+91 78383 47711`.
- [ ] Confirm voice line is `+91 80654 80898` and do not call it toll-free.
- [ ] Confirm customer/prospect sender is `contact@aicloudstrategist.com` only.
- [ ] Confirm `support@aicloudstrategist.com` appears only as support reference, never as prospecting sender.
- [ ] Confirm signature is Anushka Bhattacharya, Director, AICloudStrategist, unless Raj explicitly approved another identity.

### Recipient/route checks

- [ ] Each prospect route is public or credibly sourced.
- [ ] Email prospects have verified public email; phone-only prospects must not be forced into email outreach.
- [ ] WhatsApp/call prospects have route confidence and no ambiguity between multiple numbers.
- [ ] Healthcare prospects are business contacts only; do not request patient data, reports, passwords, OTPs, payment details, admin access, or customer databases.

### Asset checks

- [ ] Email is premium HTML with plain-text fallback only.
- [ ] WhatsApp is not plain-text-only unless Raj explicitly approves that exact plain-text experience.
- [ ] Visual creative is reviewed on mobile-sized view for crop, contrast, spelling, readability, CTA clarity, and internal-note leakage.
- [ ] Approval card shows the final production item, not file paths and ops jargon.
- [ ] Copy avoids guarantees, fake metrics, unsupported claims, client logos/testimonials not approved, legal/medical/compliance certification claims, and fear-heavy language.

### Approval checks

- [ ] Approval request is one item only.
- [ ] Raj sees the exact rendered production item or exact creative/caption/call opener.
- [ ] Reply options are simple: `APPROVE / CHANGES / REJECT`, or a clearly named approval keyword for category sends.
- [ ] No bare “approve/ok/yes” is treated as valid unless it is clearly attached to the exact current item/action/target/channel.

## 4. Asset separation rules

Every outreach lane must separate these artifacts. Do not mix them.

### A. Founder approval asset

Purpose: help Raj decide.  
May include: decision options, target count, risk note if critical, final customer item preview.  
Must not include: long internal logs, hidden assumptions, implementation scripts, or noisy file-path lists unless Raj asked.

### B. Customer-facing asset

Purpose: what the prospect/customer receives.  
Must include only polished business-facing copy/creative.  
Must not include: “founder approval only”, internal IDs, queue names, approval keywords, internal SOP notes, route confidence notes, or dashboard language.

### C. Operator execution manifest

Purpose: internal execution control.  
Contains: recipient, route source, approved asset path, approval evidence, sender, send method, status, evidence path, next follow-up gate.

### D. QA evidence

Purpose: prove readiness.  
Contains: screenshot/image review, contact grep result, render preview, guard dry-run evidence, source reverification timestamp.

Hard rule: if a visual says “prepared for founder approval only”, it can never be sent to a prospect. Create a clean external version first and get fresh approval.

## 5. Visual QA checklist

Run this for every WhatsApp creative, social image, inline email visual, and founder review card image.

- [ ] Canvas has enough safe margin; no headline, logo, footer, or CTA is cropped.
- [ ] Text is readable on mobile at WhatsApp preview size.
- [ ] Brand/logo has enough contrast.
- [ ] Footer/contact details are not too tiny.
- [ ] No internal approval text appears in customer-facing versions.
- [ ] CTA wording is consistent across headline, button, caption, and link.
- [ ] No outdated phone/email/identity appears in pixels.
- [ ] No risky or exaggerated claim appears in headline/subhead.
- [ ] Decorative shapes do not crowd business-critical text.
- [ ] Export a final PNG/WebP and review the actual exported file, not just source SVG/HTML.

Observed fixes from recent assets:

- `aesthetic-clinic-whatsapp-review-card.png`: headline is cropped on the right. Do not send externally until corrected.
- `healthcare-whatsapp-creative-founder-approval.png`: contains internal founder-approval text and low-contrast brand/footer areas. Do not send externally; produce a clean customer version first.
- `template-category-diag-lab-a-card-v2.png`: suitable as internal/founder category approval visual only; do not use as prospect WhatsApp outreach creative.

## 6. Approval-routing rules

### One-by-one routing

- Route one pending approval at a time.
- If one approval is pending, do not pile a second unrelated approval on top.
- Hourly reminder is allowed only for the single next pending item and must stay concise.

### Valid approval must include

- Exact item/action: email, WhatsApp, call, public post, website publish, correction, etc.
- Exact channel/route.
- Exact target(s) or platform(s), if applicable.
- Exact final customer/public copy or creative.
- Clear approval wording tied to that item.

### Invalid approval examples

- “ok” after a long queue summary.
- “approve” when multiple items were visible.
- “send it” when the production email was not shown/rendered.
- Approval of an internal/founder creative used to justify sending a different customer asset.

### Corrections after mistakes

If a customer-facing mistake is discovered:

1. Stop all sends in that lane.
2. Log the incident.
3. Prepare a corrected production-grade item.
4. Route correction to Raj as one standalone approval.
5. Send only after explicit correction approval, through guarded execution.

## 7. Copywriting quality bar

### Universal bar

- Clear, businesslike, Indian-English friendly.
- Specific to the sector and the likely workflow problem.
- Short enough for the channel.
- One primary CTA.
- No desperation, spam tone, fake urgency, or “AI magic” claims.
- No claim that AICS has audited the business unless an actual audit was performed.
- No “guaranteed leads/revenue/savings/compliance/security”.
- Always include a respectful opt-out line for cold WhatsApp/email.

### Email bar

- Premium HTML first; text fallback only.
- Subject should be concrete, not clickbait.
- Opening must identify why the business is being contacted without sounding surveillance-heavy.
- CTA should be a free review/call, not a hard sale.
- Footer must include current AICS channels and Anushka Director identity.
- Use guarded `contact@` send only.

### WhatsApp bar

- Prefer image + polished caption.
- Caption must be shorter than email and easy to read on mobile.
- Include opt-out: “If this is not relevant, reply STOP/not interested and we will not follow up.”
- Do not send raw walls of text.
- If calling is paired with WhatsApp, script must be approved separately or shown in same approval card.

### Call opener bar

- State name, company, and purpose within first 15 seconds.
- No pressure; ask whether to send details on WhatsApp first.
- Explicitly say no patient data/system access is needed for healthcare review.
- Stop if receptionist/business says not interested.

## 8. Sector-specific do/don't rules

### Healthcare, diagnostics, dental, aesthetic clinics

Do:
- Focus on enquiry leakage, callbacks, appointment follow-up, report-delivery queries, WhatsApp/call handover, owner visibility.
- Say “no patient data required” for initial review.
- Offer practical 3–5 fixes after a short review.

Don't:
- Claim medical outcome improvement.
- Claim NABH/ABDM/DPDP/HIPAA/legal compliance certification.
- Ask for patient records, reports, prescriptions, EMR/LIS/HIS access, screenshots with PHI, passwords, OTPs, or admin credentials.
- Use fear-heavy patient-safety language.

### Education/coaching

Do:
- Focus on missed admissions enquiries, counselling follow-up, fee/course query tracking, parent/student communication.

Don't:
- Promise admissions growth, exam results, rankings, or placement outcomes.

### Manufacturing/export/RFQ

Do:
- Focus on RFQ tracking, catalogue/website enquiry capture, distributor/export lead follow-up, quotation visibility.

Don't:
- Promise export orders, procurement approvals, or compliance certification.

### Real estate/property services

Do:
- Focus on lead source tracking, site-visit follow-up, WhatsApp/call response discipline, duplicate lead control.

Don't:
- Promise sales, investment returns, RERA/legal outcomes, or buyer financing.

### Salon/beauty/local services

Do:
- Focus on booking follow-up, missed calls, WhatsApp appointment flow, reviews, repeat customer reminders.

Don't:
- Make beauty/health outcome claims or before/after result promises.

### Food/restaurant/cloud kitchen

Do:
- Focus on order enquiry flow, catering leads, Google/WhatsApp/menu link clarity, repeat customer prompts.

Don't:
- Claim hygiene certification, delivery platform ranking, revenue growth, or food-safety compliance.

### CA/tax/professional services

Do:
- Focus on appointment scheduling, client document checklist flow, enquiry triage, recurring reminder systems.

Don't:
- Claim tax savings, legal advice, compliance guarantee, or audit protection.

## 9. Safer one-by-one approval workflow

Use this workflow for every outbound campaign.

1. Select one lane only.
2. Create/reuse customer-facing asset.
3. Run source-of-truth and recipient checks.
4. Run visual/copy QA.
5. Create internal execution manifest.
6. Send Raj one clean founder approval card with the exact final item.
7. Wait.
8. If Raj says `CHANGES`, revise and restart from QA.
9. If Raj says `REJECT`, archive lane; do not re-route immediately.
10. If Raj clearly approves, execute one recipient/platform at a time.
11. After each send/post/call, log evidence and update dashboard.
12. Do not follow up until the monitoring window matures and follow-up copy is separately approved.

## 10. Post-approval execution rules

### Email

- Reverify recipient source if approval is older than 60 minutes or if route was unstable.
- Personalize only approved placeholders.
- Send one by one via `aics_mail_send_guard.py` from `contact@aicloudstrategist.com`.
- No CC/BCC/bulk unless specifically approved.
- Save guarded evidence under `reports/outbound-mail/`.

### WhatsApp

- Use only exact approved image/caption/recipient route.
- If a number is ambiguous or unreachable, stop that recipient and log blocked; do not substitute another number.
- Do not downgrade image+caption approval into plain text.
- Do not add follow-up messages unless approved.

### Calls

- Use exact approved opener.
- If asked for details, send only approved WhatsApp/email copy or return for approval.
- Do not improvise pricing, promises, or technical commitments.

### Social/website

- Publish only approved platform/page.
- No boosts, DMs, reposts, cross-posts, or channel expansion without separate approval.
- For website, stage/noindex approval and public-publish approval are separate gates.

## 11. Quality gates before scaling beyond 1–2 sends

Do not scale a template category beyond two individually verified sends until all are true:

- No contact/identity/sender mistakes in the last 48 hours for that lane.
- At least one render/visual QA pass is recorded.
- Dashboard state is clean and unambiguous.
- Follow-up policy is defined before first send.
- Template has sector-specific risk review.
- Raj approved category-level reuse explicitly, not just one recipient.

## 12. Stop conditions

Immediately stop execution if any of these occur:

- Old WhatsApp number appears anywhere.
- Rajiv personal name appears in customer/prospect copy without explicit approval.
- `support@` is about to be used as prospecting sender.
- Creative is cropped, unreadable, or contains internal notes.
- Approval is ambiguous or multiple items were visible.
- Route/source cannot be reverified.
- Customer reply asks for pricing, proposal, data handling, contract, compliance, or technical setup details not already approved.
- Any prospect asks to stop, unsubscribe, or not be contacted.

## 13. Minimum evidence to save per lane

- Source-of-truth contact check timestamp.
- Recipient/route source evidence.
- Final customer asset path.
- Founder approval card path and approval evidence.
- Guarded send/post/call evidence.
- Dashboard update path.
- Reply-monitor/follow-up gate.

## 14. Immediate recommendations from this audit

1. Regenerate the aesthetic clinic WhatsApp card before any approval/send because the headline is cropped.
2. Create a clean external version of the healthcare WhatsApp/call creative; current founder PNG must not be sent to prospects because it contains internal approval text.
3. Keep DIAG-LAB-A in monitor-only mode until 2026-05-22 19:47 IST; no follow-up without fresh premium follow-up approval.
4. Keep diagnostics correction as a standalone approval item; do not bundle it with new outreach.
5. For all future aggressive GTM work, approve and execute one lane at a time, with a maximum of two initial sends per new sector template until QA evidence is clean.
