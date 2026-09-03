from pathlib import Path
import html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-03'
SLOT = 'morning'
SLUG = 'ai-source-evidence-card'
TITLE = 'The AI Source Evidence Card'
HOOK = 'A safe educational checklist for keeping AI-assisted business work grounded in approved sources before an answer, draft, or decision moves forward.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, medical, financial, security, certification, revenue, savings, ranking, customer-result, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    ('Source named', 'Write the document, page, record, owner, or example the AI is allowed to use.'),
    ('Date checked', 'Mark when the source was last reviewed so old instructions do not look current.'),
    ('Permission level', 'Separate public, internal, confidential, customer, payment, and credential material.'),
    ('Answer boundary', 'State what the AI may draft, what it must not claim, and where it must pause.'),
    ('Human reviewer', 'Assign a person to approve sensitive, uncertain, brand, pricing, or policy-impacting output.'),
    ('Evidence saved', 'Keep source link, prompt, draft, review note, final action, and correction trail.'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(str(s), quote=True)
def wrap(text, width=38, max_lines=4):
    words = esc(text).split(); lines=[]; line=''
    for word in words:
        if len((line + ' ' + word).strip()) > width:
            if line: lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line: lines.append(line)
    return lines[:max_lines]

cards=[]
icons = ['📄', '🕒', '🔐', '⛔', '👤', '🧾']
for i,(head,body) in enumerate(checks):
    col=i%3; row=i//3
    x=76+col*362; y=292+row*250
    body_lines=''.join(f"<tspan x='{x+32}' dy='{0 if n==0 else 22}'>{ln}</tspan>" for n,ln in enumerate(wrap(body, 38, 4)))
    cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='318' height='206' rx='30' fill='white' stroke='#d7e3f4' stroke-width='2'/>
      <rect x='{x+28}' y='{y+28}' width='54' height='54' rx='18' fill='#e0f2fe' stroke='#38bdf8'/>
      <text x='{x+55}' y='{y+65}' text-anchor='middle' font-family='Apple Color Emoji,Segoe UI Emoji,Noto Color Emoji,sans-serif' font-size='26'>{icons[i]}</text>
      <text x='{x+98}' y='{y+60}' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='#0f172a'>{esc(head)}</text>
      <text x='{x+32}' y='{y+118}' font-family='Inter,Arial,sans-serif' font-size='18' fill='#334155'>{body_lines}</text>
    </g>""")

svg=f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#082f49'/><stop offset='.55' stop-color='#0369a1'/><stop offset='1' stop-color='#0f766e'/></linearGradient>
    <filter id='shadow' x='-15%' y='-20%' width='130%' height='150%'><feDropShadow dx='0' dy='16' stdDeviation='11' flood-color='#0f172a' flood-opacity='.12'/></filter>
  </defs>
  <rect width='1200' height='900' fill='#f7fbff'/>
  <rect x='36' y='34' width='1128' height='832' rx='44' fill='white' stroke='#cfe0f7' stroke-width='3'/>
  <rect x='70' y='68' width='1060' height='168' rx='36' fill='url(#hero)'/>
  <text x='106' y='116' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#bae6fd' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING INFOGRAPHIC</text>
  <text x='106' y='174' font-family='Inter,Arial,sans-serif' font-size='52' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='106' y='214' font-family='Inter,Arial,sans-serif' font-size='20' fill='#ccfbf1'>{esc(HOOK)}</text>
  <text x='80' y='270' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>Six source checks before AI work becomes business output</text>
  {''.join(cards)}
  <rect x='78' y='812' width='1044' height='36' rx='18' fill='#f8fafc' stroke='#cbd5e1'/>
  <text x='600' y='836' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='14' fill='#64748b'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

checks_html=''.join(f"<li><strong>{esc(h)}:</strong> {esc(b)}</li>" for h,b in checks)
checks_md=''.join(f"- **{h}:** {b}\n" for h,b in checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f7fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#082f49,#0369a1,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bae6fd;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bfdbfe}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · AI source evidence</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Six source evidence checks</h2><ul>{checks_html}</ul></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Six source evidence checks\n\n{checks_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"""
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
manifest_path=pub_dir / 'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest=[m for m in manifest if m.get('slot') != SLOT and m.get('slug') != SLUG]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get('slot') == 'morning' else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links=''.join(f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a></li>" for m in manifest)
(pub_dir / 'index.html').write_text(f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>""", encoding='utf-8')
(pub_dir / 'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror = Path('/home/agent/.hermes/aicloudstrategist/publications') / DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror / 'publish-log.md').write_text((pub_dir / 'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

evidence_dir=REPO / 'docs' / 'publication-evidence'; evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`\n\nLive targets after deployment:\n- {URL}\n- {PNG_URL}\n- {REPO_URL}\n""", encoding='utf-8')
info_dir=REPO / 'infographic' / SLUG; (info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: safe AI source evidence before business output.\n- Data type: educational checklist with six source-grounding checks.\n- Layout: bento-grid / dense modular cards.\n- Style: corporate Memphis with clean blue/teal trust colors.\n- Audience: business operators using AI assistants.\n- Language: en.\n- Safety: educational only; no client, legal, compliance, medical, savings, ranking, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators keep AI-assisted business work grounded in approved sources before an answer, draft, or decision moves forward.\n\n## Six source evidence checks\n{checks_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean corporate Memphis bento-grid infographic titled '{TITLE}' using six numbered source-evidence cards, blue/teal trust colors, rounded modular cards, clear hierarchy, and safe educational language. Aspect 4:3 worksheet.\n", encoding='utf-8')

home=REPO / 'index.html'
home_text=home.read_text(encoding='utf-8')
new_article=f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Source</span><i></i><span>Boundary</span><i></i><span>Evidence</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3>{TITLE}</h3>
            <p>{HOOK}</p>
          </article>'''
home_text=re.sub(r'          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true">.*?</article>', new_article, home_text, count=1, flags=re.S)
home_text=re.sub(r'/publications/\d{4}-\d{2}-\d{2}/[^"<>]+\.html">Review the [^<]+', f'/publications/{DATE}/{SLUG}.html">Review the AI source evidence card', home_text, count=1)
home.write_text(home_text, encoding='utf-8')
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
    line=f'- [{TITLE}]({URL}) — safe educational AI source evidence checklist with infographic.\n'
    if URL not in txt:
        llms.write_text(txt.rstrip()+"\n"+line, encoding='utf-8')
print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
