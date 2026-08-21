from pathlib import Path
import html, json, subprocess

DATE = "2026-08-21"
SLOT = "evening"
SLUG = "ai-reply-approval-ladder"
TITLE = "AI Reply Approval Ladder: 5 checks before a bot answers a customer"
HOOK = "A safe educational ladder for owners to decide which customer messages can be automated, which need review, and which must stay human-only."
BOUNDARY = "Educational workflow only — no legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice."
BASE = Path("/home/agent/.hermes/aicloudstrategist")
REPO = BASE / "repos" / "support-aicloudstrategist.github.io"
PUB_ROOT = BASE / "publications" / DATE
PUB = PUB_ROOT / SLUG
WEB = REPO / "publications" / DATE
INFO = REPO / "infographic" / SLUG
EVIDENCE = REPO / "docs" / "publication-evidence"
for p in (PUB, WEB, INFO / "prompts", EVIDENCE):
    p.mkdir(parents=True, exist_ok=True)

checks = [
    ("Routine facts", "Only automate answers that repeat approved, low-risk business facts."),
    ("Customer context", "Check whether the message includes personal, sensitive, urgent, or unusual context."),
    ("Promise control", "Do not let automation promise price, timing, availability, diagnosis, refund, or results."),
    ("Human review", "Route uncertain, emotional, legal, medical, payment, credential, or complaint items to a person."),
    ("Audit trail", "Keep the source message, generated reply, owner, decision, and timestamp visible."),
]

source = f"""Topic: AI Reply Approval Ladder for customer-message automation.
Audience: founders, support managers, clinic/admin teams, agencies, SaaS teams, and local service operators considering AI-assisted first replies.
Safe boundaries: {BOUNDARY}
Core checks: {', '.join(x[0] for x in checks)}.
"""
analysis = f"""# Analysis — AI Reply Approval Ladder

- Topic: Owner-led approval ladder before AI replies to customers.
- Data type: Educational operating-control checklist.
- Complexity: Low-to-medium; built for non-technical owners and managers.
- Tone: Practical, safe, plain-English, control-first.
- Audience: Teams using forms, inboxes, chat, CRM, helpdesk, WhatsApp, or AI assistants.
- Language: English.
- Design: hierarchical-layers layout + technical-schematic style, landscape 16:9, infographic-style SVG and PNG.
- Truth boundary: {BOUNDARY}
"""
structured = "# Structured content — AI Reply Approval Ladder\n\n"
structured += f"## Title\n{TITLE}\n\n## Learning objectives\n- Help owners separate safe routine replies from messages needing review.\n- Help teams control promises, escalation, and audit evidence before automation answers customers.\n- Keep the guidance educational and claim-safe.\n\n## Sections\n"
for i, (name, detail) in enumerate(checks, 1):
    structured += f"\n### {i}. {name}\nContent: {detail}\nVisual element: Ladder rung with review gate.\nText labels: {name}; approval gate.\n"
structured += f"\n## Data points\n- No statistics used.\n- No customer examples used.\n- No performance claims used.\n\n## Boundary label\n{BOUNDARY}\n"
prompt = f"""Create a professional infographic following these specifications:

## Image Specifications
- Type: Infographic
- Layout: hierarchical-layers
- Style: technical-schematic
- Aspect Ratio: 16:9
- Language: English

## Layout Guidelines
Layered ladder structure with five ascending approval gates, clear title, concise rung labels, visual hierarchy, and a bottom truth-boundary band.

## Style Guidelines
Technical schematic style with blueprint grid, precise line art, clean sans-serif typography, navy background, cyan/green/orange accents, labeled arrows, and operational-control feel.

## Content
Title: {TITLE}
Hook: {HOOK}
Ladder gates: {', '.join(x[0] for x in checks)}.
Boundary: {BOUNDARY}
"""
(INFO / "source.md").write_text(source, encoding="utf-8")
(INFO / "analysis.md").write_text(analysis, encoding="utf-8")
(INFO / "structured-content.md").write_text(structured, encoding="utf-8")
(INFO / "prompts" / "infographic.md").write_text(prompt, encoding="utf-8")
(PUB / "source.md").write_text(source, encoding="utf-8")
(PUB / "analysis.md").write_text(analysis, encoding="utf-8")
(PUB / "structured-content.md").write_text(structured, encoding="utf-8")
(PUB / "infographic-prompt.md").write_text(prompt, encoding="utf-8")

