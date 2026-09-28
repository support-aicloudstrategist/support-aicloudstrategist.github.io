import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
RESOURCE = "/resources/singapore-pdpa-consent-data-protection-diagnostic-package/"
RESOURCE_URL = "https://aicloudstrategist.com" + RESOURCE
BRIDGE = """<aside class=\"card\" data-revenue-bridge=\"singapore-pdpa-consent-data-protection-diagnostic\"><h3>Singapore PDPA consent + data-protection diagnostic bridge</h3><p><strong>Scope before consent-management, privacy-GRC, DPO adviser, CRM, WhatsApp, booking, chatbot or automation spend</strong> for Singapore businesses that need a no-personal-data owner view of consent capture, withdrawal handling, DNC/Do Not Call questions, data-protection obligations, vendor handoffs and unsupported-claim stops. Starts from the buyer-safe diagnostic package, intake worksheet and AI-answer source card; no real customer, prospect, patient, student, employee or personal data, production export, credential, legal/privacy/security/DPO advice, PDPA compliance proof, PDPC approval, ranking, demand, lead, customer, revenue, savings, ROI or AI-accuracy claim.</p><p><a class=\"btn btn-light\" href=\"/resources/singapore-pdpa-consent-data-protection-diagnostic-package/\">View Singapore PDPA package</a> <a class=\"btn btn-light\" href=\"/free-business-review/?package=singapore-pdpa-consent-data-protection-diagnostic&amp;source=pricing-fixed-scope\">Request fit check</a></p></aside>"""

OFFER = {
    "@type": "ListItem",
    "position": 50,
    "url": RESOURCE_URL,
    "item": {
        "@type": "Service",
        "name": "Singapore PDPA consent + data-protection diagnostic",
        "provider": {"@id": "https://aicloudstrategist.com/#organization"},
        "areaServed": ["SG", "Singapore"],
        "offers": {
            "@type": "Offer",
            "url": RESOURCE_URL,
            "availability": "https://schema.org/InStock",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "description": "Scope before consent-management, privacy-GRC, DPO adviser, CRM, WhatsApp, booking, chatbot or automation spend; no real customer, prospect, patient, student, employee or personal data, production export, credential, legal/privacy/security/DPO advice, PDPA compliance proof, PDPC approval, ranking, demand, lead, customer, revenue, savings, ROI or AI-accuracy claim required for first review.",
            },
        },
    },
}


def update_itemlist(html: str) -> str:
    def repl(match: re.Match) -> str:
        payload = match.group(1)
        if "pricing#fixed-scope-diagnostics" not in payload:
            return match.group(0)
        data = json.loads(payload)
        items = data["itemListElement"]
        items = [item for item in items if item.get("url") != RESOURCE_URL]
        for idx, item in enumerate(items, start=1):
            item["position"] = idx
        items.append(OFFER)
        data["itemListElement"] = items
        data["numberOfItems"] = 50
        data["name"] = "50 fixed-scope AICS diagnostic offers"
        data["description"] = data["description"].replace("Sellable first-step diagnostics", "Sellable first-step diagnostics")
        return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "</script>"

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, html, count=0)


def update_page(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = update_itemlist(html)
    html = html.replace("49 fixed-scope AICS diagnostic offers", "50 fixed-scope AICS diagnostic offers")
    html = html.replace("Forty-nine structured fixed-scope diagnostic offers", "Fifty structured fixed-scope diagnostic offers")
    html = html.replace("Forty-nine structured fixed-scope diagnostic offers buyers can understand before a custom build.", "Fifty structured fixed-scope diagnostic offers buyers can understand before a custom build.")
    html = html.replace("49-offer", "50-offer")
    if 'data-revenue-bridge="singapore-pdpa-consent-data-protection-diagnostic"' not in html:
        marker = '<section class="section"><div class="container faq"><h2>FAQ</h2>'
        if marker not in html:
            raise RuntimeError(f"FAQ marker not found in {path}")
        html = html.replace(marker, BRIDGE + marker, 1)
    path.write_text(html, encoding="utf-8")


for page in PAGES:
    update_page(page)

print("updated Singapore PDPA pricing bridge on", ", ".join(str(p.relative_to(ROOT)) for p in PAGES))
