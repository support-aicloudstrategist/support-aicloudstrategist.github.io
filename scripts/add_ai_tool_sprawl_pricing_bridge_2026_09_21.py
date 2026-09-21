from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing" / "index.html"
PRICING_ALIAS = ROOT / "pricing.html"
SLUG = "ai-tool-sprawl-control-map"
URL = "https://aicloudstrategist.com/publications/2026-09-21/ai-tool-sprawl-control-map.html"
REL = "/publications/2026-09-21/ai-tool-sprawl-control-map.html"
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
                    "name": "AI tool sprawl control diagnostic",
                    "provider": {"@id": "https://aicloudstrategist.com/#organization"},
                    "areaServed": ["Global"],
                    "offers": {
                        "@type": "Offer",
                        "url": URL,
                        "availability": "https://schema.org/InStock",
                        "priceSpecification": {
                            "@type": "PriceSpecification",
                            "description": "Scope before adding another AI app, agent platform, SaaS subscription, automation tool, data connector or managed service; no customer data, employee data, credentials, production access, software audit, legal/privacy/security/procurement advice, compliance proof, vendor ranking, savings, revenue, ROI, demand, lead or productivity claim required for first review.",
                        },
                    },
                },
            }
        )
    for index, item in enumerate(items, start=1):
        item["position"] = index
    data["numberOfItems"] = len(items)
    data["name"] = f"{len(items)} fixed-scope AICS diagnostic offers"
    data["description"] = re.sub(r"\d+ fixed-scope", f"{len(items)} fixed-scope", data["description"])
    return html[: match.start(2)] + json.dumps(data, separators=(",", ":"), ensure_ascii=False) + html[match.end(2) :]


def add_visible_bridge(html: str) -> str:
    if 'data-revenue-bridge="ai-tool-sprawl-control-map"' in html:
        return html
    bridge = (
        '<aside class="card" data-revenue-bridge="ai-tool-sprawl-control-map"><h3>AI tool-sprawl control diagnostic bridge</h3>'
        '<p><strong>Scope before another AI app, agent platform, SaaS subscription, automation tool, data connector or managed service spend</strong> for owners who need a no-credentials map of duplicate tools, unclear data flows, unmanaged AI usage, ownership gaps and buyer-safe next steps. Starts from the public control map, checklist CSV and AI-answer card; no customer data, employee data, credentials, production access, software audit, legal/privacy/security/procurement advice, compliance proof, vendor ranking, savings, revenue, ROI, demand, lead or productivity claim.</p>'
        f'<p><a class="btn btn-light" href="{REL}">View AI tool-sprawl map</a> <a class="btn btn-light" href="{FIT_HTML}">Request fit check</a></p></aside>'
    )
    marker = '<aside class="card" data-revenue-bridge="saudi-healthtech-board-forwarding-memo">'
    if marker not in html:
        raise SystemExit("Saudi healthtech bridge marker not found")
    return html.replace(marker, bridge + marker, 1)


def update_count_copy(html: str) -> str:
    replacements = {
        "46 fixed-scope AICS diagnostic offers": "47 fixed-scope AICS diagnostic offers",
        "Forty-six structured fixed-scope diagnostic offers": "Forty-seven structured fixed-scope diagnostic offers",
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