colors = {"navy":"#0b1220","panel":"#111c2e","cyan":"#38bdf8","green":"#22c55e","orange":"#fb923c","yellow":"#facc15","text":"#e5f0ff","muted":"#a8bdd8","grid":"#24405f"}
rungs = []
ys = [600, 500, 400, 300, 200]
for i, ((name, detail), y) in enumerate(zip(checks, ys), 1):
    accent = [colors['green'], colors['cyan'], colors['yellow'], colors['orange'], '#a78bfa'][i-1]
    words = detail.split()
    line1 = ' '.join(words[:8])
    line2 = ' '.join(words[8:16])
    rungs.append(f"""<g transform='translate(130 {y})'>
<rect x='{(i-1)*70}' y='0' width='{930-(i-1)*105}' height='72' rx='18' fill='{colors['panel']}' stroke='{accent}' stroke-width='3'/>
<circle cx='{38+(i-1)*70}' cy='36' r='24' fill='{accent}'/><text x='{38+(i-1)*70}' y='45' text-anchor='middle' font-size='24' font-weight='900' fill='{colors['navy']}'>{i}</text>
<text x='{84+(i-1)*70}' y='30' font-size='26' font-weight='900' fill='{colors['text']}'>{html.escape(name)}</text>
<text x='{84+(i-1)*70}' y='57' font-size='17' fill='{colors['muted']}'>{html.escape(line1)} {html.escape(line2)}</text>
<text x='{1045}' y='44' font-size='18' font-weight='800' fill='{accent}'>APPROVAL GATE</text>
</g>""")
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1600' height='900' viewBox='0 0 1600 900' role='img' aria-labelledby='title desc'>
<title id='title'>{html.escape(TITLE)}</title><desc id='desc'>Five AI reply approval checks: routine facts, customer context, promise control, human review, and audit trail.</desc>
<defs><pattern id='grid' width='40' height='40' patternUnits='userSpaceOnUse'><path d='M40 0H0V40' fill='none' stroke='{colors['grid']}' stroke-width='1' opacity='.45'/></pattern></defs>
<rect width='1600' height='900' fill='{colors['navy']}'/><rect width='1600' height='900' fill='url(#grid)'/>
<circle cx='1410' cy='120' r='118' fill='{colors['cyan']}' opacity='.12'/><circle cx='126' cy='780' r='160' fill='{colors['green']}' opacity='.10'/>
<text x='92' y='88' font-family='Inter,Arial,sans-serif' font-size='27' font-weight='900' fill='{colors['cyan']}'>AICloudStrategist • safe educational workflow</text>
<text x='92' y='150' font-family='Inter,Arial,sans-serif' font-size='52' font-weight='900' fill='{colors['text']}'>AI Reply Approval Ladder</text>
<text x='92' y='194' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='650' fill='{colors['muted']}'>5 checks before a bot answers a customer</text>
<path d='M210 664 L460 262 L1115 262 L1290 664' fill='none' stroke='{colors['cyan']}' stroke-width='5' opacity='.48'/>
<g font-family='Inter,Arial,sans-serif'>{''.join(rungs)}</g>
<rect x='92' y='760' width='1416' height='78' rx='20' fill='#08111f' stroke='{colors['grid']}'/>
<text x='124' y='806' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='900' fill='{colors['yellow']}'>Truth boundary:</text>
<text x='318' y='806' font-family='Inter,Arial,sans-serif' font-size='19' fill='{colors['text']}'>Educational workflow only — no legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.</text>
<text x='92' y='868' font-family='Inter,Arial,sans-serif' font-size='17' fill='{colors['muted']}'>support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html</text>
</svg>"""
for root in (PUB, WEB):
    (root / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
    subprocess.run(["convert", str(root / f"{SLUG}.svg"), str(root / f"{SLUG}.png")], check=True)

checks_html = ''.join(f"<li><strong>{html.escape(name)}:</strong> {html.escape(detail)}</li>" for name, detail in checks)
checks_md = '\n'.join(f"- **{name}:** {detail}" for name, detail in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png'>
<meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#07111f;color:#e5f0ff;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0b1220,#164e63);color:white;border-radius:30px;padding:36px;border:1px solid #24405f}}.kicker{{color:#67e8f9;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45;color:#dbeafe}}.card{{background:#0f1b2d;border:1px solid #24405f;border-radius:24px;padding:24px;margin-top:22px;box-shadow:0 16px 44px #0005}}img{{max-width:100%;border-radius:22px;border:1px solid #24405f}}li{{margin:11px 0;line-height:1.45}}.note{{color:#b6c9e4;font-size:14px}}</style></head>
<body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · AI reply operations</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: AI Reply Approval Ladder with five checks'></section><section class='card'><h2>Practical checklist</h2><ul>{checks_html}</ul><p>Use this ladder before giving an AI assistant permission to answer customers. The safer path is to automate routine, approved facts and pause anything uncertain for a human owner.</p><p class='note'>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(WEB / f"{SLUG}.html").write_text(page, encoding="utf-8")
(PUB / f"{SLUG}.html").write_text(page, encoding="utf-8")
post = f"# {TITLE}\n\n{HOOK}\n\n{checks_md}\n\nUse this ladder before giving an AI assistant permission to answer customers. The safer path is to automate routine, approved facts and pause anything uncertain for a human owner.\n\nTruth boundary: {BOUNDARY}\n"
(PUB / "post.md").write_text(post, encoding="utf-8")
devto = f"![Infographic: {TITLE}](https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png)\n\n{HOOK}\n\n## Five approval checks\n\n{checks_md}\n\n## How to use it\n\nUse this ladder before giving an AI assistant permission to answer customers. The safer path is to automate routine, approved facts and pause anything uncertain for a human owner.\n\n**Truth boundary:** {BOUNDARY}\n\nInfographic and public checklist: https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html\n"
(PUB / "devto.md").write_text(devto, encoding="utf-8")

# Keep day manifest with exactly today's two scheduled slots once evening is added.
manifest_path = PUB_ROOT / "manifest.json"
manifest = []
if manifest_path.exists():
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        manifest = []
manifest = [m for m in manifest if not (m.get("slot") == SLOT or m.get("slug") == SLUG)]
manifest.append({"slot": SLOT, "slug": SLUG, "title": TITLE, "url": f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html", "png": f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png", "boundary": BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get("slot") == "morning" else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

index_links = ''.join(f"<li><a href='{html.escape(m['slug'])}.html'>{html.escape(m['slot'].title())}: {html.escape(m['title'])}</a></li>" for m in manifest)
index = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:28px;box-shadow:0 14px 36px #15203312}}li{{margin:14px 0}}</style></head><body><main><section><p><strong>AICloudStrategist daily publications</strong></p><h1>Two safe educational posts with infographics — {DATE}</h1><ul>{index_links}</ul><p>LinkedIn excluded. Educational only; no client/result/legal/compliance/performance claims.</p></section></main></body></html>"""
(WEB / "index.html").write_text(index, encoding="utf-8")

log = PUB_ROOT / "publish-log.md"
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n""" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + f"\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}\n" for m in manifest) + "\n## Verification\n- Pending HTTP verification after deployment.\n", encoding="utf-8")
(EVIDENCE / f"{DATE}-{SLOT}-{SLUG}.md").write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Repository/deployment evidence: this file and `/publications/{DATE}/` assets.\n\nVerification markers:\n- Page title: `{TITLE}`\n- Visual marker: `AI Reply Approval Ladder`\n- Boundary marker: `{BOUNDARY}`\n""", encoding="utf-8")

# Sitemap entry for GitHub Pages publication URL.
sitemap = REPO / "sitemap.xml"
if sitemap.exists():
    text = sitemap.read_text(encoding="utf-8")
    url = f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html"
    entry = f"  <url><loc>{url}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n"
    if url not in text and "</urlset>" in text:
        sitemap.write_text(text.replace("</urlset>", entry + "</urlset>"), encoding="utf-8")
print(json.dumps(manifest, indent=2))
