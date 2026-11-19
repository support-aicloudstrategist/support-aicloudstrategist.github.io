from pathlib import Path
import csv, html, json, shutil, subprocess

REPO = Path(__file__).resolve().parents[1]
DATE = "2026-11-19"
SLOT = "evening"
SLUG = "aws-bill-owner-action-path"
TITLE = "AWS Bill Too High? A 6-Step Owner Action Path"
HOOK = "A no-credentials educational path to confirm the change, find the scope, name the owner, classify the driver and choose an evidence-matched next action."
BOUNDARY = "Buyer education only — not an AWS account audit, savings guarantee, client case study, financial advice, security advice, certification, partnership or production-change instruction."
BASE = f"https://aicloudstrategist.com/publications/{DATE}"
URL = f"{BASE}/{SLUG}.html"
PNG_URL = f"{BASE}/{SLUG}.png"
SVG_URL = f"{BASE}/{SLUG}.svg"
CSV_URL = f"{BASE}/{SLUG}.csv"
CARD_URL = f"{BASE}/{SLUG}-answer-card.json"
REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}"

steps = [
    ("1", "Confirm the change", "Compare a comparable period. Separate usage from timing, tax, credits or currency."),
    ("2", "Find service + account", "Record the changed service, region, account, tag or workload."),
    ("3", "Name the owner", "Product · Platform · Finance · Experiment. Mark shared or unallocated spend explicitly."),
    ("4", "Classify the driver", "Usage · Unit price · Transfer · Storage · Logs · Managed tier · GPU/AI · Commitments · Migration."),
    ("5", "Choose by evidence", "ACT: evidence sufficient · INVESTIGATE: owner or driver unclear · HOLD: confidence thin."),
    ("6", "Set the next review", "Record owner, evidence requested, decision date and stop rule."),
]


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width=29, lines=4):
    words = text.split()
    result, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if len(candidate) > width and current:
            result.append(current)
            current = word
        else:
            current = candidate
    if current:
        result.append(current)
    return result[:lines]


pub = REPO / "publications" / DATE
pub.mkdir(parents=True, exist_ok=True)

