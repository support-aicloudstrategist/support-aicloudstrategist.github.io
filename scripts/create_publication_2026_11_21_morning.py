from pathlib import Path
import csv, html, json, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-21"
SLOT = "morning"
SLUG = "ai-tool-pilot-brief"
TITLE = "Before You Buy an AI Tool: A 6-Box Pilot Brief"
HOOK = "A safe educational brief to define a small, reviewable pilot before choosing an AI tool."
BOUNDARY = "Educational pilot-planning material only — not a client case study, performance guarantee, security assessment, legal or compliance advice, procurement recommendation or production-change instruction."
BASE = f"https://support-aicloudstrategist.github.io/publications/{DATE}"
URL = f"{BASE}/{SLUG}.html"
PNG_URL = f"{BASE}/{SLUG}.png"
SVG_URL = f"{BASE}/{SLUG}.svg"
CSV_URL = f"{BASE}/{SLUG}.csv"
CARD_URL = f"{BASE}/{SLUG}-answer-card.json"
REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}"

boxes = [
    ("1", "Business task", "Name one task, its current owner, the trigger that starts it and the output that marks it complete.", "TASK · OWNER · TRIGGER · OUTPUT"),
    ("2", "Evidence baseline", "Record current time, error, rework or queue evidence using a consistent method. If no baseline exists, observe first.", "TIME · ERROR · REWORK · QUEUE · OBSERVE FIRST"),
    ("3", "Data boundary", "List the data the pilot may use, the data it must not use and the approved storage or access path.", "ALLOWED · RESTRICTED · APPROVED PATH"),
    ("4", "Human control", "Identify who reviews outputs, what requires approval and when the workflow must stop or return to a person.", "REVIEW · APPROVAL · STOP · RETURN TO PERSON"),
    ("5", "Pilot measure", "Choose one observable process measure and one quality check. Define how both will be recorded.", "PROCESS MEASURE · QUALITY CHECK · RECORD BOTH"),
    ("6", "Exit decision", "At the review date, choose: proceed, revise or stop. Record the evidence and owner for the next decision.", "PROCEED · REVISE · STOP · EVIDENCE + OWNER"),
]
EVIDENCE = "task · owner · trigger · baseline · allowed data · restricted data · reviewer · stop condition · process measure · quality check · review date · exit decision"


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width, max_lines):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if current and len(trial) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines[:max_lines]


pub = ROOT / "publications" / DATE
pub.mkdir(parents=True, exist_ok=True)
positions = [(48, 160), (432, 160), (816, 160), (48, 350), (432, 350), (816, 350)]
colors = ["#a8d8ea", "#ffd5c2", "#b5e5cf", "#d5c6e0", "#f7df9c", "#f3b6c6"]
cards = []
for (number, heading, body, labels), (x, y), color in zip(boxes, positions, colors):
    body_lines = wrap(body, 43, 4)
    label_lines = wrap(labels, 39, 2)
    body_svg = "".join(f"<tspan x='{x+22}' dy='{0 if i == 0 else 18}'>{esc(line)}</tspan>" for i, line in enumerate(body_lines))
    label_svg = "".join(f"<tspan x='{x+22}' dy='{0 if i == 0 else 15}'>{esc(line)}</tspan>" for i, line in enumerate(label_lines))
    cards.append(f"<g filter='url(#shadow)'><rect x='{x}' y='{y}' width='336' height='164' rx='22' fill='{color}' stroke='#2d2d2d' stroke-width='3'/><circle cx='{x+35}' cy='{y+34}' r='21' fill='#2d2d2d'/><text x='{x+35}' y='{y+42}' class='num'>{number}</text><text x='{x+67}' y='{y+40}' class='heading'>{esc(heading.upper())}</text><path d='M{x+292} {y+25} q12 -10 24 0 q-12 10 -24 0z' fill='none' stroke='#2d2d2d' stroke-width='2'/><text x='{x+22}' y='{y+75}' class='body'>{body_svg}</text><path d='M{x+20} {y+125} Q{x+168} {y+119} {x+316} {y+125}' fill='none' stroke='#5b5146' stroke-width='1.5' stroke-dasharray='5 6'/><text x='{x+22}' y='{y+145}' class='labels'>{label_svg}</text></g>")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='675' viewBox='0 0 1200 675'>
