from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-healthcare-dpdp-cloud-trust-evidence-source-map"

pricing = ROOT / "pricing.html"
pricing_html = pricing.read_text(encoding="utf-8")
if 'data-revenue-bridge="india-healthcare-dpdp-cloud-trust-evidence-source-map"' not in pricing_html:
    pricing_card = (
        '<aside class="card" data-revenue-bridge="india-healthcare-dpdp-cloud-trust-evidence-source-map">'
        '<h3>India healthcare DPDP + cloud trust source-map diagnostic bridge</h3>'
        '<p><strong>Scope before DPDP software, EMR/EHR changes, WhatsApp patient workflows, AI reception, cloud migration, GRC tool or MSP spend</strong> for Indian hospitals, clinics, diagnostic labs and healthtech teams that need a no-patient-data map of evidence sources, owner accountability, adviser questions, vendor access, cloud data-location decisions and claim approval boundaries. Starts from the synthetic source-map CSV and demo owner map; no hospital, clinic, lab, patient, health record, cloud account, production export, credential, DPDP compliance proof, legal/privacy/security/medical advice, ranking, demand, lead, customer, revenue, savings, ROI or outcome claim.</p>'
        '<p><a class="btn btn-light" href="/resources/india-healthcare-dpdp-cloud-trust-evidence-source-map/">View source map</a> '
        '<a class="btn btn-light" href="/resources/india-healthcare-dpdp-cloud-trust-evidence-source-map/india-healthcare-dpdp-cloud-trust-evidence-source-map.csv">Download CSV</a> '
        '<a class="btn btn-light" href="/free-business-review/?package=india-healthcare-dpdp-cloud-trust-source-map&amp;source=pricing-fixed-scope">Request fit check</a></p>'
        '</aside>'
    )
    marker = '<p><a class="btn btn-primary" href="/contact.html?service=fixed-scope-diagnostic&stage=scoping&source=pricing-fixed-scope">Request a fixed-scope diagnostic</a> <span class="small muted">Use this when the buyer knows the problem area and needs scope, access boundaries and a written proposal before spend.</span></p>'
    pricing_html = pricing_html.replace('"numberOfItems":32', '"numberOfItems":33')
    pricing_html = pricing_html.replace('Thirty-two concrete first offers', 'Thirty-three concrete first offers')
    pricing_html = pricing_html.replace(marker, marker + pricing_card)
    pricing.write_text(pricing_html, encoding="utf-8")

fbr = ROOT / "free-business-review.html"
fbr_html = fbr.read_text(encoding="utf-8")
if 'data-review-route="india-healthcare-dpdp-cloud-trust-evidence-source-map"' not in fbr_html:
    fbr_card = (
        '        <article role="listitem" data-review-route="india-healthcare-dpdp-cloud-trust-evidence-source-map">\n'
        '          <span class="fbr-flow-number">A</span>\n'
        '          <p>India hospitals / clinics / labs / healthtech</p>\n'
        '          <h3>India healthcare DPDP + cloud trust fit check: patient-data source map, WhatsApp/AI boundaries, cloud owner evidence and adviser-ready questions</h3>\n'
        '          <small><a href="/resources/india-healthcare-dpdp-cloud-trust-evidence-source-map/">See the no-patient-data source map</a> · <a href="/resources/india-healthcare-dpdp-cloud-trust-evidence-source-map/india-healthcare-dpdp-cloud-trust-owner-map.svg">View demo owner map</a> · <a href="/resources/india-healthcare-dpdp-cloud-trust-evidence-source-map/india-healthcare-dpdp-cloud-trust-evidence-source-map.csv">Download synthetic source-map CSV</a> · <a href="/pricing.html#fixed-scope-diagnostics">See the diagnostic bridge</a></small>\n'
        '        </article>\n'
        '        <span class="fbr-flow-arrow" aria-hidden="true">→</span>\n'
    )
    marker = '      <div class="fbr-flow" role="list">\n'
    fbr_html = fbr_html.replace(marker, marker + fbr_card)
    fbr.write_text(fbr_html, encoding="utf-8")
    (ROOT / "free-business-review" / "index.html").write_text(fbr_html, encoding="utf-8")
else:
    (ROOT / "free-business-review" / "index.html").write_text(fbr_html, encoding="utf-8")

print("India healthcare DPDP cloud trust bridge updated")