# Deterministic infographic fallback: source prompt and content live under infographic/aws-bill-owner-path.
positions = [(84, 262), (440, 262), (796, 262), (84, 548), (440, 548), (796, 548)]
cards = []
for idx, ((number, title, body), (x, y)) in enumerate(zip(steps, positions)):
    title_lines = wrap(title.upper(), 22, 2)
    body_lines = wrap(body, 37, 4)
    title_svg = "".join(f"<tspan x='{x+70}' dy='{0 if i == 0 else 23}'>{esc(line)}</tspan>" for i, line in enumerate(title_lines))
    body_svg = "".join(f"<tspan x='{x+24}' dy='{0 if i == 0 else 19}'>{esc(line)}</tspan>" for i, line in enumerate(body_lines))
    gate = ""
    if number == "5":
        gate = f"<g transform='translate({x+22} {y+184})'><rect width='78' height='28' rx='8' fill='#0f766e'/><text x='39' y='19' text-anchor='middle' class='micro'>ACT</text><rect x='86' width='112' height='28' rx='8' fill='#b45309'/><text x='142' y='19' text-anchor='middle' class='micro'>INVESTIGATE</text><rect x='206' width='74' height='28' rx='8' fill='#475569'/><text x='243' y='19' text-anchor='middle' class='micro'>HOLD</text></g>"
    cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='320' height='236' rx='22' fill='#102d4c' stroke='#38bdf8' stroke-width='2'/>
      <path d='M{x+16} {y+54} H{x+304}' stroke='#285577'/>
      <circle cx='{x+40}' cy='{y+37}' r='23' fill='#f59e0b'/>
      <text x='{x+40}' y='{y+46}' text-anchor='middle' class='num'>{number}</text>
      <text x='{x+70}' y='{y+31}' class='card-title'>{title_svg}</text>
      <text x='{x+24}' y='{y+92}' class='body'>{body_svg}</text>
      {gate}
    </g>""")

connectors = """
<path d='M404 380 H430' class='connector'/><path d='M760 380 H786' class='connector'/>
<path d='M956 508 V530 H244 V538' class='connector'/>
<path d='M404 666 H430' class='connector'/><path d='M760 666 H786' class='connector'/>
"""
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
<defs>
 <pattern id='grid' width='28' height='28' patternUnits='userSpaceOnUse'><path d='M28 0H0V28' fill='none' stroke='#2a5472' stroke-width='1' opacity='.38'/></pattern>
 <linearGradient id='hero' x1='0' x2='1'><stop stop-color='#0b2138'/><stop offset='.55' stop-color='#123f63'/><stop offset='1' stop-color='#0f5265'/></linearGradient>
 <filter id='shadow' x='-15%' y='-15%' width='130%' height='140%'><feDropShadow dx='0' dy='10' stdDeviation='9' flood-color='#020617' flood-opacity='.36'/></filter>
 <marker id='arrow' markerWidth='9' markerHeight='9' refX='7' refY='3' orient='auto'><path d='M0 0L0 6L8 3Z' fill='#67e8f9'/></marker>
 <style>.title{{font-family:Arial,sans-serif;font-size:47px;font-weight:900;fill:#fff}}.subtitle{{font-family:Arial,sans-serif;font-size:19px;font-weight:800;fill:#bae6fd;letter-spacing:3px}}.num{{font-family:Arial,sans-serif;font-size:26px;font-weight:900;fill:#082f49}}.card-title{{font-family:Arial,sans-serif;font-size:18px;font-weight:900;fill:#fff;letter-spacing:.4px}}.body{{font-family:Arial,sans-serif;font-size:14px;font-weight:600;fill:#dbeafe}}.micro{{font-family:Arial,sans-serif;font-size:10px;font-weight:800;fill:#fff;letter-spacing:.5px}}.connector{{fill:none;stroke:#67e8f9;stroke-width:4;marker-end:url(#arrow)}}.footer{{font-family:Arial,sans-serif;font-size:12px;font-weight:800;fill:#dbeafe;letter-spacing:.8px}}</style>
</defs>
<rect width='1200' height='900' fill='#081c30'/><rect width='1200' height='900' fill='url(#grid)'/>
<rect x='48' y='38' width='1104' height='164' rx='30' fill='url(#hero)' stroke='#38bdf8' stroke-width='2'/>
<text x='84' y='101' class='subtitle'>AICLOUDSTRATEGIST · OWNER EDUCATION</text>
<text x='84' y='157' class='title'>AWS BILL TOO HIGH?</text>
<text x='890' y='151' class='subtitle'>6-STEP PATH</text>
{connectors}{''.join(cards)}
<rect x='70' y='814' width='1060' height='52' rx='16' fill='#0b2138' stroke='#f59e0b' stroke-width='2'/>
<text x='600' y='846' text-anchor='middle' class='footer'>NO CREDENTIALS NEEDED · BUYER EDUCATION ONLY · NOT AN ACCOUNT AUDIT OR SAVINGS GUARANTEE</text>
</svg>"""
(pub / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
subprocess.run(["convert", "-background", "none", str(pub / f"{SLUG}.svg"), str(pub / f"{SLUG}.png")], check=True)

with (pub / f"{SLUG}.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["step", "owner_action", "safe_check"])
    writer.writerows(steps)

card = {
    "topic": TITLE,
    "date": DATE,
    "slot": SLOT,
    "url": URL,
    "infographic": PNG_URL,
    "worksheet": CSV_URL,
    "steps": [{"step": n, "owner_action": t, "safe_check": b} for n, t, b in steps],
    "boundary": BOUNDARY,
    "source_resource": "https://aicloudstrategist.com/resources/customer-problem-search/aws-cloud-bill-too-high/",
}
(pub / f"{SLUG}-answer-card.json").write_text(json.dumps(card, indent=2), encoding="utf-8")

rows = "".join(f"<tr><td>{n}</td><td><strong>{esc(t)}</strong></td><td>{esc(b)}</td></tr>" for n, t, b in steps)
faq = [
    ("What should I check first when an AWS bill is too high?", "Confirm the change against a comparable period, then identify the changed service or account and its owner."),
    ("Should I buy a commitment immediately?", "Not from an unexplained bill spike. Hold commitments until demand, ownership and forecast evidence are sufficient."),
    ("Does this require AWS credentials?", "No. It is a buyer-education and evidence-intake path, not an AWS account audit."),
]
faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
article_json = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": HOOK, "image": [PNG_URL, SVG_URL], "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "AICloudStrategist"}, "publisher": {"@type": "Organization", "name": "AICloudStrategist"}, "mainEntityOfPage": URL}
faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)
page = f"""<!doctype html><html lang='en-IN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta name='robots' content='index,follow,max-image-preview:large'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:url' content='{URL}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{json.dumps(article_json, separators=(',', ':'))}</script><script type='application/ld+json'>{json.dumps(faq_json, separators=(',', ':'))}</script>
<style>body{{margin:0;background:#f4f8fb;color:#10243a;font-family:Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#081c30,#123f63,#0f5265);color:#fff;border-radius:28px;padding:36px}}.eyebrow{{color:#bae6fd;text-transform:uppercase;font-weight:900;letter-spacing:.12em;font-size:12px}}h1{{font-size:clamp(36px,6vw,60px);line-height:1.02;margin:14px 0}}.lead{{font-size:20px;line-height:1.5}}.card{{background:#fff;border:1px solid #bad4e5;border-radius:22px;padding:24px;margin:22px 0;box-shadow:0 12px 32px rgba(8,28,48,.08)}}img{{width:100%;height:auto;border-radius:18px;border:1px solid #86b6d0}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #bad4e5;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#081c30;color:#e5f3ff}}a{{color:#075985;font-weight:800}}.button{{display:inline-block;background:#0f5265;color:#fff;padding:13px 18px;border-radius:10px;text-decoration:none}}</style></head>
<body><main><section class='hero'><p class='eyebrow'>Evening publication · cloud cost owner education</p><h1>{esc(TITLE)}</h1><p class='lead'>{esc(HOOK)}</p></section>
<section class='card'><img src='{SLUG}.png' alt='Infographic showing a six-step owner action path for investigating an unexpectedly high AWS bill'></section>
<section class='card'><h2>The six-step path</h2><table><thead><tr><th>Step</th><th>Owner action</th><th>Safe check</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the six-step worksheet CSV</a> · <a href='{SLUG}-answer-card.json'>Open the AI-readable answer card</a></p></section>
<section class='card'><h2>What not to do first</h2><ul><li>Do not delete resources from a screenshot or unexplained alert.</li><li>Do not buy Savings Plans or Reserved Instances before demand, owner and forecast evidence.</li><li>Do not paste credentials, billing exports, secrets or personal data into a public form.</li><li>Do not call a synthetic example a customer saving or ROI result.</li></ul></section>
<section class='card'><h2>Buyer FAQ</h2>{faq_html}</section><section class='card boundary'><strong>Proof boundary:</strong> {esc(BOUNDARY)}</section>
<section class='card'><h2>Need an evidence-led review?</h2><p>Use the source checklist or request a fit check for a bounded Cloud and AI Cost Governance Diagnostic.</p><p><a href='/resources/customer-problem-search/aws-cloud-bill-too-high/'>Read the source owner checklist</a> · <a class='button' href='/request-fit-review/'>Request a diagnostic fit check</a></p></section></main></body></html>"""
(pub / f"{SLUG}.html").write_text(page, encoding="utf-8")

