from pathlib import Path
import html, json, subprocess

DATE = "2026-08-22"
SLOT = "morning"
SLUG = "automation-exception-queue-map"
TITLE = "Automation Exception Queue Map: 7 labels before a human hands work to AI"
HOOK = "A safe educational map for teams to separate routine work from owner-review items before automated follow-up creates confusion."
BOUNDARY = "Educational workflow only — no legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice."
BASE = Path("/home/agent/.hermes/aicloudstrategist")
REPO = BASE / "repos" / "support-aicloudstrategist.github.io"
PUB = BASE / "publications" / DATE / SLUG
WEB = REPO / "publications" / DATE
INFO = REPO / "infographic" / SLUG
EVIDENCE = REPO / "docs" / "publication-evidence"
for p in (PUB, WEB, INFO / "prompts", EVIDENCE):
    p.mkdir(parents=True, exist_ok=True)

labels = [
    ("Routine", "Approved facts, simple status updates, and low-risk reminders that match current team rules."),
    ("Needs owner", "Pricing, refunds, contracts, promises, unusual requests, or anything the team has not approved."),
    ("Sensitive", "Personal data, health, finance, identity, credentials, OTPs, access, or private documents."),
    ("Missing context", "The request cannot be answered safely because source, record, timestamp, or owner note is missing."),
    ("Customer upset", "Complaint, escalation, urgent tone, repeated follow-up, or a promise that may already be late."),
    ("Evidence saved", "Conversation link, source system, status, owner, next step, and timestamp are recorded."),
    ("Human reply", "A named person reviews the exception before any external answer or customer commitment."),
]

source = f"""Topic: Automation Exception Queue Map for safe AI-assisted operations.
Audience: owners, support teams, clinic admins, agencies, local-service teams, SaaS teams, and operations managers considering AI-assisted follow-up.
Safe boundaries: {BOUNDARY}
Core labels: {', '.join(x[0] for x in labels)}.
"""
analysis = f"""# Analysis — Automation Exception Queue Map

- Topic: Morning operating map for classifying automation exceptions before AI-assisted follow-up.
- Data type: Educational checklist and routing framework.
- Complexity: Low-to-medium; practical for non-technical owners and managers.
- Tone: Calm, operational, plain-English, safety-first.
- Audience: Teams using forms, inboxes, CRMs, WhatsApp, service desks, or AI assistants.
- Language: English.
- Design: hub-spoke layout + technical-schematic style, landscape 16:9, infographic-style SVG and PNG.
- Truth boundary: {BOUNDARY}
"""
structured = "# Structured content — Automation Exception Queue Map\n\n"
structured += f"## Title\n{TITLE}\n\n## Learning objectives\n- Help teams classify routine work and exceptions before AI-assisted follow-up.\n- Keep sensitive, missing-context, upset-customer, and owner-review items visible.\n- Keep the guidance educational and claim-safe.\n\n## Sections\n"
for i, (name, detail) in enumerate(labels, 1):
    structured += f"\n### {i}. {name}\nContent: {detail}\nVisual element: Labeled queue node connected to a central review hub.\nText labels: {name}; exception label.\n"
structured += f"\n## Data points\n- No statistics used.\n- No customer examples used.\n- No performance claims used.\n\n## Boundary label\n{BOUNDARY}\n"
prompt = f"""Create a professional infographic following these specifications:

## Image Specifications
- Type: Infographic
- Layout: hub-spoke
- Style: technical-schematic
- Aspect Ratio: 16:9
- Language: English

## Layout Guidelines
Hub-spoke operating map with one central review hub and seven connected exception labels. Use clear routing arrows, compact labels, and a safety boundary footer.

## Style Guidelines
Technical schematic style with blueprint-like grid, clean lines, precise typography, navy background, cyan and amber accents, structured labels, and professional operations tone.

## Content
Title: {TITLE}
Hook: {HOOK}
Labels: {', '.join(x[0] for x in labels)}.
Boundary: {BOUNDARY}
"""
(INFO / "source.md").write_text(source, encoding="utf-8")
(INFO / "analysis.md").write_text(analysis, encoding="utf-8")
(INFO / "structured-content.md").write_text(structured, encoding="utf-8")
(INFO / "prompts" / "infographic.md").write_text(prompt, encoding="utf-8")
PUB.mkdir(parents=True, exist_ok=True)
(PUB / "source.md").write_text(source, encoding="utf-8")
(PUB / "analysis.md").write_text(analysis, encoding="utf-8")
(PUB / "structured-content.md").write_text(structured, encoding="utf-8")
(PUB / "infographic-prompt.md").write_text(prompt, encoding="utf-8")

