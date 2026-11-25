from pathlib import Path
import csv, html, json, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-25"
SLOT = "morning"
SLUG = "recurring-report-automation-handoff"
TITLE = "Still Building the Same Report by Hand? A 6-Step Automation Handoff"
HOOK = "A safe educational handoff for defining ownership, inputs, rules, review, fallback and release controls before automating a recurring business report."
BOUNDARY = "Educational workflow-design material only — not accounting, financial, legal, compliance, security, privacy or production advice. No client result, certification, ranking, saving or guarantee is claimed."
DOMAIN = "https://aicloudstrategist.com"
BASE = f"{DOMAIN}/publications/{DATE}"
URL = f"{BASE}/{SLUG}.html"
PNG_URL = f"{BASE}/{SLUG}.png"
SVG_URL = f"{BASE}/{SLUG}.svg"
CSV_URL = f"{BASE}/{SLUG}.csv"
CARD_URL = f"{BASE}/{SLUG}-answer-card.json"
REPO_URL = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/blob/main/publications/{DATE}/{SLUG}.html"
REPO_PNG = f"https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/blob/main/publications/{DATE}/{SLUG}.png"

steps = [
    ("1", "Name the decision", "Decision + owner", "Write the decision this report supports and the person who owns that decision."),
    ("2", "List the sources", "Approved source · Owner · Timing · Access path", "Record each approved source, its owner, update timing and access path."),
    ("3", "Define the rules", "Calculation · Filter · Grouping · Exceptions", "Write the calculation, filter, grouping and exception rules in plain language."),
    ("4", "Mark the checks", "Reviewer · Checks · Evidence", "Identify who reviews the output, what they check and what evidence is retained."),
    ("5", "Set the fallback", "Missing · Late · Duplicated · Inconsistent", "Define what happens when data is missing, late, duplicated or inconsistent."),
    ("6", "Choose the release gate", "Manual + Automated → Compare → Owner accepts", "Run the automated and manual versions together; release only after the authorized owner accepts the comparison."),
]
minimum = "Decision · Owners · Sources · Timing · Rules · Reviewer · Evidence · Fallback · Comparison · Release owner"


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width=24, max_lines=3):
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
colors = ["#A8D8EA", "#B5E5CF", "#D5C6E0", "#FFD5C2", "#A8D8EA", "#FFD5C2"]
icons = ["◆", "▤", "≡", "✓", "!", "▣"]
cards = []
for i, ((number, heading, labels, _body), color, icon) in enumerate(zip(steps, colors, icons)):
    x = 35 + i * 192
    heading_lines = wrap(heading.upper(), 20, 2)
    label_lines = wrap(labels, 19, 4)
    heading_svg = "".join(f"<tspan x='{x+18}' dy='{0 if j == 0 else 18}'>{esc(line)}</tspan>" for j, line in enumerate(heading_lines))
    label_svg = "".join(f"<tspan x='{x+18}' dy='{0 if j == 0 else 17}'>{esc(line)}</tspan>" for j, line in enumerate(label_lines))
    cards.append(f"""<g filter='url(#shadow)'>
      <rect x='{x}' y='184' width='170' height='260' rx='24' fill='{color}' stroke='#2D2D2D' stroke-width='3'/>
      <circle cx='{x+33}' cy='218' r='22' fill='#2D2D2D'/><text x='{x+33}' y='226' class='num'>{number}</text>
      <text x='{x+137}' y='226' class='icon' text-anchor='middle'>{icon}</text>
      <text x='{x+18}' y='274' class='heading'>{heading_svg}</text>
      <path d='M{x+17} 320 Q{x+85} 314 {x+153} 320' fill='none' stroke='#6B6B6B' stroke-width='2' stroke-dasharray='5 6'/>
      <text x='{x+18}' y='350' class='labels'>{label_svg}</text>
    </g>""")

