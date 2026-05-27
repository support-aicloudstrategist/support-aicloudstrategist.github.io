# Task 3 Prospect CRM — Field Definitions

| Field | Meaning | Required when populated |
|---|---|---:|
| record_id | Stable internal ID, e.g. AICS-W1-0001 | YES |
| business_name | Business name exactly as found | YES |
| city | City from public source | YES |
| state | State/UT | YES |
| segment | Primary business segment | YES |
| sub_segment | More specific category | NO |
| website_url | Public website if found | NO |
| google_business_profile_url | Public GBP/maps/profile URL if used | NO |
| phone_public | Public phone exactly as found | NO |
| email_public | Public email exactly as found | NO |
| whatsapp_public | Public WhatsApp number/link exactly as found | NO |
| source_url | Public source proving row | YES |
| source_type | Website, GBP, directory, social, etc. | YES |
| source_date | Date source was checked | YES |
| fit_score | 0–100 score | YES |
| fit_reason | Why AICS is relevant | YES |
| lead_leak_hypothesis | Evidence-based possible leak; no claims beyond evidence | YES |
| dpdp_relevance | LOW/MED/HIGH/UNKNOWN | YES |
| recommended_offer | Launch Desk / Lead Recovery Desk / DPDP Sprint / AI Sales Desk / Scale Desk | YES |
| recommended_channel | Approval-only channel recommendation | YES |
| risk_notes | Quality/privacy/relevance cautions | YES |
| verification_status | EMPTY / VERIFIED / EXCLUDED / NEEDS_RECHECK | YES |
| owner | Internal owner/agent | YES |
| stage | New / Research / Approval Pending / Approved / Contacted / Excluded | YES |
| last_action | Last internal action | NO |
| next_action | Next internal action | NO |
| next_action_due | ISO date if any | NO |
| approval_status | Not requested / pending / approved / rejected | YES |
| created_at | ISO timestamp | YES |
| updated_at | ISO timestamp | YES |
