from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing" / "index.html", ROOT / "pricing.html"]
RESOURCE = "/resources/uk-private-clinic-owner-evidence-decision-memo/"
PACKAGE = "uk-private-clinic-owner-evidence-decision-memo"

NEW_ITEM = {
    "@type": "ListItem",
    "position": 53,
    "url": f"https://aicloudstrategist.com{RESOURCE}",
    "item": {
        "@type": "Service",
        "name": "UK private clinic owner-evidence diagnostic bridge",
        "provider": {"@id": "https://aicloudstrategist.com/#organization"},
        "areaServed": ["GB", "Europe"],
        "offers": {
            "@type": "Offer",
            "url": f"https://aicloudstrategist.com{RESOURCE}",
            "availability": "https://schema.org/InStock",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "description": "Scope before UK private-clinic AI receptionist, practice-management software, patient engagement, call answering, booking marketplace, agency, adviser or automation spend; no real clinic, patient data, personal data, health data, call recording, PMS/EMR export, credential, production access, legal/privacy/security/clinical/CQC/DTAC/DSPT/GDPR advice, compliance proof, ranking, demand, lead, booked appointment, patient growth, revenue, savings, ROI or AI-accuracy claim required for first review.",
            },
        },
    },
}

BRIDGE = """<aside class=\"card\" data-revenue-bridge=\"uk-private-clinic-owner-evidence-decision-memo\"><h3>UK private clinic owner-evidence diagnostic bridge</h3><p><strong>Scope before AI receptionist, practice-management software, patient engagement, call answering, booking marketplace, agency, adviser or automation spend</strong> for UK private-clinic owners and practice managers who need a no-patient-data owner memo, shortlist rubric, AI handover stop rules and GDPR evidence questions before selecting a route. Starts from the buyer-safe decision memo, CSV, owner evidence map, AI-answer source card and shortlist scoring rubric; no real clinic, patient data, personal data, health data, call recording, PMS/EMR export, credential, production access, legal/privacy/security/clinical/CQC/DTAC/DSPT/GDPR advice, compliance proof, ranking, demand, lead, appointment growth, revenue, savings, ROI or AI-accuracy claim.</p><p><a class=\"btn btn-light\" href=\"/resources/uk-private-clinic-owner-evidence-decision-memo/\">View UK clinic memo</a> <a class=\"btn btn-light\" href=\"/free-business-review/?package=uk-private-clinic-owner-evidence-decision-memo&amp;source=pricing-fixed-scope\">Request fit check</a></p></aside>\n"""

for path in PRICING_PAGES:
    html = path.read_text(encoding="utf-8")
    html = html.replace("52 fixed-scope AICS diagnostic offers", "53 fixed-scope AICS diagnostic offers")
    html = html.replace("\"numberOfItems\":52", "\"numberOfItems\":53")
    html = html.replace("Fifty-two structured fixed-scope diagnostic offers buyers can understand before a custom build.", "Fifty-three structured fixed-scope diagnostic offers buyers can understand before a custom build.")
    html = html.replace("<h2>Fifty-two structured fixed-scope diagnostic offers buyers can understand before a custom build.</h2>", "<h2>Fifty-three structured fixed-scope diagnostic offers buyers can understand before a custom build.</h2>")

    def update_itemlist(match: re.Match[str]) -> str:
        raw = match.group(1)
        if "pricing#fixed-scope-diagnostics" not in raw:
            return match.group(0)
        itemlist = json.loads(raw)
        itemlist["name"] = "53 fixed-scope AICS diagnostic offers"
        itemlist["numberOfItems"] = 53
        itemlist["itemListElement"] = [i for i in itemlist["itemListElement"] if i.get("url") != NEW_ITEM["url"]]
        itemlist["itemListElement"].append(NEW_ITEM)
        for idx, item in enumerate(itemlist["itemListElement"], start=1):
            item["position"] = idx
        return '<script type="application/ld+json">' + json.dumps(itemlist, separators=(",", ":"), ensure_ascii=False) + "</script>"

    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', update_itemlist, html)
    if 'data-revenue-bridge="uk-private-clinic-owner-evidence-decision-memo"' not in html:
        marker = '<script>document.querySelectorAll(\'.pricing-toggle button\')'
        html = html.replace(marker, BRIDGE + marker)
    path.write_text(html, encoding="utf-8")

print("updated pricing bridge for UK private clinic owner-evidence diagnostic")
