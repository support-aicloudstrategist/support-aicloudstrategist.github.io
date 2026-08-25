from pathlib import Path
import html
import json
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-25'
SLOT = 'evening'
SLUG = 'ai-vendor-access-review-board'
TITLE = 'The AI Vendor Access Review Board'
HOOK = 'A safe educational checklist for reviewing what an AI vendor or tool may access before it touches business data.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

rings = [
    ('Need', '#0ea5e9', 'What problem will the tool solve, and who owns the business decision?'),
    ('Data', '#6366f1', 'What files, messages, records, prompts, or exports will the tool read or store?'),
    ('Access', '#f97316', 'Which people, systems, keys, folders, inboxes, channels, or automations are in scope?'),
    ('Review', '#16a34a', 'Who checks exceptions, quality issues, privacy concerns, and customer-facing outputs?'),
]
questions = [
    ('Purpose', 'Is the business use case narrow enough to test safely?'),
    ('Minimum data', 'Can the workflow run with redacted, synthetic, or limited data first?'),
    ('Human gate', 'Where must a human approve before external action?'),
    ('Exit path', 'Can access be removed and records exported if the tool fails?'),
    ('Evidence', 'Will decisions, sources, reviewers, and changes be logged?'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def wrap_svg_text(text, width=43):
    words = html.escape(text).split()
    lines, line = [], ''
    for word in words:
        if len((line + ' ' + word).strip()) > width:
            lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line:
        lines.append(line)
    return lines[:3]

ring_cards = []
coords = [(95, 290), (625, 290), (95, 535), (625, 535)]
for (label, color, text), (x, y) in zip(rings, coords):
    tspans = ''.join(f"<tspan x='{x+152}' dy='{0 if j == 0 else 23}'>{ln}</tspan>" for j, ln in enumerate(wrap_svg_text(text, 46)))
    ring_cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='480' height='170' rx='30' fill='#ffffff' stroke='#dbeafe'/>
      <circle cx='{x+72}' cy='{y+85}' r='48' fill='{color}'/>
      <text x='{x+72}' y='{y+94}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='950' fill='#fff'>{html.escape(label)}</text>
      <text x='{x+152}' y='{y+62}' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='950' fill='#132033'>{html.escape(label)} check</text>
      <text x='{x+152}' y='{y+99}' font-family='Inter,Arial,sans-serif' font-size='17.5' fill='#334155'>{tspans}</text>
    </g>""")

question_items = []
for i, (label, text) in enumerate(questions):
    x = 76 + i * 210
    question_items.append(f"""
      <g>
        <rect x='{x}' y='785' width='185' height='78' rx='20' fill='#f8fafc' stroke='#cbd5e1'/>
        <text x='{x+92}' y='815' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='950' fill='#0f172a'>{html.escape(label)}</text>
        <text x='{x+15}' y='844' font-family='Inter,Arial,sans-serif' font-size='12.6' fill='#475569'>{html.escape(text[:54])}</text>
      </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#eff6ff'/><stop offset='45%' stop-color='#f5f3ff'/><stop offset='100%' stop-color='#ecfdf5'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='14' stdDeviation='14' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1200' height='900' fill='url(#bg)'/>
  <rect x='42' y='42' width='1116' height='816' rx='42' fill='rgba(255,255,255,.78)' stroke='#bfdbfe'/>
  <text x='75' y='104' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#4338ca' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING VENDOR ACCESS CHECKLIST</text>
  <text x='75' y='166' font-family='Inter,Arial,sans-serif' font-size='56' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='75' y='211' font-family='Inter,Arial,sans-serif' font-size='22' fill='#334155'>{html.escape(HOOK)}</text>
  <path d='M602 252 C602 252 602 730 602 730' stroke='#cbd5e1' stroke-width='3' stroke-dasharray='10 14'/>
  {''.join(ring_cards)}
  <text x='78' y='748' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='950' fill='#0f172a'>Five board questions before granting tool access</text>
  {''.join(question_items)}
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

rings_html = ''.join(f"<li><strong>{html.escape(label)} check:</strong> {html.escape(text)}</li>" for label, _, text in rings)
questions_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for label, text in questions)
rings_md = ''.join(f"- **{label} check:** {text}\n" for label, _, text in rings)
questions_md = ''.join(f"- **{label}:** {text}\n" for label, text in questions)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='{URL}'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='{PNG_URL}'>
<meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#172554,#4338ca);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bfdbfe;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #d8e6f3}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · AI vendor access</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Access review lanes</h2><ul>{rings_html}</ul></section><section class='card'><h2>Five board questions</h2><ul>{questions_html}</ul></section><section class='card'><h2>How to use this board</h2><p>Use this board before connecting a new AI tool to shared drives, inboxes, chat systems, CRM exports, customer records, automations, or public-response workflows. Start narrow, log the decision, and keep a named human owner for exceptions.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Access review lanes\n\n{rings_md}\n## Five board questions\n\n{questions_md}\n## How to use it\n\nUse this board before connecting a new AI tool to shared drives, inboxes, chat systems, CRM exports, customer records, automations, or public-response workflows. Start narrow, log the decision, and keep a named human owner for exceptions.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic checklist and infographic: {URL}\n"""
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')

manifest_path = pub_dir / 'manifest.json'
manifest = []
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest = [m for m in manifest if m.get('slot') != SLOT and m.get('slug') != SLUG]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get('slot') == 'morning' else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

links = ''.join(f"<li><a href='{html.escape(m['slug'])}.html'>{html.escape(m['slot'].title())}: {html.escape(m['title'])}</a></li>" for m in manifest)
index = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>"""
(pub_dir / 'index.html').write_text(index, encoding='utf-8')

log = pub_dir / 'publish-log.md'
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n""" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + f"\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')

evidence_dir = REPO / 'docs' / 'publication-evidence'
evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`\n\nLive targets after deployment:\n- {URL}\n- {PNG_URL}\n- {REPO_URL}\n""", encoding='utf-8')

home = REPO / 'index.html'
home_text = home.read_text(encoding='utf-8')
home_text = home_text.replace('<div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Draft</span><i></i><span>Review</span><i></i><span>Escalate</span></div>\n            <span class="ea-evidence-type">Public educational asset · 2026-08-24</span>\n            <h3>The AI Reply Safety Stoplight</h3>\n            <p>A safe checklist for deciding when an AI assistant may draft, pause, or escalate a customer-facing reply.</p>', '<div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Need</span><i></i><span>Data</span><i></i><span>Access</span></div>\n            <span class="ea-evidence-type">Public educational asset · 2026-08-25</span>\n            <h3>The AI Vendor Access Review Board</h3>\n            <p>A safe checklist for reviewing what an AI vendor or tool may access before it touches business data.</p>')
home_text = home_text.replace('/publications/2026-08-24/ai-reply-safety-stoplight.html">Review the AI reply safety stoplight', '/publications/2026-08-25/ai-vendor-access-review-board.html">Review the AI vendor access review board')
home.write_text(home_text, encoding='utf-8')

sitemap = REPO / 'sitemap.xml'
sitemap_text = sitemap.read_text(encoding='utf-8')
entry = f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
if URL not in sitemap_text:
    sitemap_text = sitemap_text.replace(f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n', entry + f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n')
sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
