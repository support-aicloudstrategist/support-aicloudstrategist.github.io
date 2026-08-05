#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aicloudstrategist.com"
TODAY = date.today().isoformat()
HANDCRAFTED_FLAGSHIP_SLUGS = {"ai-automation", "ai-mlops", "cloud-finops", "cloud-security"}

PRIMARY_SERVICES = [
    {"title":"Website & Digital Presence Services","slug":"website-digital-presence","kw":"website development services for small business India","desc":"Professional websites, trust pages, lead capture and digital presence systems for Indian small businesses that need to look credible and generate enquiries.","group":"Digital Growth","support":["lead-generation-seo","dpdp-compliance","whatsapp-automation"],"benefits":["Launch a credible business website with clear service, trust and contact sections.","Turn visitors into enquiries through forms, WhatsApp CTAs and lead capture journeys.","Add privacy, terms and basic compliance pages so customers trust the business."],"audience":"local businesses, clinics, consultants, education providers, manufacturers and service companies"},
    {"title":"Lead Generation & SEO Services","slug":"lead-generation-seo","kw":"lead generation services for small business India","desc":"SEO, website lead capture, local discovery and follow-up systems designed to help Indian businesses turn online visibility into qualified enquiries.","group":"Digital Growth","support":["website-digital-presence","crm-automation","ai-automation"],"benefits":["Improve discoverability for commercial search terms.","Capture enquiries from website, WhatsApp and phone channels.","Create follow-up workflows so fewer leads are lost after the first contact."],"audience":"businesses that already have a website but are not getting enough qualified leads"},
    {"title":"AI Automation Services","slug":"ai-automation","kw":"AI automation services for small business","desc":"Practical AI automation for Indian SMBs: lead qualification, appointment booking, customer support, operations workflows and AI agents that reduce manual work.","group":"AI Automation","support":["whatsapp-automation","ai-chatbot-development","voice-ai-agents","crm-automation","workflow-automation"],"benefits":["Automate repetitive sales, support and operations tasks.","Connect website, WhatsApp, CRM and phone workflows.","Deploy AI carefully with human approval gates, privacy and business context."],"audience":"business owners who need more speed without hiring a large operations team"},
    {"title":"WhatsApp Automation Services","slug":"whatsapp-automation","kw":"WhatsApp automation services India","desc":"WhatsApp lead capture, follow-up, reminders, appointment flows and consent-aware automation for Indian businesses that sell through conversations.","group":"AI Automation","support":["ai-chatbot-development","crm-automation","dpdp-compliance","lead-generation-seo"],"benefits":["Respond faster to enquiries from website, ads, calls and referrals.","Route leads into structured follow-up instead of scattered chats.","Design consent-aware message flows aligned with Indian privacy expectations."],"audience":"clinics, real estate teams, coaching centres, D2C brands, local services and consultants"},
    {"title":"AI Chatbot Development Services","slug":"ai-chatbot-development","kw":"AI chatbot development services","desc":"Website and WhatsApp chatbot development for lead capture, qualification, FAQs, appointment routing and customer support automation.","group":"AI Automation","support":["ai-automation","whatsapp-automation","crm-automation","website-digital-presence"],"benefits":["Answer common customer questions instantly.","Qualify leads before a human calls back.","Integrate chatbot conversations with CRM, WhatsApp and email workflows."],"audience":"businesses that receive repeated customer questions or need 24x7 lead capture"},
    {"title":"Voice AI Agent Services","slug":"voice-ai-agents","kw":"AI voice agent services","desc":"AI voice receptionists and calling agents for appointment booking, missed-call recovery, lead qualification and routine customer conversations.","group":"AI Automation","support":["ai-automation","crm-automation","whatsapp-automation","lead-generation-seo"],"benefits":["Recover missed calls and after-hours enquiries.","Book appointments and capture caller intent.","Escalate sensitive or high-value conversations to humans."],"audience":"clinics, salons, fitness studios, real estate teams and appointment-led businesses"},
    {"title":"CRM Automation Services","slug":"crm-automation","kw":"CRM automation services","desc":"CRM setup, sales pipeline automation, lead follow-up reminders and owner dashboards for Indian small businesses that need control over enquiries.","group":"Operations Automation","support":["lead-generation-seo","whatsapp-automation","workflow-automation","ai-automation"],"benefits":["Create one source of truth for enquiries and customer status.","Automate follow-up reminders and lead stages.","Give owners visibility into missed, hot and ageing leads."],"audience":"businesses where leads are currently tracked in WhatsApp, notebooks or disconnected spreadsheets"},
    {"title":"Workflow Automation Services","slug":"workflow-automation","kw":"workflow automation services","desc":"No-code and AI-assisted workflow automation for approvals, reminders, reporting, handoffs and repetitive operations across business tools.","group":"Operations Automation","support":["ai-automation","crm-automation","lead-generation-seo"],"benefits":["Reduce manual copy-paste and repeated coordination.","Connect forms, sheets, CRM, WhatsApp, email and reporting flows.","Document processes so automation is maintainable."],"audience":"businesses with repeated manual tasks across sales, operations, finance or customer service"},
    {"title":"Cloud FinOps & Cost Optimization Services","slug":"cloud-finops","kw":"cloud cost optimization services India","desc":"AWS, Azure and GCP cost review, FinOps controls, waste reduction, tagging hygiene, rightsizing and cloud cost governance for growing teams.","group":"Cloud & Trust","support":["devops-observability","cloud-security","ai-mlops"],"benefits":["Find avoidable cloud waste and quick savings opportunities.","Improve visibility with tagging, budgets, alerts and owner accountability.","Create long-term FinOps habits instead of one-time cleanup."],"audience":"startups, SaaS teams and cloud-heavy businesses with rising AWS, Azure or GCP bills"},
    {"title":"DevOps & Observability Services","slug":"devops-observability","kw":"DevOps consulting services India","desc":"DevOps, SRE and observability consulting for monitoring, alerting, deployment hygiene, reliability and operational visibility.","group":"Cloud & Trust","support":["cloud-finops","cloud-security","ai-mlops"],"benefits":["Improve deployment and incident visibility.","Set up monitoring, alerting and dashboards aligned to business risk.","Reduce downtime surprises and manual firefighting."],"audience":"teams running cloud applications without enough operational visibility"},
    {"title":"Cloud Security Services","slug":"cloud-security","kw":"cloud security consulting India","desc":"Cloud security reviews, AWS/Azure/GCP hygiene, access control checks, exposure reduction and practical security hardening for growing businesses.","group":"Cloud & Trust","support":["cloud-finops","devops-observability","dpdp-compliance"],"benefits":["Identify exposed services, weak access patterns and risky defaults.","Prioritize security fixes by business impact.","Align cloud hygiene with customer trust and compliance needs."],"audience":"businesses that need practical cloud security without enterprise bureaucracy"},
    {"title":"DPDP Compliance Consulting","slug":"dpdp-compliance","kw":"DPDP compliance consultant India","desc":"DPDP readiness, privacy policy, consent flows, vendor registers and website trust hygiene for Indian businesses handling customer data.","group":"Cloud & Trust","support":["website-digital-presence","whatsapp-automation","cloud-security","ai-mlops"],"benefits":["Create practical privacy and consent workflows.","Improve website trust with clear policies and contact routes.","Prepare for customer, vendor and regulatory questions."],"audience":"clinics, labs, D2C brands, SaaS companies and service businesses collecting personal data"},
    {"title":"AI/MLOps & AI Governance Services","slug":"ai-mlops","kw":"AI MLOps consulting","desc":"MLOps, LLMOps, AI deployment governance, model monitoring, cost control and risk management for teams moving AI from experiment to production.","group":"Cloud & Trust","support":["ai-automation","cloud-finops","cloud-security","dpdp-compliance"],"benefits":["Move AI workloads from prototypes to controlled production systems.","Track quality, cost, privacy and operational risk.","Create governance around prompts, data, models and human review."],"audience":"startups and teams building AI-enabled workflows or products"},
]

