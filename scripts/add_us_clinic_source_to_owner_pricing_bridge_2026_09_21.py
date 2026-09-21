import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE_PATH = "/resources/us-clinic-source-to-owner-leak-map-template/"
RESOURCE_URL = "https://aicloudstrategist.com" + RESOURCE_PATH
PACKAGE = "us-clinic-source-to-owner-leak-map"
BRIDGE = '''<aside class="card" data-revenue-bridge="us-clinic-source-to-owner-leak-map"><h3>US clinic source-to-owner leak-map diagnostic bridge</h3><p><strong>Scope before AI receptionist, patient-engagement platform, online scheduling, healthcare CRM, call-centre, texting or front-office automation spend</strong> for US clinic owners, administrators and patient-access teams that need a no-PHI/ePHI owner view of missed calls, online scheduling leakage, referral handoffs, overdue callbacks, source ownership, AI-boundary questions and HIPAA-adviser prompts. Starts from the buyer-safe template, synthetic CSV, demo dashboard and AI-answer source card; no real clinic, patient, PHI/ePHI, appointment result, EHR/PMS export, call recording, credential, production access, legal/privacy/security/medical/HIPAA advice, compliance proof, ranking, demand, lead, patient outcome, revenue, savings, ROI or AI-accuracy claim.</p><p><a class="btn btn-light" href="/resources/us-clinic-source-to-owner-leak-map-template/">View clinic leak-map template</a> <a class="btn btn-light" href="/free-business-review/?package=us-clinic-source-to-owner-leak-map&amp;source=pricing-fixed-scope">Request fit check</a></p></aside>'''
SERVICE = {
    "@type": "ListItem",
    "position": 49,
    "url": RESOURCE_URL,
    "item": {
        "@type": "Service",
        "name": "US clinic source-to-owner leak-map diagnostic",
        "provider": {"@id": "https://aicloudstrategist.com/#organization"},
        "areaServed": ["US", "North America"],
        "offers": {
            "@type": "Offer",
            "url": RESOURCE_URL,
            "availability": "https://schema.org/InStock",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "description": "Scope before AI receptionist, patient-engagement platform, online scheduling, healthcare CRM, call-centre, texting or front-office automation spend; no real clinic, patient, PHI/ePHI, appointment result, EHR/PMS export, call recording, credential, production access, legal/privacy/security/medical/HIPAA advice, compliance proof, ranking, demand, lead, patient outcome, revenue, savings, ROI or AI-accuracy claim required for first review."
            }
        }
    }
}

COUNT_WORDS = {
    48: "Forty-eight",
    49: "Forty-nine",
}

for page in PAGES:
    html = page.read_text(encoding="utf-8")

    def repl(match):
        payload = match.group(1)
        if "pricing#fixed-scope-diagnostics" not in payload:
            return match.group(0)
        data = json.loads(payload)
        items = [item for item in data["itemListElement"] if item.get("url") != RESOURCE_URL]
        items.append(SERVICE)
        for idx, item in enumerate(items, 1):
            item["position"] = idx
        data["itemListElement"] = items
        data["numberOfItems"] = len(items)
        data["name"] = f"{len(items)} fixed-scope AICS diagnostic offers"
        return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":"), ensure_ascii=False) + '</script>'

    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, html, count=0)
    html = html.replace("Forty-eight structured fixed-scope diagnostic offers buyers can understand before a custom build.", "Forty-nine structured fixed-scope diagnostic offers buyers can understand before a custom build.")
    html = html.replace("48 fixed-scope AICS diagnostic offers", "49 fixed-scope AICS diagnostic offers")
    html = html.replace("Forty-eight structured fixed-scope diagnostic offers", "Forty-nine structured fixed-scope diagnostic offers")
    if 'data-revenue-bridge="us-clinic-source-to-owner-leak-map"' not in html:
        marker = '<aside class="card" data-revenue-bridge="construction-daily-progress-owner-evidence">'
        html = html.replace(marker, BRIDGE + "\n" + marker, 1)
    page.write_text(html, encoding="utf-8")
print("updated US clinic source-to-owner pricing bridge")