arrows = []
for i in range(5):
    x = 207 + i * 192
    arrows.append(f"<path d='M{x} 310 q9 -11 18 0' fill='none' stroke='#E8655A' stroke-width='5' stroke-linecap='round'/><path d='M{x+13} 301 l10 9 -10 9' fill='none' stroke='#E8655A' stroke-width='4' stroke-linecap='round'/>")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='675' viewBox='0 0 1200 675'>
<defs><filter id='shadow' x='-15%' y='-15%' width='140%' height='150%'><feDropShadow dx='3' dy='5' stdDeviation='4' flood-color='#635b52' flood-opacity='.19'/></filter><style>.title{{font-family:Arial,sans-serif;font-size:38px;font-weight:900;fill:#2D2D2D}}.sub{{font-family:Arial,sans-serif;font-size:20px;font-weight:900;fill:#E8655A;letter-spacing:2px}}.deck{{font-family:Arial,sans-serif;font-size:15px;font-weight:700;fill:#5a554f}}.num{{font-family:Arial,sans-serif;font-size:22px;font-weight:900;fill:#fff;text-anchor:middle}}.icon{{font-family:Arial,sans-serif;font-size:24px;font-weight:900;fill:#2D2D2D}}.heading{{font-family:Arial,sans-serif;font-size:14px;font-weight:900;fill:#2D2D2D}}.labels{{font-family:Arial,sans-serif;font-size:12px;font-weight:800;fill:#3f3b36}}.strip-title{{font-family:Arial,sans-serif;font-size:14px;font-weight:900;fill:#2D2D2D}}.strip{{font-family:Arial,sans-serif;font-size:12px;font-weight:800;fill:#2D2D2D}}.footer{{font-family:Arial,sans-serif;font-size:9px;font-weight:800;fill:#fff}}</style></defs>
<rect width='1200' height='675' fill='#F5F0E8'/><path d='M40 60 Q280 31 530 55' stroke='#A8D8EA' stroke-width='13' fill='none' stroke-linecap='round' opacity='.76'/><path d='M930 42 q22 15 40 0 q-15 20 0 39 q-20 -12 -40 0 q12 -20 0 -39z' fill='#B5E5CF'/>
<text x='40' y='72' class='title'>STILL BUILDING THE SAME REPORT BY HAND?</text><text x='42' y='108' class='sub'>A 6-STEP AUTOMATION HANDOFF</text><text x='42' y='140' class='deck'>Define ownership, inputs, rules, review, fallback and release before automation.</text>
{''.join(cards)}{''.join(arrows)}
<g transform='translate(1060 126)'><circle cx='24' cy='18' r='12' fill='none' stroke='#2D2D2D' stroke-width='3'/><path d='M24 30 v40 M24 44 l-22 18 M24 44 l24 10 M24 70 l-18 28 M24 70 l22 26' fill='none' stroke='#2D2D2D' stroke-width='3' stroke-linecap='round'/><path d='M54 24 q22 -15 40 0 v42 q-18 -14 -40 0z' fill='#fff' stroke='#2D2D2D' stroke-width='2'/><path d='M62 36h24M62 46h19M62 56h22' stroke='#6B6B6B' stroke-width='2'/></g>
<rect x='35' y='474' width='1130' height='105' rx='22' fill='#fffaf3' stroke='#2D2D2D' stroke-width='3' stroke-dasharray='8 7'/><text x='58' y='507' class='strip-title'>MINIMUM HANDOFF RECORD</text><text x='58' y='541' class='strip'>{esc(minimum)}</text><text x='58' y='564' class='deck'>Run manual and automated versions together. Release only after the authorized owner accepts the comparison.</text>
<rect x='35' y='606' width='1130' height='34' rx='12' fill='#2D2D2D'/><text x='600' y='628' class='footer' text-anchor='middle'>EDUCATIONAL WORKFLOW-DESIGN MATERIAL ONLY · NO CLIENT RESULT, CERTIFICATION, RANKING, SAVING OR GUARANTEE IS CLAIMED</text>
</svg>"""
(pub / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
subprocess.run(["convert", "-background", "none", "-density", "144", str(pub / f"{SLUG}.svg"), "-resize", "1200x675", str(pub / f"{SLUG}.png")], check=True)
shutil.copy2(pub / f"{SLUG}.png", ROOT / "infographic" / "recurring-report-handoff" / "infographic.png")

with (pub / f"{SLUG}.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["step", "handoff_area", "record", "safe_instruction"])
    writer.writerows(steps)

answer = {
    "topic": TITLE, "date": DATE, "slot": SLOT, "url": URL, "infographic": PNG_URL,
    "worksheet": CSV_URL,
    "steps": [{"step": n, "handoff_area": h, "record": label, "safe_instruction": body} for n, h, label, body in steps],
    "minimum_handoff_record": minimum, "boundary": BOUNDARY,
}
(pub / f"{SLUG}-answer-card.json").write_text(json.dumps(answer, indent=2), encoding="utf-8")
rows = "".join(f"<tr><td>{n}</td><td><strong>{esc(h)}</strong></td><td>{esc(label)}</td><td>{esc(body)}</td></tr>" for n, h, label, body in steps)
faq = [
    ("What should be documented before automating a recurring report?", "Document the decision, decision owner, approved sources, rules, reviewer, retained evidence, fallback, comparison period and release owner."),
    ("How should the automated report be checked before release?", "Run the automated and manual versions together and let the authorized owner review the comparison."),
    ("Does this handoff authorize a production change?", "No. It is educational workflow-design material only; local policy and authorized owners control any production decision."),
]
faq_json = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
article_json = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": HOOK, "image": [PNG_URL, SVG_URL], "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "AICloudStrategist"}, "publisher": {"@type": "Organization", "name": "AICloudStrategist"}, "mainEntityOfPage": URL}
faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)
page = f"""<!doctype html><html lang='en-IN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta name='robots' content='index,follow,max-image-preview:large'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:url' content='{URL}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{json.dumps(article_json, separators=(',', ':'))}</script><script type='application/ld+json'>{json.dumps(faq_json, separators=(',', ':'))}</script><style>body{{margin:0;background:#F5F0E8;color:#2D2D2D;font-family:Inter,Segoe UI,Arial,sans-serif}}main{{max-width:1120px;margin:auto;padding:32px 18px}}.hero,.card{{background:#fffaf3;border:3px solid #2D2D2D;border-radius:26px;padding:30px;margin:24px 0;box-shadow:7px 7px 0 #A8D8EA}}.eyebrow{{color:#c9483e;text-transform:uppercase;font-weight:900;letter-spacing:.12em;font-size:12px}}h1{{font-size:clamp(34px,6vw,58px);line-height:1.03;margin:12px 0}}.lead{{font-size:20px;line-height:1.5}}img{{width:100%;height:auto;border-radius:18px;border:2px solid #2D2D2D}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #6B6B6B;padding:11px;text-align:left;vertical-align:top}}.boundary{{background:#2D2D2D;color:#fff;box-shadow:none}}a{{color:#075985;font-weight:800}}.button{{display:inline-block;background:#2D2D2D;color:#fff;padding:13px 18px;border-radius:10px;text-decoration:none}}</style></head><body><main><section class='hero'><p class='eyebrow'>Morning publication · workflow education</p><h1>{esc(TITLE)}</h1><p class='lead'>{esc(HOOK)}</p></section><section class='card'><img src='{PNG_URL}' alt='{esc(TITLE)}'><p><a class='button' href='{CSV_URL}'>Download the handoff worksheet (CSV)</a></p></section><section class='card'><h2>The six-step handoff</h2><table><thead><tr><th>Step</th><th>Area</th><th>Record</th><th>Safe instruction</th></tr></thead><tbody>{rows}</tbody></table></section><section class='card'><h2>Minimum handoff record</h2><p>{esc(minimum)}</p></section><section class='card'><h2>Questions buyers and operators ask</h2>{faq_html}</section><section class='card boundary'><h2>Proof boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub / f"{SLUG}.html").write_text(page, encoding="utf-8")
(pub / f"{SLUG}.md").write_text(f"# {TITLE}\n\n![{TITLE}]({PNG_URL})\n\n{HOOK}\n\n" + "\n".join(f"{n}. **{h}.** {body}" for n, h, _label, body in steps) + f"\n\nMinimum handoff record: {minimum}\n\nWorksheet: {CSV_URL}\n\n**Proof boundary:** {BOUNDARY}\n\nPublic page: {URL}\n", encoding="utf-8")
manifest = {"date": DATE, "posts": [{"slot": SLOT, "title": TITLE, "slug": SLUG, "url": URL, "visual": PNG_URL, "worksheet": CSV_URL, "answer_card": CARD_URL, "boundary": BOUNDARY}]}
(pub / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
(pub / "index.html").write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications — {DATE}</title><link rel='canonical' href='{BASE}/'></head><body><main><h1>AICS publications — {DATE}</h1><ul><li><strong>Morning:</strong> <a href='{SLUG}.html'>{esc(TITLE)}</a> · <a href='{SLUG}.png'>infographic</a> · <a href='{SLUG}.csv'>worksheet</a></li></ul></main></body></html>", encoding="utf-8")
(pub / "publish-log.md").write_text(f"# Publish log — {DATE}\n\n## Published / verified\n- GitHub repository evidence — Morning: {REPO_URL}\n\n## Infographic\n- Morning: {REPO_PNG}\n\n## Verification boundary\n- {BOUNDARY}\n", encoding="utf-8")

mirror_root = Path("/home/agent/.hermes/aicloudstrategist/publications")
mirror = mirror_root / DATE
mirror.mkdir(parents=True, exist_ok=True)
shutil.copy2(pub / "publish-log.md", mirror / "publish-log.md")
status = {"date": DATE, "timezone": "Asia/Kolkata", "successful_posts_today": 1, "target_posts_today": 2, "morning": "published", "evening": "not yet due", "successful_portals": 1, "links": [REPO_URL]}
(mirror_root / f"daily-publication-status-{DATE}.json").write_text(json.dumps(status, indent=2), encoding="utf-8")

resources = ROOT / "resources" / "index.html"
text = resources.read_text(encoding="utf-8")
if f"/publications/{DATE}/{SLUG}.html" not in text:
    card = f"<section class='section'><div class='wrap'><span class='badge'>New workflow aid · 25 Nov 2026</span><h2>{esc(TITLE)}</h2><article class='card' data-resource-card='{SLUG}'><p>{esc(HOOK)}</p><p><a href='/publications/{DATE}/{SLUG}.html'>Open the six-step handoff →</a> · <a href='/publications/{DATE}/{SLUG}.csv'>Download worksheet CSV</a></p><p><small>{esc(BOUNDARY)}</small></p></article></div></section>"
    anchor = "<footer class=\"footer\">"
    if anchor not in text:
        raise RuntimeError("resources footer anchor not found")
    text = text.replace(anchor, card + anchor, 1)
    resources.write_text(text, encoding="utf-8")
llms = ROOT / "llms.txt"
text = llms.read_text(encoding="utf-8")
if URL not in text:
    llms.write_text(text.rstrip() + f"\n- [{TITLE}]({URL}) — six-step educational recurring-report automation handoff with worksheet.\n", encoding="utf-8")
sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
for link, priority in [(URL, "0.7"), (PNG_URL, "0.5"), (SVG_URL, "0.5"), (CSV_URL, "0.5"), (CARD_URL, "0.5"), (f"{BASE}/", "0.6")]:
    if link not in text:
        text = text.replace("</urlset>", f"  <url><loc>{link}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>\n</urlset>")
sitemap.write_text(text, encoding="utf-8")
print(json.dumps(status, indent=2))