INDUSTRIES = [
    {"title":"AI Automation for Clinics","slug":"clinics","kw":"AI automation for clinics India","desc":"Digital presence, WhatsApp follow-up, voice AI reception, appointment booking and DPDP-ready trust systems for Indian clinics.","services":["ai-automation","whatsapp-automation","voice-ai-agents","dpdp-compliance","lead-generation-seo"],"problems":["Missed patient enquiries after hours","Manual appointment follow-up","Scattered WhatsApp conversations","Trust and privacy expectations around patient data"]},
    {"title":"Automation for Diagnostic Labs","slug":"diagnostic-labs","kw":"automation for diagnostic labs India","desc":"WhatsApp, lead tracking, report communication hygiene and DPDP-aware digital systems for diagnostic labs.","services":["whatsapp-automation","crm-automation","dpdp-compliance","website-digital-presence"],"problems":["High enquiry volume","Manual report/status communication","Repeat booking follow-up","Sensitive health data handling"]},
    {"title":"Digital Growth for Aesthetic Clinics","slug":"aesthetic-clinics","kw":"digital marketing automation for aesthetic clinics India","desc":"Lead generation, WhatsApp follow-up, consent-aware trust pages and automation systems for aesthetic clinics.","services":["lead-generation-seo","whatsapp-automation","crm-automation","dpdp-compliance"],"problems":["High-value enquiries need fast response","Before/after photo consent","Repeated consultation questions","Lead leakage from social channels"]},
    {"title":"Lead Automation for Dental Clinics","slug":"dental-clinics","kw":"dental clinic lead automation India","desc":"Website, WhatsApp, appointment reminders, missed call recovery and CRM automation for dental clinics.","services":["whatsapp-automation","voice-ai-agents","crm-automation","lead-generation-seo"],"problems":["Missed calls during treatment hours","No-show appointments","Manual reminders","Untracked follow-ups"]},
    {"title":"AI Automation for Real Estate","slug":"real-estate","kw":"AI automation for real estate India","desc":"Lead qualification, WhatsApp follow-up, site visit scheduling and CRM automation for real estate teams.","services":["ai-automation","whatsapp-automation","crm-automation","voice-ai-agents"],"problems":["Large volume of low-quality leads","Delayed first response","Manual site visit coordination","Lost follow-up after first call"]},
    {"title":"Automation for Education & Coaching Institutes","slug":"education-coaching","kw":"automation for coaching institutes India","desc":"Enquiry capture, WhatsApp counselling follow-up, admission pipeline tracking and local SEO for coaching and education businesses.","services":["lead-generation-seo","whatsapp-automation","crm-automation","ai-chatbot-development"],"problems":["Admission enquiry follow-up","Course FAQ repetition","Parent/student WhatsApp tracking","Local discovery competition"]},
    {"title":"WhatsApp Automation for Retail & D2C","slug":"retail-d2c","kw":"WhatsApp automation for D2C brands India","desc":"WhatsApp commerce support, abandoned enquiry follow-up, customer retention and DPDP-aware consent flows for retail and D2C brands.","services":["whatsapp-automation","lead-generation-seo","crm-automation","dpdp-compliance"],"problems":["Repeat customer engagement","Order and support queries","Abandoned carts or abandoned chats","Consent and promotional message hygiene"]},
    {"title":"Websites & Automation for Local Services","slug":"local-services","kw":"website and automation for local services India","desc":"Website, local SEO, WhatsApp lead capture, appointment booking and missed-call recovery for local service businesses.","services":["website-digital-presence","lead-generation-seo","whatsapp-automation","voice-ai-agents"],"problems":["No strong online presence","Calls missed during field work","Weak local search visibility","No structured lead follow-up"]},
    {"title":"Cloud FinOps for SaaS & Startups","slug":"saas-startups","kw":"cloud FinOps for startups India","desc":"Cloud cost optimization, DevOps visibility, AI cost governance and security hygiene for SaaS companies and startups.","services":["cloud-finops","devops-observability","cloud-security","ai-mlops"],"problems":["Rising AWS/Azure/GCP bills","Unclear cost ownership","Scaling reliability issues","AI workload cost and governance risk"]},
]

