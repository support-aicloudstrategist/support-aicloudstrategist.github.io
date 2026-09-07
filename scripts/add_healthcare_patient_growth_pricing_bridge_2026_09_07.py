from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "healthcare-ai-patient-growth-platform"
PAGE_URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_PATH = f"/resources/{SLUG}/healthcare-ai-patient-growth-owner-evidence.csv"
SVG_PATH = f"/resources/{SLUG}/healthcare-ai-patient-growth-owner-map.svg"

PRICING = ROOT / "pricing.html"
pricing_html = PRICING.read_text(encoding="utf-8")

if 'data-revenue-bridge="healthcare-ai-patient-growth-platform"' not in pricing_html:
    card = (
        '<aside class="card" data-revenue-bridge="healthcare-ai-patient-growth-platform">'
        '<h3>Healthcare AI Patient GrowthOS diagnostic bridge</h3>'
        '<p><strong>Scope before AI receptionist, patient-access automation, CRM/PMS/EHR workflow, WhatsApp follow-up, chatbot or clinic growth platform spend</strong> for clinics and healthtech teams that need a no-patient-data view of enquiry capture, appointment handoff, human approval, cloud trust, FinOps ownership, rollback paths and public-claim boundaries before build or vendor decisions. Starts from the synthetic owner-evidence CSV and demo owner map; no real healthcare client, clinic, patient, PHI/ePHI, health record, personal data, vendor export, credential, production access, GDPR/UK GDPR/DPIA/NIS2/ISO/SOC2/HIPAA compliance proof, legal/privacy/security/medical advice, ranking, demand, lead, booked appointment, patient, revenue, savings, ROI or automation-performance claim.</p>'
        '<p><a class="btn btn-light" href="/resources/healthcare-ai-patient-growth-platform/">View Patient GrowthOS checklist</a> '
        '<a class="btn btn-light" href="/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-evidence.csv">Download CSV</a> '
        '<a class="btn btn-light" href="/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-map.svg">View owner map</a> '
        '<a class="btn btn-light" href="/free-business-review/?package=healthcare-ai-patient-growth-platform&amp;source=pricing-fixed-scope">Request fit check</a></p>'
        '</aside>'
    )
    anchor = '<aside class="card" data-revenue-bridge="healthcare-ai-trust-controls">'
    pricing_html = pricing_html.replace(anchor, card + anchor, 1)
    pricing_html = pricing_html.replace('Thirty-three concrete first offers', 'Thirty-four concrete first offers', 1)
    pricing_html = pricing_html.replace('"numberOfItems":33', '"numberOfItems":34', 1)

    pattern = r'(<script type="application/ld\+json">)({"@context":"https://schema.org","@type":"ItemList".*?})(</script>)'
    match = re.search(pattern, pricing_html)
    if not match:
        raise SystemExit("pricing ItemList JSON-LD missing")
    itemlist = json.loads(match.group(2))
    urls = [item["url"] for item in itemlist["itemListElement"]]
    if PAGE_URL not in urls:
        service = {
            "@type": "ListItem",
            "position": 2,
            "url": PAGE_URL,
            "item": {
                "@type": "Service",
                "name": "Healthcare AI Patient GrowthOS evidence review",
                "provider": {"@id": "https://aicloudstrategist.com/#organization"},
                "areaServed": ["Global"],
                "offers": {
                    "@type": "Offer",
                    "url": PAGE_URL,
                    "availability": "https://schema.org/InStock",
                    "priceSpecification": {
                        "@type": "PriceSpecification",
                        "description": "Scope before patient-access automation, AI receptionist, chatbot, CRM/PMS/EHR workflow or clinic growth platform spend; no patient data, PHI/ePHI, health records, credentials, production access, compliance proof, legal/privacy/security/medical advice, revenue, savings, ROI, demand, lead, appointment or automation-performance claim required for first review."
                    },
                },
            },
        }
        itemlist["itemListElement"].insert(1, service)
        for index, item in enumerate(itemlist["itemListElement"], start=1):
            item["position"] = index
        itemlist["numberOfItems"] = len(itemlist["itemListElement"])
        new_json = json.dumps(itemlist, separators=(",", ":"), ensure_ascii=False)
        pricing_html = pricing_html[:match.start(2)] + new_json + pricing_html[match.end(2):]
    PRICING.write_text(pricing_html, encoding="utf-8")

FBR = ROOT / "free-business-review.html"
fbr_html = FBR.read_text(encoding="utf-8")
if 'data-review-route="healthcare-ai-patient-growth-platform"' not in fbr_html:
    fbr_card = (
        '        <article role="listitem" data-review-route="healthcare-ai-patient-growth-platform">\n'
        '          <span class="fbr-flow-number">A</span>\n'
        '          <p>Clinics / healthtech patient-growth teams</p>\n'
        '          <h3>Healthcare AI Patient GrowthOS fit check: enquiry capture, appointment handoff, trust controls, FinOps ownership and no-patient-data evidence boundaries</h3>\n'
        '          <small><a href="/resources/healthcare-ai-patient-growth-platform/">See the Patient GrowthOS evidence checklist</a> · <a href="/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-evidence.csv">Download synthetic owner-evidence CSV</a> · <a href="/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-map.svg">View demo owner map</a> · <a href="/pricing.html#fixed-scope-diagnostics">See the diagnostic bridge</a></small>\n'
        '        </article>\n'
        '        <span class="fbr-flow-arrow" aria-hidden="true">→</span>\n'
    )
    marker = '      <div class="fbr-flow" role="list">\n'
    fbr_html = fbr_html.replace(marker, marker + fbr_card, 1)
    FBR.write_text(fbr_html, encoding="utf-8")
(ROOT / "free-business-review" / "index.html").write_text(fbr_html, encoding="utf-8")

print("Healthcare AI Patient GrowthOS revenue bridge updated")
