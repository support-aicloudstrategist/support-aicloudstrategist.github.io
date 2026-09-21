from pathlib import Path
import csv, html, json, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-21'
SLOT = 'morning'
SLUG = 'ai-tool-sprawl-control-map'
TITLE = 'AI Tool Sprawl Control Map: 6 Safe Questions Before Adding Another App'
HOOK = 'A safe educational checklist for owners to reduce duplicate tools, unclear data flows and unmanaged AI usage before buying another subscription.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, financial, security, procurement, certification, revenue, savings, approval, or guaranteed-performance advice.'
BASE = f'https://aicloudstrategist.com/publications/{DATE}'
URL = f'{BASE}/{SLUG}.html'
PNG_URL = f'{BASE}/{SLUG}.png'
SVG_URL = f'{BASE}/{SLUG}.svg'
CSV_URL = f'{BASE}/{SLUG}.csv'
JSON_URL = f'{BASE}/{SLUG}-answer-card.json'
INDEX_URL = f'{BASE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    {'step':'1','check':'Name the business problem','owner_question':'What work is actually slow, risky or duplicated today?','safe_action':'Write the problem in plain language before comparing AI features.'},
    {'step':'2','check':'Map the current tools','owner_question':'Which apps already collect, store, summarize or send the same information?','safe_action':'List owners, logins, costs and data touched by each tool.'},
    {'step':'3','check':'Find the handoff point','owner_question':'Where does work move from customer, staff, vendor, inbox, spreadsheet or dashboard?','safe_action':'Fix the handoff rule before adding another automation layer.'},
    {'step':'4','check':'Set a human approval line','owner_question':'Which outputs may affect customers, payments, staff, private data or public claims?','safe_action':'Keep human review for sensitive or externally visible outputs.'},
    {'step':'5','check':'Decide what not to connect','owner_question':'Which files, inboxes, chats or records should stay out of the pilot?','safe_action':'Start with the smallest safe data set and document exclusions.'},
    {'step':'6','check':'Review before renewal','owner_question':'What evidence will show whether this tool should expand, pause or be removed?','safe_action':'Use internal observations and owner feedback; avoid inflated ROI claims.'},
]

def esc(v): return html.escape(str(v), quote=True)
def wrap(text, width=30, max_lines=4):
    out=[]; line=''
    for word in esc(text).split():
        if len((line+' '+word).strip()) > width:
            if line: out.append(line)
            line=word
        else:
            line=(line+' '+word).strip()
    if line: out.append(line)
    return out[:max_lines]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)
