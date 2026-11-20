from pathlib import Path
import csv, html, json, shutil, subprocess

REPO = Path(__file__).resolve().parents[1]
DATE = "2026-11-20"
SLOT = "morning"
SLUG = "manual-work-automation-readiness-map"
TITLE = "Too Much Manual Work? A 5-Check Automation Readiness Map"
HOOK = "A safe educational map to define a workflow, expose handoffs, separate rules from exceptions and choose an evidence-matched next move."
BOUNDARY = "Educational workflow review only — not a client case study, productivity guarantee, security assessment, legal or compliance advice, vendor recommendation or production-change instruction."
BASE = f"https://support-aicloudstrategist.github.io/publications/{DATE}"
URL = f"{BASE}/{SLUG}.html"
PNG_URL = f"{BASE}/{SLUG}.png"
SVG_URL = f"{BASE}/{SLUG}.svg"
CSV_URL = f"{BASE}/{SLUG}.csv"
CARD_URL = f"{BASE}/{SLUG}-answer-card.json"
REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}"

checks = [
    ("1", "Name the workflow", "Write one clear start event, one end result and the person who owns the outcome.", "START · END · OWNER"),
    ("2", "Map the handoffs", "Mark every system, person, queue and approval the work passes through.", "SYSTEM · PERSON · QUEUE · APPROVAL"),
    ("3", "Check repeatability", "Separate stable rules from judgment calls, rare cases and missing information.", "STABLE RULES · JUDGMENT · RARE CASES · MISSING INFO"),
    ("4", "Protect the exceptions", "Define when automation must stop, ask for review or return work to a human owner.", "STOP · REVIEW · HUMAN OWNER"),
    ("5", "Choose the next move", "AUTOMATE when rules and evidence are clear; SIMPLIFY when the process has avoidable steps; OBSERVE when the pattern is still unclear.", "AUTOMATE · SIMPLIFY · OBSERVE"),
]
EVIDENCE = "workflow owner · trigger · inputs · decision rules · exceptions · expected output · review point · rollback path"


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width, max_lines):
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:max_lines]


