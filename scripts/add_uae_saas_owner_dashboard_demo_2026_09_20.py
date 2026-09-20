from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-saas-cloud-trust-finops-readiness-checklist"
BASE = ROOT / "resources" / SLUG
PAGE = BASE / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SVG_NAME = "uae-saas-cloud-trust-finops-owner-dashboard-demo.svg"
SVG = BASE / SVG_NAME

svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc">
  <title id="title">Synthetic UAE SaaS Cloud Trust and FinOps owner dashboard demo</title>
  <desc id="desc">A demo-labelled owner dashboard layout for UAE SaaS cloud spend, AI spend, privileged access, backup proof and vendor evidence review. It uses synthetic examples only and makes no savings, compliance or security claim.</desc>
  <rect width="1200" height="760" fill="#f3f8fc"/>
  <rect x="48" y="40" width="1104" height="92" rx="22" fill="#061321"/>
  <text x="78" y="88" fill="#ffffff" font-family="Arial, sans-serif" font-size="29" font-weight="700">UAE SaaS Cloud Trust + FinOps owner board</text>
  <text x="78" y="116" fill="#cde9f7" font-family="Arial, sans-serif" font-size="16">Synthetic demo — cloud bill, AI spend, access, backup and vendor evidence before FinOps/GRC/tool spend</text>
  <rect x="846" y="62" width="270" height="42" rx="21" fill="#18a0fb"/>
  <text x="890" y="89" fill="#ffffff" font-family="Arial, sans-serif" font-size="16" font-weight="700">NO REAL CUSTOMER DATA</text>

  <g font-family="Arial, sans-serif">
    <rect x="48" y="164" width="250" height="132" rx="18" fill="#ffffff" stroke="#d4e4f0"/>
    <text x="72" y="198" fill="#18324a" font-size="16" font-weight="700">Cloud spend owners missing</text>
    <text x="72" y="238" fill="#b35400" font-size="44" font-weight="700">8</text>
    <text x="72" y="268" fill="#607487" font-size="15">Example billing rows unowned</text>

    <rect x="326" y="164" width="250" height="132" rx="18" fill="#ffffff" stroke="#d4e4f0"/>
    <text x="350" y="198" fill="#18324a" font-size="16" font-weight="700">AI spend approval gaps</text>
    <text x="350" y="238" fill="#b00020" font-size="44" font-weight="700">5</text>
    <text x="350" y="268" fill="#607487" font-size="15">LLM/GPU/model usage needs review</text>

    <rect x="604" y="164" width="250" height="132" rx="18" fill="#ffffff" stroke="#d4e4f0"/>
    <text x="628" y="198" fill="#18324a" font-size="16" font-weight="700">Access review exceptions</text>
    <text x="628" y="238" fill="#0b5cab" font-size="44" font-weight="700">11</text>
    <text x="628" y="268" fill="#607487" font-size="15">Privileged/service accounts</text>

    <rect x="882" y="164" width="270" height="132" rx="18" fill="#ffffff" stroke="#d4e4f0"/>
    <text x="906" y="198" fill="#18324a" font-size="16" font-weight="700">Backup/vendor evidence due</text>
    <text x="906" y="238" fill="#0a7f49" font-size="44" font-weight="700">6</text>
    <text x="906" y="268" fill="#607487" font-size="15">Restore tests + renewals</text>
  </g>

  <rect x="48" y="328" width="1104" height="350" rx="20" fill="#ffffff" stroke="#d4e4f0"/>
  <text x="76" y="368" fill="#18324a" font-family="Arial, sans-serif" font-size="22" font-weight="700">Example owner queue fields for monthly CFO/CTO review</text>
  <g font-family="Arial, sans-serif" font-size="15">
    <rect x="76" y="394" width="1050" height="44" rx="8" fill="#e9f3fb"/>
    <text x="96" y="422" fill="#18324a" font-weight="700">Decision area</text>
    <text x="278" y="422" fill="#18324a" font-weight="700">Evidence source</text>
    <text x="478" y="422" fill="#18324a" font-weight="700">Owner</text>
    <text x="630" y="422" fill="#18324a" font-weight="700">Stop rule</text>
    <text x="850" y="422" fill="#18324a" font-weight="700">Next safe action</text>

    <text x="96" y="474" fill="#263b50">Unexplained spend spike</text>
    <text x="278" y="474" fill="#607487">Billing export + tags</text>
    <text x="478" y="474" fill="#607487">CFO / CTO</text>
    <text x="630" y="474" fill="#b00020">No savings claim yet</text>
    <text x="850" y="474" fill="#263b50">Assign workload and purpose owner</text>
    <line x1="76" y1="500" x2="1126" y2="500" stroke="#edf3f8"/>

    <text x="96" y="540" fill="#263b50">New AI/API usage</text>
    <text x="278" y="540" fill="#607487">Model logs / invoices</text>
    <text x="478" y="540" fill="#607487">Product lead</text>
    <text x="630" y="540" fill="#b00020">No hidden data use</text>
    <text x="850" y="540" fill="#263b50">Confirm approval threshold</text>
    <line x1="76" y1="566" x2="1126" y2="566" stroke="#edf3f8"/>

    <text x="96" y="606" fill="#263b50">Vendor evidence renewal</text>
    <text x="278" y="606" fill="#607487">DPA/security notes</text>
    <text x="478" y="606" fill="#607487">Ops / adviser</text>
    <text x="630" y="606" fill="#b00020">Adviser review required</text>
    <text x="850" y="606" fill="#263b50">Update evidence owner list</text>
  </g>
  <text x="60" y="718" fill="#607487" font-family="Arial, sans-serif" font-size="14">AICS synthetic proof-of-method asset. Not a case study, not legal/privacy/security/FinOps advice, not proof of savings, compliance, ranking, revenue, customer demand or AI accuracy.</text>
