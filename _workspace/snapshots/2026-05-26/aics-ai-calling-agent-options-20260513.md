# AICloudStrategist: AI Calling / Voice Automation Options for Indian Prospect Outreach

Date: 2026-05-13  
Scope: free/low-cost options to set up an AI calling agent for Indian prospect outreach and qualification. No calls were made, no accounts were created, and no paid signup was performed.

## Executive recommendation

**Recommended first low-cost path:** do **not** begin with cold automated outbound calls. Start with a **consent-first inbound/opt-in MVP** using an Indian cloud telephony provider plus an Indian-language voice stack.

Best practical sequence:

1. **Week 1 MVP, lowest compliance risk:** WhatsApp / landing page / form asks prospects to opt in to a callback or voice note. Use AI to draft personalized WhatsApp text + short voice-note scripts, but keep sending and calling human-approved.
2. **Week 2 voice bot pilot:** inbound or scheduled callback only, using **Exotel or Knowlarity** for Indian numbers/telephony + webhook/SIP bridge to **LiveKit Agents** or a simple server. Use **Sarvam AI** for Indian STT/TTS, with OpenAI/Azure/OpenAI Realtime or another LLM for reasoning.
3. **Outbound automation only after compliance setup:** use consented numbers, NCPR/DND scrubbing, telemarketer/principal entity/provider approvals, opt-out handling, recording disclosure, and daily call caps. Keep a human fallback.

Why: India has strict UCC/DND enforcement. Twilio’s India voice guidance says outbound calls to India through Twilio can only be made from international non-Indian numbers and that commercial-call consent is required; TRAI says mobile numbers cannot be used for telemarketing and UCC complaints can cause disconnection/blacklisting. Indian providers are more realistic for domestic caller ID, KYC, routing, and regulatory operations.

## Key requirements fit

| Requirement | Best-fit options | Notes |
|---|---|---|
| Realistic human-like Indian/North Indian voice | Sarvam Bulbul, ElevenLabs, Azure Neural TTS, Google TTS | Sarvam is strongest India-first option; ElevenLabs is high quality but Indian language/accent fit must be tested. |
| Hindi + English switching | Sarvam STT/TTS + LLM prompt/router; OpenAI/Azure realtime | Prompt agent to identify user language and switch register: professional English vs local Hindi/Hinglish. |
| Regional languages | Sarvam, Bhashini, Google/Azure | Bhashini can be useful but may require onboarding and SLA validation. |
| Inbound/outbound calling in India | Exotel, Knowlarity, Plivo India, local SIP provider | Twilio is constrained for domestic India outbound. |
| Recording/transcription | Exotel/Knowlarity/Plivo recording + Sarvam/Google/Azure STT | Always disclose recording and store securely. |
| CRM logging | Webhooks to HubSpot/Zoho/Airtable/Sheets | Capture call outcome, transcript, consent, language, lead score. |
| Low cost/free tier | Plivo $10 credits; Azure free Speech hours; ElevenLabs free credits; Sarvam pay-as-you-go | Telephony and compliance setup can still require KYC or sales contact. |
| Human-like latency | LiveKit/Retell/Vapi/Bland/OpenAI realtime | Full-duplex interruption/barge-in is harder with DIY Asterisk. |

## Provider and stack comparison

### 1. Exotel

**Fit:** high for India telephony, numbers, call recording, IVR/contact center, possible AI/automation integrations.  
**Strengths:** India-first provider; likely smoother KYC, domestic routing, caller ID, DND/compliance workflows; good for businesses that need Indian numbers and reliable call flows.  
**Weaknesses:** pricing not transparent on public page; AI voice quality depends on integration/provider; may require sales call and contract.  
**Cost expectation:** public page asks to contact sales. For planning, assume Indian cloud telephony voice often lands around **₹0.8–₹2.5/min** plus number/platform/recording/agent costs, but verify before committing.  
**Use:** recommended telephony layer for serious India pilot.

### 2. Knowlarity

**Fit:** high for Indian cloud telephony, IVR, auto dialer, virtual numbers, speech analytics/voicebot categories.  
**Strengths:** India presence, enterprise voice, telemarketing-aware workflows.  
**Weaknesses:** pricing and modern LLM agent integration need sales validation.  
**Cost expectation:** likely custom/package pricing.  
**Use:** compare with Exotel if domestic outbound is important.

### 3. Plivo

