from pathlib import Path
import csv, html, json, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-21'
SLOT = 'evening'
SLUG = 'cloud-cost-alert-triage-board'
TITLE = 'Cloud Cost Alert Triage Board: 7 Safe Checks Before Cutting Resources'
HOOK = 'A safe educational board for owners and operators to inspect cloud cost alerts without making risky shutdowns, performance promises, or savings claims.'
BOUNDARY = 'Educational operations guide only — not financial, legal, compliance, security, procurement, architecture, certification, savings, uptime, approval, or guaranteed-performance advice.'
BASE = f'https://aicloudstrategist.com/publications/{DATE}'
URL = f'{BASE}/{SLUG}.html'
PNG_URL = f'{BASE}/{SLUG}.png'
SVG_URL = f'{BASE}/{SLUG}.svg'
CSV_URL = f'{BASE}/{SLUG}.csv'
JSON_URL = f'{BASE}/{SLUG}-answer-card.json'
INDEX_URL = f'{BASE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    {'step':'1','check':'Confirm the alert window','owner_question':'Is the spike hourly, daily, monthly, or only a one-time reporting delay?','safe_action':'Compare the same service and time window before changing anything.'},
    {'step':'2','check':'Name the service owner','owner_question':'Who understands why this workload, storage bucket, model, job, or database exists?','safe_action':'Find the business owner and technical owner before shutdown decisions.'},
    {'step':'3','check':'Separate waste from work','owner_question':'Is this unused spend, planned activity, backup growth, testing, traffic, or a temporary batch job?','safe_action':'Tag the alert as investigate, expected, idle, duplicate, or unknown.'},
    {'step':'4','check':'Check customer and staff impact','owner_question':'Could stopping this resource affect customers, payments, support, reporting, staff, or compliance records?','safe_action':'Use a human approval line for any externally visible or sensitive system.'},
    {'step':'5','check':'Look for automation loops','owner_question':'Did a script, scheduler, retry queue, AI job, or integration create repeated usage?','safe_action':'Pause expansion paths before deleting core data or production resources.'},
    {'step':'6','check':'Document the decision','owner_question':'What evidence explains the alert, the owner, the proposed change, and the rollback path?','safe_action':'Record screenshots, IDs, timestamps, owners, and the reversible next step.'},
    {'step':'7','check':'Review after action','owner_question':'Did the change reduce noise without breaking the workload or hiding a real problem?','safe_action':'Review internal telemetry and owner feedback; avoid public savings claims.'},
]