colors = ['#e0f2fe','#dcfce7','#fef9c3','#fae8ff','#e0e7ff','#ffedd5']
strokes = ['#0284c7','#16a34a','#ca8a04','#c026d3','#4f46e5','#ea580c']
positions = [(88,286),(476,286),(864,286),(88,586),(476,586),(864,586)]
cards=[]
for i,c in enumerate(checks):
    x,y=positions[i]
    title=''.join(f"<tspan x='{x+70}' dy='{0 if n==0 else 24}'>{t}</tspan>" for n,t in enumerate(wrap(c['check'],22,2)))
    q=''.join(f"<tspan x='{x+24}' dy='{0 if n==0 else 17}'>{t}</tspan>" for n,t in enumerate(wrap(c['owner_question'],42,3)))
    a=''.join(f"<tspan x='{x+24}' dy='{0 if n==0 else 17}'>{t}</tspan>" for n,t in enumerate(wrap(c['safe_action'],42,3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='330' height='244' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+38}' cy='{y+40}' r='24' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+38}' y='{y+49}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+70}' y='{y+34}' font-family='Inter,Arial,sans-serif' font-size='19' font-weight='950' fill='#111827'>{title}</text>
    <text x='{x+24}' y='{y+104}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='950' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+24}' y='{y+129}' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='750' fill='#1f2937'>{q}</text>
    <text x='{x+24}' y='{y+190}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='950' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+24}' y='{y+213}' font-family='Inter,Arial,sans-serif' font-size='12.4' fill='#111827'>{a}</text>
  </g>""")
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='930' viewBox='0 0 1400 930'>
  <defs><linearGradient id='hero' x1='0' x2='1'><stop stop-color='#111827'/><stop offset='.55' stop-color='#2563eb'/><stop offset='1' stop-color='#22c55e'/></linearGradient><filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#111827' flood-opacity='.16'/></filter></defs>
  <rect width='1400' height='930' fill='#f8fafc'/><rect x='40' y='34' width='1320' height='862' rx='48' fill='white' stroke='#dbeafe' stroke-width='3'/>
  <rect x='76' y='70' width='1248' height='174' rx='36' fill='url(#hero)'/>
  <text x='112' y='118' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#bbf7d0' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING INFOGRAPHIC</text>
  <text x='112' y='166' font-family='Inter,Arial,sans-serif' font-size='38' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='112' y='207' font-family='Inter,Arial,sans-serif' font-size='18' fill='#eff6ff'>{esc(HOOK)}</text>
  <g transform='translate(1162 98)'><rect width='126' height='98' rx='24' fill='rgba(255,255,255,.18)' stroke='#bbf7d0'/><text x='63' y='38' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='26' font-weight='950' fill='white'>6</text><text x='63' y='66' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='850' fill='#dcfce7'>Safe checks</text></g>
  {''.join(cards)}
  <rect x='92' y='852' width='1216' height='44' rx='22' fill='#111827'/><text x='700' y='870' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='12.8' font-weight='850' fill='#bbf7d0'>Control sprawl by naming the problem, mapping tools, fixing handoffs, defining human review, limiting data and reviewing renewals.</text><text x='700' y='889' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='11.2' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)
with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(checks[0].keys())); w.writeheader(); w.writerows(checks)
list_md=''.join(f"- **{c['step']}. {c['check']}:** Owner question: {c['owner_question']} Safe first action: {c['safe_action']}\n" for c in checks)
rows=''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['check'])}</strong></td><td>{esc(c['owner_question'])}</td><td>{esc(c['safe_action'])}</td></tr>" for c in checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script><style>body{{margin:0;background:#f8fafc;color:#142033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#111827,#2563eb,#22c55e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bbf7d0;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #dbeafe;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #dbeafe}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #dbeafe;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#111827;color:#e5f0ff}}a{{color:#2563eb;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · AI operations</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Six safe questions</h2><table><thead><tr><th>#</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section><section class='card'><h2>Reusable assets</h2><p><a href='{SLUG}.csv'>Download worksheet CSV</a> · <a href='{SLUG}-answer-card.json'>Open AI-answer source card JSON</a> · <a href='{SLUG}.svg'>Open SVG</a></p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Six safe questions\n\n{list_md}\nWorksheet: {CSV_URL}\nAI-readable card: {JSON_URL}\n\n**Truth boundary:** {BOUNDARY}\n\nPublic page: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer={'topic':TITLE,'date':DATE,'slot':SLOT,'url':URL,'infographic':PNG_URL,'csv':CSV_URL,'boundary':BOUNDARY,'checks':checks,'safe_scope':'Educational tool-sprawl control checklist; no legal, compliance, financial, security, procurement, certification, revenue, savings, approval or performance guarantees.'}
(pub_dir / f'{SLUG}-answer-card.json').write_text(json.dumps(answer, indent=2), encoding='utf-8')
manifest_path=pub_dir/'manifest.json'
raw=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'date':DATE,'posts':[]}
manifest=raw.get('posts', raw) if isinstance(raw,dict) else raw
manifest=[m for m in manifest if not (m.get('slot')==SLOT or m.get('slug')==SLUG)]
manifest.append({'slot':SLOT,'slug':SLUG,'title':TITLE,'url':URL,'png':PNG_URL,'svg':SVG_URL,'csv':CSV_URL,'answer_card':JSON_URL,'repository':REPO_URL,'boundary':BOUNDARY})
manifest.sort(key=lambda m:{'morning':0,'evening':1}.get(m.get('slot'),9))
manifest_path.write_text(json.dumps({'date':DATE,'posts':manifest}, indent=2), encoding='utf-8')
links=''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a> · <a href='{esc(m['answer_card'].split('/')[-1])}'>answer card</a></li>" for m in manifest)
(pub_dir/'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable worksheets.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#2563eb;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, financial, security, certification, procurement, revenue, savings, approval, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir/'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror=Path('/home/agent/.hermes/aicloudstrategist/publications')/DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror/'publish-log.md').write_text((pub_dir/'publish-log.md').read_text(), encoding='utf-8')
info_dir=REPO/'infographic'/SLUG
(info_dir/'prompts').mkdir(parents=True, exist_ok=True)
(info_dir/'source.md').write_text(post_md, encoding='utf-8')
(info_dir/'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: AI tool sprawl control.\n- Data type: safe educational checklist.\n- Layout: bento-grid.\n- Style: corporate-memphis / operational dashboard.\n- Audience: owners and operators considering AI apps.\n- Safety: educational only; no legal, compliance, financial, security, procurement, certification, revenue, savings, approval or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir/'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp owners reduce duplicate tools, unclear data flows and unmanaged AI usage before buying another subscription.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir/'prompts'/'infographic.md').write_text(f"Create a bento-grid infographic titled '{TITLE}'. Six numbered rounded cards with check, owner question and safe first action. Use clean corporate memphis style, blue/green accents, white background, clear labels, and footer truth boundary.\n", encoding='utf-8')
home=REPO/'index.html'
if home.exists():
    t=home.read_text(encoding='utf-8')
    card=f'''          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Problem</span><i></i><span>Tools</span><i></i><span>Review</span></div>\n            <span class="ea-evidence-type">Public educational asset · {DATE}</span>\n            <h3><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h3>\n            <p>{esc(HOOK)}</p>\n          </article>\n\n'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        marker='          <article class="ea-evidence-item">\n'
        t=t.replace(marker, card+marker, 1) if marker in t else t.replace('</main>', card+'</main>',1)
        home.write_text(t, encoding='utf-8')
resources=REPO/'resources'/'index.html'
if resources.exists():
    t=resources.read_text(encoding='utf-8')
    card=f'''<article class="card" data-resource-card="{SLUG}"><h2><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href="/publications/{DATE}/{SLUG}.csv">Download tool-sprawl worksheet CSV</a> · <a href="/publications/{DATE}/{SLUG}-answer-card.json">Open AI-answer source card JSON</a></p></article>'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        t=t.replace('<article class="card"', card+'<article class="card"', 1) if '<article class="card"' in t else t.replace('</main>', card+'</main>',1)
        resources.write_text(t, encoding='utf-8')
llms=REPO/'llms.txt'
if llms.exists():
    t=llms.read_text(encoding='utf-8')
    for line in [f'- [{TITLE}]({URL}) — safe AI tool-sprawl control checklist with infographic.\n', f'- [AI tool-sprawl worksheet CSV]({CSV_URL}) — problem, current tools, handoff, review line, excluded data and renewal review worksheet.\n', f'- [AI tool-sprawl card JSON]({JSON_URL}) — concise LLM-readable safe-scope and blocked-claim boundary.\n']:
        link=line.split('](')[1].split(')')[0]
        if link not in t: t=t.rstrip()+'\n'+line
    llms.write_text(t, encoding='utf-8')
builder=REPO/'scripts'/'build_sitemap.py'
if builder.exists(): subprocess.run(['python3', str(builder)], cwd=str(REPO), check=True)
sitemap=REPO/'sitemap.xml'
if sitemap.exists():
    st=sitemap.read_text(encoding='utf-8')
    for loc,prio in [(URL,'0.6'),(PNG_URL,'0.5'),(SVG_URL,'0.5'),(CSV_URL,'0.5'),(JSON_URL,'0.5'),(INDEX_URL,'0.6')]:
        if loc not in st:
            st=st.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
    sitemap.write_text(st, encoding='utf-8')
print(json.dumps({'slot':SLOT,'title':TITLE,'url':URL,'png':PNG_URL,'csv':CSV_URL,'answer_card':JSON_URL,'repository':REPO_URL}, indent=2))