**Fit:** medium-high; programmable voice, AI agents, free credits.  
**Evidence:** public pricing page showed **$10 free credits**, voice local outbound **$0.0115/min**, inbound **$0.0055/min**, AI voice agent **$0.05/min**, ASR **$0.02/15 sec**, transcription **$0.0095/min**, call recording included/free on that page.  
**Indicative cost:** telephony local outbound ≈ **₹0.96/min** at ₹83/USD; AI agent add-on ≈ **₹4.15/min**, so roughly **₹5–₹7/min** before taxes/extra model usage if using Plivo AI Agent.  
**Strengths:** transparent pricing, developer-friendly, credits.  
**Risks:** confirm India number availability, KYC, domestic outbound caller ID, and compliance constraints before using for real outreach.

### 4. Twilio

**Fit:** medium for international programmable voice; lower for India domestic outbound.  
**Evidence:** Twilio India voice guidelines state outbound calls to India can only be made from international non-Indian numbers, and commercial communication requires recipient consent. Toll-free in-locale inbound is supported, but toll-free outbound is not.  
**Strengths:** excellent APIs, docs, recordings, webhooks, SIP/BYOC.  
**Weaknesses:** not ideal for Indian prospect calls because international CLI can reduce pickup and may trigger spam suspicion.  
**Use:** useful for prototypes, international calling, or BYOC/SIP, but not the first choice for Indian domestic outreach.

### 5. Asterisk / FreePBX

**Fit:** medium for DIY telephony control; low for fast human-like AI unless paired with realtime media bridge.  
**Strengths:** open-source PBX, SIP trunks, call recording, IVR, queues, low infra cost.  
**Weaknesses:** India SIP trunk/KYC still needed; real-time barge-in, streaming STT/TTS, turn-taking, and observability are engineering-heavy; maintenance/security burden.  
**Indicative cost:** VPS ₹500–₹2,000/month + SIP trunk/minutes + engineering time.  
**Use:** good if you already operate telephony; not best first MVP.

### 6. LiveKit Agents + SIP

**Fit:** high for custom real-time agent architecture.  
**Evidence:** LiveKit Agents supports Python/Node realtime voice agents, transcripts/traces in cloud, inbound/outbound call support via telephony/SIP; LiveKit phone numbers are US-focused, but it supports third-party SIP trunks.  
**Strengths:** open framework, strong latency/turn-taking, provider-agnostic STT/LLM/TTS, deploy yourself or cloud.  
**Weaknesses:** you still need Indian SIP/telephony provider; more engineering than Vapi/Bland/Retell.  
**Use:** best customizable stack with Exotel/Knowlarity/SIP + Sarvam/OpenAI.

### 7. Vapi

**Fit:** high for rapid voice-agent prototyping; medium for India telephony unless BYO telephony works cleanly.  
**Evidence:** pricing page showed **$0.05/min** Vapi hosting, 10 included concurrent calls, model provider costs at-cost or bring-your-own key.  
**Indicative cost:** **₹4.15/min** Vapi + telephony + STT/LLM/TTS.  
**Strengths:** fast build, tool calling, integrations, supports provider choice.  
**Weaknesses:** India number/caller ID/compliance must be solved separately; model stack can become expensive.  
**Use:** good prototype UI/orchestration if budget allows.

### 8. Bland AI

**Fit:** medium-high for fast hosted voice AI; uncertain India domestic calling.  
**Evidence:** pricing page showed **$0.14/min** individual plan, includes LLM/STT/TTS/telephony, 10 concurrent calls, 100 calls/day; free credits and inbound number mentioned.  
**Indicative cost:** **₹11.6/min** all-in before taxes, assuming India calling supported at same rate; verify.  
**Strengths:** simple flat pricing, fast to test, good agent tooling.  
**Weaknesses:** more expensive; India phone support and compliance uncertain; data residency likely not India by default.  
**Use:** demo/proof-of-concept, not cheapest India production path.

### 9. Retell AI

**Fit:** high for polished voice agents; India telephony must be validated.  
**Strengths:** batch calling, post-call analysis, integrations, call transfer, verified phone features.  
**Weaknesses:** pricing page extraction did not show rates; likely usage-based; domestic India and compliance need verification.  
**Use:** compare if quality and speed matter more than lowest cost.

### 10. Sarvam AI

**Fit:** very high for Indian languages and voices.  
**Evidence:** public API pricing showed pay-as-you-go, Pro ₹10,000, Business ₹50,000; TTS Bulbul v3 **₹30/10K characters**, Bulbul v2 **₹15/10K characters**; STT **₹30/hour**, STT with diarization **₹45/hour**; translation **₹20/10K characters**.  
**Indicative per-minute speech cost:** STT ≈ **₹0.50/min**; TTS depends on words/characters, roughly **₹1–₹4/min** for typical bot speech.  
**Strengths:** India-first language support, Hindi/regional coverage, likely best for natural local voice.  
**Weaknesses:** you still need telephony and agent orchestration.  
**Use:** recommended TTS/STT layer.

