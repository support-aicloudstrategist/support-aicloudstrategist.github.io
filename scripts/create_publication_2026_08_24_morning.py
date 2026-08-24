from pathlib import Path
import html
import json
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-24'
SLOT = 'morning'
SLUG = 'ai-task-intake-clarity-map'
TITLE = 'The AI Task Intake Clarity Map'
HOOK = 'A safe educational checklist for deciding what an AI workflow is allowed to do before anyone automates a business task.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://support-aicloudstrategist.github.io/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    ('1', 'Goal', 'Write the business task in plain language before choosing any model, agent, app, or automation tool.'),
    ('2', 'Inputs', 'List the data sources the workflow may read and exclude private, sensitive, or unapproved material.'),
    ('3', 'Decision rights', 'Mark what AI can suggest, what a human must approve, and what the system must never decide alone.'),
    ('4', 'Handoff', 'Define the owner, escalation path, fallback step, and expected response time for unclear cases.'),
    ('5', 'Evidence', 'Keep a short log of input category, action taken, reviewer, final status, and unresolved exceptions.'),
    ('6', 'Review', 'Recheck the workflow after real use and remove shortcuts that create risk, confusion, or customer friction.'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

colors = ['#0f766e', '#2563eb', '#7c3aed', '#ea580c', '#0891b2', '#475569']
cards = []
for i, (num, label, text) in enumerate(checks):
    x = 80 + i * 170
    y = 300 + (22 if i % 2 else 0)
    color = colors[i]
    safe_text = html.escape(text)
    words = safe_text.split()
    lines = []
    line = ''
    for word in words:
        if len((line + ' ' + word).strip()) > 24:
            lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line:
        lines.append(line)
    tspans = ''.join(f"<tspan x='{x+22}' dy='{0 if j == 0 else 23}'>{ln}</tspan>" for j, ln in enumerate(lines[:6]))
    cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='150' height='310' rx='28' fill='#ffffff' stroke='#d8e6f3'/>
      <circle cx='{x+75}' cy='{y+62}' r='42' fill='{color}'/>
      <text x='{x+75}' y='{y+76}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='40' font-weight='950' fill='#fff'>{num}</text>
      <text x='{x+75}' y='{y+139}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='#152033'>{html.escape(label)}</text>
      <text x='{x+22}' y='{y+180}' font-family='Inter,Arial,sans-serif' font-size='16.5' fill='#334155'>{tspans}</text>
    </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#eef2ff'/><stop offset='48%' stop-color='#ecfeff'/><stop offset='100%' stop-color='#fff7ed'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='14' stdDeviation='13' flood-color='#0f172a' flood-opacity='.16'/></filter>
  </defs>
  <rect width='1200' height='900' fill='url(#bg)'/>
  <rect x='42' y='42' width='1116' height='816' rx='42' fill='rgba(255,255,255,.72)' stroke='#bfdbfe'/>
  <text x='75' y='108' font-family='Inter,Arial,sans-serif' font-size='19' font-weight='900' fill='#0f766e' letter-spacing='3'>AICLOUDSTRATEGIST · SAFE AI AUTOMATION</text>
  <text x='75' y='170' font-family='Inter,Arial,sans-serif' font-size='56' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='75' y='213' font-family='Inter,Arial,sans-serif' font-size='22' fill='#334155'>{html.escape(HOOK)}</text>
  <path d='M145 660 C275 730, 420 705, 555 750 S850 785, 1048 706' fill='none' stroke='#99f6e4' stroke-width='18' stroke-linecap='round' opacity='.65'/>
  {''.join(cards)}
  <rect x='75' y='770' width='1050' height='76' rx='22' fill='#0f172a'/>
  <text x='100' y='803' font-family='Inter,Arial,sans-serif' font-size='19' font-weight='850' fill='#bae6fd'>Truth boundary</text>
  <text x='100' y='831' font-family='Inter,Arial,sans-serif' font-size='17' fill='#e5f0ff'>{html.escape(BOUNDARY)}</text>
</svg>"""

(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

checks_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for _, label, text in checks)
checks_md = ''.join(f"- **{label}:** {text}\n" for _, label, text in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='{URL}'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='{PNG_URL}'>
<meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#152033,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#99f6e4;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #d8e6f3}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Safe educational AI workflow</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Six checks before automating a task</h2><ol>{checks_html}</ol></section><section class='card'><h2>How to use this map</h2><p>Use this map before building or buying an AI workflow. It keeps the discussion focused on task clarity, approved inputs, human decision rights, handoffs, evidence, and review discipline.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Six checks before automating a task\n\n{checks_md}\n## How to use it\n\nUse this map before building or buying an AI workflow. It keeps the discussion focused on task clarity, approved inputs, human decision rights, handoffs, evidence, and review discipline.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic checklist and infographic: {URL}\n"""
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
index = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>"""
(pub_dir / 'index.html').write_text(index, encoding='utf-8')

log = pub_dir / 'publish-log.md'
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n""" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + f"\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