post_md = f"# {TITLE}\n\n![{TITLE}]({PNG_URL})\n\n{HOOK}\n\n" + "\n".join(f"{n}. **{t}.** {b}" for n, t, b in steps) + f"\n\nWorksheet: {CSV_URL}\n\n**Proof boundary:** {BOUNDARY}\n\nPublic page: {URL}\n"
(pub / f"{SLUG}.md").write_text(post_md, encoding="utf-8")

manifest_path = pub / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"date": DATE, "posts": []}
manifest["posts"] = [item for item in manifest.get("posts", []) if item.get("slot") != SLOT and item.get("slug") != SLUG]
manifest["posts"].append({"slot": SLOT, "slug": SLUG, "title": TITLE, "url": URL, "png": PNG_URL, "svg": SVG_URL, "csv": CSV_URL, "answer_card": CARD_URL, "repository": REPO_URL, "boundary": BOUNDARY})
manifest["posts"].sort(key=lambda item: {"morning": 0, "evening": 1}.get(item["slot"], 9))
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
links = "".join(f"<li><strong>{esc(item['slot'].title())}:</strong> <a href='{esc(item['slug'])}.html'>{esc(item['title'])}</a> · <a href='{esc(item['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(item['csv'].split('/')[-1])}'>CSV</a></li>" for item in manifest["posts"])
(pub / "index.html").write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications — {DATE}</title><link rel='canonical' href='{BASE}/'><style>body{{font-family:Inter,Arial,sans-serif;background:#f4f8fb;color:#10243a}}main{{max-width:850px;margin:auto;padding:40px 18px}}section{{background:#fff;border:1px solid #bad4e5;border-radius:22px;padding:24px}}a{{color:#075985;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable worksheets.</p><ul>{links}</ul></section></main></body></html>", encoding="utf-8")
(pub / "publish-log.md").write_text(f"# Publish log — {DATE}\n\n## Published / verified\n- AICS website / GitHub Pages — Evening: {URL}\n- GitHub repository / deployment evidence — Evening: {REPO_URL}\n\n## Infographic\n- {PNG_URL}\n\n## Verification boundary\n{BOUNDARY}\n", encoding="utf-8")

mirror = Path("/home/agent/.hermes/aicloudstrategist/publications") / DATE
mirror.mkdir(parents=True, exist_ok=True)
shutil.copy2(pub / "publish-log.md", mirror / "publish-log.md")

# Add public discovery links without altering existing cards when already present.
resources = REPO / "resources" / "index.html"
if resources.exists():
    text = resources.read_text(encoding="utf-8")
    if URL not in text and f"/publications/{DATE}/{SLUG}.html" not in text:
        card_html = f"<article class='card' data-resource-card='{SLUG}'><h2><a href='/publications/{DATE}/{SLUG}.html'>{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href='/publications/{DATE}/{SLUG}.csv'>Download worksheet CSV</a></p></article>"
        text = text.replace("</main>", card_html + "</main>", 1)
        resources.write_text(text, encoding="utf-8")

llms = REPO / "llms.txt"
if llms.exists():
    text = llms.read_text(encoding="utf-8")
    for line in [f"- [{TITLE}]({URL}) — six-step no-credentials AWS bill owner action path.\n", f"- [AWS bill owner path worksheet]({CSV_URL}) — educational evidence and ownership checklist.\n"]:
        if line.split("](")[1].split(")")[0] not in text:
            text = text.rstrip() + "\n" + line
    llms.write_text(text, encoding="utf-8")

# The legacy sitemap builder can fail on retired routes; preserve the existing sitemap and append this verified publication deterministically.
subprocess.run(["python3", str(REPO / "scripts" / "build_sitemap.py")], cwd=REPO, check=False)
sitemap = REPO / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for link, priority in [(URL, "0.7"), (PNG_URL, "0.5"), (SVG_URL, "0.5"), (CSV_URL, "0.5"), (CARD_URL, "0.5"), (f"{BASE}/", "0.6")]:
    if link not in text:
        text = text.replace("</urlset>", f"  <url><loc>{link}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")

print(json.dumps({"slot": SLOT, "title": TITLE, "url": URL, "png": PNG_URL, "repository": REPO_URL}, indent=2))
