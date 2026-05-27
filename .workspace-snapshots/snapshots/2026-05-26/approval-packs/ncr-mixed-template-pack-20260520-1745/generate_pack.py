from pathlib import Path
import json, csv, html, textwrap
out = Path('reports/approval-packs/ncr-mixed-template-pack-20260520-1745')
contacts = {
  'brand':'AICloudStrategist',
  'website':'https://aicloudstrategist.com/',
  'freeReview':'https://aicloudstrategist.com/free-business-review',
  'email':'contact@aicloudstrategist.com',
  'supportEmail':'support@aicloudstrategist.com',
  'whatsapp':'+91 87963 02608',
  'whatsappUrl':'https://wa.me/918796302608?text=Namaste%20AICloudStrategist%2C%20I%20want%20a%20free%20business%20review.',
  'voiceLine':'+91 80654 80898',
  'voiceTel':'+918065480898',
}
templates = {
'HEALTHCARE-A':{
 'name':'Healthcare / diagnostics / dental / aesthetic clinics','subject':'Free enquiry-flow review for {{business_name}}','pre':'Find missed patient enquiries across calls, WhatsApp, forms and callbacks — without patient medical data.','hero':'Patient enquiries should not disappear between calls, WhatsApp and follow-ups','lead':'Many clinics and diagnostics teams receive enquiries from calls, WhatsApp, website forms and repeat follow-ups. The practical gap is usually visibility: who needs a callback, what is pending, and where the enquiry came from.','promise':'AICloudStrategist helps clinic teams review the admin workflow and identify simple fixes for enquiry capture, callback visibility and appointment follow-up. No patient medical data is required for the first review.','bullets':['Missed call / WhatsApp enquiry visibility','Callback and appointment follow-up status','Staff handover and daily owner/manager summary','Privacy-aware first review; no treatment or outcome claims'], 'cta':'Can we share a free 10-minute enquiry-leakage review for {{business_name}}?','guard':'Healthcare guardrail: admin/enquiry workflow only; no medical advice, outcome, diagnosis, treatment or compliance guarantee claims.'},
'EDU-A':{
 'name':'Education / coaching / training institutes','subject':'Free course-enquiry leakage review for {{business_name}}','pre':'A simple review of how course enquiries move from call/WhatsApp/form to counsellor follow-up.','hero':'Course enquiries go cold when follow-up is invisible','lead':'Training and coaching teams usually receive enquiries from calls, WhatsApp, website forms and repeat student or parent questions. Good leads can go cold when counsellor routing and follow-up are not visible.','promise':'AICloudStrategist helps institutes review enquiry capture, counsellor assignment and follow-up reminders so the admissions/support team has a cleaner operating flow.','bullets':['New enquiry capture across website/call/WhatsApp','Counsellor assignment and pending follow-up reminders','FAQ and WhatsApp routing opportunities','Daily lead visibility without admissions/result promises'], 'cta':'Can we share a free 10-minute lead-leakage review for {{business_name}}?','guard':'Education guardrail: no claims about admissions, marks, ranks, results or conversion guarantees.'},
'MFG-A':{
 'name':'Manufacturing / export / RFQ businesses','subject':'Free RFQ and buyer follow-up review for {{business_name}}','pre':'Find gaps in RFQ capture, catalogue sharing, quote follow-up and buyer visibility.','hero':'B2B enquiries should not get lost between forms, catalogues and quotes','lead':'Manufacturers and exporters often receive enquiries from website forms, phone calls, WhatsApp, catalogues and repeat quote follow-ups. The leakage is usually operational: RFQs are not captured consistently or followed up visibly.','promise':'AICloudStrategist helps B2B teams review RFQ capture, catalogue/spec-sheet routing, quote follow-up reminders and secure cloud document sharing.','bullets':['RFQ and enquiry capture hygiene','Catalogue/spec-sheet response workflow','Quote follow-up reminders and sales visibility','Cloud folder and basic domain/email hygiene review'], 'cta':'Can we share a free 10-minute RFQ leakage review for {{business_name}}?','guard':'Manufacturing guardrail: consultative workflow review only; no unsupported revenue/export performance claims.'},
'RE-A':{
 'name':'Real estate / brokerage / property services','subject':'Free lead-routing visibility review for {{business_name}}','pre':'A practical review of source-wise lead capture, team routing and callback visibility.','hero':'Real estate leads need fast routing, not more chaos','lead':'Real estate leads often arrive from ads, website forms, WhatsApp, calls and branch teams. The problem is not only lead generation; it is whether every lead is routed and followed up on time.','promise':'AICloudStrategist helps teams review source-wise lead capture, branch/team assignment, callback visibility and daily manager summaries.','bullets':['Source-wise lead capture and routing','Team/branch assignment visibility','Pending callback and WhatsApp follow-up support','Daily manager summary without investment-return claims'], 'cta':'Can we share a free 10-minute lead-routing review for {{business_name}}?','guard':'Real-estate guardrail: no investment return, price appreciation, RERA/legal or sales guarantee claims.'},
'SALON-A':{
 'name':'Salon / beauty / aesthetic chains','subject':'Free appointment-flow review for {{business_name}}','pre':'Review missed bookings, WhatsApp/Instagram enquiries, outlet routing and feedback capture.','hero':'Bookings are lost when enquiries sit across calls, WhatsApp and Instagram','lead':'Salon and beauty enquiries often come through calls, WhatsApp, Instagram, repeat customers and outlet teams. Missed follow-ups affect appointment flow and customer experience.','promise':'AICloudStrategist helps salons review booking enquiries, outlet-wise follow-up visibility, WhatsApp reply support and feedback/review capture.','bullets':['Missed enquiry and booking follow-up tracking','Outlet-wise owner/manager visibility','WhatsApp reply and reminder workflow','Feedback and review capture opportunities'], 'cta':'Can we share a free 10-minute appointment-flow review for {{business_name}}?','guard':'Salon guardrail: appointment/customer-experience workflow only; no medical/aesthetic outcome claims.'},
'FOOD-A':{
 'name':'Restaurant / bakery / cloud kitchen / food retail','subject':'Free customer-support workflow review for {{business_name}}','pre':'Review scattered order queries, support routing, SLA visibility and feedback capture.','hero':'Customer queries should not scatter across store, app, phone and WhatsApp channels','lead':'Food and retail brands receive customer queries from websites, apps, phone, WhatsApp and store channels. When support and feedback are scattered, issues take longer to resolve.','promise':'AICloudStrategist helps teams review enquiry and complaint routing, WhatsApp/order-help workflows, SLA visibility, cloud backup and process hygiene.','bullets':['Enquiry and complaint routing map','WhatsApp/order-help automation opportunities','SLA and pending-ticket visibility','Feedback/review capture and process hygiene'], 'cta':'Can we share a free 10-minute customer-support workflow review for {{business_name}}?','guard':'Food/retail guardrail: operational support review only; no platform integration or SLA guarantee unless scoped later.'},
'PROF-A':{
 'name':'CA / tax / professional services firms','subject':'Free secure client-workflow review for {{business_name}}','pre':'Review client intake, document reminders, cloud folder structure and pending-task visibility.','hero':'Client documents and reminders need a secure workflow, not scattered follow-ups','lead':'Professional-service firms handle client documents, reminders and follow-ups across email, WhatsApp and calls. The risk is scattered intake and missed client actions.','promise':'AICloudStrategist helps firms review client intake tracking, document collection reminders, secure cloud folder structure and basic email/domain/cloud hygiene.','bullets':['Client intake and pending task visibility','Document collection reminders','Secure cloud folder structure review','Email/domain/cloud hygiene without legal or tax advice'], 'cta':'Can we share a free 10-minute client-workflow review for {{business_name}}?','guard':'Professional-services guardrail: technology/process support only; no tax/legal advice or compliance guarantee claims.'},
}
base_css='font-family:Arial,Helvetica,sans-serif;color:#17213a;'
for code,t in templates.items():
    safe_code=code.lower()
    bullet_html=''.join(f'<tr><td style="padding:8px 0;font-size:15px;line-height:23px;color:#33415f;">✅ {html.escape(b)}</td></tr>' for b in t['bullets'])
    body=f'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{html.escape(t['subject'])}</title></head>
