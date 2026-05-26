# Sparsh Hair Skin Dermatology Clinic — WhatsApp Board Demo Plan

Date: 2026-05-19
Status: Internal prep complete; customer reply/demo send requires Raj approval.

## Customer context
- Business: Sparsh Hair Skin Dermatology Clinic, Prayagraj
- Outbound WhatsApp sent earlier: plain/simple text asking if AICS can share a free WhatsApp bot demo.
- Inbound reply: `Ok`
- Evidence: `aics-lead-engine-v1/whatsapp-agent/events.log` line 2759
- Current next action: prepare approval-ready formatted WhatsApp reply + demo visual, then send only after Raj approves.

## Demo objective
Show a practical clinic WhatsApp enquiry board, not a generic chatbot.

The demo should make the clinic owner understand:
1. WhatsApp/missed-call/website enquiries can be captured into one simple board.
2. Staff can see what needs reply/callback/appointment confirmation.
3. Owner/manager gets a daily summary.
4. No patient medical data is needed for the first demo.
5. This can work without replacing their existing clinic software.

## What we will show

### 1. WhatsApp incoming enquiry examples
Sample, non-patient-data messages:
- “Hair fall consultation timing?”
- “Acne treatment appointment after 6 PM?”
- “Missed call — please call back.”
- “Laser consultation price range?”

### 2. Clinic enquiry board
Visual board columns:
- New WhatsApp Enquiries
- Appointment Requests
- Staff Follow-up
- Closed / Summary

Demo asset:
- HTML: `reports/sparsh-whatsapp-board-demo-20260519/sparsh-whatsapp-board-demo.html`
- PNG: `reports/sparsh-whatsapp-board-demo-20260519/sparsh-whatsapp-board-demo.png`

### 3. Automation flow
Demo flow:
1. Patient enquiry arrives from WhatsApp/missed call/website/Instagram.
2. System captures name, need, preferred time and consent-safe notes.
3. Staff sees item on board.
4. Reminder triggers for callback/no response.
5. Owner receives daily summary.

### 4. Healthcare/privacy boundary
Say clearly:
- Demo uses sample data only.
- No diagnosis or treatment recommendations.
- No sensitive medical records in first demo.
- Actual deployment will use consent-aware fields and role-based access.

## Demo talking points
- “This is not a heavy CRM.”
- “It is a simple clinic follow-up board for WhatsApp and missed enquiries.”
- “Your staff can use it to avoid missed callbacks.”
- “Owner gets visibility without checking every WhatsApp chat manually.”
- “First step can be a small pilot for enquiry capture and reminders.”

## Approval-ready WhatsApp reply to Sparsh
Use this only with the demo image attached. Do not send as plain text alone.

```text
Namaste Sparsh Hair Skin Dermatology Clinic 👋

Thanks for confirming.

I’m sharing a small *sample WhatsApp enquiry board demo* for a dermatology / skin / hair clinic.

The demo shows how patient enquiries from WhatsApp, missed calls, website forms, or Instagram can be organised into one simple board:

✅ New enquiries
✅ Appointment requests
✅ Staff callback follow-ups
✅ Owner daily summary
✅ No patient medical data required for the first demo

This is not a heavy CRM replacement. It is a practical follow-up board to reduce missed enquiries and make staff handover cleaner.

If useful, we can show a 10–15 minute walkthrough for Sparsh Clinic and adapt the sample flow to your actual enquiry process.

— Anushka Bhattacharya
Director, AICloudStrategist
Website: https://aicloudstrategist.com
WhatsApp: +91 87963 02608
Voice line: +91 80654 80898
Email: contact@aicloudstrategist.com
```

## Readiness status
Ready:
- Demo concept
- Demo board visual
- Approval-ready WhatsApp caption
- Healthcare/privacy talking points

Blocked / needs approval:
- Sending the demo image + caption to Sparsh on WhatsApp.
- Scheduling or offering an exact walkthrough time.

## Recommended next action
Send Raj one approval request for WhatsApp reply to Sparsh with:
- demo board image attached,
- final caption exactly as above,
- clear APPROVE / CHANGES / REJECT options.