RESOURCES = [
    {"title":"AI Automation for Small Business: Practical Use Cases","slug":"ai-automation-small-business-use-cases","kw":"AI automation use cases for small business","desc":"A practical guide to AI automation use cases Indian SMBs can implement across leads, WhatsApp, appointments, support and operations.","service":"ai-automation"},
    {"title":"WhatsApp Business API vs WhatsApp Business App in India","slug":"whatsapp-business-api-vs-direct-whatsapp-india","kw":"WhatsApp Business API vs WhatsApp Business app India","desc":"A plain-English comparison of direct WhatsApp, WhatsApp Business app and WhatsApp Business API for Indian businesses planning automation.","service":"whatsapp-automation"},
    {"title":"AI Chatbot Development Cost in India","slug":"ai-chatbot-development-cost-india","kw":"AI chatbot development cost India","desc":"What affects AI chatbot development cost in India, from use case and integrations to WhatsApp, CRM, knowledge base and human handoff.","service":"ai-chatbot-development"},
    {"title":"AI Voice Agents for Appointment Booking","slug":"ai-voice-agents-appointment-booking","kw":"AI voice agents for appointment booking","desc":"How AI voice agents can answer calls, qualify enquiries, book appointments and recover missed calls for appointment-led businesses.","service":"voice-ai-agents"},
    {"title":"Lead Follow-Up Automation Guide for Indian SMBs","slug":"lead-follow-up-automation-guide","kw":"lead follow-up automation","desc":"How to design a lead follow-up system across website, WhatsApp, calls, CRM and reminders so fewer enquiries are lost.","service":"crm-automation"},
    {"title":"Small Business Website Checklist India","slug":"small-business-website-checklist-india","kw":"small business website checklist India","desc":"A practical checklist for Indian small businesses building a website that must create trust and generate enquiries.","service":"website-digital-presence"},
    {"title":"AWS Cost Optimization Checklist","slug":"aws-cost-optimization-checklist","kw":"AWS cost optimization checklist","desc":"A practical checklist to find avoidable AWS cost waste across compute, storage, databases, networking, monitoring and commitments.","service":"cloud-finops"},
    {"title":"DPDP Compliance Checklist for Small Businesses in India","slug":"dpdp-compliance-checklist-small-business-india","kw":"DPDP compliance checklist small business India","desc":"A practical DPDP readiness checklist for Indian SMB websites, enquiry forms, WhatsApp flows and customer data handling.","service":"dpdp-compliance"},
]

PROOFS = [
    {"title":"AICloudStrategist SEO/GEO Turnaround Proof","slug":"aicloudstrategist-geo-turnaround","kw":"AICloudStrategist SEO proof","desc":"Build-in-public proof showing how AICloudStrategist improves its own search and AI answer visibility through technical SEO and content authority.","service":"lead-generation-seo","label":"Real internal proof"},
    {"title":"Dental Clinic Lead Leakage Demo Audit","slug":"demo-dental-clinic-lead-leakage","kw":"dental clinic lead leakage audit","desc":"A clearly labelled demo audit showing how dental clinics can lose enquiries through missed calls, weak WhatsApp follow-up and no CRM tracking.","service":"crm-automation","label":"Demo audit"},
    {"title":"WhatsApp + CRM Lead Recovery Benchmark","slug":"benchmark-whatsapp-crm-lead-recovery","kw":"WhatsApp CRM lead recovery benchmark","desc":"A simulated benchmark showing how structured WhatsApp follow-up and CRM stages can improve lead recovery speed and owner visibility.","service":"whatsapp-automation","label":"Simulated benchmark"},
    {"title":"SaaS Cloud FinOps Control Demo Audit","slug":"demo-saas-cloud-finops-control","kw":"SaaS cloud FinOps audit","desc":"A demo audit showing common SaaS cloud cost leaks and how FinOps controls improve AWS/Azure/GCP visibility.","service":"cloud-finops","label":"Demo audit"},
]

