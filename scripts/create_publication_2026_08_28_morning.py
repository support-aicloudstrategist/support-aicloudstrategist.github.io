from pathlib import Path
import html
import json
import re
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-28'
SLOT = 'morning'
SLUG = 'ai-escalation-receipt'
TITLE = 'The AI Escalation Receipt'
HOOK = 'A safe educational worksheet for recording why an AI-assisted task stopped, who owns the decision, and what evidence is needed before work continues.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

boxes = [
    ('01', 'Stop reason', '#dc2626', 'Write the plain-language reason the AI output should not move forward automatically: missing evidence, sensitive data, unclear owner, or risky impact.'),
    ('02', 'Source evidence', '#2563eb', 'List the exact notes, tickets, emails, screenshots, logs, or documents that are allowed to support the next decision.'),
    ('03', 'Decision owner', '#7c3aed', 'Name the person or role that must approve, reject, rewrite, or park the AI-assisted work before it affects anyone else.'),
    ('04', 'Safe next step', '#16a34a', 'Choose one reversible action: ask for missing facts, create a human-review draft, update the checklist, or record “not enough information”.'),
    ('05', 'Audit trail', '#f97316', 'Save the receipt with date, task, source list, reviewer, decision, and unresolved questions so the team can inspect it later.'),
]
questions = [
    ('Why stop?', 'What made the AI-assisted task unsafe, uncertain, or incomplete?'),
    ('What facts?', 'Which exact sources may be used for the next review?'),
    ('Who owns it?', 'Who has authority to approve or reject the next action?'),
    ('What is safe?', 'Which reversible step can happen without external impact?'),
    ('What is logged?', 'What evidence proves the handoff was reviewed?'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def wrap(text, width=38, max_lines=5):
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
positions = [(72, 260), (438, 260), (804, 260), (252, 552), (618, 552)]
for (num, label, color, text), (x, y) in zip(boxes, positions):
    lines = ''.join(f"<tspan x='{x+28}' dy='{0 if i == 0 else 20}'>{ln}</tspan>" for i, ln in enumerate(wrap(text)))
    cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='330' height='230' rx='28' fill='#ffffff' stroke='#dbeafe'/>
      <circle cx='{x+58}' cy='{y+56}' r='32' fill='{color}'/>
      <text x='{x+58}' y='{y+65}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#fff'>{num}</text>
      <text x='{x+108}' y='{y+63}' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='950' fill='#111827'>{html.escape(label)}</text>
      <text x='{x+28}' y='{y+116}' font-family='Inter,Arial,sans-serif' font-size='16.5' fill='#334155'>{lines}</text>
    </g>""")

q_items = []
for i, (label, text) in enumerate(questions):
    x = 64 + i * 220
    q_items.append(f"""
      <g>
        <path d='M{x} 824 h168 a18 18 0 0 1 18 18 v46 a18 18 0 0 1 -18 18 h-168 a18 18 0 0 1 -18 -18 v-46 a18 18 0 0 1 18 -18z' fill='#f8fafc' stroke='#cbd5e1'/>
        <text x='{x+84}' y='853' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='950' fill='#0f172a'>{html.escape(label)}</text>
        <text x='{x+8}' y='881' font-family='Inter,Arial,sans-serif' font-size='12.2' fill='#475569'>{html.escape(text[:64])}</text>
      </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='940' viewBox='0 0 1200 940'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#fff7ed'/><stop offset='48%' stop-color='#eef2ff'/><stop offset='100%' stop-color='#ecfdf5'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='14' stdDeviation='12' flood-color='#0f172a' flood-opacity='.13'/></filter>
  </defs>
  <rect width='1200' height='940' fill='url(#bg)'/>
  <rect x='42' y='42' width='1116' height='856' rx='44' fill='rgba(255,255,255,.78)' stroke='#fed7aa'/>
  <text x='76' y='106' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#9a3412' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING AI HANDOFF WORKSHEET</text>
  <text x='76' y='166' font-family='Inter,Arial,sans-serif' font-size='58' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='76' y='212' font-family='Inter,Arial,sans-serif' font-size='21' fill='#334155'>{html.escape(HOOK)}</text>
  <path d='M600 234 C600 274 600 314 600 356' stroke='#fdba74' stroke-width='7' stroke-linecap='round' stroke-dasharray='14 15'/>
  {''.join(cards)}
  <text x='76' y='802' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='#0f172a'>Five prompts to complete the receipt before work resumes</text>
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
<style>body{{margin:0;background:#fffaf5;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#9a3412,#3730a3);color:white;border-radius:30px;padding:36px}}.kicker{{color:#fed7aa;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #f3dcc6;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #f3dcc6}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · AI escalation hygiene</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Five fields in an escalation receipt</h2><ul>{boxes_html}</ul></section><section class='card'><h2>Five prompts before work resumes</h2><ul>{questions_html}</ul></section><section class='card'><h2>How to use this receipt</h2><p>Use this receipt when an AI-assisted workflow reaches uncertainty: a missing fact, a sensitive decision, unclear ownership, or a public/customer-facing consequence. The goal is to pause safely, capture evidence, and route the next step to a responsible reviewer.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Five fields in an escalation receipt\n\n{boxes_md}\n## Five prompts before work resumes\n\n{questions_md}\n## How to use it\n\nUse this receipt when an AI-assisted workflow reaches uncertainty: a missing fact, a sensitive decision, unclear ownership, or a public/customer-facing consequence. The goal is to pause safely, capture evidence, and route the next step to a responsible reviewer.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"""
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

info_dir = REPO / 'infographic' / SLUG
(info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: AI-assisted escalation and human review hygiene.\n- Layout: bento-grid / dashboard-style worksheet.\n- Style: corporate Memphis / clean educational cards.\n- Audience: business operators adopting AI workflows.\n- Language: en.\n- Safety: educational only; no customer, legal, compliance, savings, ranking, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp teams record why an AI-assisted task paused and how to route safe human review.\n\n## Sections\n{boxes_md}\n## Review prompts\n{questions_md}\n\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean corporate Memphis bento-grid infographic titled '{TITLE}' using the five fields and five prompts from structured-content.md. Aspect 16:9-ish wide educational worksheet. Keep all claims educational and avoid client/result/legal/compliance claims.\n", encoding='utf-8')

home = REPO / 'index.html'
home_text = home.read_text(encoding='utf-8')
new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Stop</span><i></i><span>Owner</span><i></i><span>Receipt</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3>{TITLE}</h3>
            <p>{HOOK}</p>
          </article>'''
home_text = re.sub(r'          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true">.*?</article>', new_article, home_text, count=1, flags=re.S)
home_text = re.sub(r'/publications/\d{4}-\d{2}-\d{2}/[^"<>]+\.html">Review the [^<]+', f'/publications/{DATE}/{SLUG}.html">Review the AI escalation receipt', home_text, count=1)
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
