from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"
PRICING_ALIAS = ROOT / "pricing.html"
SLUG = "saudi-healthtech-board-forwarding-memo"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
REL = f"/resources/{SLUG}/"
FIT = f"/free-business-review/?package={SLUG}&source=pricing-fixed-scope"
FIT_HTML = FIT.replace("&", "&amp;")


def replace_itemlist(html: str) -> str:
    pattern = re.compile(
        r'(<script type="application/ld\+json">)({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})(</script>)'
    )
    match = pattern.search(html)
    if not match:
        raise SystemExit("pricing ItemList JSON-LD not found")
    data = json.loads(match.group(2))
    items = data["itemListElement"]
    if not any(item["url"] == URL for item in items):
        items.append(
            {
                "@type": "ListItem",
                "position": len(items) + 1,
                "url": URL,
                "item": {
                    "@type": "Service",
                    "name": "Saudi healthtech board-forwarding owner-evidence diagnostic",
                    "provider": {"@id": "https://aicloudstrategist.com/#organization"},
                    "areaServed": ["SA", "GCC", "Global"],
                    "offers": {
                        "@type": "Offer",
                        "url": URL,
                        "availability": "https://schema.org/InStock",
                        "priceSpecification": {
                            "@type": "PriceSpecification",
                            "description": "Scope before Saudi healthtech EHR/HIS, RCM/NPHIES-adjacent integration, AI receptionist, WhatsApp automation, cloud/MSP, FinOps, GRC or adviser spend; no patient data, health data, personal data, claim files, payer records, credentials, production access, Saudi client proof, legal/privacy/security/clinical/billing/procurement/audit advice, compliance proof, regulator approval, ranking, demand, lead, appointment, patient outcome, savings, revenue, ROI or AI-accuracy claim required for first review.",
                        },
                    },
                },
            }
        )
    for index, item in enumerate(items, start=1):
        item["position"] = index
    data["numberOfItems"] = len(items)
    data["name"] = f"{len(items)} fixed-scope AICS diagnostic offers"
    data["description"] = data["description"].replace("45 fixed-scope", f"{len(items)} fixed-scope")
    return html[: match.start(2)] + json.dumps(data, separators=(",", ":"), ensure_ascii=False) + html[match.end(2) :]


def add_visible_bridge(html: str) -> str:
    if 'data-revenue-bridge="saudi-healthtech-board-forwarding-memo"' in html:
        return html
    bridge = (
        '<aside class="card" data-revenue-bridge="saudi-healthtech-board-forwarding-memo"><h3>Saudi healthtech board-forwarding owner-evidence diagnostic bridge</h3>'
        '<p><strong>Scope before EHR/HIS, RCM/NPHIES-adjacent integration, AI receptionist, WhatsApp automation, cloud/MSP, FinOps, GRC or adviser spend</strong> for Saudi clinic groups, healthtech teams, payer-adjacent vendors and patient-engagement operators that need a no-patient-data board-forwardable owner-evidence packet. Starts from the public memo, checklist CSV and AI-answer source card; no patient data, health data, personal data, claim files, payer records, credential, production access, Saudi client proof, legal/privacy/security/clinical/billing/procurement/audit advice, compliance proof, regulator approval, ranking, demand, lead, appointment, patient outcome, savings, revenue, ROI or AI-accuracy claim.</p>'
        f'<p><a class="btn btn-light" href="{REL}">View Saudi board memo</a> <a class="btn btn-light" href="{FIT_HTML}">Request fit check</a></p></aside>'
    )
    marker = '<aside class="card" data-revenue-bridge="uk-private-clinic-patient-growthos-trust-comparison">'
    if marker not in html:
        raise SystemExit("UK private-clinic bridge marker not found")
    return html.replace(marker, bridge + marker, 1)


def update_count_copy(html: str) -> str:
    replacements = {
        "45 fixed-scope AICS diagnostic offers": "46 fixed-scope AICS diagnostic offers",
        "Forty-five structured fixed-scope diagnostic offers": "Forty-six structured fixed-scope diagnostic offers",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html


def main() -> None:
    html = PRICING.read_text(encoding="utf-8")
    html = replace_itemlist(html)
    html = add_visible_bridge(html)
    html = update_count_copy(html)
    PRICING.write_text(html, encoding="utf-8")
    PRICING_ALIAS.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