SERVICE_BY_SLUG = {s['slug']: s for s in PRIMARY_SERVICES}
IND_BY_SLUG = {i['slug']: i for i in INDUSTRIES}

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(s, quote=True)

def url(path): return BASE + path

def service_path(slug): return f"/services/{slug}/"
def industry_path(slug): return f"/industries/{slug}/"
def resource_path(slug): return f"/resources/{slug}/"
def proof_path(slug): return f"/case-studies/{slug}/"

def schema_org(page):
    data = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"Organization","@id":BASE+"/#organization","name":"AICloudStrategist","url":BASE+"/","description":"AICloudStrategist provides websites, lead generation, SEO, AI automation, cloud FinOps, DevOps, security and compliance services for Indian businesses.","areaServed":["India","Global"]},
            {"@type":"WebSite","@id":BASE+"/#website","url":BASE+"/","name":"AICloudStrategist","publisher":{"@id":BASE+"/#organization"}},
            page
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

def layout(title, desc, canonical, h1, eyebrow, body, schema_page, extra_head=""):
    full_title = title if "AICloudStrategist" in title else f"{title} | AICloudStrategist"
    return f'''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(full_title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{esc(url(canonical))}">
  <meta property="og:title" content="{esc(full_title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{esc(url(canonical))}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <style>
    :root{{--bg:#06131b;--panel:#0b202b;--ink:#edf8ff;--muted:#a8bdc9;--line:rgba(255,255,255,.12);--brand:#58c8ff;--accent:#25e6c8;--gold:#ffd166;--max:1120px}}
    *{{box-sizing:border-box}} body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:radial-gradient(circle at 20% 0%,rgba(88,200,255,.18),transparent 34%),linear-gradient(180deg,#041018,#071a23);color:var(--ink);line-height:1.65}} a{{color:inherit}} .wrap{{max-width:var(--max);margin:auto;padding:24px}} .nav{{display:flex;gap:18px;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding:10px 0 18px;position:sticky;top:0;background:rgba(6,19,27,.88);backdrop-filter:blur(12px);z-index:5}} .brand{{font-weight:800;text-decoration:none;letter-spacing:.2px}} .brand span{{color:var(--brand)}} .links{{display:flex;gap:14px;flex-wrap:wrap;font-size:.94rem}} .links a{{text-decoration:none;color:var(--muted)}} .links a:hover{{color:var(--ink)}} .hero{{padding:74px 0 42px}} .eyebrow{{display:inline-block;color:var(--accent);font-weight:800;font-size:.78rem;text-transform:uppercase;letter-spacing:.14em;margin-bottom:16px}} h1{{font-size:clamp(2.2rem,5vw,4.6rem);line-height:1.05;margin:0 0 18px;letter-spacing:-.04em}} h2{{font-size:clamp(1.55rem,3vw,2.35rem);line-height:1.15;margin:46px 0 14px}} h3{{font-size:1.12rem;margin:24px 0 8px}} p{{color:var(--muted);font-size:1.04rem}} .lead{{font-size:1.2rem;max-width:850px}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}} .grid2{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}} .card{{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.025));border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 24px 60px -40px #000}} .card p{{font-size:.98rem}} .tag{{display:inline-flex;padding:5px 10px;border:1px solid var(--line);border-radius:999px;color:var(--gold);font-size:.78rem;font-weight:700;margin:4px 6px 4px 0}} .cta{{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}} .btn{{display:inline-flex;align-items:center;justify-content:center;padding:12px 18px;border-radius:999px;text-decoration:none;font-weight:800;background:linear-gradient(90deg,var(--brand),var(--accent));color:#041018}} .btn.secondary{{background:transparent;color:var(--ink);border:1px solid var(--line)}} .breadcrumb{{font-size:.88rem;color:var(--muted);margin:18px 0}} .breadcrumb a{{color:var(--muted);text-decoration:none}} .section{{padding:18px 0}} .footer{{margin-top:56px;border-top:1px solid var(--line);padding:28px 0;color:var(--muted);font-size:.92rem}} ul{{padding-left:20px;color:var(--muted)}} li{{margin:7px 0}} .money{{border-color:rgba(88,200,255,.38)}} .note{{border-left:4px solid var(--accent);padding-left:16px;color:var(--muted)}} @media(max-width:820px){{.grid,.grid2{{grid-template-columns:1fr}}.nav{{position:relative;display:block}}.links{{margin-top:12px}}}}
  </style>
  <script type="application/ld+json">{schema_org(schema_page)}</script>
  {extra_head}
</head>
<body>
  <div class="wrap">
    <nav class="nav" aria-label="Main navigation">
      <a class="brand" href="/">AI<span>Cloud</span>Strategist</a>
      <div class="links">
        <a href="/services/">Services</a><a href="/industries/">Industries</a><a href="/resources/">Resources</a><a href="/case-studies/">Proof</a><a href="/pricing.html">Pricing</a><a href="/about/">About</a><a href="/free-business-review/">Free review</a>
      </div>
    </nav>
    <div class="breadcrumb"><a href="/">Home</a> / {breadcrumb(canonical)}</div>
    <header class="hero"><span class="eyebrow">{esc(eyebrow)}</span><h1>{esc(h1)}</h1><p class="lead">{esc(desc)}</p><div class="cta"><a class="btn" href="/free-business-review/">Get free growth review</a><a class="btn secondary" href="/contact.html">Talk to AICloudStrategist</a></div></header>
    {body}
    <footer class="footer">
      <strong>AICloudStrategist</strong> — websites, lead generation, SEO, AI automation, cloud FinOps, security and compliance for Indian businesses.<br>
      Key pages: <a href="/services/ai-automation/">AI Automation</a> · <a href="/services/whatsapp-automation/">WhatsApp Automation</a> · <a href="/services/cloud-finops/">Cloud FinOps</a> · <a href="/services/dpdp-compliance/">DPDP Compliance</a> · <a href="/industries/clinics/">Clinics</a>
    </footer>
  </div>
</body>
</html>
'''