def esc(v): return html.escape(str(v), quote=True)
def wrap(text, width=28, max_lines=4):
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
colors = ['#fee2e2','#ffedd5','#fef9c3','#dcfce7','#dbeafe','#ede9fe','#fce7f3']
strokes = ['#dc2626','#ea580c','#ca8a04','#16a34a','#2563eb','#7c3aed','#db2777']
positions = [(82,278),(410,278),(738,278),(1066,278),(246,566),(574,566),(902,566)]
cards=[]
for i,c in enumerate(checks):
    x,y=positions[i]
    title=''.join(f"<tspan x='{x+66}' dy='{0 if n==0 else 22}'>{t}</tspan>" for n,t in enumerate(wrap(c['check'],20,2)))
    q=''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{t}</tspan>" for n,t in enumerate(wrap(c['owner_question'],34,3)))
    a=''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{t}</tspan>" for n,t in enumerate(wrap(c['safe_action'],34,3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='280' height='226' rx='26' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+36}' cy='{y+38}' r='23' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+36}' y='{y+47}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+66}' y='{y+32}' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='950' fill='#111827'>{title}</text>
    <text x='{x+22}' y='{y+91}' font-family='Inter,Arial,sans-serif' font-size='10.5' font-weight='950' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+22}' y='{y+116}' font-family='Inter,Arial,sans-serif' font-size='12.2' font-weight='750' fill='#1f2937'>{q}</text>
    <text x='{x+22}' y='{y+174}' font-family='Inter,Arial,sans-serif' font-size='10.5' font-weight='950' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+22}' y='{y+198}' font-family='Inter,Arial,sans-serif' font-size='11.4' fill='#111827'>{a}</text>
  </g>""")
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='930' viewBox='0 0 1400 930'>
  <defs><linearGradient id='hero' x1='0' x2='1'><stop stop-color='#111827'/><stop offset='.45' stop-color='#0f766e'/><stop offset='1' stop-color='#f97316'/></linearGradient><filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#111827' flood-opacity='.16'/></filter></defs>
  <rect width='1400' height='930' fill='#f8fafc'/><rect x='40' y='34' width='1320' height='862' rx='48' fill='white' stroke='#fed7aa' stroke-width='3'/>
  <rect x='76' y='70' width='1248' height='166' rx='36' fill='url(#hero)'/>
  <text x='112' y='118' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#fed7aa' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='112' y='166' font-family='Inter,Arial,sans-serif' font-size='38' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='112' y='207' font-family='Inter,Arial,sans-serif' font-size='18' fill='#fffbeb'>{esc(HOOK)}</text>
  <g transform='translate(1162 96)'><rect width='126' height='96' rx='24' fill='rgba(255,255,255,.18)' stroke='#fed7aa'/><text x='63' y='38' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='26' font-weight='950' fill='white'>7</text><text x='63' y='66' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='850' fill='#ffedd5'>Triage checks</text></g>
  {''.join(cards)}
  <rect x='92' y='836' width='1216' height='60' rx='22' fill='#111827'/><text x='700' y='860' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='12.8' font-weight='850' fill='#fed7aa'>Inspect the alert window, owner, workload purpose, impact, loops, evidence and after-action review before cutting resources.</text><text x='700' y='883' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='11.2' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)
with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(checks[0].keys())); w.writeheader(); w.writerows(checks)
list_md=''.join(f"- **{c['step']}. {c['check']}:** Owner question: {c['owner_question']} Safe first action: {c['safe_action']}\n" for c in checks)
rows=''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['check'])}</strong></td><td>{esc(c['owner_question'])}</td><td>{esc(c['safe_action'])}</td></tr>" for c in checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script><style>body{{margin:0;background:#f8fafc;color:#142033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#111827,#0f766e,#f97316);color:white;border-radius:30px;padding:36px}}.kicker{{color:#fed7aa;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #fed7aa;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #fed7aa}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #fed7aa;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#111827;color:#e5f0ff}}a{{color:#0f766e;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · Cloud cost operations</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{esc(PNG_URL)}' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Seven safe checks</h2><table><thead><tr><th>#</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{esc(CSV_URL)}'>Download CSV worksheet</a> · <a href='{esc(JSON_URL)}'>Open AI-readable answer card</a></p></section><section class='card'><h2>Need a safe cloud-cost review?</h2><p>AICloudStrategist can run a free business review first, then a read-only cloud cost review with no production changes without approval. Start at <a href='https://aicloudstrategist.com/free-business-review/'>Free Business Review</a>, email <a href='mailto:contact@aicloudstrategist.com'>contact@aicloudstrategist.com</a>, or WhatsApp <a href='https://wa.me/918796302608'>+91 87963 02608</a>.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Seven safe checks\n\n{list_md}\nWorksheet: {CSV_URL}\nAI-readable card: {JSON_URL}\n\n**Truth boundary:** {BOUNDARY}\n\nPublic page: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer={'topic':TITLE,'date':DATE,'slot':SLOT,'url':URL,'infographic':PNG_URL,'csv':CSV_URL,'boundary':BOUNDARY,'checks':checks,'safe_scope':'Educational cloud cost alert triage checklist; no financial, legal, compliance, security, procurement, architecture, certification, savings, uptime, approval or performance guarantees.'}
(pub_dir / f'{SLUG}-answer-card.json').write_text(json.dumps(answer, indent=2), encoding='utf-8')
manifest_path=pub_dir/'manifest.json'
raw=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'date':DATE,'posts':[]}
manifest=raw.get('posts', raw) if isinstance(raw,dict) else raw
manifest=[m for m in manifest if not (m.get('slot')==SLOT or m.get('slug')==SLUG)]
manifest.append({'slot':SLOT,'slug':SLUG,'title':TITLE,'url':URL,'png':PNG_URL,'svg':SVG_URL,'csv':CSV_URL,'answer_card':JSON_URL,'repository':REPO_URL,'boundary':BOUNDARY})
manifest.sort(key=lambda m:{'morning':0,'evening':1}.get(m.get('slot'),9))
manifest_path.write_text(json.dumps({'date':DATE,'posts':manifest}, indent=2), encoding='utf-8')
links=''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a> · <a href='{esc(m['answer_card'].split('/')[-1])}'>answer card</a></li>" for m in manifest)
(pub_dir/'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable worksheets.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#2563eb;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, financial, security, certification, procurement, revenue, savings, approval, or guaranteed-performance advice.</p><ul>{links}</ul><p><strong>Need a practical review?</strong> Request a free business review through <a href='/free-business-review/'>AICloudStrategist</a>, email <a href='mailto:contact@aicloudstrategist.com'>contact@aicloudstrategist.com</a>, or WhatsApp <a href='https://wa.me/918796302608'>+91 87963 02608</a>.</p></section></main></body></html>", encoding='utf-8')
(pub_dir/'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror=Path('/home/agent/.hermes/aicloudstrategist/publications')/DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror/'publish-log.md').write_text((pub_dir/'publish-log.md').read_text(), encoding='utf-8')
info_dir=REPO/'infographic'/SLUG
(info_dir/'prompts').mkdir(parents=True, exist_ok=True)
(info_dir/'source.md').write_text(post_md, encoding='utf-8')
(info_dir/'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: Cloud cost alert triage.\n- Data type: safe educational checklist.\n- Layout: bento-grid.\n- Style: corporate-memphis / operations board.\n- Audience: owners, operators and technical managers reviewing cloud cost alerts.\n- Safety: educational only; no financial, legal, compliance, security, procurement, architecture, certification, savings, uptime, approval or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir/'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp owners inspect cloud cost alerts safely before making risky resource cuts.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir/'prompts'/'infographic.md').write_text(f"Create a bento-grid infographic titled '{TITLE}'. Seven numbered rounded cards with check, owner question and safe first action. Use clean corporate memphis style, teal/orange accents, white background, clear labels, and footer truth boundary.\n", encoding='utf-8')
home=REPO/'index.html'
if home.exists():
    t=home.read_text(encoding='utf-8')
    card=f'''          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Alert</span><i></i><span>Owner</span><i></i><span>Review</span></div>\n            <span class="ea-evidence-type">Public educational asset · {DATE}</span>\n            <h3><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h3>\n            <p>{esc(HOOK)}</p>\n          </article>\n\n'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        marker='          <article class="ea-evidence-item">\n'
        t=t.replace(marker, card+marker, 1) if marker in t else t.replace('</main>', card+'</main>',1)
        home.write_text(t, encoding='utf-8')
resources=REPO/'resources'/'index.html'
if resources.exists():
    t=resources.read_text(encoding='utf-8')
    card=f'''<article class="card" data-resource-card="{SLUG}"><h2><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href="/publications/{DATE}/{SLUG}.csv">Download cloud cost alert worksheet CSV</a> · <a href="/publications/{DATE}/{SLUG}-answer-card.json">Open AI-answer source card JSON</a></p></article>'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        t=t.replace('<article class="card"', card+'<article class="card"', 1) if '<article class="card"' in t else t.replace('</main>', card+'</main>',1)
        resources.write_text(t, encoding='utf-8')
llms=REPO/'llms.txt'
if llms.exists():
    t=llms.read_text(encoding='utf-8')
    for line in [f'- [{TITLE}]({URL}) — safe cloud cost alert triage checklist with infographic.\n', f'- [Cloud cost alert worksheet CSV]({CSV_URL}) — alert window, owner, workload purpose, impact, loop, evidence and review worksheet.\n', f'- [Cloud cost alert card JSON]({JSON_URL}) — concise LLM-readable safe-scope and blocked-claim boundary.\n']:
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
