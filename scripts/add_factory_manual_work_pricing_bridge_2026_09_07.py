from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"
html = PRICING.read_text(encoding="utf-8")

bridge = (
    '<aside class="card" data-revenue-bridge="factory-manual-work-reduction">'
    '<h3>Factory manual-work reduction diagnostic bridge</h3>'
    '<p><strong>Scope before ERP/MRP, workflow automation, custom software, WhatsApp automation or owner-dashboard spend</strong> '
    'for small manufacturers, fabrication units, packaging teams, exporters and operations owners who need a no-credentials view of order status, material follow-up, production-stage leakage, dispatch handoff, payment reminder and owner-review fields before build or vendor decisions. Starts from the buyer problem page and synthetic owner-evidence CSV; no real factory client, customer data, employee record, ERP export, vendor contract, invoice, credential, production access, job-cut, savings, productivity, delivery, revenue, ranking, demand, lead, customer, testimonial, certification, software-partnership or outcome claim.</p>'
    '<p><a class="btn btn-light" href="/resources/customer-problem-search/factory-manual-work-reduce/">View factory checklist</a> '
    '<a class="btn btn-light" href="/resources/customer-problem-search/factory-manual-work-reduce/factory-manual-work-owner-evidence.csv">Download CSV</a> '
    '<a class="btn btn-light" href="/free-business-review/?package=factory-manual-work-reduction&amp;source=pricing-fixed-scope">Request fit check</a> '
    '<a class="btn btn-light" href="/services/workflow-automation/">Workflow automation path</a></p></aside>'
)

if 'data-revenue-bridge="factory-manual-work-reduction"' not in html:
    html = html.replace(
        '<h2>Thirty-four concrete first offers buyers can understand before a custom build.</h2>',
        '<h2>Thirty-five concrete first offers buyers can understand before a custom build.</h2>',
    )
    html = html.replace(
        'Use these when a founder, clinic owner, law-firm operator or SaaS team asks',
        'Use these when a founder, factory owner, clinic owner, law-firm operator or SaaS team asks',
    )
    marker = '<aside class="card" data-revenue-bridge="healthcare-ai-patient-growth-platform">'
    html = html.replace(marker, bridge + marker, 1)
else:
    html = html.replace('Thirty-four concrete first offers', 'Thirty-five concrete first offers')

pattern = re.compile(r'(<script type="application/ld\+json">)(\{"@context":"https://schema.org","@type":"ItemList","@id":"https://aicloudstrategist.com/pricing#fixed-scope-diagnostics".*?\})(</script>)')
match = pattern.search(html)
if not match:
    raise SystemExit("fixed-scope ItemList JSON-LD not found")
item_list = json.loads(match.group(2))
item_list["name"] = "Thirty-five fixed-scope AICS diagnostic offers"
item_list["description"] = item_list["description"].replace("34", "35") if "34" in item_list["description"] else item_list["description"]
item_list["numberOfItems"] = 35
factory_url = "https://aicloudstrategist.com/resources/customer-problem-search/factory-manual-work-reduce/"
if not any(item.get("url") == factory_url for item in item_list["itemListElement"]):
    item_list["itemListElement"].append({
        "@type": "ListItem",
        "position": 35,
        "url": factory_url,
        "item": {
            "@type": "Service",
            "name": "Factory manual-work reduction evidence review",
            "provider": {"@id": "https://aicloudstrategist.com/#organization"},
            "areaServed": ["IN", "Global"],
            "offers": {
                "@type": "Offer",
                "url": factory_url,
                "availability": "https://schema.org/InStock",
                "priceSpecification": {
                    "@type": "PriceSpecification",
                    "description": "Scope before quote; no factory client data, employee record, ERP export, vendor contract, invoice, credentials, production access, job-cut, savings, productivity, delivery, revenue, ranking, demand, customer or outcome claim."
                }
            }
        }
    })
for index, item in enumerate(item_list["itemListElement"], start=1):
    item["position"] = index
json_text = json.dumps(item_list, separators=(",", ":"), ensure_ascii=False)
html = html[:match.start(2)] + json_text + html[match.end(2):]
PRICING.write_text(html, encoding="utf-8")
print("updated pricing factory manual-work bridge")
