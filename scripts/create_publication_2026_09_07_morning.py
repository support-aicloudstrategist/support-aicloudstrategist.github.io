from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-07'
SLOT = 'morning'
SLUG = 'manual-work-automation-triage'
TITLE = 'Manual Work Automation Triage: 6 Checks Before You Automate'
HOOK = 'A safe educational checklist for business owners deciding which repetitive work is ready for automation and which tasks still need human judgement first.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, medical, financial, security, certification, revenue, savings, ranking, customer-result, approval, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
SVG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.svg'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
INDEX_URL = f'https://aicloudstrategist.com/publications/{DATE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    {'step':'1','check':'Frequency is visible','owner_question':'Does this task happen often enough to justify a workflow?','safe_action':'Count occurrences for one week before building automation.'},
    {'step':'2','check':'Input is predictable','owner_question':'Do requests arrive in a consistent format, channel, or form field?','safe_action':'Standardise intake before asking software to decide.'},
    {'step':'3','check':'Decision rule is simple','owner_question':'Can a non-expert explain the route, approval, or next step in one sentence?','safe_action':'Automate routing and reminders before automating judgement.'},
    {'step':'4','check':'Exception path exists','owner_question':'Where should unclear, emotional, high-value, or sensitive cases go?','safe_action':'Send exceptions to a named human owner with context.'},
    {'step':'5','check':'Evidence is retained','owner_question':'Will the business keep the source message, timestamp, owner, and final action?','safe_action':'Log the before/after decision trail, not just the task status.'},
    {'step':'6','check':'Customer impact is reversible','owner_question':'Can the action be corrected quickly if automation is wrong?','safe_action':'Start with drafts, reminders, tags, and queues before external commitments.'},
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(str(s), quote=True)

def wrap(text, width=28, max_lines=3):
    words = esc(text).split(); lines=[]; line=''
    for word in words:
        if len((line+' '+word).strip()) > width:
            if line: lines.append(line)
            line = word
        else:
            line = (line+' '+word).strip()
    if line: lines.append(line)
    return lines[:max_lines]

colors = ['#dbeafe','#dcfce7','#fef3c7','#ede9fe','#cffafe','#fee2e2']
strokes = ['#2563eb','#16a34a','#d97706','#7c3aed','#0891b2','#dc2626']
positions = [(84,260),(448,260),(812,260),(84,520),(448,520),(812,520)]
cards = []
for i, c in enumerate(checks):
    x,y = positions[i]
    title = ''.join(f"<tspan x='{x+78}' dy='{0 if n==0 else 24}'>{line}</tspan>" for n,line in enumerate(wrap(c['check'],20,2)))
    q = ''.join(f"<tspan x='{x+28}' dy='{0 if n==0 else 18}'>{line}</tspan>" for n,line in enumerate(wrap(c['owner_question'],36,4)))
    action = ''.join(f"<tspan x='{x+28}' dy='{0 if n==0 else 18}'>{line}</tspan>" for n,line in enumerate(wrap(c['safe_action'],36,3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='304' height='206' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+42}' cy='{y+42}' r='25' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+42}' y='{y+51}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='26' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+78}' y='{y+36}' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='950' fill='#0f172a'>{title}</text>
    <text x='{x+28}' y='{y+96}' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='900' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+28}' y='{y+122}' font-family='Inter,Arial,sans-serif' font-size='14' font-weight='750' fill='#1e293b'>{q}</text>
    <text x='{x+28}' y='{y+172}' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='900' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+28}' y='{y+196}' font-family='Inter,Arial,sans-serif' font-size='13' fill='#0f172a'>{action}</text>
  </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#0f172a'/><stop offset='.55' stop-color='#1d4ed8'/><stop offset='1' stop-color='#0f766e'/></linearGradient>
    <filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='8' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1200' height='900' fill='#f8fafc'/>
  <rect x='36' y='34' width='1128' height='832' rx='44' fill='white' stroke='#bfdbfe' stroke-width='3'/>
  <rect x='70' y='68' width='1060' height='152' rx='34' fill='url(#hero)'/>
  <text x='106' y='112' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#bfdbfe' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING INFOGRAPHIC</text>
  <text x='106' y='162' font-family='Inter,Arial,sans-serif' font-size='45' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='106' y='198' font-family='Inter,Arial,sans-serif' font-size='18' fill='#ecfeff'>{esc(HOOK)}</text>
  {''.join(cards)}
  <rect x='78' y='804' width='1044' height='52' rx='22' fill='#0f172a'/>
  <text x='600' y='826' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#bfdbfe'>Start with drafts, queues, routing and evidence before automated external commitments.</text>
  <text x='600' y='846' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='12' fill='#e5f6ff'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir/f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir/f'{SLUG}.svg'), str(pub_dir/f'{SLUG}.png')], check=True)

with (pub_dir/f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(checks[0].keys()))
    writer.writeheader(); writer.writerows(checks)

