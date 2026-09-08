from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-08"
SLUG = "ai-agent-cost-spike-triage"
TITLE = "AI Agent Cost Spike Triage: 7 Checks Before You Scale or Switch Tools"

page = ROOT / "publications" / DATE / f"{SLUG}.html"
html = page.read_text(encoding="utf-8")
bridge = """<section class='card' id='cost-spike-diagnostic-bridge'><h2>When this should become a paid diagnostic</h2><p>If the spike is tied to customer-facing AI, tool calls, retries, model routing, support workflows or vendor budget decisions, AICS can turn the worksheet into a bounded AI cost evidence review before you scale, switch tools, cancel automation or expose production access.</p><ul><li><strong>Buyer trigger:</strong> AI agent, chatbot, workflow or token costs are rising and the owner needs a tool-neutral decision record.</li><li><strong>Safe first scope:</strong> no credentials, customer data, production changes, savings promise, ROI claim, legal advice, security certification or vendor approval claim.</li><li><strong>Output:</strong> cost trigger map, retry and handoff findings, quality evidence notes, options list, owner cadence and next-decision recommendation.</li></ul><p><a href='/pricing#fixed-scope-diagnostics'>View fixed-scope diagnostics</a> · <a href='/free-business-review/?package=ai-agent-cost-spike-triage&amp;source=publication-2026-09-08'>Request fit check</a> · <a href='ai-agent-cost-spike-triage.csv'>Use the CSV first</a></p></section>"""
if "id='cost-spike-diagnostic-bridge'" not in html:
    html = html.replace("<section class='card boundary'><h2>Truth boundary</h2>", bridge + "<section class='card boundary'><h2>Truth boundary</h2>", 1)
page.write_text(html, encoding="utf-8")

md_path = ROOT / "publications" / DATE / f"{SLUG}.md"
md = md_path.read_text(encoding="utf-8")
md_bridge = f"""
## When this should become a paid diagnostic

If the spike is tied to customer-facing AI, tool calls, retries, model routing, support workflows or vendor budget decisions, AICS can turn the worksheet into a bounded AI cost evidence review before you scale, switch tools, cancel automation or expose production access.

- Buyer trigger: AI agent, chatbot, workflow or token costs are rising and the owner needs a tool-neutral decision record.
- Safe first scope: no credentials, customer data, production changes, savings promise, ROI claim, legal advice, security certification or vendor approval claim.
- Output: cost trigger map, retry and handoff findings, quality evidence notes, options list, owner cadence and next-decision recommendation.

Fit-check route: https://aicloudstrategist.com/free-business-review/?package=ai-agent-cost-spike-triage&source=publication-2026-09-08
Pricing context: https://aicloudstrategist.com/pricing#fixed-scope-diagnostics
"""
if "When this should become a paid diagnostic" not in md:
    md = md.replace("**Truth boundary:**", md_bridge + "\n**Truth boundary:**", 1)
md_path.write_text(md, encoding="utf-8")

print(f"Added revenue bridge to /publications/{DATE}/{SLUG}.html")
