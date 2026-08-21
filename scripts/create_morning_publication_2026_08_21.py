from pathlib import Path
import html, json, subprocess

DATE = "2026-08-21"
SLOT = "morning"
SLUG = "lead-follow-up-triage-board"
TITLE = "Lead Follow-up Triage Board: 6 morning checks before the inbox gets busy"
HOOK = "A safe educational board for owners and teams to review new enquiries, missed replies, and automation exceptions before customer promises drift."
BOUNDARY = "Educational workflow only — no legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice."
BASE = Path("/home/agent/.hermes/aicloudstrategist")
REPO = BASE / "repos" / "support-aicloudstrategist.github.io"
PUB = BASE / "publications" / DATE / SLUG
WEB = REPO / "publications" / DATE
INFO = REPO / "infographic" / SLUG
EVIDENCE = REPO / "docs" / "publication-evidence"
for p in (PUB, WEB, INFO / "prompts", EVIDENCE):
    p.mkdir(parents=True, exist_ok=True)

checks = [
    ("New enquiries", "Are all new form, WhatsApp, email, phone, and social enquiries in one visible queue?"),
    ("Aging replies", "Which leads have waited too long and need a human response before more automation runs?"),
    ("Owner assigned", "Does every open item have a named owner for the next action or escalation?"),
    ("Risk pause", "Are legal, medical, tax, pricing, refund, credential, OTP, or sensitive-data items paused for review?"),
    ("Promise check", "Do automated replies match what the team can actually honour today?"),
    ("Evidence saved", "Are source, timestamp, status, and next-step notes captured for later review?"),
]

source = f"""Topic: Lead Follow-up Triage Board for morning operations.
Audience: business owners, clinic/admin teams, local service operators, agencies, SaaS teams, and support managers using websites, forms, WhatsApp, email, CRMs, or AI-assisted workflows.
Safe boundaries: {BOUNDARY}
Core checks: {', '.join(x[0] for x in checks)}.
"""
analysis = f"""# Analysis — Lead Follow-up Triage Board

- Topic: Morning triage board for owner-led lead follow-up and automation exception review.
- Data type: Educational checklist and operating-control framework.
- Complexity: Low-to-medium; practical for non-technical owners and managers.
- Tone: Calm, operational, safe, plain-English.
- Audience: Small and mid-sized teams using forms, inboxes, CRMs, WhatsApp, support tools, or AI assistants.
- Language: English.
- Design: dashboard layout + corporate-memphis style, landscape 16:9, infographic-style SVG and PNG.
- Truth boundary: {BOUNDARY}
"""
structured = "# Structured content — Lead Follow-up Triage Board\n\n"
structured += f"## Title\n{TITLE}\n\n## Learning objectives\n- Help owners review lead follow-up before the workday gets busy.\n- Help teams keep enquiries, aging replies, owners, risk pauses, promises, and evidence visible.\n- Keep the guidance educational and claim-safe.\n\n## Sections\n"
for i, (name, detail) in enumerate(checks, 1):
    structured += f"\n### {i}. {name}\nContent: {detail}\nVisual element: Dashboard card with status badge.\nText labels: {name}; morning check.\n"
structured += f"\n## Data points\n- No statistics used.\n- No customer examples used.\n- No performance claims used.\n\n## Boundary label\n{BOUNDARY}\n"
prompt = f"""Create a professional infographic following these specifications:

## Image Specifications
- Type: Infographic
- Layout: dashboard
- Style: corporate-memphis
- Aspect Ratio: 16:9
- Language: English

## Layout Guidelines
Dashboard-style arrangement with a clear title, six status cards, owner/review indicators, visual hierarchy, and concise labels.

## Style Guidelines
Flat vector corporate Memphis style with a light background, saturated teal, purple, orange, navy, and yellow accents, clean sans-serif typography, friendly business operations tone.

## Content
Title: {TITLE}
Hook: {HOOK}
Cards: {', '.join(x[0] for x in checks)}.
Boundary: {BOUNDARY}
"""
(INFO / "source.md").write_text(source, encoding="utf-8")
(INFO / "analysis.md").write_text(analysis, encoding="utf-8")
(INFO / "structured-content.md").write_text(structured, encoding="utf-8")
(INFO / "prompts" / "infographic.md").write_text(prompt, encoding="utf-8")

