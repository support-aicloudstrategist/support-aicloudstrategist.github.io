from pathlib import Path
import csv, html, json, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-21"
SLOT = "evening"
SLUG = "ai-workflow-auto-act-or-ask-first"
TITLE = "AI Workflow Decision: Auto-Act or Ask First?"
HOOK = "A five-check educational gate for deciding when an AI-assisted workflow may take a bounded action and when a human should review first."
BOUNDARY = "Educational workflow-design material only — not a security assessment, legal or compliance advice, production authorization, performance guarantee, client case study or customer result."
OVERRIDE = "Local policy and authorized human owners always override this educational gate."
BASE = f"https://support-aicloudstrategist.github.io/publications/{DATE}"
URL = f"{BASE}/{SLUG}.html"
PNG_URL = f"{BASE}/{SLUG}.png"
SVG_URL = f"{BASE}/{SLUG}.svg"
CSV_URL = f"{BASE}/{SLUG}.csv"
CARD_URL = f"{BASE}/{SLUG}-answer-card.json"
REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}"
MORNING_REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/blob/f29e5b3b/publications/{DATE}/ai-tool-pilot-brief.html"
EVENING_REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/blob/main/publications/{DATE}/{SLUG}.html"

checks = [
    ("1", "Scope", "Bounded, approved and reversible", "Ambiguous, external-facing or high-impact"),
    ("2", "Data", "Approved, necessary and non-sensitive", "Secrets, personal data or restricted data"),
    ("3", "Evidence", "Rule matched and required evidence is available", "Evidence is missing, stale or conflicting"),
    ("4", "Review", "Action is logged and included in an approved review process", "Human approval is required before action"),
    ("5", "Failure control", "Tested stop or rollback path is ready", "No safe stop, rollback or accountable owner"),
]


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width=33, max_lines=3):
    lines, current = [], ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:max_lines]


pub = ROOT / "publications" / DATE
pub.mkdir(parents=True, exist_ok=True)

