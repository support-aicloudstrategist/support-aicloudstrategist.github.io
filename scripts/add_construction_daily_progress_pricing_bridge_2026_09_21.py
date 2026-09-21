import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "https://aicloudstrategist.com/resources/global-construction-project-delay-daily-progress-owner-evidence-checklist/"
BRIDGE = '''<aside class="card" data-revenue-bridge="construction-daily-progress-owner-evidence"><h3>Construction daily-progress owner-evidence diagnostic bridge</h3><p><strong>Scope before project-management software, field-reporting apps, ERP modules, WhatsApp automation, AI dashboards or construction consulting spend</strong> for builders, contractors, renovators and project owners who need a no-site-data owner view of delayed daily updates, site-photo evidence, subcontractor handoffs, material blockers, change-order approvals and risky claim boundaries. Starts from the buyer-safe construction checklist, synthetic CSV and AI-answer source card; no real project, site, worker, subcontractor, supplier, client, permit, safety, payment, contract, photo, production export, legal/safety/engineering/procurement/dispute advice, compliance proof, schedule recovery, productivity, savings, ROI, ranking, demand, lead, customer or revenue claim.</p><p><a class="btn btn-light" href="/resources/global-construction-project-delay-daily-progress-owner-evidence-checklist/">View construction checklist</a> <a class="btn btn-light" href="/free-business-review/?package=construction-daily-progress-owner-evidence&amp;source=pricing-fixed-scope">Request fit check</a></p></aside>'''
SERVICE = {
    "@type": "ListItem",
    "position": 48,
    "url": RESOURCE,
    "item": {
        "@type": "Service",
        "name": "Construction daily-progress owner-evidence diagnostic",
        "provider": {"@id": "https://aicloudstrategist.com/#organization"},
        "areaServed": ["Global"],
        "offers": {
            "@type": "Offer",
            "url": RESOURCE,
            "availability": "https://schema.org/InStock",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "description": "Scope before project-management software, field-reporting apps, ERP modules, WhatsApp automation, AI dashboards or construction consulting spend; no real project, site, worker, subcontractor, supplier, client, permit, safety, payment, contract, photo, production export, legal/safety/engineering/procurement/dispute advice, compliance proof, schedule recovery, productivity, savings, ROI, ranking, demand, lead, customer or revenue claim required for first review."
            }
        }
    }
}

for page in PAGES:
    html = page.read_text(encoding="utf-8")
    def repl(match):
        payload = match.group(1)
        if "pricing#fixed-scope-diagnostics" not in payload:
            return match.group(0)
        data = json.loads(payload)
        items = data["itemListElement"]
        items = [item for item in items if item.get("url") != RESOURCE]
        items.append(SERVICE)
        for idx, item in enumerate(items, 1):
            item["position"] = idx
        data["itemListElement"] = items
        data["numberOfItems"] = len(items)
        data["name"] = f"{len(items)} fixed-scope AICS diagnostic offers"
        return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":"), ensure_ascii=False) + '</script>'
    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, html, count=0)
    html = html.replace("Forty-seven structured fixed-scope diagnostic offers buyers can understand before a custom build.", "Forty-eight structured fixed-scope diagnostic offers buyers can understand before a custom build.")
    html = html.replace("47 fixed-scope AICS diagnostic offers", "48 fixed-scope AICS diagnostic offers")
    html = html.replace("Forty-seven structured fixed-scope diagnostic offers", "Forty-eight structured fixed-scope diagnostic offers")
    if 'data-revenue-bridge="construction-daily-progress-owner-evidence"' not in html:
        marker = '<aside class="card" data-revenue-bridge="us-dental-treatment-plan-follow-up">'
        html = html.replace(marker, BRIDGE + "\n" + marker, 1)
    page.write_text(html, encoding="utf-8")
print("updated construction daily progress pricing bridge")