colors = {"navy":"#152033","teal":"#00b8a9","purple":"#7c4dff","orange":"#ff8a3d","yellow":"#ffd166","bg":"#f6fbff","line":"#d8e6f3"}
card_positions = [(72,250),(430,250),(788,250),(72,520),(430,520),(788,520)]
svg_cards = []
for i, ((name, detail), (x, y)) in enumerate(zip(checks, card_positions), 1):
    accent = [colors['teal'], colors['purple'], colors['orange'], colors['yellow'], '#3b82f6', '#10b981'][i-1]
    words = detail.split()
    line1 = ' '.join(words[:8])
    line2 = ' '.join(words[8:16])
    line3 = ' '.join(words[16:24])
    svg_cards.append(f"""<g transform='translate({x} {y})'>
<rect width='316' height='210' rx='26' fill='#ffffff' stroke='{colors['line']}' stroke-width='2'/>
<circle cx='48' cy='48' r='26' fill='{accent}'/><text x='48' y='57' text-anchor='middle' font-size='25' font-weight='900' fill='white'>{i}</text>
<text x='90' y='44' font-size='24' font-weight='900' fill='{colors['navy']}'>{html.escape(name)}</text>
<rect x='90' y='63' width='116' height='24' rx='12' fill='{accent}' opacity='.16'/><text x='103' y='81' font-size='13' font-weight='800' fill='{colors['navy']}'>MORNING CHECK</text>
<text x='32' y='122' font-size='18' fill='#475569'>{html.escape(line1)}</text>
<text x='32' y='150' font-size='18' fill='#475569'>{html.escape(line2)}</text>
<text x='32' y='178' font-size='18' fill='#475569'>{html.escape(line3)}</text>
</g>""")
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900' role='img' aria-labelledby='title desc'>
<title id='title'>{html.escape(TITLE)}</title><desc id='desc'>Six morning lead follow-up triage checks: new enquiries, aging replies, owner assigned, risk pause, promise check, evidence saved.</desc>
<rect width='1200' height='900' fill='{colors['bg']}'/>
<circle cx='1070' cy='105' r='125' fill='{colors['yellow']}' opacity='.58'/><circle cx='140' cy='805' r='150' fill='{colors['purple']}' opacity='.10'/>
<path d='M845 150c92 28 185 12 270-52' fill='none' stroke='{colors['teal']}' stroke-width='18' stroke-linecap='round' opacity='.22'/>
<text x='72' y='92' font-family='Inter,Arial,sans-serif' font-size='30' font-weight='900' fill='{colors['teal']}'>AICloudStrategist • safe educational workflow</text>
<text x='72' y='154' font-family='Inter,Arial,sans-serif' font-size='48' font-weight='900' fill='{colors['navy']}'>Lead Follow-up Triage Board</text>
<text x='72' y='202' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='650' fill='#43546a'>6 morning checks before the inbox gets busy</text>
<g font-family='Inter,Arial,sans-serif'>{''.join(svg_cards)}</g>
<rect x='72' y='760' width='1056' height='74' rx='22' fill='{colors['navy']}'/>
<text x='104' y='803' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='800' fill='#ffffff'>Truth boundary:</text>
<text x='278' y='803' font-family='Inter,Arial,sans-serif' font-size='19' fill='#dbeafe'>Educational workflow only — no legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.</text>
<text x='72' y='866' font-family='Inter,Arial,sans-serif' font-size='17' fill='#64748b'>support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html</text>
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
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#152033,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#99f6e4;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin-top:22px;box-shadow:0 16px 44px #15203314}}img{{max-width:100%;border-radius:22px;border:1px solid #d8e6f3}}li{{margin:11px 0;line-height:1.45}}.note{{color:#475569;font-size:14px}}</style></head>
<body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · Lead follow-up operations</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: Lead Follow-up Triage Board with six morning checks'></section><section class='card'><h2>Practical checklist</h2><ul>{checks_html}</ul><p>Use this board before connecting more tools or sending automated replies. A useful morning review keeps the queue, owner, risk boundary, customer promise, and evidence visible.</p><p class='note'>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(WEB / f"{SLUG}.html").write_text(page, encoding="utf-8")
(PUB / f"{SLUG}.html").write_text(page, encoding="utf-8")
post = f"# {TITLE}\n\n{HOOK}\n\n{checks_md}\n\nUse this board before connecting more tools or sending automated replies. A useful morning review keeps the queue, owner, risk boundary, customer promise, and evidence visible.\n\nTruth boundary: {BOUNDARY}\n"
(PUB / "post.md").write_text(post, encoding="utf-8")
devto = f"![Infographic: {TITLE}](https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png)\n\n{HOOK}\n\n## Six morning checks\n\n{checks_md}\n\n## How to use it\n\nUse this board before connecting more tools or sending automated replies. A useful morning review keeps the queue, owner, risk boundary, customer promise, and evidence visible.\n\n**Truth boundary:** {BOUNDARY}\n\nInfographic and public checklist: https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html\n"
(PUB / "devto.md").write_text(devto, encoding="utf-8")
manifest = [{"slot": SLOT, "slug": SLUG, "title": TITLE, "url": f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html", "png": f"https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png", "boundary": BOUNDARY}]
(BASE / "publications" / DATE).mkdir(parents=True, exist_ok=True)
(BASE / "publications" / DATE / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
log = BASE / "publications" / DATE / "publish-log.md"
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n- Morning — {TITLE}: https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html\n- Morning PNG: https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png\n\n## Published / verified\n- AICS website / GitHub Pages — Morning: https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html\n- GitHub repository / deployment evidence — Morning: https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}\n\n## Verification\n- Pending HTTP verification after deployment.\n""", encoding="utf-8")
(EVIDENCE / f"{DATE}-{SLOT}-{SLUG}.md").write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Repository/deployment evidence: this file and `/publications/{DATE}/` assets.\n\nVerification markers:\n- Page title: `{TITLE}`\n- Visual marker: `Lead Follow-up Triage Board`\n- Boundary marker: `{BOUNDARY}`\n""", encoding="utf-8")
print(json.dumps(manifest, indent=2))
