import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "pricing" / "index.html", ROOT / "pricing.html"]
SLUG = "dpdp-compliance-checklist-small-business-india"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
REL = f"/resources/{SLUG}/"
FIT = f"/free-business-review/?package={SLUG}&source=pricing-fixed-scope"
FIT_HTML = FIT.replace("&", "&amp;")
BRIDGE = (
    '<aside class="card" data-revenue-bridge="dpdp-smb-owner-evidence-diagnostic">'
    '<h3>India SMB DPDP owner-evidence diagnostic bridge</h3>'
    '<p><strong>Scope before CRM, WhatsApp automation, chatbot, lead-capture, privacy-consultant, legal-review, agency or internal spreadsheet spend</strong> for Indian small businesses that need a no-customer-data owner view of forms, consent/notice copy, vendor access, request handling, redacted evidence and unsupported DPDP-claim stops. Starts from the buyer-safe checklist, synthetic evidence register, AI-answer source card and shortlist matrix; no real customer, prospect, patient, child, financial, payment, health, sensitive personal or production data, credential, legal/privacy/security advice, DPDP compliance proof, regulator approval, audit opinion, ranking, demand, lead, customer, revenue, savings, ROI or automation-performance claim.</p>'
    f'<p><a class="btn btn-light" href="{REL}">View DPDP SMB checklist</a> '
    f'<a class="btn btn-light" href="{REL}dpdp-smb-shortlist-scoring-matrix.csv">Download shortlist matrix</a> '
    f'<a class="btn btn-light" href="{FIT_HTML}">Request fit check</a></p>'
    '</aside>'
)
SERVICE = {
    "@type": "ListItem",
    "position": 999,
    "url": URL,
    "item": {
        "@type": "Service",
        "name": "India SMB DPDP owner-evidence diagnostic bridge",
        "provider": {"@id": "https://aicloudstrategist.com/#organization"},
        "areaServed": ["India"],
        "offers": {
            "@type": "Offer",
            "url": URL,
            "availability": "https://schema.org/InStock",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "description": "Scope before CRM, WhatsApp automation, chatbot, lead-capture, privacy-consultant, legal-review, agency or internal spreadsheet spend; no real customer, prospect, patient, child, financial, payment, health, sensitive personal or production data, credential, legal/privacy/security advice, DPDP compliance proof, regulator approval, audit opinion, ranking, demand, lead, customer, revenue, savings, ROI or automation-performance claim required for first review.",
            },
        },
    },
}
ITEMLIST_RE = re.compile(r'(<script type="application/ld\+json">)({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})(</script>)')


def update_itemlist(html: str) -> str:
    match = ITEMLIST_RE.search(html)
    if not match:
        raise SystemExit("fixed-scope ItemList JSON-LD not found")
    data = json.loads(match.group(2))
    items = [item for item in data["itemListElement"] if item["url"] != URL]
    items.append(SERVICE)
    for position, item in enumerate(items, start=1):
        item["position"] = position
    data["itemListElement"] = items
    data["numberOfItems"] = len(items)
    data["name"] = f"{len(items)} fixed-scope AICS diagnostic offers"
    replacement = match.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + match.group(3)
    return html[: match.start()] + replacement + html[match.end():]


def update_page(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = update_itemlist(html)
    html = html.replace("54 fixed-scope AICS diagnostic offers", "55 fixed-scope AICS diagnostic offers")
    html = html.replace("Fifty-four structured fixed-scope diagnostic offers", "Fifty-five structured fixed-scope diagnostic offers")
    if 'data-revenue-bridge="dpdp-smb-owner-evidence-diagnostic"' not in html:
        marker = '<aside class="card" data-revenue-bridge="priority-answer-engine-routes">'
        if marker not in html:
            raise SystemExit(f"visible bridge insertion marker missing in {path}")
        html = html.replace(marker, BRIDGE + marker, 1)
    path.write_text(html, encoding="utf-8")


for page in PAGES:
    update_page(page)

print("added DPDP SMB pricing bridge to pricing routes")