def breadcrumb(path):
    parts=[p for p in path.strip('/').split('/') if p]
    if not parts: return 'Home'
    return ' / '.join(esc(p.replace('-',' ').title()) for p in parts)

def card(title, desc, href, cls=""):
    return f'<article class="card {cls}"><h3><a href="{esc(href)}">{esc(title)}</a></h3><p>{esc(desc)}</p></article>'

def write_page(path, content):
    dest=ROOT / path.strip('/') / 'index.html' if path.endswith('/') else ROOT / path.strip('/')
    ensure_dir(dest.parent)
    dest.write_text(content, encoding='utf-8')

# Services hub
service_cards='\n'.join(card(s['title'], s['desc'], service_path(s['slug']), 'money') for s in PRIMARY_SERVICES)
body=f'''<main>
<section class="section"><h2>Commercial SEO service architecture</h2><p>AICloudStrategist combines practical digital growth, AI automation, cloud architecture and compliance into one execution layer for Indian businesses.</p><div class="grid">{service_cards}</div></section>
<section class="section"><h2>How the service system works</h2><div class="grid2"><div class="card"><h3>1. Build digital presence</h3><p>Websites, trust pages, lead capture and local discoverability for businesses that need a stronger online base.</p></div><div class="card"><h3>2. Add automation</h3><p>WhatsApp, AI chatbots, voice agents, CRM and workflow automation to reduce manual follow-up.</p></div><div class="card"><h3>3. Control cloud and operations</h3><p>FinOps, DevOps, observability and security for teams running cloud systems.</p></div><div class="card"><h3>4. Strengthen trust</h3><p>DPDP readiness, consent flows, privacy pages and AI governance to support long-term credibility.</p></div></div></section>
</main>'''
write_page('/services/', layout('AICloudStrategist Services', 'Explore AICloudStrategist services for websites, lead generation, SEO, AI automation, WhatsApp automation, cloud FinOps, DevOps, security and DPDP compliance.', '/services/', 'Digital growth, AI automation and cloud trust services', 'Services', body, {"@type":"CollectionPage","@id":url('/services/')+"#webpage","url":url('/services/'),"name":"AICloudStrategist Services","description":"Service hub for AICloudStrategist."}))

# Individual service pages
for s in PRIMARY_SERVICES:
    if s["slug"] in HANDCRAFTED_FLAGSHIP_SLUGS:
        continue
    related = [SERVICE_BY_SLUG[x] for x in s.get('support',[]) if x in SERVICE_BY_SLUG]
    rel_cards='\n'.join(card(r['title'], r['desc'], service_path(r['slug'])) for r in related)
    inds=[i for i in INDUSTRIES if s['slug'] in i['services']][:5]
    ind_cards='\n'.join(card(i['title'], i['desc'], industry_path(i['slug'])) for i in inds)
    res=[r for r in RESOURCES if r['service']==s['slug']]
    if not res: res=RESOURCES[:2]
    res_cards='\n'.join(card(r['title'], r['desc'], resource_path(r['slug'])) for r in res)
    proof=[p for p in PROOFS if p['service']==s['slug']]
    if not proof: proof=PROOFS[:1]
    proof_cards='\n'.join(card(p['title'], p['desc'], proof_path(p['slug'])) for p in proof)
    benefit_items=''.join(f'<li>{esc(b)}</li>' for b in s['benefits'])
    body=f'''<main>
<section class="section"><h2>What this service solves</h2><div class="grid2"><div class="card money"><h3>Primary SEO target</h3><p><strong>{esc(s['kw'])}</strong></p><p>This page is the money page for {esc(s['kw'])} and related commercial searches.</p></div><div class="card"><h3>Best fit</h3><p>{esc(s['audience'])}.</p></div></div></section>
<section class="section"><h2>Outcomes</h2><ul>{benefit_items}</ul></section>
<section class="section"><h2>Related services</h2><div class="grid">{rel_cards}</div></section>
<section class="section"><h2>Industries this supports</h2><div class="grid">{ind_cards}</div></section>
<section class="section"><h2>Guides and resources</h2><div class="grid">{res_cards}</div></section>
<section class="section"><h2>Proof and demos</h2><div class="grid">{proof_cards}</div><p class="note">Demo and benchmark pages are clearly labelled. AICloudStrategist does not present simulated examples as client case studies.</p></section>
</main>'''
    schema={"@type":"Service","@id":url(service_path(s['slug']))+"#service","url":url(service_path(s['slug'])),"name":s['title'],"description":s['desc'],"provider":{"@id":BASE+"/#organization"},"areaServed":"India","serviceType":s['kw']}
    write_page(service_path(s['slug']), layout(s['title'], s['desc'], service_path(s['slug']), s['title'], s['group'], body, schema))

