# DPDP Compliance Sprint — Scoped Delivery Template

Canonical artifact: `/home/OpenClaw/.openclaw/workspace/reports/week1-brief/templates/dpdp-sprint-scoped-delivery-template.md`
Status: TEMPLATE — not legal advice and not customer-specific until scoped with verified client data.
Owner: AICloudStrategist / Jarvis orchestration
Approval requirement: Any customer-facing version requires an approval pack before sending.

---

## 1. Scope Summary

**Client / Business name:** [VERIFIED BUSINESS NAME]
**Business category:** [CATEGORY]
**Website / app reviewed:** [URL]
**Prepared for:** [CONTACT NAME or UNKNOWN]
**Prepared by:** AICloudStrategist
**Date:** [YYYY-MM-DD]

**Sprint objective:** Help the business create a practical first-layer DPDP/privacy readiness foundation for its website, lead forms, WhatsApp enquiry handling, consent language, internal process documentation, and vendor/contact-data hygiene.

**Sprint price:** ₹14,999 one-time, no retainer commitment. Founder Customer Program discount available — see https://aicloudstrategist.com/pricing.html

**Important disclaimer:** This sprint is an operational/privacy-readiness implementation support package. It is not legal advice. The client should consult qualified legal counsel for legal interpretation or final compliance sign-off.

## Brand and People Note

Anushka Bhattacharya is Director at AICloudStrategist and her photo/name may appear in AICloudStrategist public-facing material. Keep Anushka's Director identity and name intact wherever already used. Do not replace Anushka's photo/name with an unverified Rajiv/Raj headshot unless founder identity is confirmed with HIGH confidence and Rajiv approves the exact asset.

---

## 2. Included Deliverables

| Deliverable | Included? | Output format | Owner | Notes |
|---|---:|---|---|---|
| Website privacy/trust review | YES | Findings table | AICS | Based on public website and client inputs |
| Privacy policy gap checklist | YES | Markdown/Doc | AICS | Not legal advice |
| Consent language recommendations | YES | Copy block | AICS | For forms/WhatsApp where applicable |
| Lead form data-flow map | YES | Table/diagram | AICS + client | Requires client process input |
| WhatsApp enquiry handling SOP | YES | SOP | AICS | Covers consent-aware follow-up |
| Vendor/tool register template | YES | Spreadsheet/table | AICS | Client must verify tools/vendors |
| Data retention starter policy | YES | Draft SOP | AICS | Client must approve retention periods |
| Incident/breach readiness checklist | YES | Checklist | AICS | Operational readiness only |
| Staff handling checklist | YES | Checklist | AICS | Simple SMB-friendly version |
| Final implementation summary | YES | Report | AICS | With evidence and open items |

---

## 3. Explicit Exclusions

This sprint does not include unless separately approved and scoped:

- Legal opinion or legal representation
- Formal DPO appointment
- Enterprise GRC platform implementation
- Security penetration testing
- SOC 2 / ISO 27001 certification
- Full audit of all internal systems
- Bulk customer messaging
- Any claim that the client is “fully compliant”
- Any regulatory filing unless explicitly approved

---

## 4. Client Inputs Required

| Input | Required? | Status | Notes |
|---|---:|---|---|
| Website URL | YES | [PENDING/RECEIVED] | [Notes] |
| Forms/contact pages list | YES | [PENDING/RECEIVED] | [Notes] |
| WhatsApp/call enquiry process | YES | [PENDING/RECEIVED] | [Notes] |
| CRM/sheet/tool list | YES | [PENDING/RECEIVED] | [Notes] |
| Staff who access leads | YES | [PENDING/RECEIVED] | [Notes] |
| Current privacy policy | IF AVAILABLE | [PENDING/RECEIVED/NA] | [Notes] |
| Consent language currently used | IF AVAILABLE | [PENDING/RECEIVED/NA] | [Notes] |
| Vendor list | IF AVAILABLE | [PENDING/RECEIVED/NA] | [Notes] |
| Data retention expectations | YES | [PENDING/RECEIVED] | [Notes] |
| Escalation contact for incidents | YES | [PENDING/RECEIVED] | [Notes] |

Unknown fields must be marked `UNKNOWN`.

---

## 5. Sprint Workflow

### 14-Day Delivery Calendar

| Day | Activity | Output / acceptance evidence |
|---:|---|---|
| Day 1 | Kickoff call (60 min), client inputs collected, scope confirmed, deliverable acceptance criteria signed | Kickoff notes, input checklist, signed/approved acceptance criteria |
| Day 2-4 | Privacy policy draft + cookie banner code deployment + form consent language deployment | Draft policy, deployed/ready code snippets, form consent screenshots or implementation notes |
| Day 5-7 | WhatsApp opt-in templates submitted for Meta approval + opt-in process documentation | Submitted template IDs/status, opt-in SOP draft, approval/pending evidence |
| Day 8-10 | Data inventory CSV completed + data-handling SOP draft + vendor register completed | Completed CSV, SOP draft, vendor register with UNKNOWNs marked |
| Day 11-13 | Board-ready 1-page compliance summary + staff handling checklist + breach escalation playbook | Summary, checklist, escalation playbook |
| Day 14 | Final review call, sign-off, evidence pack handover, 30-day check-in scheduled | Final call notes, signed/confirmed handover, evidence pack path, check-in date |

