from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]
SLUG = "home-care-referral-intake-diagnostic-package"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
REL = f"/resources/{SLUG}/"
FIT = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"
BRIDGE = f'''<aside class="card" data-revenue-bridge="home-care-referral-intake-diagnostic-package"><h3>Home-care referral intake diagnostic bridge</h3><p><strong>Scope before home-care CRM, care-management platform, answering service, AI receptionist or caregiver scheduling software spend</strong> for home-care, home-health and senior-care agencies that need a no-patient-data owner view of missed family enquiries, referral-source handoffs, start-of-care blockers, callback ageing and caregiver scheduling exceptions. Starts from the buyer-safe diagnostic package, synthetic scope matrix and owner-dashboard demo; no real home-care agency, patient/resident data, family data, caregiver files, referral records, care-plan data, call recording, credential, production access, legal/privacy/compliance/clinical/staffing/billing advice, ranking, demand, lead, customer, admission, census, revenue, savings, ROI or AI-accuracy claim.</p><p><a class="btn btn-light" href="{REL}">View diagnostic package</a> <a class="btn btn-light" href="{FIT}">Request fit check</a></p></aside>'''

ITEMLIST_RE = re.compile(r'(<script type="application/ld\+json">)({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})(</script>)')
INSERT_BEFORE = '<section class="section"><div class="container faq">'


def update_html(html: str) -> str:
    match = ITEMLIST_RE.search(html)
    if not match:
        raise RuntimeError("pricing fixed-scope ItemList JSON-LD missing")
    data = json.loads(match.group(2))
    if not any(item.get("url") == URL for item in data["itemListElement"]):
        position = len(data["itemListElement"]) + 1
        data["itemListElement"].append(
            {
                "@type": "ListItem",
                "position": position,
                "url": URL,
                "item": {
                    "@type": "Service",
                    "name": "Home-care referral intake diagnostic package",
                    "provider": {"@id": "https://aicloudstrategist.com/#organization"},
                    "areaServed": ["US", "UK", "CA", "AU", "Global"],
                    "offers": {
                        "@type": "Offer",
                        "url": URL,
                        "availability": "https://schema.org/InStock",
                        "priceSpecification": {
                            "@type": "PriceSpecification",
                            "description": "Scope before home-care CRM, care-management platform, answering service, AI receptionist or caregiver scheduling software spend; no patient/resident data, family data, caregiver files, referral records, care-plan data, call recording, credential, production access, legal/privacy/compliance/clinical/staffing/billing advice, ranking, demand, lead, customer, admission, census, revenue, savings, ROI or AI-accuracy claim required for first review.",
                        },
                    },
                },
            }
        )
    data["numberOfItems"] = len(data["itemListElement"])
    data["name"] = f'{data["numberOfItems"]} fixed-scope AICS diagnostic offers'
    compact = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    html = html[: match.start()] + match.group(1) + compact + match.group(3) + html[match.end() :]
    if 'data-revenue-bridge="home-care-referral-intake-diagnostic-package"' not in html:
        html = html.replace(INSERT_BEFORE, BRIDGE + INSERT_BEFORE)
    return html


for path in FILES:
    path.write_text(update_html(path.read_text(encoding="utf-8")), encoding="utf-8")
