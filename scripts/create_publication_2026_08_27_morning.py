from pathlib import Path
import html
import json
import re
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-27'
SLOT = 'morning'
SLUG = 'ai-prompt-scope-box'
TITLE = 'The AI Prompt Scope Box'
HOOK = 'A safe educational checklist for keeping AI tasks narrow, testable, and reviewable before teams use them in daily work.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

boxes = [
    ('01', 'One job only', '#0ea5e9', 'Ask the AI to complete one clear task, not strategy, writing, analysis, and approval in the same instruction.'),
    ('02', 'Known inputs', '#6366f1', 'List the exact source notes, fields, documents, or examples the AI may use. If a fact is absent, require “not enough information”.'),
    ('03', 'Allowed output', '#16a34a', 'Define the format: bullets, table, checklist, draft, summary, or triage label. Ban unsupported claims and invented details.'),
    ('04', 'Review owner', '#f97316', 'Name who checks the result before it affects a customer, employee, vendor, payment, policy, system, or public page.'),
    ('05', 'Stop rules', '#dc2626', 'Pause when the task involves sensitive data, regulated decisions, identity, legal meaning, pricing, security, or emotional customer replies.'),
]
questions = [
    ('Purpose', 'What decision or workflow does this prompt support?'),
    ('Evidence', 'Which facts are allowed, and where did they come from?'),
    ('Output', 'What should the AI return, and what must it never claim?'),
    ('Risk', 'What makes the result unsafe or uncertain?'),
    ('Owner', 'Who reviews, approves, and records the final use?'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def wrap(text, width=36, max_lines=4):
    words = html.escape(text).split()
    lines, line = [], ''
    for word in words:
        if len((line + ' ' + word).strip()) > width:
            if line:
                lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line:
        lines.append(line)
    return lines[:max_lines]

cards = []
positions = [(78, 260), (438, 260), (798, 260), (258, 535), (618, 535)]
for (num, label, color, text), (x, y) in zip(boxes, positions):
    lines = ''.join(f"<tspan x='{x+30}' dy='{0 if i == 0 else 21}'>{ln}</tspan>" for i, ln in enumerate(wrap(text, 43)))
    cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='322' height='220' rx='28' fill='#ffffff' stroke='#dbeafe'/>
      <rect x='{x+22}' y='{y+22}' width='68' height='48' rx='17' fill='{color}'/>
      <text x='{x+56}' y='{y+55}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='#fff'>{num}</text>
      <text x='{x+104}' y='{y+55}' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='#111827'>{html.escape(label)}</text>
      <text x='{x+30}' y='{y+110}' font-family='Inter,Arial,sans-serif' font-size='17' fill='#334155'>{lines}</text>
    </g>""")

q_items = []
for i, (label, text) in enumerate(questions):
    x = 72 + i * 214
    q_items.append(f"""
      <g>
        <rect x='{x}' y='795' width='186' height='72' rx='20' fill='#f8fafc' stroke='#cbd5e1'/>
        <text x='{x+93}' y='823' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='950' fill='#0f172a'>{html.escape(label)}</text>
        <text x='{x+14}' y='850' font-family='Inter,Arial,sans-serif' font-size='12.5' fill='#475569'>{html.escape(text[:58])}</text>
      </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#eef2ff'/><stop offset='50%' stop-color='#ecfeff'/><stop offset='100%' stop-color='#f0fdf4'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='14' stdDeviation='13' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1200' height='900' fill='url(#bg)'/>
  <rect x='42' y='42' width='1116' height='816' rx='42' fill='rgba(255,255,255,.78)' stroke='#bae6fd'/>
  <text x='75' y='104' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#0369a1' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING PROMPT SAFETY CHECKLIST</text>
  <text x='75' y='164' font-family='Inter,Arial,sans-serif' font-size='56' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='75' y='210' font-family='Inter,Arial,sans-serif' font-size='22' fill='#334155'>{html.escape(HOOK)}</text>
  <path d='M600 236 C600 276 600 304 600 344' stroke='#93c5fd' stroke-width='6' stroke-linecap='round' stroke-dasharray='12 16'/>
  {''.join(cards)}
  <text x='78' y='762' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='950' fill='#0f172a'>Five checks before reusing a prompt inside the business</text>
  {''.join(q_items)}
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

boxes_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for _, label, _, text in boxes)
questions_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for label, text in questions)
boxes_md = ''.join(f"- **{label}:** {text}\n" for _, label, _, text in boxes)
questions_md = ''.join(f"- **{label}:** {text}\n" for label, text in questions)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='{URL}'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='{PNG_URL}'>
<meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#1d4ed8,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bfdbfe;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #d8e6f3}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · AI prompt safety</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Five prompt scope boxes</h2><ul>{boxes_html}</ul></section><section class='card'><h2>Five checks before reuse</h2><ul>{questions_html}</ul></section><section class='card'><h2>How to use this box</h2><p>Use this prompt scope box when a team wants to reuse an AI instruction for inbox sorting, report drafting, ticket triage, internal summaries, or operational checklists. Keep the task small, define the allowed evidence, and require review before the result affects people or public communication.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Five prompt scope boxes\n\n{boxes_md}\n## Five checks before reuse\n\n{questions_md}\n## How to use it\n\nUse this prompt scope box when a team wants to reuse an AI instruction for inbox sorting, report drafting, ticket triage, internal summaries, or operational checklists. Keep the task small, define the allowed evidence, and require review before the result affects people or public communication.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic checklist and infographic: {URL}\n"""
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
new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Scope</span><i></i><span>Facts</span><i></i><span>Review</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3>{TITLE}</h3>
            <p>{HOOK}</p>
          </article>'''
home_text = re.sub(r'          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true">.*?</article>', new_article, home_text, count=1, flags=re.S)
home_text = re.sub(r'/publications/\d{4}-\d{2}-\d{2}/[^"<>]+\.html">Review the [^<]+', f'/publications/{DATE}/{SLUG}.html">Review the AI prompt scope box', home_text, count=1)
home.write_text(home_text, encoding='utf-8')

sitemap = REPO / 'sitemap.xml'
sitemap_text = sitemap.read_text(encoding='utf-8')
index_entry = f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
page_entry = f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
if f'https://aicloudstrategist.com/publications/{DATE}/' not in sitemap_text:
    sitemap_text = sitemap_text.replace('</urlset>', index_entry + '</urlset>')
if URL not in sitemap_text:
    sitemap_text = sitemap_text.replace(index_entry, page_entry + index_entry)
sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
