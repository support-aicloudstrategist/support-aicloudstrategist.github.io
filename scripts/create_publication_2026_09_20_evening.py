from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-20'
SLOT = 'evening'
SLUG = 'clinic-missed-call-recovery-map'
TITLE = 'Clinic Missed-Call Recovery Map: 7 Safe Checks Before Automating Follow-Up'
HOOK = 'A safe educational checklist for clinics and service businesses to tighten missed-call handling before adding bots, auto-replies or dashboards.'
BOUNDARY = 'Educational operations guide only — not medical, legal, compliance, financial, marketing, revenue, savings, patient-growth, clinical, approval, or guaranteed-performance advice.'
BASE = f'https://aicloudstrategist.com/publications/{DATE}'
URL = f'{BASE}/{SLUG}.html'
PNG_URL = f'{BASE}/{SLUG}.png'
SVG_URL = f'{BASE}/{SLUG}.svg'
CSV_URL = f'{BASE}/{SLUG}.csv'
JSON_URL = f'{BASE}/{SLUG}-answer-card.json'
INDEX_URL = f'{BASE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    {'step':'1','check':'Capture every call route','owner_question':'Which numbers, WhatsApp links, ads, reception lines and website buttons can create missed calls?','safe_action':'List each route before changing automation or scripts.'},
    {'step':'2','check':'Separate urgent from routine','owner_question':'Which missed calls may need human judgment because they mention care, symptoms, complaints or sensitive data?','safe_action':'Use human review for sensitive or unclear items; do not let bots assess care needs.'},
    {'step':'3','check':'Confirm consent-safe follow-up','owner_question':'What follow-up channel is appropriate: callback, WhatsApp, SMS, email or no message?','safe_action':'Use clear, minimal, non-diagnostic wording and respect opt-outs.'},
    {'step':'4','check':'Time-box the first response','owner_question':'Who owns the first callback window, backup owner and escalation if reception is busy?','safe_action':'Create a visible owner rota before buying another tool.'},
    {'step':'5','check':'Track reason codes','owner_question':'Was the missed call caused by after-hours timing, busy staff, wrong number, ad mismatch, pricing query or appointment question?','safe_action':'Record a simple reason code so fixes target the real leak.'},
    {'step':'6','check':'Protect private data','owner_question':'Could the note, recording, screenshot or bot transcript expose patient, customer or staff information?','safe_action':'Keep logs minimal, role-limited and free of unnecessary sensitive details.'},
    {'step':'7','check':'Review weekly patterns','owner_question':'Which repeat pattern should be fixed this week: staffing window, website CTA, ad promise, call routing or follow-up wording?','safe_action':'Improve one bottleneck at a time and label results as internal observations only.'},
]

def esc(v):
    return html.escape(str(v), quote=True)