# Industries hub and pages
ind_cards='\n'.join(card(i['title'], i['desc'], industry_path(i['slug'])) for i in INDUSTRIES)
body=f'''<main><section class="section"><h2>Industry landing pages</h2><p>Each industry page maps business problems to website, lead generation, AI automation, WhatsApp, cloud, security and compliance services.</p><div class="grid">{ind_cards}</div></section></main>'''
write_page('/industries/', layout('Industries Served', 'Industry-specific AI automation, website, lead generation, WhatsApp, cloud FinOps and compliance solutions for Indian businesses.', '/industries/', 'Industry-specific digital growth and AI automation', 'Industries', body, {"@type":"CollectionPage","@id":url('/industries/')+"#webpage","url":url('/industries/'),"name":"Industries Served"}))

for i in INDUSTRIES:
    svc_cards='\n'.join(card(SERVICE_BY_SLUG[slug]['title'], SERVICE_BY_SLUG[slug]['desc'], service_path(slug), 'money') for slug in i['services'] if slug in SERVICE_BY_SLUG)
    problems=''.join(f'<li>{esc(p)}</li>' for p in i['problems'])
    res_cards='\n'.join(card(r['title'], r['desc'], resource_path(r['slug'])) for r in RESOURCES if r['service'] in i['services']) or ''.join(card(r['title'], r['desc'], resource_path(r['slug'])) for r in RESOURCES[:3])
    proof_cards='\n'.join(card(p['title'], p['desc'], proof_path(p['slug'])) for p in PROOFS if p['service'] in i['services']) or ''.join(card(p['title'], p['desc'], proof_path(p['slug'])) for p in PROOFS[:2])
    body=f'''<main>
<section class="section"><h2>Problems we solve for this industry</h2><ul>{problems}</ul></section>
<section class="section"><h2>Recommended service bundle</h2><div class="grid">{svc_cards}</div></section>
<section class="section"><h2>Useful resources</h2><div class="grid">{res_cards}</div></section>
<section class="section"><h2>Relevant proof and demos</h2><div class="grid">{proof_cards}</div></section>
</main>'''
    schema={"@type":"WebPage","@id":url(industry_path(i['slug']))+"#webpage","url":url(industry_path(i['slug'])),"name":i['title'],"description":i['desc'],"about":i['kw'],"isPartOf":{"@id":BASE+"/#website"}}
    write_page(industry_path(i['slug']), layout(i['title'], i['desc'], industry_path(i['slug']), i['title'], 'Industry solution', body, schema))

# Resources (do not overwrite resources hub; create individual cluster pages)
for r in RESOURCES:
    s=SERVICE_BY_SLUG[r['service']]
    siblings=[x for x in RESOURCES if x['slug']!=r['slug']][:4]
    sib_cards='\n'.join(card(x['title'], x['desc'], resource_path(x['slug'])) for x in siblings)
    body=f'''<main>
<section class="section"><h2>Quick answer</h2><p>{esc(r['desc'])}</p><p>This guide supports the <a href="{service_path(s['slug'])}">{esc(s['title'])}</a> money page and helps Google connect AICloudStrategist with the topic: <strong>{esc(r['kw'])}</strong>.</p></section>
<section class="section"><h2>Practical implementation checklist</h2><div class="grid2"><div class="card"><h3>1. Clarify the business outcome</h3><p>Define whether the goal is more leads, faster response, lower cost, stronger trust or less manual work.</p></div><div class="card"><h3>2. Map the current workflow</h3><p>Document website, WhatsApp, phone, CRM, spreadsheet, cloud or compliance gaps before adding tools.</p></div><div class="card"><h3>3. Build the smallest useful system</h3><p>Start with one measurable workflow, then expand once the first result is stable.</p></div><div class="card"><h3>4. Add tracking and review</h3><p>Use dashboards, owner visibility and periodic checks so the system keeps improving.</p></div></div></section>
<section class="section"><h2>Related reading</h2><div class="grid">{sib_cards}</div></section>
<section class="section"><h2>Next step</h2><p>For implementation help, review <a href="{service_path(s['slug'])}">{esc(s['title'])}</a> or request a <a href="/free-business-review/">free business growth review</a>.</p></section>
</main>'''
    schema={"@type":"Article","@id":url(resource_path(r['slug']))+"#article","url":url(resource_path(r['slug'])),"headline":r['title'],"description":r['desc'],"author":{"@id":BASE+"/#organization"},"publisher":{"@id":BASE+"/#organization"},"dateModified":TODAY,"mainEntityOfPage":url(resource_path(r['slug']))}
    write_page(resource_path(r['slug']), layout(r['title'], r['desc'], resource_path(r['slug']), r['title'], 'Resource guide', body, schema))

