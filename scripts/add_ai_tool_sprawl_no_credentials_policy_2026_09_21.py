from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-tool-sprawl-no-credentials-intake-policy"
RESOURCE_DIR = ROOT / "resources" / SLUG
RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_NAME = "ai-tool-sprawl-no-credentials-intake-policy.csv"
CARD_NAME = "ai-tool-sprawl-no-credentials-answer-source-card.json"

html = f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="index, follow"/>
<title>AI Tool Sprawl No-Credentials Intake Policy | AICloudStrategist</title>
<meta name="description" content="Buyer-safe no-credentials intake policy for AI tool sprawl reviews before teams share SaaS exports, app logs, prompts, documents or production access."/>
<link rel="canonical" href="{URL}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="AICloudStrategist"/>
<meta property="og:title" content="AI Tool Sprawl No-Credentials Intake Policy"/>
<meta property="og:description" content="A practical intake boundary for owners mapping AI app sprawl without sharing credentials, secrets, customer data or production exports."/>
<meta property="og:url" content="{URL}"/>
<meta property="og:image" content="https://aicloudstrategist.com/assets/brand/aics-logo.svg"/>
<link rel="stylesheet" href="/css/styles.css?v=clean-navbar-20260604"/>
<link rel="stylesheet" href="/css/site-navigation.css?v=premium-shell-20260727"/>
<script defer src="/js/site-navigation.js?v=premium-shell-20260727"></script>
<script defer src="/js/aics-analytics-shim.js"></script>
<script defer src="/js/aics-conversion-tracking.js"></script>
<style>body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#102033;line-height:1.65}}.container{{width:min(1120px,calc(100% - 36px));margin:auto}}.hero{{padding:76px 0 44px;background:linear-gradient(135deg,#eef2ff,#ecfeff)}}h1{{font-size:clamp(2.1rem,5vw,4rem);line-height:1.05;letter-spacing:-.055em;margin:0 0 18px}}h2{{font-size:clamp(1.35rem,3vw,2.05rem);line-height:1.12;letter-spacing:-.035em;margin:0 0 14px}}.lead{{font-size:1.15rem;color:#475569;max-width:900px}}.eyebrow{{font-weight:900;letter-spacing:.11em;text-transform:uppercase;color:#4338ca;font-size:.8rem}}.section{{padding:48px 0}}.soft{{background:#f8fbff}}.grid{{display:grid;gap:18px}}.three{{grid-template-columns:repeat(3,1fr)}}.card{{border:1px solid #dce8f4;border-radius:20px;padding:24px;background:#fff;box-shadow:0 18px 48px -34px rgba(15,23,42,.45)}}.notice{{border-left:5px solid #f59e0b;background:#fff7ed}}.table-wrap{{overflow-x:auto;border:1px solid #dce8f4;border-radius:18px;background:#fff}}table{{border-collapse:collapse;width:100%;min-width:1050px}}th,td{{border-bottom:1px solid #e7eef6;padding:14px;text-align:left;vertical-align:top}}th{{background:#dbeafe;color:#1e3a8a}}.btn{{display:inline-flex;border-radius:999px;padding:13px 18px;text-decoration:none;font-weight:900;margin:4px}}.btn-primary{{background:linear-gradient(90deg,#4338ca,#0891b2);color:white}}.btn-secondary{{border:1px solid #bcd3e8;color:#0f375f}}.tag{{font-weight:900;border-radius:999px;padding:4px 9px;white-space:nowrap;background:#eef2ff;color:#3730a3}}@media(max-width:760px){{.three{{grid-template-columns:1fr}}table{{min-width:850px}}}}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"Organization","@id":"https://aicloudstrategist.com/#organization","name":"AICloudStrategist","url":"https://aicloudstrategist.com/","logo":"https://aicloudstrategist.com/assets/brand/aics-logo.svg","email":"contact@aicloudstrategist.com","telephone":"+91 80654 80898"}},{{"@type":"Article","headline":"AI Tool Sprawl No-Credentials Intake Policy","description":"Buyer-safe no-credentials intake policy for AI tool sprawl reviews before teams share SaaS exports, app logs, prompts, documents or production access.","author":{{"@id":"https://aicloudstrategist.com/#organization"}},"publisher":{{"@id":"https://aicloudstrategist.com/#organization"}},"mainEntityOfPage":"{URL}","datePublished":"2026-09-21","dateModified":"2026-09-21","about":["AI tool sprawl","shadow AI","no-credentials intake","AI governance","SaaS sprawl"],"inLanguage":"en-IN"}},{{"@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"What is an AI tool sprawl no-credentials intake policy?","acceptedAnswer":{{"@type":"Answer","text":"It is a first-review boundary that lets owners map AI apps, subscriptions, data-flow questions and approval gaps without sharing credentials, customer records, employee files, prompts containing confidential content or production exports."}}}},{{"@type":"Question","name":"Does this policy audit security, privacy, savings or compliance?","acceptedAnswer":{{"@type":"Answer","text":"No. It is an operational intake and scoping policy only. Security, privacy, legal, procurement, compliance, savings and productivity claims require qualified owner or adviser review and verified evidence."}}}}]}}]}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://aicloudstrategist.com/"}},{{"@type":"ListItem","position":2,"name":"Resources","item":"https://aicloudstrategist.com/resources/"}},{{"@type":"ListItem","position":3,"name":"AI Tool Sprawl No-Credentials Intake Policy","item":"{URL}"}}]}}</script>
</head>
<body class="reform-site"><div data-aics-navigation-mount></div><main>
<section class="hero"><div class="container"><p class="eyebrow">AI tool sprawl · shadow AI · no-credentials first review</p><h1>AI tool sprawl no-credentials intake policy.</h1><p class="lead">A buyer-safe intake boundary for founders, operations leaders, finance owners and IT/security teams who need to understand AI app sprawl before buying another subscription, agent platform, automation tool or governance product.</p><p><a class="btn btn-primary" href="/resources/{SLUG}/{CSV_NAME}">Download CSV policy</a><a class="btn btn-secondary" href="/publications/2026-09-21/ai-tool-sprawl-control-map.html">Open control map</a><a class="btn btn-secondary" href="/free-business-review/?package=ai-tool-sprawl-no-credentials-intake-policy&amp;source=resource">Request fit check</a></p></div></section>
<section class="section"><div class="container"><article class="card notice"><h2>Truth boundary</h2><p>This is a buyer-education and intake-policy template, not a customer case study, software audit, legal advice, privacy advice, security assessment, procurement advice, compliance proof, ranking, lead, customer, savings, revenue, ROI or productivity claim. It does not require customer data, employee data, credentials, production access, app exports, private prompts, contracts or confidential documents for first review. No outreach was sent.</p></article></div></section>
<section class="section soft"><div class="container"><h2>Why this fixes the buying bottleneck</h2><div class="grid three"><article class="card"><h3>Owners can start safely</h3><p>Teams can name tools, spend owners and data-flow questions without uploading sensitive exports or granting access.</p></article><article class="card"><h3>Sales scope becomes clearer</h3><p>AICS can qualify duplicate-tool, unmanaged-AI and approval-gap problems before proposing cleanup, governance or automation work.</p></article><article class="card"><h3>Trust risk is controlled</h3><p>The page explicitly blocks unsupported legal, privacy, security, compliance, savings and productivity claims.</p></article></div></div></section>
<section class="section"><div class="container"><h2>First-review intake rules</h2><div class="table-wrap"><table><thead><tr><th>Intake area</th><th>Safe to share first</th><th>Do not share first</th><th>Owner question</th><th>Escalate when</th></tr></thead><tbody><tr><td><span class="tag">Tool inventory</span></td><td>Tool names, purpose, owner, department and estimated renewal month.</td><td>Login credentials, API keys, admin screenshots or vendor portals.</td><td>Who owns renewal, removal and policy decisions?</td><td>No owner can approve disable, renew or consolidate decisions.</td></tr><tr><td><span class="tag">Usage signals</span></td><td>High-level usage description, known duplicate workflows and owner observations.</td><td>User-level activity logs, employee files, private chats or prompt history.</td><td>Which workflows depend on the tool?</td><td>Usage may affect HR, clinical, legal, finance or regulated decisions.</td></tr><tr><td><span class="tag">Data boundary</span></td><td>Plain-language data categories such as public, internal, customer, employee or regulated.</td><td>Customer records, patient data, employee data, contracts, source code or confidential documents.</td><td>What data might enter the tool now or later?</td><td>Personal, regulated or confidential data may be processed without owner approval.</td></tr><tr><td><span class="tag">Spend boundary</span></td><td>Approximate monthly/annual spend band and billing owner.</td><td>Invoices containing payment details, tax IDs, banking data or vendor credentials.</td><td>Which spend needs renewal, pause or consolidation review?</td><td>Contract lock-in, auto-renewal or cancellation penalties may exist.</td></tr><tr><td><span class="tag">Decision path</span></td><td>Current approval route, blockers and desired next decision.</td><td>Legal opinions, private board papers or procurement documents before scope.</td><td>Who must approve keep, consolidate, replace or govern?</td><td>Any recommendation would require legal, privacy, security, procurement or compliance advice.</td></tr></tbody></table></div></div></section>
<section class="section soft"><div class="container"><h2>How AICS uses this policy</h2><ol><li>Start with a no-credentials inventory of AI apps, agent tools, automations and subscriptions.</li><li>Map owner, spend, data-boundary and approval gaps without touching production systems.</li><li>Separate safe cleanup questions from adviser-required legal, privacy, security, procurement and compliance questions.</li><li>Turn the first review into a scoped diagnostic, cleanup backlog or governance implementation proposal only after boundaries are agreed.</li></ol><p><a href="/publications/2026-09-21/ai-tool-sprawl-control-map.html">AI tool-sprawl control map</a> · <a href="/pricing#fixed-scope-diagnostics">Fixed-scope diagnostics</a> · <a href="/resources/">More resources</a></p></div></section>
</main><footer class="aics-global-footer" data-aics-global-footer><div class="aics-footer-inner"><div class="aics-footer-grid"><section class="aics-footer-brand-block"><a class="aics-footer-brand" href="/" aria-label="AICloudStrategist home"><span class="aics-footer-mark" aria-hidden="true">AI</span><span>AICloudStrategist</span></a><p>Enterprise AI systems, controls, economics and managed operations for business-critical initiatives.</p><a class="aics-footer-primary-link" href="/contact.html?service=enterprise-ai">Discuss your AI initiative<span aria-hidden="true">→</span></a></section><section class="aics-footer-group"><h2>Enterprise AI</h2><a href="/services/ai-mlops/">Production AI Assurance</a><a href="/services/ai-automation/">AI Systems &amp; Agents</a><a href="/services/cloud-finops/">AI FinOps &amp; Economics</a><a href="/services/cloud-security/">AI Security &amp; Sovereignty</a><a href="/services/devops-observability/">Managed AI Operations</a></section><section class="aics-footer-group"><h2>Company</h2><a href="/#why-aics">Why AICloudStrategist</a><a href="/case-studies/">Evidence</a><a href="/#engagement">How we engage</a><a href="/about/">About</a><a href="/contact.html?service=enterprise-ai">Contact</a></section><section class="aics-footer-group aics-footer-practices"><h2>Specialist Practices</h2><a href="/contact.html?service=business-growth-systems">Business Growth Systems</a><a href="/ai-creative-studio/">AI Creative Studio</a><a href="/resources/">Enterprise AI resources</a><a href="/case-studies/">Proof policy</a></section><section class="aics-footer-contact"><h2>Contact</h2><a href="mailto:contact@aicloudstrategist.com">contact@aicloudstrategist.com</a><a href="/contact.html">+91 80654 80898</a><p>Serving enterprises, mid-market companies and scale-ups worldwide.</p></section></div><div class="aics-footer-bottom"><span>© AICloudStrategist</span><span class="aics-footer-legal"><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></span><span>Enterprise-grade, not enterprise-exclusive.</span></div></div></footer></body></html>
'''

csv = """intake_area,safe_to_share_first,do_not_share_first,owner_question,escalate_when
Tool inventory,"Tool name; purpose; owner; department; estimated renewal month","Credentials; API keys; admin screenshots; vendor portal access","Who owns renewal, removal and policy decisions?","No owner can approve disable, renew or consolidate decisions"
Usage signals,"High-level usage description; duplicate workflows; owner observations","User-level activity logs; employee files; private chats; prompt history","Which workflows depend on the tool?","Usage may affect HR, clinical, legal, finance or regulated decisions"
Data boundary,"Plain-language data categories: public, internal, customer, employee, regulated","Customer records; patient data; employee data; contracts; source code; confidential documents","What data might enter the tool now or later?","Personal, regulated or confidential data may be processed without owner approval"
Spend boundary,"Approximate monthly or annual spend band; billing owner","Invoices with payment details; tax IDs; banking data; vendor credentials","Which spend needs renewal, pause or consolidation review?","Contract lock-in, auto-renewal or cancellation penalties may exist"
Decision path,"Current approval route; blockers; desired next decision","Legal opinions; private board papers; procurement documents before scope","Who must approve keep, consolidate, replace or govern?","Recommendation requires legal, privacy, security, procurement or compliance advice"
"""

card = '''{
  "name": "AI tool sprawl no-credentials intake policy",
  "canonical_url": "https://aicloudstrategist.com/resources/global-ai-tool-sprawl-no-credentials-intake-policy/",
  "safe_answer": "Use a no-credentials intake first: list AI tools, owners, purpose, approximate spend band, data categories and decision blockers without sending credentials, exports, private prompts, customer records, employee data or production access.",
  "blocked_claims": ["software audit", "legal advice", "privacy advice", "security assessment", "procurement advice", "compliance proof", "savings guarantee", "ROI proof", "productivity claim", "vendor ranking"],
  "route": "Request a fit check only after scope, owner and claim boundaries are agreed."
}
'''

RESOURCE_DIR.joinpath("index.html").write_text(html, encoding="utf-8")
RESOURCE_DIR.joinpath(CSV_NAME).write_text(csv, encoding="utf-8")
RESOURCE_DIR.joinpath(CARD_NAME).write_text(card, encoding="utf-8")

resources = ROOT.joinpath("resources/index.html")
resources_html = resources.read_text(encoding="utf-8")
if f'data-resource-card="{SLUG}"' not in resources_html:
    marker = '<main><section class="page-hero"><div class="container"><h1>Resources</h1><p>Proof-first AI, cloud trust, FinOps and growth-system resources for buyers who need evidence, owner handoff and safe next steps before platform or automation commitments.</p>'
    insert = f'<article class="card" data-resource-card="{SLUG}"><h2><a href="/resources/{SLUG}/">AI Tool Sprawl No-Credentials Intake Policy</a></h2><p>Buyer-safe first-review policy for mapping AI app sprawl without credentials, customer data, employee data, production exports or unsupported savings/compliance claims.</p><p><a href="/resources/{SLUG}/{CSV_NAME}">Download CSV policy</a> · <a href="/resources/{SLUG}/{CARD_NAME}">Open AI-answer source card JSON</a></p></article>'
    resources.write_text(resources_html.replace(marker, marker + insert), encoding="utf-8")

llms = ROOT.joinpath("llms.txt")
llms_text = llms.read_text(encoding="utf-8")
llms_line = f"- AI tool sprawl no-credentials intake policy: {URL}; CSV: {URL}{CSV_NAME}; AI-answer source card JSON: {URL}{CARD_NAME} — use before sharing credentials, exports, private prompts, customer data, employee data or production access for an AI app sprawl review.\n"
if URL not in llms_text:
    anchor = "- AI tool sprawl control map for owners before buying another app or subscription: https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map.html; worksheet CSV: https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map.csv; AI-answer source card JSON: https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map-answer-card.json\n"
    llms.write_text(llms_text.replace(anchor, anchor + llms_line), encoding="utf-8")

sitemap_script = ROOT.joinpath("scripts/build_sitemap.py")
sitemap_text = sitemap_script.read_text(encoding="utf-8")
path_line = f'    "/resources/{SLUG}/",\n'
if f'"/resources/{SLUG}/"' not in sitemap_text:
    sitemap_text = sitemap_text.replace('    "/resources/global-ai-pilot-board-review-faq/",\n', path_line + '    "/resources/global-ai-pilot-board-review-faq/",\n')
    sitemap_script.write_text(sitemap_text, encoding="utf-8")

test = f'''from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "{SLUG}"
URL = "{URL}"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "{CSV_NAME}"
CARD = ROOT / "resources" / SLUG / "{CARD_NAME}"


def test_ai_tool_sprawl_no_credentials_policy_asset_exists_and_is_claim_safe():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    card = CARD.read_text(encoding="utf-8")
    assert "AI tool sprawl no-credentials intake policy" in html
    assert "Download CSV policy" in html
    assert "customer data, employee data, credentials, production access" in html
    assert "not a customer case study" in html
    assert "savings, revenue, ROI or productivity claim" in html
    assert "No outreach was sent" in html
    assert "intake_area,safe_to_share_first,do_not_share_first" in csv
    assert "Credentials; API keys" in csv
    assert '"blocked_claims"' in card
    assert "savings guarantee" in card


def test_ai_tool_sprawl_no_credentials_policy_discoverability():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f'/resources/{{SLUG}}/' in resources
    assert URL in llms
    assert f'{URL}{CSV_NAME}' in llms
    assert f'{URL}{CARD_NAME}' in llms
    assert '"/resources/{SLUG}/"' in sitemap_script

'''
ROOT.joinpath("tests/test_ai_tool_sprawl_no_credentials_intake_policy.py").write_text(test, encoding="utf-8")