rows = ''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['check'])}</strong></td><td>{esc(c['owner_question'])}</td><td>{esc(c['safe_action'])}</td></tr>" for c in checks)
list_md = ''.join(f"- **{c['step']}. {c['check']}:** Owner question: {c['owner_question']} Safe first action: {c['safe_action']}\n" for c in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f8fafc;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f172a,#1d4ed8,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bfdbfe;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #dbeafe;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #c7d2fe}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #dbeafe;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#0f172a;color:#e5f0ff}}a{{color:#075985;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · workflow automation</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Six checks before automation</h2><table><thead><tr><th>Step</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the triage CSV</a></p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir/f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md = f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\n\n## Six checks before automation\n\n{list_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir/f'{SLUG}.md').write_text(post_md, encoding='utf-8')

manifest_path = pub_dir/'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest = [m for m in manifest if not (m.get('slot') == SLOT or m.get('slug') == SLUG)]
manifest.append({'slot':SLOT,'slug':SLUG,'title':TITLE,'url':URL,'png':PNG_URL,'svg':SVG_URL,'csv':CSV_URL,'repository':REPO_URL,'boundary':BOUNDARY})
manifest.sort(key=lambda m: {'morning':0,'evening':1}.get(m.get('slot'),9))
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links = ''.join(f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV template</a></li>" for m in manifest)
(pub_dir/'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, medical, financial, security, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir/'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror = Path('/home/agent/.hermes/aicloudstrategist/publications')/DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror/'publish-log.md').write_text((pub_dir/'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

evidence_dir = REPO/'docs'/'publication-evidence'
evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir/f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}

Post: {TITLE}

Safe educational boundaries:
- No client names, testimonials, savings, rankings, bookings, revenue, legal, medical, compliance, security, certification, approval, or guaranteed-performance claims.
- Infographic-style visual included as SVG and PNG.
- CSV worksheet included for manual-work automation triage.

Published surfaces in this repository:
- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`
- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`
- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`
- CSV template: `/publications/{DATE}/{SLUG}.csv`

Live targets after deployment:
- {URL}
- {PNG_URL}
- {CSV_URL}
- {REPO_URL}
""", encoding='utf-8')

info_dir = REPO/'infographic'/SLUG
(info_dir/'prompts').mkdir(parents=True, exist_ok=True)
(info_dir/'source.md').write_text(post_md, encoding='utf-8')
(info_dir/'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: manual-work automation triage.\n- Data type: educational checklist with six checks.\n- Layout: bento-grid.\n- Style: corporate Memphis / clean infographic.\n- Audience: business owners considering workflow automation.\n- Language: en.\n- Safety: educational only; no legal, compliance, medical, financial, security, savings, ranking, customer, approval, or guaranteed claims.\n", encoding='utf-8')
(info_dir/'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators decide which repetitive work is ready for automation and which tasks need human judgement first.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir/'prompts'/'infographic.md').write_text(f"Create a clean bento-grid corporate Memphis infographic titled '{TITLE}'. Six rounded cards, numbered 1 to 6, with check, owner question, and safe first action. Use navy, blue, green, amber, violet, cyan, and red accents. Aspect 4:3. Include educational-only truth boundary in footer.\n", encoding='utf-8')

home = REPO/'index.html'
home_text = home.read_text(encoding='utf-8')
new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Count</span><i></i><span>Route</span><i></i><span>Automate</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3><a href="/publications/{DATE}/{SLUG}.html">{TITLE}</a></h3>
            <p>{HOOK}</p>
          </article>

'''
insert_before='          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Check</span>'
if f'/publications/{DATE}/{SLUG}.html' not in home_text:
    if insert_before in home_text:
        home_text = home_text.replace(insert_before, new_article + insert_before, 1)
    else:
        home_text = re.sub(r'(\s*</div>\s*</section>)', new_article + r'\1', home_text, count=1)
home.write_text(home_text, encoding='utf-8')

llms = REPO/'llms.txt'
txt = llms.read_text(encoding='utf-8')
for line in [
    f'- [{TITLE}]({URL}) — safe educational manual-work automation triage checklist with infographic.\n',
    f'- [Manual work automation triage CSV]({CSV_URL}) — reusable owner-review worksheet for deciding what to automate first.\n',
]:
    link = line.split('](')[1].split(')')[0]
    if link not in txt:
        txt = txt.rstrip() + '\n' + line
llms.write_text(txt, encoding='utf-8')

builder = REPO/'scripts'/'build_sitemap.py'
if builder.exists():
    subprocess.run(['python3', str(builder)], cwd=str(REPO), check=True)
else:
    sitemap = REPO/'sitemap.xml'; sitemap_text = sitemap.read_text(encoding='utf-8')
    for loc, prio in [(URL,'0.6'),(PNG_URL,'0.5'),(CSV_URL,'0.5'),(INDEX_URL,'0.6')]:
        if loc not in sitemap_text:
            sitemap_text = sitemap_text.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
    sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot':SLOT,'title':TITLE,'url':URL,'png':PNG_URL,'csv':CSV_URL,'repository':REPO_URL}, indent=2))