<defs><filter id='shadow' x='-12%' y='-12%' width='135%' height='145%'><feDropShadow dx='3' dy='5' stdDeviation='4' flood-color='#5b5146' flood-opacity='.20'/></filter><style>.title{{font-family:Arial,sans-serif;font-size:43px;font-weight:900;fill:#2d2d2d}}.sub{{font-family:Arial,sans-serif;font-size:20px;font-weight:900;fill:#d8544a;letter-spacing:2px}}.deck{{font-family:Arial,sans-serif;font-size:16px;font-weight:600;fill:#555}}.num{{font-family:Arial,sans-serif;font-size:20px;font-weight:900;fill:white;text-anchor:middle}}.heading{{font-family:Arial,sans-serif;font-size:17px;font-weight:900;fill:#2d2d2d}}.body{{font-family:Arial,sans-serif;font-size:13px;font-weight:600;fill:#2d2d2d}}.labels{{font-family:Arial,sans-serif;font-size:10px;font-weight:900;fill:#514a44;letter-spacing:.5px}}.strip{{font-family:Arial,sans-serif;font-size:11px;font-weight:800;fill:#2d2d2d}}.footer{{font-family:Arial,sans-serif;font-size:8.7px;font-weight:800;fill:white;letter-spacing:.25px}}</style></defs>
<rect width='1200' height='675' fill='#fff8f0'/><path d='M44 58 Q320 31 680 55' fill='none' stroke='#a8d8ea' stroke-width='12' stroke-linecap='round' opacity='.72'/><text x='48' y='72' class='title'>BEFORE YOU BUY AN AI TOOL</text><text x='50' y='105' class='sub'>A 6-BOX PILOT BRIEF</text><text x='50' y='133' class='deck'>Define a small, reviewable pilot before choosing an AI tool.</text><path d='M1110 55l8 17 18 3-13 12 3 18-16-8-16 8 3-18-13-12 18-3z' fill='#e8655a'/>
{''.join(cards)}
<rect x='48' y='535' width='1104' height='69' rx='19' fill='#fffdf8' stroke='#2d2d2d' stroke-width='3' stroke-dasharray='8 7'/><text x='70' y='560' class='heading'>MINIMUM PILOT RECORD</text><text x='70' y='583' class='strip'>{esc(EVIDENCE)}</text>
<rect x='48' y='622' width='1104' height='32' rx='12' fill='#2d2d2d'/><text x='600' y='642' class='footer' text-anchor='middle'>EDUCATIONAL PILOT-PLANNING MATERIAL · NOT A PERFORMANCE GUARANTEE, SECURITY ASSESSMENT, LEGAL OR COMPLIANCE ADVICE, PROCUREMENT RECOMMENDATION OR PRODUCTION-CHANGE INSTRUCTION</text>
</svg>"""
(pub / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
subprocess.run(["convert", "-background", "none", "-density", "144", str(pub / f"{SLUG}.svg"), "-resize", "1200x675", str(pub / f"{SLUG}.png")], check=True)
shutil.copy2(pub / f"{SLUG}.png", ROOT / "infographic" / "ai-tool-pilot-brief" / "infographic.png")

with (pub / f"{SLUG}.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["box", "review_area", "safe_instruction", "labels"])
    writer.writerows(boxes)

answer = {"topic": TITLE, "date": DATE, "slot": SLOT, "url": URL, "infographic": PNG_URL, "worksheet": CSV_URL, "boxes": [{"box": n, "review_area": h, "safe_instruction": b, "labels": l} for n, h, b, l in boxes], "minimum_pilot_record": EVIDENCE, "boundary": BOUNDARY}
(pub / f"{SLUG}-answer-card.json").write_text(json.dumps(answer, indent=2), encoding="utf-8")
rows = "".join(f"<tr><td>{n}</td><td><strong>{esc(h)}</strong></td><td>{esc(b)}</td><td>{esc(l)}</td></tr>" for n, h, b, l in boxes)
article_json = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": HOOK, "image": [PNG_URL, SVG_URL], "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "AICloudStrategist"}, "publisher": {"@type": "Organization", "name": "AICloudStrategist"}, "mainEntityOfPage": URL}
faq = [("What should be defined before an AI-tool pilot?", "Define the business task, evidence baseline, data boundary, human control, pilot measure and exit decision."), ("What if no baseline exists?", "Observe first and record current evidence using a consistent method."), ("Does this brief recommend a particular AI tool?", "No. It is educational pilot-planning material, not a procurement recommendation or performance guarantee.")]
faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)
page = f"""<!doctype html><html lang='en-IN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta name='robots' content='index,follow,max-image-preview:large'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:url' content='{URL}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{json.dumps(article_json, separators=(',', ':'))}</script><script type='application/ld+json'>{json.dumps(faq_json, separators=(',', ':'))}</script><style>body{{margin:0;background:#fff8f0;color:#2d2d2d;font-family:Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1120px;margin:auto;padding:32px 18px}}.hero,.card{{background:#fffdf8;border:3px solid #2d2d2d;border-radius:26px;padding:30px;margin:24px 0;box-shadow:7px 7px 0 #a8d8ea}}.eyebrow{{color:#c4473e;text-transform:uppercase;font-weight:900;letter-spacing:.12em;font-size:12px}}h1{{font-size:clamp(34px,6vw,58px);line-height:1.02;margin:12px 0}}.lead{{font-size:20px;line-height:1.5}}img{{width:100%;height:auto;border-radius:18px;border:2px solid #2d2d2d}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #6b6b6b;padding:11px;text-align:left;vertical-align:top}}.boundary{{background:#2d2d2d;color:#fff;box-shadow:none}}a{{color:#075985;font-weight:800}}.button{{display:inline-block;background:#2d2d2d;color:#fff;padding:13px 18px;border-radius:10px;text-decoration:none}}</style></head><body><main><section class='hero'><p class='eyebrow'>Morning publication · AI buyer education</p><h1>{esc(TITLE)}</h1><p class='lead'>{esc(HOOK)}</p></section><section class='card'><img src='{PNG_URL}' alt='{esc(TITLE)} infographic' width='1200' height='675'></section><section class='card'><h2>Six-box pilot brief</h2><table><thead><tr><th>Box</th><th>Area</th><th>Safe instruction</th><th>Record</th></tr></thead><tbody>{rows}</tbody></table><p><strong>Minimum pilot record:</strong> {esc(EVIDENCE)}</p><p><a class='button' href='{CSV_URL}'>Download the worksheet CSV</a></p></section><section class='card'><h2>Quick answers</h2>{faq_html}</section><section class='card boundary'><h2>Proof boundary</h2><p>{esc(BOUNDARY)}</p></section><p><a href='{REPO_URL}'>Repository and deployment evidence</a> · <a href='{CARD_URL}'>Machine-readable answer card</a> · <a href='{SVG_URL}'>Accessible SVG</a></p></main></body></html>"""
(pub / f"{SLUG}.html").write_text(page, encoding="utf-8")
(pub / f"{SLUG}.md").write_text(f"# {TITLE}\n\n![{TITLE}]({PNG_URL})\n\n{HOOK}\n\n" + "\n".join(f"{n}. **{h}.** {b}" for n, h, b, _ in boxes) + f"\n\nMinimum pilot record: {EVIDENCE}\n\nWorksheet: {CSV_URL}\n\n**Proof boundary:** {BOUNDARY}\n\nPublic page: {URL}\n", encoding="utf-8")
manifest = {"date": DATE, "posts": [{"slot": SLOT, "slug": SLUG, "title": TITLE, "url": URL, "png": PNG_URL, "svg": SVG_URL, "csv": CSV_URL, "answer_card": CARD_URL, "repository": REPO_URL, "boundary": BOUNDARY}]}
(pub / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
(pub / "index.html").write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications — {DATE}</title><link rel='canonical' href='{BASE}/'></head><body><main><h1>AICS publications — {DATE}</h1><ul><li><strong>Morning:</strong> <a href='{SLUG}.html'>{esc(TITLE)}</a> · <a href='{SLUG}.png'>infographic</a> · <a href='{SLUG}.csv'>CSV</a></li></ul></main></body></html>", encoding="utf-8")
(pub / "publish-log.md").write_text(f"# Publish log — {DATE}\n\n## Published / verified\n- AICS website / GitHub Pages — Morning: {URL}\n- GitHub repository / deployment evidence — Morning: {REPO_URL}\n\n## Infographic\n- {PNG_URL}\n\n## Verification boundary\n{BOUNDARY}\n", encoding="utf-8")

mirror_root = Path("/home/agent/.hermes/aicloudstrategist/publications")
mirror = mirror_root / DATE
mirror.mkdir(parents=True, exist_ok=True)
shutil.copy2(pub / "publish-log.md", mirror / "publish-log.md")
status = {"date": DATE, "timezone": "Asia/Kolkata", "target_posts": 2, "successful_posts": 1, "morning": {"status": "published", "topic": TITLE, "successful_portals": [{"name": "AICS website / GitHub Pages", "url": URL}, {"name": "GitHub repository / deployment evidence", "url": REPO_URL}]}, "evening": {"status": "not yet due", "successful_portals": []}, "successful_portal_count": 2}
(mirror_root / f"daily-publication-status-{DATE}.json").write_text(json.dumps(status, indent=2), encoding="utf-8")

resources = ROOT / "resources" / "index.html"
text = resources.read_text(encoding="utf-8")
if f"/publications/{DATE}/{SLUG}.html" not in text:
    text = text.replace("</main>", f"<article class='card' data-resource-card='{SLUG}'><h2><a href='/publications/{DATE}/{SLUG}.html'>{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href='/publications/{DATE}/{SLUG}.csv'>Download worksheet CSV</a></p></article></main>", 1)
    resources.write_text(text, encoding="utf-8")
llms = ROOT / "llms.txt"
text = llms.read_text(encoding="utf-8")
if URL not in text:
    llms.write_text(text.rstrip() + f"\n- [{TITLE}]({URL}) — six-box educational AI-tool pilot brief with worksheet.\n", encoding="utf-8")
sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for link, priority in [(URL, "0.7"), (PNG_URL, "0.5"), (SVG_URL, "0.5"), (CSV_URL, "0.5"), (CARD_URL, "0.5"), (f"{BASE}/", "0.6")]:
    if link not in text:
        text = text.replace("</urlset>", f"  <url><loc>{link}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")
print(json.dumps(status, indent=2))
