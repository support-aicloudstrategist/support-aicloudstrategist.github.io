from pathlib import Path
import csv, html, json, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-10-06'
SLOT = 'evening'
SLUG = 'ai-vendor-claim-reality-check'
TITLE = 'AI Vendor Claim Reality Check: 8 Questions Before You Buy or Automate'
HOOK = 'A safe educational checklist for owners to inspect AI promises, demos, data use, handoffs, support, lock-in and human approval before committing.'
BOUNDARY = 'Educational buyer-readiness guide only — not legal, compliance, procurement, financial, security, certification, vendor-selection, contract, savings, revenue, or guaranteed-performance advice.'
BASE = f'https://aicloudstrategist.com/publications/{DATE}'
URL = f'{BASE}/{SLUG}.html'
PNG_URL = f'{BASE}/{SLUG}.png'
SVG_URL = f'{BASE}/{SLUG}.svg'
CSV_URL = f'{BASE}/{SLUG}.csv'
JSON_URL = f'{BASE}/{SLUG}-answer-card.json'
INDEX_URL = f'{BASE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    {'step':'1','question':'What problem is being solved?','safe_check':'Write the business pain in plain language before comparing AI features.'},
    {'step':'2','question':'What evidence is real?','safe_check':'Separate live proof, demo footage, internal benchmark and marketing claim.'},
    {'step':'3','question':'What data is touched?','safe_check':'List customer, staff, payment, health, legal, support and operational data before connecting tools.'},
    {'step':'4','question':'Where does a human approve?','safe_check':'Keep human approval for refunds, promises, pricing, sensitive answers and account changes.'},
    {'step':'5','question':'What happens when it is wrong?','safe_check':'Define fallback owner, correction path, logs and customer-safe recovery steps.'},
    {'step':'6','question':'Can we exit cleanly?','safe_check':'Check export, deletion, portability, admin access and dependency risk before lock-in.'},
    {'step':'7','question':'Who supports day two?','safe_check':'Name the owner for monitoring, prompts, model changes, permissions and incident review.'},
    {'step':'8','question':'How will value be measured?','safe_check':'Use internal before-after measures; avoid public savings or revenue claims without evidence.'},
]

def esc(v): return html.escape(str(v), quote=True)
def wrap(text, width=24, max_lines=3):
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
colors = ['#e0f2fe','#dcfce7','#fef9c3','#ffedd5','#ede9fe','#fce7f3','#ccfbf1','#fee2e2']
strokes = ['#0284c7','#16a34a','#ca8a04','#ea580c','#7c3aed','#db2777','#0f766e','#dc2626']
positions = [(72,270),(392,270),(712,270),(1032,270),(72,560),(392,560),(712,560),(1032,560)]
cards=[]
for i,c in enumerate(checks):
    x,y=positions[i]
    q=''.join(f"<tspan x='{x+68}' dy='{0 if n==0 else 23}'>{t}</tspan>" for n,t in enumerate(wrap(c['question'],22,2)))
    a=''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 17}'>{t}</tspan>" for n,t in enumerate(wrap(c['safe_check'],35,4)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='292' height='230' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+38}' cy='{y+42}' r='24' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+38}' y='{y+51}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+68}' y='{y+34}' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#111827'>{q}</text>
    <text x='{x+22}' y='{y+112}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='950' fill='#475569'>SAFE CHECK</text>
    <text x='{x+22}' y='{y+140}' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='760' fill='#111827'>{a}</text>
  </g>""")
svg=f"""<svg xmlns='http://www.w3.org/2000/svg' width='1400' height='900' viewBox='0 0 1400 900'>
  <defs><linearGradient id='hero' x1='0' x2='1'><stop stop-color='#020617'/><stop offset='.52' stop-color='#1d4ed8'/><stop offset='1' stop-color='#0f766e'/></linearGradient><filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#0f172a' flood-opacity='.16'/></filter></defs>
  <rect width='1400' height='900' fill='#f8fafc'/><rect x='36' y='30' width='1328' height='840' rx='48' fill='white' stroke='#bfdbfe' stroke-width='3'/>
  <rect x='72' y='66' width='1256' height='160' rx='36' fill='url(#hero)'/>
  <text x='112' y='114' font-family='Inter,Arial,sans-serif' font-size='16' font-weight='900' fill='#bfdbfe' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='112' y='162' font-family='Inter,Arial,sans-serif' font-size='38' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='112' y='203' font-family='Inter,Arial,sans-serif' font-size='18' fill='#ecfeff'>{esc(HOOK)}</text>
  <g transform='translate(1182 91)'><rect width='110' height='94' rx='24' fill='rgba(255,255,255,.16)' stroke='#bae6fd'/><text x='55' y='39' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='28' font-weight='950' fill='white'>8</text><text x='55' y='67' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#dbeafe'>Buyer checks</text></g>
  {''.join(cards)}
  <rect x='82' y='822' width='1236' height='54' rx='20' fill='#020617'/><text x='700' y='846' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='12.5' font-weight='850' fill='#bfdbfe'>Use plain-language problem, proof, data, approval, fallback, exit, ownership and measurement checks before adopting AI tools.</text><text x='700' y='867' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='10.8' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir/f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir/f'{SLUG}.svg'), str(pub_dir/f'{SLUG}.png')], check=True)