Calendar rule: If a client dependency is missing, mark the day as `WAITING_CLIENT_INPUT`, record the blocker, and do not invent missing facts.

---

## 6. DPDP Readiness Checklist

| Area | Current status | Evidence | Risk | Recommended action |
|---|---|---|---|---|
| Privacy policy visible | [YES/NO/UNKNOWN] | [URL/path] | [LOW/MED/HIGH] | [Action] |
| Contact form consent language | [YES/NO/UNKNOWN] | [URL/path] | [LOW/MED/HIGH] | [Action] |
| WhatsApp opt-in clarity | [YES/NO/UNKNOWN] | [URL/path] | [LOW/MED/HIGH] | [Action] |
| Purpose limitation clarity | [YES/NO/UNKNOWN] | [URL/path] | [LOW/MED/HIGH] | [Action] |
| Data retention stated | [YES/NO/UNKNOWN] | [URL/path] | [LOW/MED/HIGH] | [Action] |
| Vendor/tool list exists | [YES/NO/UNKNOWN] | [client input] | [LOW/MED/HIGH] | [Action] |
| Staff access process defined | [YES/NO/UNKNOWN] | [client input] | [LOW/MED/HIGH] | [Action] |
| Customer deletion/correction process | [YES/NO/UNKNOWN] | [client input] | [LOW/MED/HIGH] | [Action] |
| Breach escalation path | [YES/NO/UNKNOWN] | [client input] | [LOW/MED/HIGH] | [Action] |
| Consent-aware marketing process | [YES/NO/UNKNOWN] | [client input] | [LOW/MED/HIGH] | [Action] |

## 6a. Reusable Artifact Library

These sub-templates are ready to fork per client. Replace all bracketed placeholders before customer-facing use.

### Cookie banner HTML/JS snippet

```html
<div id="aics-cookie-banner" style="display:none; position:fixed; left:16px; right:16px; bottom:16px; z-index:9999; max-width:960px; margin:auto; padding:16px; border-radius:14px; background:#111827; color:#ffffff; box-shadow:0 12px 35px rgba(0,0,0,0.25); font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <p style="margin:0 0 10px; line-height:1.5;">
    [BUSINESS NAME] uses essential cookies to run this website and optional cookies to understand enquiries and improve service. Read our
    <a href="[PRIVACY URL]" style="color:#93c5fd; text-decoration:underline;">privacy policy</a>.
  </p>
  <div style="display:flex; gap:10px; flex-wrap:wrap;">
    <button type="button" id="aics-cookie-accept" style="border:0; border-radius:999px; padding:10px 16px; background:#22c55e; color:#052e16; font-weight:700; cursor:pointer;">Accept optional cookies</button>
    <button type="button" id="aics-cookie-reject" style="border:1px solid #64748b; border-radius:999px; padding:10px 16px; background:transparent; color:#ffffff; font-weight:700; cursor:pointer;">Reject optional cookies</button>
  </div>
</div>
<script>
(function () {
  var cookieName = 'aics_cookie_consent';
  function getCookie(name) {
    return document.cookie.split('; ').find(function (row) { return row.indexOf(name + '=') === 0; });
  }
  function setConsent(value) {
    var maxAge = 60 * 60 * 24 * 180;
    document.cookie = cookieName + '=' + encodeURIComponent(value) + '; Max-Age=' + maxAge + '; Path=/; SameSite=Lax';
    document.getElementById('aics-cookie-banner').style.display = 'none';
    window.dispatchEvent(new CustomEvent('aicsCookieConsent', { detail: { consent: value } }));
  }
  function init() {
    var banner = document.getElementById('aics-cookie-banner');
    if (!banner || getCookie(cookieName)) return;
    banner.style.display = 'block';
    document.getElementById('aics-cookie-accept').addEventListener('click', function () { setConsent('accepted'); });
    document.getElementById('aics-cookie-reject').addEventListener('click', function () { setConsent('rejected'); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>
```

### Data inventory CSV template

```csv
data_field,collection_point,purpose,retention_period,processor,location,consent_basis,access_owner
full_name,website_contact_form,respond_to_enquiry,[RETENTION PERIOD],[PROCESSOR],[LOCATION],[CONSENT/LEGITIMATE PURPOSE],[ROLE/OWNER]
phone_number,whatsapp_or_call,respond_to_enquiry_and_follow_up,[RETENTION PERIOD],[PROCESSOR],[LOCATION],[CONSENT/LEGITIMATE PURPOSE],[ROLE/OWNER]
email,website_contact_form,send_requested_information,[RETENTION PERIOD],[PROCESSOR],[LOCATION],[CONSENT/LEGITIMATE PURPOSE],[ROLE/OWNER]
service_interest,lead_form_or_whatsapp,understand_customer_requirement,[RETENTION PERIOD],[PROCESSOR],[LOCATION],[CONSENT/LEGITIMATE PURPOSE],[ROLE/OWNER]
```