<body style="margin:0;padding:0;background:#edf3ff;{base_css}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#edf3ff;font-size:1px;line-height:1px;">{html.escape(t['pre'])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#edf3ff;"><tr><td align="center" style="padding:28px 10px;">
<table role="presentation" width="720" cellpadding="0" cellspacing="0" border="0" style="width:720px;max-width:720px;background:#ffffff;border-radius:22px;overflow:hidden;box-shadow:0 14px 38px rgba(16,38,83,.14);">
<tr><td style="background:linear-gradient(135deg,#07101f,#102653 55%,#1f62ff);padding:34px 40px;color:#fff;">
<div style="font-size:12px;letter-spacing:1.3px;text-transform:uppercase;color:#a9c5ff;font-weight:bold;">AICloudStrategist free workflow review • {code}</div>
<h1 style="margin:12px 0 10px;font-size:32px;line-height:40px;color:#ffffff;">{html.escape(t['hero'])}</h1>
<p style="margin:0;font-size:16px;line-height:26px;color:#dce8ff;">Prepared for <strong>{{{{business_name}}}}</strong></p>
</td></tr>
<tr><td style="padding:30px 40px 8px;">
<p style="margin:0 0 18px;font-size:16px;line-height:27px;color:#33415f;">Namaste {{{{business_name}}}} Team,</p>
<p style="margin:0 0 18px;font-size:17px;line-height:29px;color:#33415f;">{html.escape(t['lead'])}</p>
<p style="margin:0 0 20px;font-size:17px;line-height:29px;color:#33415f;">{html.escape(t['promise'])}</p>
</td></tr>
<tr><td style="padding:10px 40px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8fbff;border:1px solid #dde8fb;border-radius:18px;"><tr><td style="padding:22px 24px;">
<div style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#59667d;font-weight:bold;">What the free review checks</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:8px;">{bullet_html}</table>
</td></tr></table></td></tr>
<tr><td style="padding:24px 40px 8px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#102653;border-radius:20px;"><tr><td style="padding:24px;color:#ffffff;">
<h2 style="margin:0 0 10px;font-size:24px;line-height:31px;color:#ffffff;">{html.escape(t['cta'])}</h2>
<p style="margin:0;font-size:15px;line-height:25px;color:#dce8ff;">If useful, reply <strong>REVIEW</strong> or book a free review. We will keep it practical and specific to your current enquiry/support workflow.</p>
</td></tr></table>
</td></tr>
<tr><td style="padding:22px 40px 30px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="background:#1f62ff;border-radius:14px;"><a href="{contacts['freeReview']}" style="display:inline-block;padding:15px 24px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:bold;">Book the free review</a></td>
<td width="14"></td>
<td style="background:#ecf3ff;border:1px solid #d7e5ff;border-radius:14px;"><a href="{contacts['whatsappUrl']}" style="display:inline-block;padding:14px 22px;color:#102653;text-decoration:none;font-size:15px;font-weight:bold;">WhatsApp AICloudStrategist</a></td>
</tr></table>
<p style="margin:18px 0 0;font-size:14px;line-height:23px;color:#5a6780;">{html.escape(t['guard'])}</p>
</td></tr>
<tr><td style="padding:0 40px 30px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #dde8fb;border-radius:18px;background:#f8fbff;"><tr><td style="padding:20px 22px;">
<div style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#59667d;font-weight:bold;">Contact resources</div>
<p style="margin:8px 0 0;font-size:15px;line-height:25px;color:#33415f;"><strong>Website:</strong> <a href="{contacts['website']}" style="color:#1f62ff;text-decoration:none;">aicloudstrategist.com</a><br>
<strong>Free review:</strong> <a href="{contacts['freeReview']}" style="color:#1f62ff;text-decoration:none;">aicloudstrategist.com/free-business-review</a><br>
<strong>WhatsApp Business:</strong> <a href="{contacts['whatsappUrl']}" style="color:#1f62ff;text-decoration:none;">{contacts['whatsapp']}</a><br>
<strong>Voice line:</strong> <a href="tel:{contacts['voiceTel']}" style="color:#1f62ff;text-decoration:none;">{contacts['voiceLine']}</a><br>
<strong>Email:</strong> <a href="mailto:{contacts['email']}" style="color:#1f62ff;text-decoration:none;">{contacts['email']}</a><br>
<strong>Support:</strong> <a href="mailto:{contacts['supportEmail']}" style="color:#1f62ff;text-decoration:none;">{contacts['supportEmail']}</a></p>
</td></tr></table></td></tr>
<tr><td style="background:#07101f;padding:24px 40px;color:#aebde0;font-size:12px;line-height:20px;">
<strong style="color:#ffffff;">Anushka Bhattacharya</strong><br>Director, AICloudStrategist<br>Website: <a href="{contacts['website']}" style="color:#dce8ff;text-decoration:none;">aicloudstrategist.com</a> • Email: <a href="mailto:{contacts['email']}" style="color:#dce8ff;text-decoration:none;">contact@aicloudstrategist.com</a> • WhatsApp: {contacts['whatsapp']} • Voice line: {contacts['voiceLine']}<br><br>If this is not relevant, reply STOP and we will not follow up.
</td></tr>
</table></td></tr></table></body></html>'''
    (out/'html'/f'{safe_code}-premium-email.html').write_text(body, encoding='utf-8')
    txt=f"""Subject: {t['subject']}
Sender: Anushka Bhattacharya, Director, AICloudStrategist <contact@aicloudstrategist.com>

Namaste {{{{business_name}}}} Team,

{t['lead']}

{t['promise']}

What the free review checks:
""" + ''.join(f"- {b}\n" for b in t['bullets']) + f"""
{t['cta']}

Free review: {contacts['freeReview']}
WhatsApp: {contacts['whatsapp']}
Voice line: {contacts['voiceLine']}
Email: {contacts['email']}
Support: {contacts['supportEmail']}

— Anushka Bhattacharya
Director, AICloudStrategist
Website: {contacts['website']}

Guardrail: {t['guard']}
If this is not relevant, reply STOP and we will not follow up.
"""
    (out/'text'/f'{safe_code}-fallback.txt').write_text(txt, encoding='utf-8')
# Build target mapping from prospect CSV
mapping=[]
category_to_code={'Dental clinic':'HEALTHCARE-A','Diagnostics centre':'HEALTHCARE-A','Hospital group':'HEALTHCARE-A','Dermatology/aesthetic clinic':'HEALTHCARE-A','IT training institute':'EDU-A','Training company':'EDU-A','Coaching / test prep':'EDU-A','School coaching institute':'EDU-A','Industrial equipment manufacturer':'MFG-A','Industrial components manufacturer/exporter':'MFG-A','Plastic injection moulding manufacturer':'MFG-A','Private label clothing manufacturer/exporter':'MFG-A','Garment manufacturer/exporter':'MFG-A','Real estate services':'RE-A','Salon chain':'SALON-A','Salon/aesthetic chain':'SALON-A','Bakery/cloud kitchen/e-commerce food':'FOOD-A','Restaurant/sweets chain':'FOOD-A','CA / professional services firm':'PROF-A','CA / tax advisory firm':'PROF-A','CA firm':'PROF-A','CA / NRI tax advisory firm':'PROF-A'}
with open('reports/prospecting/ncr-mixed-20260520/prospects.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        code=category_to_code.get(r['category'],'REVIEW')
        mapping.append({'business_name':r['business_name'],'template_code':code,'recommended_channel':r['recommended_channel'],'public_email':r['public_email'],'public_phone_whatsapp':r['public_phone_whatsapp'],'website_source_url':r['website_source_url'],'confidence':r['confidence'],'risk_notes':r['risk_notes']})
(out/'target-template-map.json').write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding='utf-8')
with open(out/'target-template-map.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=mapping[0].keys()); w.writeheader(); w.writerows(mapping)
summary = ['# NCR Mixed Prospect Premium Outreach Template Pack — 2026-05-20 17:45 IST','', 'Status: **Approval-ready internal asset; no customer send/public post performed.**','', '## SOP verification','- Live contact source checked: https://aicloudstrategist.com/contact-channels.json at 2026-05-20 17:45 IST / 12:15 UTC.','- WhatsApp Business: **+91 87963 02608**.','- Voice line: **+91 80654 80898**.','- Sender/primary customer email: **contact@aicloudstrategist.com**.','- Support email used only as support reference: **support@aicloudstrategist.com**.','- Default signature: **Anushka Bhattacharya, Director, AICloudStrategist**.','- Email format: **premium HTML** with plain-text fallback only.','- Customer sends/public outreach blocked until Raj approval and guarded contact@ execution.','', '## Files created']
for code in templates:
    summary.append(f'- `{out}/html/{code.lower()}-premium-email.html` — {templates[code]["name"]}')
    summary.append(f'- `{out}/text/{code.lower()}-fallback.txt` — fallback only')
summary += ['', '## Target queue','- Prospects: 25 from `reports/prospecting/ncr-mixed-20260520/prospects.csv`.','- Mapping JSON: `target-template-map.json`.','- Mapping CSV: `target-template-map.csv`.','', '## Next safe action','After Raj approves NCR category/template mapping, send Raj personal approval email(s) with rendered production HTML before any customer send. Then execute only approved sends via `aics_mail_send_guard.py` from contact@.']
(out/'README.md').write_text('\n'.join(summary)+'\n', encoding='utf-8')
print(out)