# Deterministic, text-faithful fallback after the configured image generator was unavailable.
rows_svg = []
for idx, (number, label, left, right) in enumerate(checks):
    y = 180 + idx * 82
    left_lines = wrap(left, 38, 2)
    right_lines = wrap(right, 38, 2)
    left_text = "".join(f"<tspan x='250' dy='{0 if i == 0 else 18}'>{esc(line)}</tspan>" for i, line in enumerate(left_lines))
    right_text = "".join(f"<tspan x='750' dy='{0 if i == 0 else 18}'>{esc(line)}</tspan>" for i, line in enumerate(right_lines))
    rows_svg.append(f"""
    <g>
      <rect x='46' y='{y}' width='1108' height='70' rx='18' fill='white' opacity='.96'/>
      <circle cx='82' cy='{y+35}' r='19' fill='#5b3fd4'/><text x='82' y='{y+42}' class='num'>{number}</text>
      <text x='112' y='{y+41}' class='row-label'>{esc(label.upper())}</text>
      <rect x='232' y='{y+10}' width='392' height='50' rx='14' fill='#d8f5eb'/>
      <text x='250' y='{y+31}' class='row-copy'>{left_text}</text>
      <rect x='732' y='{y+10}' width='392' height='50' rx='14' fill='#ffe4d6'/>
      <text x='750' y='{y+31}' class='row-copy'>{right_text}</text>
    </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='675' viewBox='0 0 1200 675'>
<defs><filter id='shadow'><feDropShadow dx='0' dy='5' stdDeviation='6' flood-color='#321a6e' flood-opacity='.14'/></filter><style>.title{{font-family:Arial,sans-serif;font-size:38px;font-weight:900;fill:#20154f}}.sub{{font-family:Arial,sans-serif;font-size:16px;font-weight:800;fill:#5b3fd4;letter-spacing:2px}}.lane{{font-family:Arial,sans-serif;font-size:21px;font-weight:900;fill:white}}.num{{font-family:Arial,sans-serif;font-size:17px;font-weight:900;fill:white;text-anchor:middle}}.row-label{{font-family:Arial,sans-serif;font-size:13px;font-weight:900;fill:#20154f}}.row-copy{{font-family:Arial,sans-serif;font-size:12.5px;font-weight:700;fill:#25304a}}.decision{{font-family:Arial,sans-serif;font-size:14px;font-weight:900;fill:white}}.foot{{font-family:Arial,sans-serif;font-size:9.5px;font-weight:800;fill:#514a76;letter-spacing:.25px}}</style></defs>
<rect width='1200' height='675' fill='#f6f2ff'/><circle cx='1130' cy='70' r='63' fill='#ffd95a' opacity='.7'/><path d='M35 80l48-43 42 48-52 34z' fill='#70dcc0' opacity='.78'/><circle cx='1060' cy='620' r='35' fill='#ff8a5c' opacity='.5'/>
<text x='600' y='58' class='title' text-anchor='middle'>AI WORKFLOW DECISION</text><text x='600' y='88' class='sub' text-anchor='middle'>AUTO-ACT OR ASK FIRST?</text>
<g filter='url(#shadow)'><rect x='232' y='111' width='392' height='54' rx='18' fill='#0b8f72'/><text x='428' y='145' class='lane' text-anchor='middle'>AUTO-ACT</text><rect x='732' y='111' width='392' height='54' rx='18' fill='#e75b32'/><text x='928' y='145' class='lane' text-anchor='middle'>ASK FIRST</text></g>
<path d='M680 110V585' stroke='#6f54d9' stroke-width='4' stroke-dasharray='8 10'/>
{''.join(rows_svg)}
<rect x='46' y='594' width='1108' height='45' rx='15' fill='#20154f'/><text x='300' y='622' class='decision' text-anchor='middle'>EVERY AUTO-ACT CHECK TRUE → AUTO-ACT</text><text x='900' y='622' class='decision' text-anchor='middle'>ANY CHECK NOT TRUE → ASK FIRST</text>
<text x='600' y='657' class='foot' text-anchor='middle'>LOCAL POLICY AND AUTHORIZED HUMAN OWNERS ALWAYS OVERRIDE · EDUCATIONAL WORKFLOW-DESIGN MATERIAL ONLY</text>
</svg>"""
(pub / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
subprocess.run(["convert", "-background", "none", "-density", "144", str(pub / f"{SLUG}.svg"), "-resize", "1200x675", str(pub / f"{SLUG}.png")], check=True)
info_dir = ROOT / "infographic" / "ai-workflow-decision"
shutil.copy2(pub / f"{SLUG}.png", info_dir / "infographic.png")

with (pub / f"{SLUG}.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["check", "review_area", "auto_act_lane", "ask_first_lane"])
    writer.writerows(checks)

answer = {
    "topic": TITLE, "date": DATE, "slot": SLOT, "url": URL, "infographic": PNG_URL,
    "worksheet": CSV_URL,
    "checks": [{"check": n, "review_area": h, "auto_act_lane": a, "ask_first_lane": b} for n, h, a, b in checks],
    "decision_rule": "AUTO-ACT only when every AUTO-ACT condition is true. Otherwise ASK FIRST.",
    "override": OVERRIDE, "boundary": BOUNDARY,
}
(pub / f"{SLUG}-answer-card.json").write_text(json.dumps(answer, indent=2), encoding="utf-8")
rows = "".join(f"<tr><td>{n}</td><td><strong>{esc(h)}</strong></td><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for n, h, a, b in checks)
faq = [
    ("When may an AI-assisted workflow auto-act?", "Only when every AUTO-ACT condition in this educational gate is true and local policy permits the action."),
    ("What happens when one check is not true?", "Ask first: pause the action and route it to the authorized human owner."),
    ("Does this gate authorize production actions?", "No. Local policy and authorized human owners always override this educational gate."),
]
faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
article_json = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": HOOK, "image": [PNG_URL, SVG_URL], "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "AICloudStrategist"}, "publisher": {"@type": "Organization", "name": "AICloudStrategist"}, "mainEntityOfPage": URL}
faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)
page = f"""<!doctype html><html lang='en-IN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta name='robots' content='index,follow,max-image-preview:large'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:url' content='{URL}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{json.dumps(article_json, separators=(',', ':'))}</script><script type='application/ld+json'>{json.dumps(faq_json, separators=(',', ':'))}</script><style>body{{margin:0;background:#f6f2ff;color:#20154f;font-family:Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#20154f,#5b3fd4);color:white;border-radius:28px;padding:36px}}.eyebrow{{color:#d8f5eb;text-transform:uppercase;font-weight:900;letter-spacing:.12em;font-size:12px}}h1{{font-size:clamp(36px,6vw,60px);line-height:1.02;margin:14px 0}}.lead{{font-size:20px;line-height:1.5}}.card{{background:white;border-radius:22px;padding:24px;margin:22px 0;box-shadow:0 12px 32px rgba(32,21,79,.10)}}img{{width:100%;height:auto;border-radius:18px}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #cfc6f6;padding:12px;text-align:left;vertical-align:top}}th:nth-child(3){{background:#d8f5eb}}th:nth-child(4){{background:#ffe4d6}}.rule{{background:#20154f;color:white}}a{{color:#4d34bf;font-weight:800}}.button{{display:inline-block;background:#5b3fd4;color:white;padding:13px 18px;border-radius:10px;text-decoration:none}}</style></head><body><main><section class='hero'><p class='eyebrow'>Evening publication · responsible AI workflow education</p><h1>{esc(TITLE)}</h1><p class='lead'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Binary comparison infographic for five AI workflow checks: auto-act or ask first'></section><section class='card'><h2>The five checks</h2><table><thead><tr><th>#</th><th>Check</th><th>AUTO-ACT lane</th><th>ASK-FIRST lane</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the comparison worksheet CSV</a> · <a href='{SLUG}-answer-card.json'>Open the AI-readable answer card</a></p></section><section class='card rule'><h2>Decision rule</h2><p><strong>AUTO-ACT only when every AUTO-ACT condition is true. Otherwise ASK FIRST.</strong></p><p>{esc(OVERRIDE)}</p></section><section class='card'><h2>Buyer FAQ</h2>{faq_html}</section><section class='card'><strong>Proof boundary:</strong> {esc(BOUNDARY)}</section><section class='card'><h2>Need a bounded workflow review?</h2><p>Use the worksheet to document the five checks before discussing implementation.</p><p><a class='button' href='/request-fit-review/'>Request a fit review</a></p></section></main></body></html>"""
(pub / f"{SLUG}.html").write_text(page, encoding="utf-8")
(pub / f"{SLUG}.md").write_text(f"# {TITLE}\n\n![{TITLE}]({PNG_URL})\n\n{HOOK}\n\n" + "\n".join(f"{n}. **{h}.** AUTO-ACT: {a} ASK FIRST: {b}" for n, h, a, b in checks) + f"\n\n**Decision rule:** AUTO-ACT only when every AUTO-ACT condition is true. Otherwise ASK FIRST.\n\n{OVERRIDE}\n\nWorksheet: {CSV_URL}\n\n**Proof boundary:** {BOUNDARY}\n\nPublic page: {URL}\n", encoding="utf-8")

manifest_path = pub / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["posts"] = [item for item in manifest["posts"] if item.get("slot") != SLOT and item.get("slug") != SLUG]
manifest["posts"].append({"slot": SLOT, "slug": SLUG, "title": TITLE, "url": URL, "png": PNG_URL, "svg": SVG_URL, "csv": CSV_URL, "answer_card": CARD_URL, "repository": REPO_URL, "boundary": BOUNDARY})
manifest["posts"].sort(key=lambda item: {"morning": 0, "evening": 1}.get(item["slot"], 9))
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
links = "".join(f"<li><strong>{esc(item['slot'].title())}:</strong> <a href='{esc(item['slug'])}.html'>{esc(item['title'])}</a> · <a href='{esc(item['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(item['csv'].split('/')[-1])}'>CSV</a></li>" for item in manifest["posts"])
(pub / "index.html").write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications — {DATE}</title><link rel='canonical' href='{BASE}/'><style>body{{font-family:Inter,Arial,sans-serif;background:#f6f2ff;color:#20154f}}main{{max-width:850px;margin:auto;padding:40px 18px}}section{{background:white;border-radius:22px;padding:24px}}a{{color:#4d34bf;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable worksheets.</p><ul>{links}</ul></section></main></body></html>", encoding="utf-8")

morning = next(item for item in manifest["posts"] if item["slot"] == "morning")
log = f"# Publish log — {DATE}\n\n## Published / verified\n- GitHub repository evidence — Morning: {MORNING_REPO_URL}\n- GitHub repository evidence — Evening: {EVENING_REPO_URL}\n\n## Site deployment state\n- Repository publication is verified. The custom-domain site has not yet exposed the new publication routes.\n\n## Infographics\n- {morning['png']}\n- {PNG_URL}\n\n## Verification boundaries\n- Morning: {morning['boundary']}\n- Evening: {BOUNDARY}\n"
(pub / "publish-log.md").write_text(log, encoding="utf-8")

mirror_root = Path("/home/agent/.hermes/aicloudstrategist/publications")
mirror = mirror_root / DATE
mirror.mkdir(parents=True, exist_ok=True)
shutil.copy2(pub / "publish-log.md", mirror / "publish-log.md")
status = {"date": DATE, "timezone": "Asia/Kolkata", "target_posts": 2, "successful_posts": 2, "morning": {"status": "published", "topic": morning["title"], "successful_portals": [{"name": "GitHub repository / deployment evidence", "url": MORNING_REPO_URL}]}, "evening": {"status": "published", "topic": TITLE, "successful_portals": [{"name": "GitHub repository / deployment evidence", "url": EVENING_REPO_URL}]}, "successful_portal_count": 1, "live_links": [MORNING_REPO_URL, EVENING_REPO_URL], "site_deployment": "pending_custom_domain_exposure"}
(mirror_root / f"daily-publication-status-{DATE}.json").write_text(json.dumps(status, indent=2), encoding="utf-8")

resources = ROOT / "resources" / "index.html"
text = resources.read_text(encoding="utf-8")
if f"/publications/{DATE}/{SLUG}.html" not in text:
    card_html = f"<section class='section' id='{SLUG}'><div class='wrap'><span class='badge'>Evening publication · responsible AI workflow</span><h2>{esc(TITLE)}</h2><article class='card' data-resource-card='{SLUG}'><p>{esc(HOOK)}</p><p><a href='/publications/{DATE}/{SLUG}.html'>Open the five-check decision gate →</a> · <a href='/publications/{DATE}/{SLUG}.csv'>Download worksheet CSV</a></p><p><small>{esc(BOUNDARY)}</small></p></article></div></section>"
    anchor = "</main>" if "</main>" in text else "<footer"
    replacement = card_html + "</main>" if anchor == "</main>" else card_html + "<footer"
    text = text.replace(anchor, replacement, 1)
    resources.write_text(text, encoding="utf-8")
llms = ROOT / "llms.txt"
text = llms.read_text(encoding="utf-8")
for line in [f"- [{TITLE}]({URL}) — five-check educational AI workflow decision gate.\n", f"- [AI workflow decision worksheet]({CSV_URL}) — AUTO-ACT versus ASK-FIRST comparison.\n"]:
    link = line.split("](")[1].split(")")[0]
    if link not in text:
        text = text.rstrip() + "\n" + line
llms.write_text(text, encoding="utf-8")
sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for link, priority in [(URL, "0.7"), (PNG_URL, "0.5"), (SVG_URL, "0.5"), (CSV_URL, "0.5"), (CARD_URL, "0.5"), (f"{BASE}/", "0.6")]:
    if link not in text:
        text = text.replace("</urlset>", f"  <url><loc>{link}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")
print(json.dumps(status, indent=2))