### 11. Bhashini

**Fit:** useful India-language infrastructure, especially for public/low-cost experimentation.  
**Strengths:** Indian language mission, ASR/TTS/translation ecosystem.  
**Weaknesses:** production API access, latency, quality, documentation, quotas, and SLA must be validated; may not be as plug-and-play as commercial APIs.  
**Use:** test as fallback/benchmark, not primary first production path unless access is confirmed.

### 12. Azure / Google Speech / OpenAI Realtime

**Azure Speech:** free tier includes 5 audio hours/month STT and 0.5M TTS characters/month; good enterprise compliance and Indian languages, but voice naturalness must be tested.  
**Google Speech/TTS:** broad language support; public pricing page was hard to extract in this run, but it is a mature option for STT/TTS.  
**OpenAI Realtime:** excellent for low-latency speech-to-speech and language switching. Public pricing showed GPT-Realtime-2 audio token pricing and Whisper realtime transcription at **$0.017/min**; actual full speech-to-speech cost varies by token usage.  
**Use:** OpenAI/Azure can power intelligence and real-time conversation; Sarvam may sound more Indian/local.

### 13. Rasa / LLM voice bot

**Fit:** medium for deterministic flows, qualification scripts, handoff rules.  
**Strengths:** good for controlled dialogue and forms; can pair with LLM for flexible language.  
**Weaknesses:** voice stack still required; Rasa alone is not a calling solution.  
**Use:** only if qualification flow needs strict state machine and auditability.

### 14. WhatsApp voice-note alternative

**Fit:** high for low-risk outreach, low cost, and Indian prospect comfort.  
**Approach:** send a consent-based WhatsApp message or short AI-generated voice note from a verified WhatsApp Business workflow; ask “Would you like a 2-minute callback?” Then call only opt-ins.  
**Strengths:** avoids cold-call perception, better context, async, cheaper, easier personalization.  
**Weaknesses:** WhatsApp Business policy and templates apply; bulk unsolicited messaging is also risky; true conversational calling is not achieved.  
**Use:** recommended before automated outbound calls.

## Compliance and risk notes for India

Not legal advice; verify with counsel/provider before production.

1. **Consent is central.** Commercial calls without consent can be treated as UCC. Maintain proof of consent: source, timestamp, purpose, number, opt-in wording.
2. **DND/NCPR scrubbing.** TRAI says users can register preferences in NCPR/DND and complain to 1909. Scrub campaign lists and suppress DND unless legally permitted with consent/transactional basis.
3. **Do not use ordinary mobile numbers for telemarketing.** TRAI FAQ says using a mobile number for telemarketing can lead to disconnection and blacklisting.
4. **Provider onboarding/KYC.** Indian virtual numbers, toll-free, SIP trunks, and outbound campaigns generally need business KYC and use-case approval.
5. **Call recording disclosure.** Announce recording at start or obtain explicit consent. Store recordings/transcripts with access control and retention limits.
6. **AI disclosure.** Safer script: “I’m an AI assistant calling on behalf of AICloudStrategist. Is this a good time?” Deceptive human impersonation is a reputational and regulatory risk.
7. **Opt-out.** Support “do not call me again” in Hindi/English/regional language; immediately write to suppression list.
8. **Calling windows and frequency.** Restrict hours, cap retries, avoid repeated attempts, never auto-redial aggressively.
9. **Sensitive sectors.** Finance, insurance, healthcare, education, real estate may have additional consent and advertising rules.
10. **Data protection.** Treat phone numbers, recordings, transcripts, and lead scores as personal data. Minimize fields, encrypt, and honor deletion requests.

## Suggested MVP architecture

### Consent-first inbound/callback MVP

```text
Lead source / WhatsApp / form
        ↓ consent + language preference
CRM / Google Sheet / Airtable / Zoho
        ↓ approved callback queue
Indian telephony provider: Exotel / Knowlarity / Plivo / SIP trunk
        ↓ SIP/WebSocket media bridge
LiveKit Agents or Vapi
        ↓
STT: Sarvam STT or Azure/Google/OpenAI Whisper realtime
LLM: OpenAI / Azure OpenAI / local hosted LLM for lead qualification
TTS: Sarvam Bulbul Hindi/Indian English voice, fallback ElevenLabs/Azure
        ↓
Call recording + transcript + lead score + next action
        ↓
CRM log + suppression/opt-out list + human handoff
```

### Agent behavior