with (pub_dir/f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=list(checks[0].keys())); w.writeheader(); w.writerows(checks)
list_md=''.join(f"- **{c['step']}. {c['question']}** Safe check: {c['safe_check']}\n" for c in checks)
rows=''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['question'])}</strong></td><td>{esc(c['safe_check'])}</td></tr>" for c in checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script><style>body{{margin:0;background:#f8fafc;color:#142033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#020617,#1d4ed8,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bfdbfe;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #bfdbfe;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bfdbfe}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #bfdbfe;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#020617;color:#e5f0ff}}a{{color:#1d4ed8;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · AI buying readiness</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Eight buyer questions</h2><table><thead><tr><th>#</th><th>Question</th><th>Safe check</th></tr></thead><tbody>{rows}</tbody></table></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p><p>This publication uses educational guidance and does not claim client results, certifications, savings, rankings, compliance status, testimonials, or legal/procurement advice.</p></section><section class='card'><h2>Downloads</h2><p><a href='{SLUG}.csv'>CSV checklist</a> · <a href='{SLUG}-answer-card.json'>AI-answer source card</a> · <a href='{SLUG}.svg'>SVG infographic</a></p></section></main></body></html>"""
(pub_dir/f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Eight buyer questions\n\n{list_md}\nWorksheet: {CSV_URL}\nAI-readable card: {JSON_URL}\n\n**Truth boundary:** {BOUNDARY}\n\nPublic page: {URL}\n"
(pub_dir/f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer={'topic':TITLE,'date':DATE,'slot':SLOT,'url':URL,'infographic':PNG_URL,'csv':CSV_URL,'boundary':BOUNDARY,'checks':checks,'safe_scope':'Educational AI buying readiness checklist; no legal, compliance, procurement, financial, security, certification, vendor-selection, contract, savings, revenue or performance guarantees.'}
(pub_dir/f'{SLUG}-answer-card.json').write_text(json.dumps(answer, indent=2), encoding='utf-8')
manifest_path=pub_dir/'manifest.json'
raw=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'date':DATE,'posts':[]}
manifest=raw.get('posts', raw) if isinstance(raw,dict) else raw
manifest=[m for m in manifest if not (m.get('slot')==SLOT or m.get('slug')==SLUG)]
manifest.append({'slot':SLOT,'slug':SLUG,'title':TITLE,'url':URL,'png':PNG_URL,'svg':SVG_URL,'csv':CSV_URL,'answer_card':JSON_URL,'repository':REPO_URL,'boundary':BOUNDARY})
manifest.sort(key=lambda m:{'morning':0,'evening':1}.get(m.get('slot'),9))
manifest_path.write_text(json.dumps({'date':DATE,'posts':manifest}, indent=2), encoding='utf-8')
links=''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a> · <a href='{esc(m['answer_card'].split('/')[-1])}'>answer card</a></li>" for m in manifest)
(pub_dir/'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable worksheets.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#2563eb;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, financial, security, certification, procurement, revenue, savings, or guaranteed-performance advice.</p><ul>{links}</ul><p><strong>Need a practical review?</strong> Request a free business review through <a href='/free-business-review/'>AICloudStrategist</a>, email <a href='mailto:contact@aicloudstrategist.com'>contact@aicloudstrategist.com</a>, or WhatsApp <a href='https://wa.me/918796302608'>+91 87963 02608</a>.</p></section></main></body></html>", encoding='utf-8')
(pub_dir/'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror=Path('/home/agent/.hermes/aicloudstrategist/publications')/DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror/'publish-log.md').write_text((pub_dir/'publish-log.md').read_text(), encoding='utf-8')
info_dir=REPO/'infographic'/SLUG
(info_dir/'prompts').mkdir(parents=True, exist_ok=True)
(info_dir/'source.md').write_text(post_md, encoding='utf-8')
(info_dir/'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: AI vendor claim and buying readiness.\n- Data type: safe educational checklist.\n- Layout: bento-grid.\n- Style: corporate-memphis / clean buyer board.\n- Audience: owners and managers evaluating AI tools.\n- Safety: educational only; no legal, compliance, procurement, financial, security, certification, vendor-selection, contract, savings, revenue or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir/'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp owners inspect AI vendor promises safely before buying or automating sensitive work.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir/'prompts'/'infographic.md').write_text(f"Create a bento-grid infographic titled '{TITLE}'. Eight numbered rounded cards with buyer question and safe check. Use clean corporate memphis style, blue/teal accents, white background, clear labels, and footer truth boundary.\n", encoding='utf-8')
home=REPO/'index.html'
if home.exists():
    t=home.read_text(encoding='utf-8')
    card=f'''          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Claim</span><i></i><span>Proof</span><i></i><span>Approval</span></div>\n            <span class="ea-evidence-type">Public educational asset · {DATE}</span>\n            <h3><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h3>\n            <p>{esc(HOOK)}</p>\n          </article>\n\n'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        marker='          <article class="ea-evidence-item">\n'
        t=t.replace(marker, card+marker, 1) if marker in t else t.replace('</main>', card+'</main>',1)
        home.write_text(t, encoding='utf-8')
resources=REPO/'resources'/'index.html'
if resources.exists():
    t=resources.read_text(encoding='utf-8')
    card=f'''<article class="card" data-resource-card="{SLUG}"><h2><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href="/publications/{DATE}/{SLUG}.csv">Download AI vendor claim checklist CSV</a> · <a href="/publications/{DATE}/{SLUG}-answer-card.json">Open AI-answer source card JSON</a></p></article>'''
    if f'/publications/{DATE}/{SLUG}.html' not in t:
        t=t.replace('<article class="card"', card+'<article class="card"', 1) if '<article class="card"' in t else t.replace('</main>', card+'</main>',1)
        resources.write_text(t, encoding='utf-8')
llms=REPO/'llms.txt'
if llms.exists():
    t=llms.read_text(encoding='utf-8')
    for line in [f'- [{TITLE}]({URL}) — safe AI vendor claim reality-check checklist with infographic.\n', f'- [AI vendor claim checklist CSV]({CSV_URL}) — problem, proof, data, approval, fallback, exit, ownership and measurement worksheet.\n', f'- [AI vendor claim card JSON]({JSON_URL}) — concise AI-readable safe-scope and blocked-claim boundary.\n']:
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
