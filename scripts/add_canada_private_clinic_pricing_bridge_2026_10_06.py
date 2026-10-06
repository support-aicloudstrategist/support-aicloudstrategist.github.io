from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "canada-private-clinic-patient-growthos-pipeda-proof-pack"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
FIT = f"/free-business-review/?package={SLUG}&amp;source=pricing-fixed-scope"
BRIDGE = '''<aside class="card" data-revenue-bridge="canada-private-clinic-patient-growthos-pipeda-proof-pack"><h3>Canada private-clinic Patient GrowthOS + PIPEDA proof-pack diagnostic bridge</h3><p><strong>Scope before AI receptionist, patient-engagement, EMR/clinic software, call-answering, healthcare CRM, privacy/GRC or digital-marketing spend</strong> for Canadian private clinics that need a no-PHI/no-patient-data owner view of missed calls, patient follow-up, source ownership, PIPEDA/provincial-health-privacy adviser questions and unsupported appointment-growth stops. Starts from the buyer-safe proof pack and AI-answer source card; no real Canadian clinic, patient, PHI/personal-health data, call recording, EMR/PMS export, credential, production access, legal/privacy/security/clinical/PIPEDA advice, compliance proof, ranking, demand, lead, appointment-growth, patient outcome, revenue, savings, ROI or AI-accuracy claim.</p><p><a class="btn btn-light" href="/resources/canada-private-clinic-patient-growthos-pipeda-proof-pack/">View Canada proof pack</a> <a class="btn btn-light" href="/free-business-review/?package=canada-private-clinic-patient-growthos-pipeda-proof-pack&amp;source=pricing-fixed-scope">Request fit check</a></p></aside>'''

script_re = re.compile(r'(<script type="application/ld\+json">)({"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?})(</script>)')

def update(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    if 'data-revenue-bridge="canada-private-clinic-patient-growthos-pipeda-proof-pack"' not in html:
        marker = '<aside class="card" data-revenue-bridge="dpdp-smb-owner-evidence-diagnostic">'
        html = html.replace(marker, BRIDGE + marker, 1)
    m = script_re.search(html)
    if not m:
        raise RuntimeError(f"ItemList JSON-LD not found in {path}")
    data = json.loads(m.group(2))
    if not any(item.get("url") == URL for item in data["itemListElement"]):
        data["itemListElement"].append({
            "@type": "ListItem",
            "position": len(data["itemListElement"]) + 1,
            "url": URL,
            "item": {
                "@type": "Service",
                "name": "Canada private-clinic Patient GrowthOS + PIPEDA proof-pack diagnostic bridge",
                "provider": {"@id": "https://aicloudstrategist.com/#organization"},
                "areaServed": ["Canada"],
                "offers": {
                    "@type": "Offer",
                    "url": URL,
                    "availability": "https://schema.org/InStock",
                    "priceSpecification": {
                        "@type": "PriceSpecification",
                        "description": "Scope before AI receptionist, patient-engagement, EMR/clinic software, call-answering, healthcare CRM, privacy/GRC or digital-marketing spend; no real Canadian clinic, patient, PHI/personal-health data, call recording, EMR/PMS export, credential, production access, legal/privacy/security/clinical/PIPEDA advice, compliance proof, ranking, demand, lead, appointment-growth, patient outcome, revenue, savings, ROI or AI-accuracy claim."
                    }
                }
            }
        })
    data["numberOfItems"] = len(data["itemListElement"])
    data["name"] = f"{data['numberOfItems']} fixed-scope AICS diagnostic offers"
    compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = html[:m.start(2)] + compact + html[m.end(2):]
    heading_match = re.search(r'<h2>Fifty-five structured fixed-scope diagnostic offers buyers can understand before a custom build\.</h2>', html)
    if heading_match:
        html = html.replace(heading_match.group(0), '<h2>Fifty-six structured fixed-scope diagnostic offers buyers can understand before a custom build.</h2>', 1)
    path.write_text(html, encoding="utf-8")

for rel in ["pricing/index.html", "pricing.html"]:
    update(ROOT / rel)

print("updated Canada private-clinic pricing bridge on pricing/index.html and pricing.html")
