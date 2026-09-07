from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "australia-ndis-intake-vs-answering-service-crm-comparison"

pricing = ROOT / "pricing.html"
pricing_html = pricing.read_text(encoding="utf-8")
if 'data-revenue-bridge="australia-ndis-intake-comparison"' not in pricing_html:
    pricing_card = (
        '<aside class="card" data-revenue-bridge="australia-ndis-intake-comparison">'
        '<h3>Australia NDIS intake owner-evidence diagnostic bridge</h3>'
        '<p><strong>Scope before NDIS answering service, CRM, rostering software, referral marketing, AI receptionist or workflow automation spend</strong> for Australian NDIS providers that need a no-participant-data view of missed participant calls, support-coordinator referrals, consent prompts, capacity handoff, owner dashboards, human review and public-claim boundaries. Starts from the synthetic comparison matrix and demo owner map; no real NDIS provider, participant, nominee, carer, personal/health data, customer export, credential, NDIS registration/compliance proof, legal/privacy/security/disability-service advice, ranking, demand, lead, provider enquiry, participant-growth, revenue, savings, ROI or automation-performance claim.</p>'
        '<p><a class="btn btn-light" href="/resources/australia-ndis-intake-vs-answering-service-crm-comparison/">View comparison</a> '
        '<a class="btn btn-light" href="/resources/australia-ndis-intake-vs-answering-service-crm-comparison/australia-ndis-intake-comparison-matrix.csv">Download CSV</a> '
        '<a class="btn btn-light" href="/resources/australia-ndis-intake-vs-answering-service-crm-comparison/australia-ndis-intake-comparison-map.svg">View owner map</a> '
        '<a class="btn btn-light" href="/free-business-review/?package=australia-ndis-intake-comparison&amp;source=pricing-fixed-scope">Request fit check</a></p>'
        '</aside>'
    )
    marker = '<p><a class="btn btn-primary" href="/contact.html?service=fixed-scope-diagnostic&stage=scoping&source=pricing-fixed-scope">Request a fixed-scope diagnostic</a> <span class="small muted">Use this when the buyer knows the problem area and needs scope, access boundaries and a written proposal before spend.</span></p>'
    if marker not in pricing_html:
        raise SystemExit("pricing insertion marker not found")
    pricing_html = pricing_html.replace('"numberOfItems":35', '"numberOfItems":36')
    pricing_html = pricing_html.replace('Thirty-five concrete first offers', 'Thirty-six concrete first offers')
    pricing_html = pricing_html.replace(marker, marker + pricing_card)
    pricing.write_text(pricing_html, encoding="utf-8")

fbr = ROOT / "free-business-review.html"
fbr_html = fbr.read_text(encoding="utf-8")
if 'data-review-route="australia-ndis-intake-comparison"' not in fbr_html:
    fbr_card = (
        '        <article role="listitem" data-review-route="australia-ndis-intake-comparison">\n'
        '          <span class="fbr-flow-number">A</span>\n'
        '          <p>Australia NDIS providers</p>\n'
        '          <h3>Australia NDIS intake fit check: missed participant calls, support-coordinator referrals, consent prompts, capacity handoff and owner dashboards</h3>\n'
        '          <small><a href="/resources/australia-ndis-intake-vs-answering-service-crm-comparison/">See the no-participant-data comparison</a> · <a href="/resources/australia-ndis-intake-vs-answering-service-crm-comparison/australia-ndis-intake-comparison-matrix.csv">Download synthetic comparison CSV</a> · <a href="/resources/australia-ndis-intake-vs-answering-service-crm-comparison/australia-ndis-intake-comparison-map.svg">View demo owner map</a> · <a href="/pricing.html#fixed-scope-diagnostics">See the diagnostic bridge</a></small>\n'
        '        </article>\n'
        '        <span class="fbr-flow-arrow" aria-hidden="true">→</span>\n'
    )
    marker = '      <div class="fbr-flow" role="list">\n'
    if marker not in fbr_html:
        raise SystemExit("free-review insertion marker not found")
    fbr_html = fbr_html.replace(marker, marker + fbr_card)
    fbr.write_text(fbr_html, encoding="utf-8")
    (ROOT / "free-business-review" / "index.html").write_text(fbr_html, encoding="utf-8")
else:
    (ROOT / "free-business-review" / "index.html").write_text(fbr_html, encoding="utf-8")

print("Australia NDIS intake diagnostic bridge updated")