# Proof pages (do not overwrite existing geo page if exists? overwrite only new except existing slug? keep consistent)
for p in PROOFS:
    s=SERVICE_BY_SLUG[p['service']]
    body=f'''<main>
<section class="section"><div class="card money"><span class="tag">{esc(p['label'])}</span><h2>What this proof page shows</h2><p>{esc(p['desc'])}</p></div></section>
<section class="section"><h2>What AICloudStrategist would inspect</h2><ul><li>Current lead, website, WhatsApp, cloud or compliance workflow.</li><li>Where business value is leaking through delay, manual tracking, weak visibility or unclear trust signals.</li><li>Which service page solves the problem: <a href="{service_path(s['slug'])}">{esc(s['title'])}</a>.</li><li>What should be measured before and after implementation.</li></ul></section>
<section class="section"><h2>Related commercial page</h2><div class="grid">{card(s['title'], s['desc'], service_path(s['slug']), 'money')}</div></section>
<section class="section"><p class="note">This page is intentionally labelled as {esc(p['label'].lower())}. Real client claims will only be published when earned and approved.</p></section>
</main>'''
    schema={"@type":"CreativeWork","@id":url(proof_path(p['slug']))+"#proof","url":url(proof_path(p['slug'])),"name":p['title'],"description":p['desc'],"about":p['kw'],"publisher":{"@id":BASE+"/#organization"}}
    write_page(proof_path(p['slug']), layout(p['title'], p['desc'], proof_path(p['slug']), p['title'], p['label'], body, schema))

# Tools hub + calculators/checklists summary
body='''<main><section class="section"><h2>SEO tools, calculators and templates</h2><p>Fast utility assets that support AICloudStrategist service pages and help Indian businesses estimate gaps before requesting help.</p><div class="grid">
'''
for title, desc, href in [
    ('Lead leakage calculator','Estimate how many enquiries are lost through slow response and weak follow-up.','/lead-leakage-calculator.html'),
    ('Healthcare ROI leakage calculator','Estimate missed patient enquiry impact for clinics.','/healthcare-roi-leakage-calculator/'),
    ('DPDP readiness assessment','Check practical DPDP and website trust readiness.','/dpdp-readiness-assessment.html'),
    ('WhatsApp link generator','Create simple WhatsApp click-to-chat links for campaigns.','/whatsapp-link-generator.html'),
]: body += card(title, desc, href)
body+='</div></section></main>'
write_page('/tools/', layout('Tools and Calculators', 'Free calculators, checklists and templates for lead leakage, cloud cost, DPDP readiness and WhatsApp setup.', '/tools/', 'Tools, calculators and templates for digital growth', 'Tools', body, {"@type":"CollectionPage","@id":url('/tools/')+"#webpage","url":url('/tools/'),"name":"Tools and Calculators"}))

# Trust security page
body='''<main><section class="section"><h2>Trust principles</h2><div class="grid2"><div class="card"><h3>Human approval where it matters</h3><p>External outreach, public publishing, sensitive data and paid actions need explicit approval.</p></div><div class="card"><h3>Privacy-aware automation</h3><p>Automation should capture only necessary data, document consent and keep clear escalation paths.</p></div><div class="card"><h3>Cloud and AI hygiene</h3><p>Cloud, AI and automation work should include access control, monitoring, cost visibility and rollback thinking.</p></div><div class="card"><h3>Honest proof</h3><p>Demo audits and simulated benchmarks are labelled. Real case studies are published only when earned.</p></div></div></section><section class="section"><h2>Relevant services</h2><div class="grid">'''
for slug in ['dpdp-compliance','cloud-security','ai-mlops','cloud-finops','ai-automation']:
    s=SERVICE_BY_SLUG[slug]; body+=card(s['title'],s['desc'],service_path(slug),'money')
body+='</div></section></main>'
write_page('/trust-security/', layout('Trust, Security and Compliance', 'How AICloudStrategist approaches privacy, approval gates, AI governance, cloud security, DPDP readiness and honest proof.', '/trust-security/', 'Trust, security and compliance at AICloudStrategist', 'Trust', body, {"@type":"AboutPage","@id":url('/trust-security/')+"#webpage","url":url('/trust-security/'),"name":"Trust, Security and Compliance"}))

# Add home internal link block before closing body if not present
idx=ROOT/'index.html'
text=idx.read_text(encoding='utf-8', errors='ignore')
if 'seo-expansion-links' not in text:
    block='''
<section id="seo-expansion-links" style="position:relative;z-index:3;max-width:1180px;margin:24px auto 42px;padding:0 24px;color:#eaf6fb;font-family:Inter,ui-sans-serif,system-ui,sans-serif;">
  <div style="border:1px solid rgba(255,255,255,.12);border-radius:22px;padding:24px;background:rgba(255,255,255,.045);">
    <p style="margin:0 0 12px;color:#9db4c0;font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;">Explore AICloudStrategist</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;">
      <a href="/services/" style="color:#58c8ff;">Services</a>
      <a href="/services/ai-automation/" style="color:#58c8ff;">AI Automation</a>
      <a href="/services/whatsapp-automation/" style="color:#58c8ff;">WhatsApp Automation</a>
      <a href="/services/cloud-finops/" style="color:#58c8ff;">Cloud FinOps</a>
      <a href="/services/dpdp-compliance/" style="color:#58c8ff;">DPDP Compliance</a>
      <a href="/industries/" style="color:#58c8ff;">Industries</a>
      <a href="/resources/" style="color:#58c8ff;">Resources</a>
      <a href="/case-studies/" style="color:#58c8ff;">Proof</a>
    </div>
  </div>
</section>
'''
    text=text.replace('</body>', block+'\n</body>')
    if '<meta name="description"' not in text[:3000]:
        text=text.replace('<link rel="canonical" href="https://aicloudstrategist.com/">','<meta name="description" content="AICloudStrategist builds websites, lead generation systems, SEO, AI automation, WhatsApp automation, cloud FinOps, DevOps, security and DPDP compliance for Indian businesses.">\n<link rel="canonical" href="https://aicloudstrategist.com/">')
    idx.write_text(text, encoding='utf-8')