</svg>
'''
SVG.write_text(svg, encoding="utf-8")

page = PAGE.read_text(encoding="utf-8")
image_schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ImageObject","name":"Synthetic UAE SaaS Cloud Trust and FinOps owner dashboard demo","description":"Synthetic examples only: demo owner dashboard for UAE SaaS cloud spend, AI spend, access review, backup proof and vendor evidence queues; not a customer case study, savings proof, security proof or compliance proof.","url":"https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg","isPartOf":"https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/","dateModified":"2026-09-20","inLanguage":"en-AE","publisher":{"@id":"https://aicloudstrategist.com/#organization"}}</script>\n'
if 'Synthetic UAE SaaS Cloud Trust and FinOps owner dashboard demo' not in page:
    page = page.replace('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList"', image_schema + '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList"')
page = page.replace(
    '<li>A public demo owner-dashboard screenshot labelled demo/internal/simulated, showing cost movement, AI-spend approval, access exceptions, backup evidence and vendor-renewal decisions.</li>',
    '<li><a href="/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg">A public demo owner-dashboard screenshot labelled demo/internal/simulated</a>, showing cost movement, AI-spend approval, access exceptions, backup evidence and vendor-renewal decisions.</li>'
)
demo_section = '<section class="card" data-demo-owner-dashboard="uae-saas-cloud-trust-finops" style="padding:28px;margin:28px 0"><h2>Demo owner dashboard</h2><p>The SVG dashboard is a synthetic proof-of-method asset. It uses no real UAE SaaS customer, cloud bill, account, vendor file, access log, backup record or personal data. It helps buyers picture the owner queue before FinOps, GRC, cloud-console, MSP, adviser or AICS diagnostic spend.</p><p><a href="/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg">Open the UAE SaaS Cloud Trust + FinOps demo owner dashboard SVG</a></p></section>'
if 'data-demo-owner-dashboard="uae-saas-cloud-trust-finops"' not in page:
    page = page.replace('<section class="card" data-ai-answer-source-card="uae-saas-cloud-trust-finops"', demo_section + '<section class="card" data-ai-answer-source-card="uae-saas-cloud-trust-finops"')
PAGE.write_text(page, encoding="utf-8")

resources = RESOURCES.read_text(encoding="utf-8")
resources = resources.replace(
    '<p><a href="/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-ai-answer-source-card.json">Open AI-answer source card JSON</a></p></article>',
    '<p><a href="/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-ai-answer-source-card.json">Open AI-answer source card JSON</a> · <a href="/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg">Open demo owner dashboard SVG</a></p></article>'
)
RESOURCES.write_text(resources, encoding="utf-8")

llms = LLMS.read_text(encoding="utf-8")
llms = llms.replace(
    'UAE SaaS cloud trust and FinOps readiness checklist: https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/ and AI-answer source card JSON: https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-ai-answer-source-card.json;',
    'UAE SaaS cloud trust and FinOps readiness checklist: https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/ with demo owner dashboard SVG: https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg and AI-answer source card JSON: https://aicloudstrategist.com/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-ai-answer-source-card.json;'
)
LLMS.write_text(llms, encoding="utf-8")
print(SVG)