pub = REPO / "publications" / DATE
pub.mkdir(parents=True, exist_ok=True)
positions = [(64, 224, 330, 208), (435, 224, 330, 208), (806, 224, 330, 208), (64, 466, 516, 218), (620, 466, 516, 218)]
colors = ["#a8d8ea", "#ffd5c2", "#b5e5cf", "#d5c6e0", "#f7df9c"]
cards = []
for (number, heading, body, labels), (x, y, w, h), color in zip(checks, positions, colors):
    body_lines = wrap(body, 38 if w < 400 else 60, 4)
    label_lines = wrap(labels, 28 if w < 400 else 54, 2)
    body_svg = "".join(f"<tspan x='{x+26}' dy='{0 if i == 0 else 22}'>{esc(line)}</tspan>" for i, line in enumerate(body_lines))
    label_svg = "".join(f"<tspan x='{x+26}' dy='{0 if i == 0 else 18}'>{esc(line)}</tspan>" for i, line in enumerate(label_lines))
    cards.append(f"""<g filter='url(#shadow)'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='25' fill='{color}' stroke='#2d2d2d' stroke-width='3'/><circle cx='{x+40}' cy='{y+41}' r='25' fill='#2d2d2d'/><text x='{x+40}' y='{y+50}' class='num'>{number}</text><path d='M{x+w-66} {y+28} q20 -14 39 0 q-19 14 -39 0z' fill='none' stroke='#2d2d2d' stroke-width='3'/><circle cx='{x+w-56}' cy='{y+28}' r='3' fill='#e8655a'/><circle cx='{x+w-39}' cy='{y+28}' r='3' fill='#e8655a'/><text x='{x+76}' y='{y+48}' class='heading'>{esc(heading.upper())}</text><text x='{x+26}' y='{y+91}' class='body'>{body_svg}</text><path d='M{x+24} {y+h-58} Q{x+w/2} {y+h-65} {x+w-24} {y+h-58}' fill='none' stroke='#6b6b6b' stroke-width='2' stroke-dasharray='6 7'/><text x='{x+26}' y='{y+h-35}' class='labels'>{label_svg}</text></g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
<defs><filter id='shadow' x='-15%' y='-15%' width='140%' height='145%'><feDropShadow dx='3' dy='7' stdDeviation='6' flood-color='#5b5146' flood-opacity='.2'/></filter><style>.title{{font-family:Arial,sans-serif;font-size:49px;font-weight:900;fill:#2d2d2d}}.sub{{font-family:Arial,sans-serif;font-size:21px;font-weight:900;fill:#e8655a;letter-spacing:2px}}.deck{{font-family:Arial,sans-serif;font-size:17px;font-weight:600;fill:#555}}.num{{font-family:Arial,sans-serif;font-size:25px;font-weight:900;fill:#fff}}.heading{{font-family:Arial,sans-serif;font-size:18px;font-weight:900;fill:#2d2d2d}}.body{{font-family:Arial,sans-serif;font-size:15px;font-weight:600;fill:#2d2d2d}}.labels{{font-family:Arial,sans-serif;font-size:12px;font-weight:900;fill:#544d47;letter-spacing:.7px}}.evidence{{font-family:Arial,sans-serif;font-size:14px;font-weight:800;fill:#2d2d2d}}.footer{{font-family:Arial,sans-serif;font-size:11px;font-weight:800;fill:#fff;letter-spacing:.65px}}</style></defs>
<rect width='1200' height='900' fill='#f5f0e8'/><path d='M56 76 Q340 48 690 74' fill='none' stroke='#a8d8ea' stroke-width='13' stroke-linecap='round' opacity='.65'/><text x='64' y='105' class='title'>TOO MUCH MANUAL WORK?</text><text x='66' y='145' class='sub'>A 5-CHECK AUTOMATION READINESS MAP</text><text x='66' y='181' class='deck'>Use this educational map before automating a repetitive business workflow.</text>
<g fill='#e8655a'><path d='M1125 77l8 18 19 3-14 13 3 19-16-9-17 9 4-19-15-13 20-3z'/></g>
{''.join(cards)}
<path d='M395 328 q18 -15 36 0' fill='none' stroke='#6b6b6b' stroke-width='3' stroke-dasharray='6 7'/><path d='M766 328 q18 -15 36 0' fill='none' stroke='#6b6b6b' stroke-width='3' stroke-dasharray='6 7'/><path d='M580 575 q18 -15 36 0' fill='none' stroke='#6b6b6b' stroke-width='3' stroke-dasharray='6 7'/>
<rect x='64' y='724' width='1072' height='88' rx='24' fill='#fffaf2' stroke='#2d2d2d' stroke-width='3' stroke-dasharray='9 8'/><text x='90' y='757' class='heading'>MINIMUM EVIDENCE TO RECORD</text><text x='90' y='787' class='evidence'>{esc(EVIDENCE)}</text>
<rect x='64' y='832' width='1072' height='38' rx='14' fill='#2d2d2d'/><text x='600' y='856' text-anchor='middle' class='footer'>EDUCATIONAL WORKFLOW REVIEW · NOT A PRODUCTIVITY GUARANTEE OR PRODUCTION-CHANGE INSTRUCTION</text>
</svg>"""
(pub / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
subprocess.run(["convert", "-background", "none", str(pub / f"{SLUG}.svg"), str(pub / f"{SLUG}.png")], check=True)
info = REPO / "infographic" / "manual-work-readiness"
shutil.copy2(pub / f"{SLUG}.png", info / "infographic.png")

with (pub / f"{SLUG}.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["check", "review_area", "safe_question", "labels"])
    writer.writerows(checks)

card = {"topic": TITLE, "date": DATE, "slot": SLOT, "url": URL, "infographic": PNG_URL, "worksheet": CSV_URL, "checks": [{"check": n, "review_area": h, "safe_question": b, "labels": l} for n, h, b, l in checks], "minimum_evidence": EVIDENCE, "boundary": BOUNDARY}
(pub / f"{SLUG}-answer-card.json").write_text(json.dumps(card, indent=2), encoding="utf-8")

rows = "".join(f"<tr><td>{n}</td><td><strong>{esc(h)}</strong></td><td>{esc(b)}</td><td>{esc(l)}</td></tr>" for n, h, b, l in checks)
article_json = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": HOOK, "image": [PNG_URL, SVG_URL], "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "AICloudStrategist"}, "publisher": {"@type": "Organization", "name": "AICloudStrategist"}, "mainEntityOfPage": URL}
faq = [("What should be mapped before automating manual work?", "Record the workflow owner, trigger, inputs, decision rules, exceptions, expected output, review point and rollback path."), ("When should a workflow be observed instead of automated?", "Observe when the pattern, ownership, decision rules or exceptions are still unclear."), ("Does this map guarantee a productivity result?", "No. It is an educational workflow review, not a productivity guarantee or production-change instruction.")]
faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)
page = f"""<!doctype html><html lang='en-IN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta name='robots' content='index,follow,max-image-preview:large'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:url' content='{URL}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{json.dumps(article_json, separators=(',', ':'))}</script><script type='application/ld+json'>{json.dumps(faq_json, separators=(',', ':'))}</script><style>body{{margin:0;background:#f5f0e8;color:#2d2d2d;font-family:Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:#fffaf2;border:3px solid #2d2d2d;border-radius:28px;padding:34px;box-shadow:8px 8px 0 #a8d8ea}}.eyebrow{{color:#c4473e;text-transform:uppercase;font-weight:900;letter-spacing:.12em;font-size:12px}}h1{{font-size:clamp(36px,6vw,60px);line-height:1.02;margin:14px 0}}.lead{{font-size:20px;line-height:1.5}}.card{{background:#fffaf2;border:2px solid #2d2d2d;border-radius:22px;padding:24px;margin:24px 0}}img{{width:100%;height:auto;border-radius:18px;border:2px solid #2d2d2d}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #6b6b6b;padding:11px;text-align:left;vertical-align:top}}.boundary{{background:#2d2d2d;color:#fff}}a{{color:#075985;font-weight:800}}.button{{display:inline-block;background:#2d2d2d;color:#fff;padding:13px 18px;border-radius:10px;text-decoration:none}}</style></head><body><main><section class='hero'><p class='eyebrow'>Morning publication · workflow automation education</p><h1>{esc(TITLE)}</h1><p class='lead'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic showing five checks for assessing whether repetitive manual work is ready for automation'></section><section class='card'><h2>The five-check map</h2><table><thead><tr><th>Check</th><th>Review area</th><th>Safe question</th><th>Labels</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the worksheet CSV</a> · <a href='{SLUG}-answer-card.json'>Open the AI-readable answer card</a></p></section><section class='card'><h2>Minimum evidence to record</h2><p>{esc(EVIDENCE)}</p></section><section class='card'><h2>Buyer FAQ</h2>{faq_html}</section><section class='card boundary'><strong>Proof boundary:</strong> {esc(BOUNDARY)}</section><section class='card'><h2>Need a bounded workflow review?</h2><p>Use the worksheet to prepare an evidence-led fit discussion without sharing credentials or secrets.</p><p><a class='button' href='/request-fit-review/'>Request a fit check</a></p></section></main></body></html>"""
(pub / f"{SLUG}.html").write_text(page, encoding="utf-8")
(pub / f"{SLUG}.md").write_text(f"# {TITLE}\n\n![{TITLE}]({PNG_URL})\n\n{HOOK}\n\n" + "\n".join(f"{n}. **{h}.** {b}" for n, h, b, _ in checks) + f"\n\nMinimum evidence: {EVIDENCE}\n\nWorksheet: {CSV_URL}\n\n**Proof boundary:** {BOUNDARY}\n\nPublic page: {URL}\n", encoding="utf-8")
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

resources = REPO / "resources" / "index.html"
if resources.exists():
    text = resources.read_text(encoding="utf-8")
    if f"/publications/{DATE}/{SLUG}.html" not in text:
        text = text.replace("</main>", f"<article class='card' data-resource-card='{SLUG}'><h2><a href='/publications/{DATE}/{SLUG}.html'>{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href='/publications/{DATE}/{SLUG}.csv'>Download worksheet CSV</a></p></article></main>", 1)
        resources.write_text(text, encoding="utf-8")
llms = REPO / "llms.txt"
if llms.exists():
    text = llms.read_text(encoding="utf-8")
    line = f"- [{TITLE}]({URL}) — five-check educational automation readiness map with worksheet.\n"
    if URL not in text:
        llms.write_text(text.rstrip() + "\n" + line, encoding="utf-8")
sitemap = REPO / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for link, priority in [(URL, "0.7"), (PNG_URL, "0.5"), (SVG_URL, "0.5"), (CSV_URL, "0.5"), (CARD_URL, "0.5"), (f"{BASE}/", "0.6")]:
    if link not in text:
        text = text.replace("</urlset>", f"  <url><loc>{link}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")
print(json.dumps(status, indent=2))