# Update resources index with cluster links if possible
res_index=ROOT/'resources/index.html'
if res_index.exists():
    tx=res_index.read_text(encoding='utf-8', errors='ignore')
    if 'seo-cluster-links-2026' not in tx:
        links=''.join(f'<li><a href="{resource_path(r["slug"])}">{esc(r["title"])}</a> — {esc(r["kw"])}</li>' for r in RESOURCES)
        block=f'''<section id="seo-cluster-links-2026" style="max-width:1120px;margin:32px auto;padding:24px;border:1px solid rgba(255,255,255,.12);border-radius:18px;"><h2>New topical SEO clusters</h2><ul>{links}</ul></section>'''
        tx=tx.replace('</main>', block+'</main>') if '</main>' in tx else tx.replace('</body>', block+'</body>')
        res_index.write_text(tx, encoding='utf-8')

# Redirects for legacy paths to canonical clean URLs
redirects=ROOT/'_redirects'
redir=redirects.read_text(encoding='utf-8') if redirects.exists() else ''
new_rules='''
# SEO expansion canonical redirects
/industries.html /industries/ 301!
/products.html /services/ 301!
/website-digital-presence/ /services/website-digital-presence/ 301!
/small-business-automation-india.html /services/ai-automation/small-business/ 301!
/whatsapp-lead-management-india.html /services/whatsapp-automation/lead-management/ 301!
/website-lead-capture-sprint.html /services/lead-generation-seo/website-lead-capture/ 301!
/operations-automation-sprint.html /services/workflow-automation/operations-automation-sprint/ 301!
/dpdp-compliance-consultant-india.html /services/dpdp-compliance/ 301!
/aesthetic-clinics/ /industries/aesthetic-clinics/ 301!
/dpdp-for-clinics/ /industries/clinics/ 301!
/dpdp-for-diagnostic-labs/ /industries/diagnostic-labs/ 301!
/healthcare-growthos/ /industries/clinics/ 301!
/cloud-trust-finops/ /services/cloud-finops/ 301!
/ai-cloud-cost-review/ /services/cloud-finops/cloud-cost-review/ 301!
/ai-cloud-cost-efficiency/ /services/cloud-finops/ 301!
'''
if 'SEO expansion canonical redirects' not in redir:
    redirects.write_text(redir.rstrip()+"\n"+new_rules, encoding='utf-8')

# Sitemap: include important html directories/pages, exclude assets and internals
urls=[]
priority={"/": "1.0", "/services/":"0.95", "/industries/":"0.9", "/resources/":"0.85", "/case-studies/":"0.85"}
def add(path, pri='0.7'):
    if path not in [u[0] for u in urls]: urls.append((path, priority.get(path,pri)))
add('/', '1.0')
for path in ['/services/','/industries/','/resources/','/case-studies/','/tools/','/trust-security/','/pricing.html','/about/','/free-business-review/','/contact.html','/privacy.html','/terms.html']:
    add(path)
for s in PRIMARY_SERVICES: add(service_path(s['slug']), '0.9')
for i in INDUSTRIES: add(industry_path(i['slug']), '0.82')
for r in RESOURCES: add(resource_path(r['slug']), '0.78')
for p in PROOFS: add(proof_path(p['slug']), '0.78')
# Include existing useful resources/case studies but not assets
for f in sorted(ROOT.rglob('index.html')):
    rel='/' + str(f.relative_to(ROOT).parent).replace('\\','/') + '/'
    if rel.startswith(('/.git','/.workspace-snapshots','/assets/','/functions/','/seo/')): continue
    if rel == '/./': rel='/'
    add(rel, '0.65')
for f in sorted(ROOT.glob('*.html')):
    name=f.name
    if name in ['404.html'] or 'old' in name or 'backup' in name: continue
    add('/'+name, '0.55')
xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p,pri in urls:
    xml += ['  <url>', f'    <loc>{BASE}{p}</loc>', f'    <lastmod>{TODAY}</lastmod>', '    <changefreq>weekly</changefreq>', f'    <priority>{pri}</priority>', '  </url>']
xml.append('</urlset>')
(ROOT/'sitemap.xml').write_text('\n'.join(xml)+'\n', encoding='utf-8')

# Update llms.txt with new architecture summary
llms=ROOT/'llms.txt'
lt=llms.read_text(encoding='utf-8', errors='ignore') if llms.exists() else '# AICloudStrategist\n'
if '## SEO service architecture' not in lt:
    lt += '\n## SEO service architecture\nAICloudStrategist core commercial pages live under /services/: AI automation, WhatsApp automation, AI chatbot development, voice AI agents, CRM automation, workflow automation, website digital presence, lead generation SEO, cloud FinOps, DevOps observability, cloud security, DPDP compliance, and AI/MLOps. Industry pages live under /industries/. Topical resources live under /resources/. Proof and demo pages live under /case-studies/.\n'
llms.write_text(lt, encoding='utf-8')

print('Generated', len(PRIMARY_SERVICES), 'service pages,', len(INDUSTRIES), 'industry pages,', len(RESOURCES), 'resource pages,', len(PROOFS), 'proof pages.')
print('Updated sitemap, redirects, llms, home links.')