colors = {"bg":"#081626","panel":"#0f2540","cyan":"#36d1dc","amber":"#ffd166","green":"#4ade80","purple":"#a78bfa","red":"#fb7185","line":"#5eead455","text":"#e7f5ff","muted":"#a8c3d8"}
positions = [(156,248),(432,202),(708,202),(984,248),(984,542),(708,628),(432,628)]
accents = [colors['green'], colors['amber'], colors['red'], colors['purple'], '#f97316', colors['cyan'], '#93c5fd']
nodes = []
for i, ((name, detail), (x, y), accent) in enumerate(zip(labels, positions, accents), 1):
    words = detail.split()
    line1 = ' '.join(words[:7])
    line2 = ' '.join(words[7:14])
    line3 = ' '.join(words[14:21])
    nodes.append(f"""<g transform='translate({x} {y})'>
<line x1='0' y1='72' x2='{600-x}' y2='{420-y}' stroke='{colors['line']}' stroke-width='3' stroke-dasharray='8 8'/>
<rect x='-124' y='-6' width='248' height='168' rx='22' fill='{colors['panel']}' stroke='{accent}' stroke-width='2'/>
<circle cx='-88' cy='34' r='22' fill='{accent}'/><text x='-88' y='43' text-anchor='middle' font-size='22' font-weight='900' fill='#081626'>{i}</text>
<text x='-52' y='31' font-size='22' font-weight='900' fill='{colors['text']}'>{html.escape(name)}</text>
<rect x='-52' y='48' width='126' height='22' rx='11' fill='{accent}' opacity='.18'/><text x='-40' y='64' font-size='12' font-weight='800' fill='{colors['text']}'>QUEUE LABEL</text>
<text x='-96' y='102' font-size='15' fill='{colors['muted']}'>{html.escape(line1)}</text>
<text x='-96' y='124' font-size='15' fill='{colors['muted']}'>{html.escape(line2)}</text>
<text x='-96' y='146' font-size='15' fill='{colors['muted']}'>{html.escape(line3)}</text>
</g>""")
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900' role='img' aria-labelledby='title desc'>
<title id='title'>{html.escape(TITLE)}</title><desc id='desc'>Seven exception queue labels before human-to-AI handoff: routine, needs owner, sensitive, missing context, customer upset, evidence saved, and human reply.</desc>
<defs><pattern id='grid' width='36' height='36' patternUnits='userSpaceOnUse'><path d='M36 0H0V36' fill='none' stroke='#173b63' stroke-width='1'/></pattern><filter id='glow'><feGaussianBlur stdDeviation='4' result='b'/><feMerge><feMergeNode in='b'/><feMergeNode in='SourceGraphic'/></feMerge></filter></defs>
<rect width='1200' height='900' fill='{colors['bg']}'/><rect width='1200' height='900' fill='url(#grid)' opacity='.8'/>
<circle cx='600' cy='420' r='118' fill='#0f2540' stroke='{colors['cyan']}' stroke-width='4' filter='url(#glow)'/>
<circle cx='600' cy='420' r='82' fill='#0b1c30' stroke='{colors['amber']}' stroke-width='2'/>
<text x='600' y='394' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='900' fill='{colors['text']}'>HUMAN</text>
<text x='600' y='426' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='900' fill='{colors['text']}'>REVIEW HUB</text>
<text x='600' y='460' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='16' fill='{colors['muted']}'>route before AI follows up</text>
<text x='66' y='84' font-family='Inter,Arial,sans-serif' font-size='28' font-weight='900' fill='{colors['cyan']}'>AICloudStrategist • safe educational workflow</text>
<text x='66' y='142' font-family='Inter,Arial,sans-serif' font-size='43' font-weight='900' fill='{colors['text']}'>Automation Exception Queue Map</text>
<text x='66' y='188' font-family='Inter,Arial,sans-serif' font-size='22' fill='{colors['muted']}'>7 labels before a human hands work to AI</text>
<g font-family='Inter,Arial,sans-serif'>{''.join(nodes)}</g>
<rect x='66' y='780' width='1068' height='76' rx='22' fill='#0b1c30' stroke='#173b63'/>
<text x='96' y='824' font-family='Inter,Arial,sans-serif' font-size='20' font-weight='900' fill='{colors['amber']}'>Truth boundary:</text>
<text x='264' y='824' font-family='Inter,Arial,sans-serif' font-size='18' fill='{colors['text']}'>Educational workflow only — no legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.</text>
<text x='66' y='882' font-family='Inter,Arial,sans-serif' font-size='16' fill='{colors['muted']}'>support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html</text>
</svg>"""
for root in (PUB, WEB):
    (root / f"{SLUG}.svg").write_text(svg, encoding="utf-8")
    subprocess.run(["convert", str(root / f"{SLUG}.svg"), str(root / f"{SLUG}.png")], check=True)

labels_html = ''.join(f"<li><strong>{html.escape(name)}:</strong> {html.escape(detail)}</li>" for name, detail in labels)
labels_md = '\n'.join(f"- **{name}:** {detail}" for name, detail in labels)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png'>
<meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#081626;color:#e7f5ff;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f2540,#064e3b);border:1px solid #173b63;border-radius:30px;padding:36px}}.kicker{{color:#5eead4;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45;color:#dbeafe}}.card{{background:#0f2540;border:1px solid #173b63;border-radius:24px;padding:24px;margin-top:22px;box-shadow:0 16px 44px #0005}}img{{max-width:100%;border-radius:22px;border:1px solid #173b63}}li{{margin:11px 0;line-height:1.45}}.note{{color:#a8c3d8;font-size:14px}}</style></head>
<body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · Safe automation operations</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: Automation Exception Queue Map with seven labels'></section><section class='card'><h2>Practical labels</h2><ul>{labels_html}</ul><p>Use this map before allowing AI-assisted tools to draft or send follow-up. The safer path is to identify exceptions first, save evidence, and route uncertain items to a named human owner.</p><p class='note'>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
for root in (PUB, WEB):
    (root / f"{SLUG}.html").write_text(page, encoding="utf-8")
post = f"# {TITLE}\n\n{HOOK}\n\n{labels_md}\n\nUse this map before allowing AI-assisted tools to draft or send follow-up. The safer path is to identify exceptions first, save evidence, and route uncertain items to a named human owner.\n\nTruth boundary: {BOUNDARY}\n"
(PUB / "post.md").write_text(post, encoding="utf-8")
devto = f"![Infographic: {TITLE}](https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png)\n\n{HOOK}\n\n## Seven queue labels\n\n{labels_md}\n\n## How to use it\n\nUse this map before allowing AI-assisted tools to draft or send follow-up. The safer path is to identify exceptions first, save evidence, and route uncertain items to a named human owner.\n\n**Truth boundary:** {BOUNDARY}\n\nInfographic and public checklist: https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html\n"
(PUB / "devto.md").write_text(devto, encoding="utf-8")
manifest_path = BASE / "publications" / DATE / "manifest.json"
manifest = []
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest = [m for m in manifest if m.get("slot") != SLOT]
manifest.append({"slot": SLOT, "slug": SLUG, "title": TITLE, "url": f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html", "png": f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png", "boundary": BOUNDARY})
manifest_path.parent.mkdir(parents=True, exist_ok=True)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
items = ''.join(f"<li><a href='/publications/{DATE}/{m['slug']}.html'>{m['slot'].title()}: {html.escape(m['title'])}</a></li>" for m in manifest)
index = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://support-aicloudstrategist.github.io/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:28px;box-shadow:0 14px 36px #15203312}}li{{margin:14px 0}}.cta{{display:inline-block;margin-top:12px;padding:12px 16px;border-radius:999px;background:#0f766e;color:white;text-decoration:none;font-weight:800}}</style></head><body><main><section><p><strong>AICloudStrategist daily publications</strong></p><h1>Safe educational posts with infographics — {DATE}</h1><ul>{items}</ul><p>LinkedIn excluded. Educational only; no client/result/legal/compliance/performance claims.</p><a class='cta' href='/free-business-review/'>Request a free business review</a></section></main></body></html>"""
(WEB / "index.html").write_text(index, encoding="utf-8")
log = BASE / "publications" / DATE / "publish-log.md"
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n""" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + f"\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}\n" for m in manifest) + "\n## Verification\n- Pending HTTP verification after deployment.\n", encoding="utf-8")
(EVIDENCE / f"{DATE}-{SLOT}-{SLUG}.md").write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Repository/deployment evidence: this file and `/publications/{DATE}/` assets.\n\nVerification markers:\n- Page title: `{TITLE}`\n- Visual marker: `Automation Exception Queue Map`\n- Boundary marker: `{BOUNDARY}`\n""", encoding="utf-8")
print(json.dumps(manifest, indent=2))