def wrap(text, width=32, max_lines=4):
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
colors = ['#dbeafe','#dcfce7','#fef3c7','#fce7f3','#ede9fe','#cffafe','#fee2e2']
strokes = ['#2563eb','#16a34a','#d97706','#db2777','#7c3aed','#0891b2','#dc2626']
positions = [(76,288),(390,288),(704,288),(1018,288),(236,578),(550,578),(864,578)]
cards=[]
for i,c in enumerate(checks):
    x,y=positions[i]
    title=''.join(f"<tspan x='{x+62}' dy='{0 if n==0 else 22}'>{t}</tspan>" for n,t in enumerate(wrap(c['check'],18,2)))
    q=''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{t}</tspan>" for n,t in enumerate(wrap(c['owner_question'],37,4)))
    a=''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{t}</tspan>" for n,t in enumerate(wrap(c['safe_action'],37,3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='266' height='232' rx='26' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+34}' cy='{y+36}' r='22' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+34}' y='{y+44}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+62}' y='{y+32}' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#0f172a'>{title}</text>
    <text x='{x+22}' y='{y+96}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+22}' y='{y+120}' font-family='Inter,Arial,sans-serif' font-size='12.2' font-weight='750' fill='#1e293b'>{q}</text>
    <text x='{x+22}' y='{y+186}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+22}' y='{y+207}' font-family='Inter,Arial,sans-serif' font-size='11.6' fill='#0f172a'>{a}</text>
  </g>""")
svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='930' viewBox='0 0 1400 930'>
  <defs><linearGradient id='hero' x1='0' x2='1'><stop stop-color='#082f49'/><stop offset='.55' stop-color='#0369a1'/><stop offset='1' stop-color='#14b8a6'/></linearGradient><filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#0f172a' flood-opacity='.16'/></filter></defs>
  <rect width='1400' height='930' fill='#f0f9ff'/><rect x='38' y='34' width='1324' height='862' rx='48' fill='white' stroke='#bae6fd' stroke-width='3'/>
  <rect x='76' y='70' width='1248' height='174' rx='36' fill='url(#hero)'/>
  <text x='112' y='118' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#a7f3d0' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='112' y='166' font-family='Inter,Arial,sans-serif' font-size='37' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='112' y='207' font-family='Inter,Arial,sans-serif' font-size='18' fill='#e0f2fe'>{esc(HOOK)}</text>
  <g transform='translate(1162 98)'><rect width='126' height='98' rx='24' fill='rgba(255,255,255,.18)' stroke='#a7f3d0'/><text x='63' y='38' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='26' font-weight='950' fill='white'>7</text><text x='63' y='66' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='850' fill='#dff7ff'>Safe checks</text></g>
  {''.join(cards)}
  <rect x='92' y='848' width='1216' height='48' rx='22' fill='#0f172a'/><text x='700' y='868' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#a7f3d0'>Start with call routes, sensitivity, consent-safe channel, owner rota, reason codes, privacy and weekly pattern review.</text><text x='700' y='888' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='11.4' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)
with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(checks[0].keys())); w.writeheader(); w.writerows(checks)
list_md=''.join(f"- **{c['step']}. {c['check']}:** Owner question: {c['owner_question']} Safe first action: {c['safe_action']}\n" for c in checks)
rows=''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['check'])}</strong></td><td>{esc(c['owner_question'])}</td><td>{esc(c['safe_action'])}</td></tr>" for c in checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script><style>body{{margin:0;background:#f0f9ff;color:#142033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#082f49,#0369a1,#14b8a6);color:white;border-radius:30px;padding:36px}}.kicker{{color:#a7f3d0;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #bae6fd;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bae6fd}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #bae6fd;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#0f172a;color:#e5f0ff}}a{{color:#0369a1;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · missed-call recovery</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{esc(PNG_URL)}' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Seven safe checks</h2><table><thead><tr><th>#</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{CSV_URL}'>Download CSV worksheet</a> · <a href='{JSON_URL}'>Open AI-answer source card JSON</a> · <a href='{SVG_URL}'>Open SVG</a></p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Seven safe checks\n\n{list_md}\nWorksheet: {CSV_URL}\nAI-readable card: {JSON_URL}\n\n**Truth boundary:** {BOUNDARY}\n\nPublic page: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer={'topic':TITLE,'date':DATE,'slot':SLOT,'url':URL,'infographic':PNG_URL,'csv':CSV_URL,'boundary':BOUNDARY,'checks':checks,'safe_scope':'Educational checklist for operational missed-call recovery; no medical, legal, compliance, financial, marketing, revenue, savings, patient-growth, clinical, approval or performance guarantees.'}
(pub_dir / f'{SLUG}-answer-card.json').write_text(json.dumps(answer, indent=2), encoding='utf-8')
manifest_path=pub_dir/'manifest.json'
raw=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'date':DATE,'posts':[]}
manifest=raw.get('posts', raw) if isinstance(raw,dict) else raw
manifest=[m for m in manifest if not (m.get('slot')==SLOT or m.get('slug')==SLUG)]
manifest.append({'slot':SLOT,'slug':SLUG,'title':TITLE,'url':URL,'png':PNG_URL,'svg':SVG_URL,'csv':CSV_URL,'answer_card':JSON_URL,'repository':REPO_URL,'boundary':BOUNDARY})
manifest.sort(key=lambda m:{'morning':0,'evening':1}.get(m.get('slot'),9))
manifest_path.write_text(json.dumps({'date':DATE,'posts':manifest}, indent=2), encoding='utf-8')
links=''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a> · <a href='{esc(m['answer_card'].split('/')[-1])}'>answer card</a></li>" for m in manifest)
(pub_dir/'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable worksheets.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#0369a1;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not medical, legal, compliance, financial, security, certification, revenue, savings, patient-growth, approval, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir/'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror=Path('/home/agent/.hermes/aicloudstrategist/publications')/DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror/'publish-log.md').write_text((pub_dir/'publish-log.md').read_text(), encoding='utf-8')
info_dir=REPO/'infographic'/SLUG
(info_dir/'prompts').mkdir(parents=True, exist_ok=True)
(info_dir/'source.md').write_text(post_md, encoding='utf-8')
(info_dir/'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: clinic missed-call recovery.\n- Data type: safe educational checklist.\n- Layout: bento-grid.\n- Style: corporate-memphis / clean operational dashboard.\n- Audience: clinics and service businesses.\n- Safety: educational only; no medical, legal, compliance, financial, marketing, revenue, savings, patient-growth, clinical, approval or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir/'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators tighten missed-call recovery before adding bots, auto-replies or dashboards.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir/'prompts'/'infographic.md').write_text(f"Create a bento-grid infographic titled '{TITLE}'. Seven numbered rounded cards with check, owner question and safe first action. Use clean corporate memphis style, teal/blue/green accents, white background, clear labels, and footer truth boundary.\n", encoding='utf-8')
# index/resource discovery
home=REPO/'index.html'
if home.exists():
    t=home.read_text(encoding='utf-8')
    card=f'''          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Call</span><i></i><span>Owner</span><i></i><span>Review</span></div>\n            <span class="ea-evidence-type">Public educational asset · {DATE}</span>\n            <h3><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h3>\n            <p>{esc(HOOK)}</p>\n          </article>\n\n'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        marker='          <article class="ea-evidence-item">\n'
        t=t.replace(marker, card+marker, 1) if marker in t else t.replace('</main>', card+'</main>',1)
        home.write_text(t, encoding='utf-8')
resources=REPO/'resources'/'index.html'
if resources.exists():
    t=resources.read_text(encoding='utf-8')
    card=f'''<article class="card" data-resource-card="{SLUG}"><h2><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href="/publications/{DATE}/{SLUG}.csv">Download missed-call recovery worksheet CSV</a> · <a href="/publications/{DATE}/{SLUG}-answer-card.json">Open AI-answer source card JSON</a></p></article>'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        t=t.replace('<article class="card"', card+'<article class="card"', 1) if '<article class="card"' in t else t.replace('</main>', card+'</main>',1)
        resources.write_text(t, encoding='utf-8')
llms=REPO/'llms.txt'
if llms.exists():
    t=llms.read_text(encoding='utf-8')
    for line in [f'- [{TITLE}]({URL}) — safe missed-call recovery checklist with infographic.\n', f'- [Clinic missed-call recovery worksheet CSV]({CSV_URL}) — route, owner, consent-safe channel and weekly pattern review worksheet.\n', f'- [Clinic missed-call recovery card JSON]({JSON_URL}) — concise LLM-readable safe-scope and blocked-claim boundary.\n']:
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
