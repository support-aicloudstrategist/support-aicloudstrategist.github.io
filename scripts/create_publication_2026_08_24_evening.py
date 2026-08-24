from pathlib import Path
import html
import json
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-24'
SLOT = 'evening'
SLUG = 'ai-reply-safety-stoplight'
TITLE = 'The AI Reply Safety Stoplight'
HOOK = 'A safe educational checklist for deciding when an AI assistant may draft, pause, or escalate a customer-facing reply.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

lanes = [
    ('Green', '#16a34a', 'Routine answer', 'Use only approved facts, current public information, and a visible owner-approved knowledge source.'),
    ('Amber', '#f59e0b', 'Needs review', 'Pause for a human when the message includes uncertainty, unusual context, pricing nuance, or customer frustration.'),
    ('Red', '#dc2626', 'Must escalate', 'Do not auto-answer legal, medical, compliance, security, payment, credential, identity, contract, or result-claim topics.'),
]
checks = [
    ('Source', 'Can the answer be traced to an approved source?'),
    ('Scope', 'Is the request inside the assistant’s allowed boundary?'),
    ('Risk', 'Could the reply create a legal, financial, health, privacy, security, or promise risk?'),
    ('Owner', 'Is a named human responsible for exceptions?'),
    ('Record', 'Will the decision, source, reviewer, and final status be logged?'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

lane_cards = []
for i, (label, color, heading, text) in enumerate(lanes):
    y = 268 + i * 158
    words = html.escape(text).split()
    lines, line = [], ''
    for word in words:
        if len((line + ' ' + word).strip()) > 62:
            lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line:
        lines.append(line)
    tspans = ''.join(f"<tspan x='268' dy='{0 if j == 0 else 24}'>{ln}</tspan>" for j, ln in enumerate(lines[:4]))
    lane_cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='86' y='{y}' width='1028' height='122' rx='28' fill='#ffffff' stroke='#dbeafe'/>
      <circle cx='160' cy='{y+61}' r='42' fill='{color}'/>
      <text x='160' y='{y+70}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='20' font-weight='950' fill='#fff'>{label}</text>
      <text x='235' y='{y+45}' font-family='Inter,Arial,sans-serif' font-size='28' font-weight='950' fill='#132033'>{html.escape(heading)}</text>
      <text x='268' y='{y+79}' font-family='Inter,Arial,sans-serif' font-size='18' fill='#334155'>{tspans}</text>
    </g>""")

check_items = []
for i, (label, text) in enumerate(checks):
    x = 94 + i * 204
    check_items.append(f"""
      <g>
        <rect x='{x}' y='762' width='176' height='82' rx='20' fill='#eff6ff' stroke='#bfdbfe'/>
        <text x='{x+88}' y='793' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#1d4ed8'>{html.escape(label)}</text>
        <text x='{x+16}' y='823' font-family='Inter,Arial,sans-serif' font-size='13.5' fill='#334155'>{html.escape(text[:48])}</text>
      </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#f0fdfa'/><stop offset='48%' stop-color='#eef2ff'/><stop offset='100%' stop-color='#fff7ed'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='14' stdDeviation='14' flood-color='#0f172a' flood-opacity='.15'/></filter>
  </defs>
  <rect width='1200' height='900' fill='url(#bg)'/>
  <rect x='42' y='42' width='1116' height='816' rx='42' fill='rgba(255,255,255,.74)' stroke='#bae6fd'/>
  <text x='75' y='104' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#0f766e' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING SAFE AI WORKFLOW</text>
  <text x='75' y='166' font-family='Inter,Arial,sans-serif' font-size='58' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='75' y='211' font-family='Inter,Arial,sans-serif' font-size='22' fill='#334155'>{html.escape(HOOK)}</text>
  {''.join(lane_cards)}
  <text x='92' y='726' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='950' fill='#0f172a'>Five checks before a customer-facing reply leaves the queue</text>
  {''.join(check_items)}
  <rect x='75' y='858' width='1050' height='1' fill='#cbd5e1'/>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

lane_html = ''.join(f"<li><strong>{html.escape(label)} — {html.escape(heading)}:</strong> {html.escape(text)}</li>" for label, _, heading, text in lanes)
checks_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for label, text in checks)
lane_md = ''.join(f"- **{label} — {heading}:** {text}\n" for label, _, heading, text in lanes)
checks_md = ''.join(f"- **{label}:** {text}\n" for label, text in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='{URL}'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='{PNG_URL}'>
<meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#132033,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#99f6e4;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #d8e6f3}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · safe AI replies</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Stoplight lanes</h2><ul>{lane_html}</ul></section><section class='card'><h2>Five checks before sending</h2><ul>{checks_html}</ul></section><section class='card'><h2>How to use this stoplight</h2><p>Use this stoplight before allowing an AI assistant to draft or send customer-facing replies. It keeps routine answers separate from replies that need a named human owner.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Stoplight lanes\n\n{lane_md}\n## Five checks before sending\n\n{checks_md}\n## How to use it\n\nUse this stoplight before allowing an AI assistant to draft or send customer-facing replies. It keeps routine answers separate from replies that need a named human owner.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic checklist and infographic: {URL}\n"""
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

# Homepage latest-publication card.
home = REPO / 'index.html'
home_text = home.read_text(encoding='utf-8')
home_text = home_text.replace('<div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Intake</span><i></i><span>Rights</span><i></i><span>Evidence</span></div>\n            <span class="ea-evidence-type">Public educational asset · 2026-08-24</span>\n            <h3>The AI Task Intake Clarity Map</h3>\n            <p>A safe checklist for deciding what an AI workflow may read, suggest, escalate and log before a business task is automated.</p>', '<div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Draft</span><i></i><span>Review</span><i></i><span>Escalate</span></div>\n            <span class="ea-evidence-type">Public educational asset · 2026-08-24</span>\n            <h3>The AI Reply Safety Stoplight</h3>\n            <p>A safe checklist for deciding when an AI assistant may draft, pause, or escalate a customer-facing reply.</p>')
home_text = home_text.replace('/publications/2026-08-24/ai-task-intake-clarity-map.html">Review the AI task intake map', '/publications/2026-08-24/ai-reply-safety-stoplight.html">Review the AI reply safety stoplight')
home.write_text(home_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