Required columns: `data_field`, `collection_point`, `purpose`, `retention_period`, `processor`, `location`, `consent_basis`, `access_owner`.

### Board summary doc template

```markdown
# DPDP Readiness Sprint — 1-Page Board Summary

## Business context
[BUSINESS NAME], [VERTICAL], [CITY]. Scope covered: website, lead forms, WhatsApp enquiry handling, vendor/tool register, staff handling process.

## Applicability of DPDP
[Plain-English applicability summary. Mark UNKNOWN where legal interpretation is needed. This is operational readiness support, not legal advice.]

## Key risks identified
1. [Risk 1 + evidence/source]
2. [Risk 2 + evidence/source]
3. [Risk 3 + evidence/source]

## Remediations completed
- [Completed remediation 1 + evidence]
- [Completed remediation 2 + evidence]
- [Completed remediation 3 + evidence]

## Open items
- [Open item 1 + owner + due date]
- [Open item 2 + owner + due date]
- [Open item 3 + owner + due date]

## Next-review date
[YYYY-MM-DD]
```

---

## 6b. Acceptance Criteria per Deliverable

| Deliverable | Done means |
|---|---|
| Website privacy/trust review | All in-scope public website pages and lead/contact paths are reviewed, source URLs are recorded, and findings are categorized by risk. Unknown or inaccessible items are explicitly marked `UNKNOWN` rather than assumed. |
| Privacy policy gap checklist | A checklist exists comparing visible/current policy coverage against practical DPDP readiness needs, with each gap tied to evidence or client input. It avoids legal-certification language and clearly marks counsel-review items. |
| Consent language recommendations | Draft consent/helper text is prepared for every in-scope form, WhatsApp flow, and relevant enquiry channel. Each copy block is ready for client/legal review and does not imply consent where no opt-in process exists. |
| Lead form data-flow map | Every in-scope data field is mapped from collection point to destination, processor/tool, access owner, purpose, and retention assumption. Missing client inputs are listed as open dependencies. |
| WhatsApp enquiry handling SOP | A step-by-step SOP exists for consent-aware WhatsApp response, follow-up, opt-out handling, and escalation. Any Meta template approval dependency is recorded separately and not treated as complete until evidence exists. |
| Vendor/tool register template | A vendor/tool register is created with all known processors and UNKNOWN placeholders for missing client-confirmed tools. The register includes purpose, data handled, owner, and follow-up action. |
| Data retention starter policy | A starter retention SOP exists with proposed retention periods, deletion/review triggers, and owner roles. Final retention periods remain client/legal decisions unless explicitly confirmed. |
| Incident/breach readiness checklist | A practical incident checklist exists covering detection, internal escalation, evidence capture, client/customer communication decision points, and owner responsibilities. It does not claim regulatory compliance or legal sufficiency. |
| Staff handling checklist | A simple staff-facing checklist exists for enquiry data handling, access discipline, sharing restrictions, WhatsApp/email hygiene, and deletion/escalation steps. It is short enough to be used operationally. |
| Final implementation summary | A final report summarizes completed work, evidence paths, open items, client dependencies, and next review date. It includes the disclaimer that this is operational readiness support, not legal advice. |

---

## 7. Recommended Copy Blocks

### Contact form consent helper text

By submitting this form, you agree that [BUSINESS NAME] may contact you about your enquiry using the contact details provided. Your information will be used only for responding to your enquiry and related service communication.

### WhatsApp enquiry consent helper text

When you message us on WhatsApp, we use your message and contact details only to respond to your enquiry, share requested information, and follow up on your service request.

### Privacy/trust page intro

[BUSINESS NAME] respects customer privacy. We collect only the information needed to respond to enquiries, provide services, manage appointments, and improve customer support.

Note: These are operational draft blocks, not legal advice. Final wording should be reviewed by the client and legal counsel where required.

---

## 8. Final Sprint Report Structure

Customer-facing final report must include:

1. Executive summary
2. Reviewed URLs/pages
3. Data collection points
4. Data-flow map
5. DPDP readiness checklist
6. Recommended copy/SOP updates
7. Open items needing client/legal decision
8. Implementation roadmap
9. Evidence appendix
10. Disclaimer

---

## 9. Internal QA Checklist

Before customer-facing use:

- [ ] Client/business facts verified from public source or client input.
- [ ] Every source URL recorded.
- [ ] Unknown fields marked `UNKNOWN`.
- [ ] No claim of full compliance.
- [ ] No legal advice language.
- [ ] No invented metrics or regulatory claims.
- [ ] Approval pack created.
- [ ] Rajiv approved exact rendered version before sending.

---

## 10. Approval Requirement

Any DPDP sprint proposal, customer-facing report, WhatsApp message, email, or public post must go through the mandatory approval pack process before external sending.