- Opening: disclose AI + company + purpose + ask permission to continue.
- Language detection: start in professional English; if user replies Hindi/Hinglish, switch to local Hindi/Hinglish. For North India: polite, concise, non-pushy.
- Qualification fields: business type, current challenge, budget/timeline, decision-maker, preferred follow-up channel.
- Safety: no false claims, no pressure, no sensitive financial/medical advice.
- Handoff: transfer to human or schedule meeting if qualified/interested/confused/angry.
- Close: summarize, confirm consent for follow-up, offer opt-out.

## Rough monthly cost scenarios

Assumptions: 1,000 calls/month, average 2 minutes, 2,000 call-minutes. INR/USD ≈ 83. Provider taxes/platform fees excluded.

| Stack | Estimated variable cost | Notes |
|---|---:|---|
| Exotel/Knowlarity + Sarvam + LLM | ~₹4,000–₹15,000/month | Telephony estimate ₹1–₹2.5/min + Sarvam speech ₹1.5–₹4/min + LLM. Verify provider quotes. |
| Plivo AI Agent | ~₹10,000–₹14,000/month | Based on Plivo voice $0.0115/min + AI agent $0.05/min; India support/compliance must be validated. |
| Vapi + Indian SIP + Sarvam/OpenAI | ~₹12,000–₹25,000/month | Vapi hosting ₹4.15/min + SIP + model costs. Faster build. |
| Bland hosted | ~₹23,000+/month | $0.14/min all-in if India supported at same rate; simplest but pricier. |
| Asterisk/FreePBX DIY + Sarvam | Lowest cash, highest engineering | VPS cheap, but realtime AI integration and compliance ops cost time. |
| WhatsApp opt-in + human callback | Lowest risk/cost | AI assists scripts, summaries, and qualification; calling can remain human initially. |

## Recommended implementation plan

### Phase 0: Compliance and data hygiene (2–3 days)

- Define permitted target list: existing contacts, inbound leads, event opt-ins, website leads.
- Create consent fields in CRM: source, timestamp, purpose, language, opt-out status.
- Create suppression list and DND-scrub process.
- Draft approved scripts in English, Hindi, Hinglish.
- Decide recording disclosure text and retention policy.

### Phase 1: Non-calling proof (2–4 days)

- Build WhatsApp/email/landing opt-in workflow.
- Generate personalized voice-note/text scripts with AI.
- Human approves first 50 messages.
- Capture opt-in callback requests.

### Phase 2: Inbound/scheduled callback agent (1–2 weeks)

- Get Indian telephony sandbox/number from Exotel/Knowlarity/Plivo.
- Build webhook server + LiveKit/Vapi agent.
- Use Sarvam STT/TTS and LLM qualification prompt.
- Log transcript, summary, disposition, lead score to CRM.
- Test with internal numbers only, then 20–50 opt-in prospects.

### Phase 3: Limited outbound pilot (after approvals)

- Only consented prospects.
- Max 1–2 attempts/contact, business hours only.
- Human monitoring and instant takeover for first 100 calls.
- Track pickup rate, hang-up rate, complaint/opt-out rate, qualified meetings, cost per qualified lead.

## Practical recommendation

For AICloudStrategist, the best first build is:

**Exotel or Knowlarity for Indian telephony + LiveKit Agents + Sarvam AI STT/TTS + OpenAI/Azure/OpenAI-compatible LLM + CRM webhook.**

If fastest demo matters more than control, test **Vapi** or **Plivo AI Agent** with BYO Sarvam/OpenAI and confirm India calling before production. If lowest compliance risk matters, start with **WhatsApp opt-in voice-note workflow** and schedule AI-assisted callbacks only after explicit consent.

## Sources checked

- TRAI UCC FAQ: mobile numbers not permitted for telemarketing; DND/NCPR complaint process via 1909.
- Twilio India Voice Guidelines: outbound to India only from international non-Indian numbers; consent required for commercial communications.
- Twilio India Regulatory Guidelines: India toll-free regulatory info.
- Plivo Pricing: $10 credits, voice, AI agent, transcription/ASR pricing.
- Sarvam AI API Pricing: STT/TTS/translation/chat pricing in INR.
- Vapi Pricing: $0.05/min hosting plus model provider cost.
- Bland AI Pricing: $0.14/min individual flat rate and included features.
- Azure Speech Pricing: free tier with STT hours and TTS characters.
- OpenAI API Pricing: realtime and transcription prices.
- LiveKit Agents and Telephony docs: realtime agents, SIP trunks, inbound/outbound call support.
- Exotel and Knowlarity public pages: India cloud telephony/contact center/automation positioning; detailed pricing requires sales validation.
