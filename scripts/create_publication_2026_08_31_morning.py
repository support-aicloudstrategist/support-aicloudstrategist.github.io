from pathlib import Path
import html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-08-31'
SLOT = 'morning'
SLUG = 'ai-meeting-action-receipt'
TITLE = 'The AI Meeting Action Receipt'
HOOK = 'A safe educational one-page checklist for turning meeting notes into accountable actions without hiding ownership, uncertainty, or customer-impact risk.'
BOUNDARY = 'Educational operations checklist only — not legal, compliance, medical, financial, security, certification, revenue, savings, ranking, customer-result, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    ('Decision', 'Write the actual decision separately from background discussion.'),
    ('Owner', 'Assign one accountable person or role for each next action.'),
    ('Due window', 'Use a realistic date or review window, not an open-ended reminder.'),
    ('Evidence', 'Attach the source note, customer request, document, or metric that triggered the action.'),
    ('Risk pause', 'Flag any item involving pricing, legal terms, private data, customer promises, or uncertain facts.'),
    ('Close loop', 'Record when the action is done, deferred, corrected, or cancelled.'),
]
usage_steps = [
    'Run the receipt after important meetings, not after every casual chat.',
    'Keep risk-pause items human-reviewed before any customer-facing message.',
    'Review open receipts weekly so automation does not multiply stale tasks.',
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(s, quote=True)
def wrap(text, width=40, max_lines=4):
    words = esc(text).split(); lines=[]; line=''
    for word in words:
        if len((line + ' ' + word).strip()) > width:
            if line: lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line: lines.append(line)
    return lines[:max_lines]

card_svg=[]
positions=[(88,300),(456,300),(824,300),(88,555),(456,555),(824,555)]
colors=['#dbeafe','#ccfbf1','#fef3c7','#ede9fe','#ffe4e6','#dcfce7']
for i, ((label,text),(x,y)) in enumerate(zip(checks,positions)):
    lines=''.join(f"<tspan x='{x+34}' dy='{0 if n==0 else 22}'>{ln}</tspan>" for n,ln in enumerate(wrap(text, 31, 4)))
    card_svg.append(f"""
    <g filter='url(#soft)'>
      <rect x='{x}' y='{y}' width='288' height='178' rx='28' fill='white' stroke='#d8e6f3'/>
      <circle cx='{x+42}' cy='{y+46}' r='24' fill='{colors[i]}'/>
      <text x='{x+42}' y='{y+55}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='#0f172a'>{i+1}</text>
      <text x='{x+80}' y='{y+54}' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>{esc(label)}</text>
      <text x='{x+34}' y='{y+105}' font-family='Inter,Arial,sans-serif' font-size='17' fill='#475569'>{lines}</text>
    </g>""")

step_svg=[]
for i,step in enumerate(usage_steps):
    x=110+i*340
    lines=''.join(f"<tspan x='{x+24}' dy='{0 if n==0 else 19}'>{ln}</tspan>" for n,ln in enumerate(wrap(step, 36, 3)))
    step_svg.append(f"""
    <g>
      <rect x='{x}' y='805' width='302' height='94' rx='24' fill='#f8fafc' stroke='#cbd5e1'/>
      <text x='{x+24}' y='837' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='950' fill='#2563eb'>USE {i+1}</text>
      <text x='{x+24}' y='868' font-family='Inter,Arial,sans-serif' font-size='14' fill='#475569'>{lines}</text>
    </g>""")

svg=f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='960' viewBox='0 0 1200 960'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#0f172a'/><stop offset='.55' stop-color='#1d4ed8'/><stop offset='1' stop-color='#0f766e'/></linearGradient>
    <filter id='soft' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='13' stdDeviation='10' flood-color='#0f172a' flood-opacity='.12'/></filter>
  </defs>
  <rect width='1200' height='960' fill='#f6fbff'/>
  <rect x='42' y='38' width='1116' height='884' rx='44' fill='white' stroke='#bfdbfe' stroke-width='3'/>
  <rect x='74' y='72' width='1052' height='172' rx='36' fill='url(#hero)'/>
  <text x='108' y='120' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#bfdbfe' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING INFOGRAPHIC GUIDE</text>
  <text x='108' y='177' font-family='Inter,Arial,sans-serif' font-size='50' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='108' y='217' font-family='Inter,Arial,sans-serif' font-size='20' fill='#dcfce7'>{esc(HOOK)}</text>
  <text x='88' y='276' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>Six fields that keep AI-assisted action tracking accountable</text>
  {''.join(card_svg)}
  <text x='110' y='775' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>How to use the receipt</text>
  {''.join(step_svg)}
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

checks_html=''.join(f"<li><strong>{esc(label)}:</strong> {esc(text)}</li>" for label,text in checks)
steps_html=''.join(f"<li>{esc(step)}</li>" for step in usage_steps)
checks_md=''.join(f"- **{label}:** {text}\n" for label,text in checks)
steps_md=''.join(f"- {step}\n" for step in usage_steps)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f172a,#1d4ed8,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bfdbfe;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bfdbfe}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · AI meeting operations</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Six receipt fields</h2><ul>{checks_html}</ul></section><section class='card'><h2>How to use it</h2><ol>{steps_html}</ol></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Six receipt fields\n\n{checks_md}\n## How to use it\n\n{steps_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"""
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
manifest_path=pub_dir / 'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest=[m for m in manifest if m.get('slot') != SLOT and m.get('slug') != SLUG]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get('slot') == 'morning' else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links=''.join(f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a></li>" for m in manifest)
index=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>"""
(pub_dir / 'index.html').write_text(index, encoding='utf-8')
log=pub_dir / 'publish-log.md'
log.write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
evidence_dir=REPO / 'docs' / 'publication-evidence'; evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`\n\nLive targets after deployment:\n- {URL}\n- {PNG_URL}\n- {REPO_URL}\n""", encoding='utf-8')
info_dir=REPO / 'infographic' / SLUG; (info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: AI-assisted meeting action tracking.\n- Data type: educational checklist with six fields and three usage notes.\n- Layout: bento-grid / dashboard receipt.\n- Style: corporate Memphis with clean trust colors and card modules.\n- Audience: business operators using AI to summarize meetings and track actions.\n- Language: en.\n- Safety: educational only; no client, legal, compliance, medical, savings, ranking, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators convert meeting notes into accountable AI-assisted action tracking while keeping ownership, due windows, evidence, risk pauses, and close-loop status visible.\n\n## Receipt fields\n{checks_md}\n## Usage steps\n{steps_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean corporate Memphis bento-grid infographic titled '{TITLE}' using the six receipt fields and three usage steps from structured-content.md. Use blue/teal trust colors, white cards, numbered badges, clear hierarchy, and safe educational language. Aspect 16:9-ish wide worksheet.\n", encoding='utf-8')
# homepage latest card and link
home=REPO / 'index.html'
home_text=home.read_text(encoding='utf-8')
new_article=f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Decision</span><i></i><span>Owner</span><i></i><span>Close</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3>{TITLE}</h3>
            <p>{HOOK}</p>
          </article>'''
home_text=re.sub(r'          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true">.*?</article>', new_article, home_text, count=1, flags=re.S)
home_text=re.sub(r'/publications/\d{4}-\d{2}-\d{2}/[^"<>]+\.html">Review the [^<]+', f'/publications/{DATE}/{SLUG}.html">Review the AI meeting action receipt', home_text, count=1)
home.write_text(home_text, encoding='utf-8')
# sitemap + llms
sitemap=REPO / 'sitemap.xml'; sitemap_text=sitemap.read_text(encoding='utf-8')
index_entry=f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
page_entry=f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
if f'https://aicloudstrategist.com/publications/{DATE}/' not in sitemap_text:
    sitemap_text=sitemap_text.replace('</urlset>', index_entry + '</urlset>')
if URL not in sitemap_text:
    sitemap_text=sitemap_text.replace(index_entry, page_entry + index_entry)
sitemap.write_text(sitemap_text, encoding='utf-8')
llms=REPO/'llms.txt'
if llms.exists():
    txt=llms.read_text(encoding='utf-8')
    line=f'- [{TITLE}]({URL}) — safe educational AI meeting action receipt with infographic.\n'
    if URL not in txt:
        llms.write_text(txt.rstrip()+"\n"+line, encoding='utf-8')
print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
