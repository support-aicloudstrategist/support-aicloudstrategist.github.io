from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-09-08'
SLOT = 'evening'
SLUG = 'ai-agent-cost-spike-triage'
TITLE = 'AI Agent Cost Spike Triage: 7 Checks Before You Scale or Switch Tools'
HOOK = 'A safe educational checklist for founders and operators when AI agent, chatbot, workflow, or token usage costs start rising faster than expected.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, medical, financial, security, certification, savings, ranking, customer-result, approval, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
SVG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.svg'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
INDEX_URL = f'https://aicloudstrategist.com/publications/{DATE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    {'step':'1','check':'Find the trigger','owner_question':'Which release, prompt, integration, traffic source, or schedule changed before the spike?','safe_action':'Mark the first abnormal day or hour and link it to a visible change record.'},
    {'step':'2','check':'Split fixed vs variable cost','owner_question':'Is spend rising from seats, base platform fees, runs, tokens, storage, tools, or retries?','safe_action':'Separate subscription cost from usage cost before judging the tool.'},
    {'step':'3','check':'Measure retry loops','owner_question':'Are agents repeating failed steps, calling tools too often, or reprocessing the same items?','safe_action':'Sample failed runs and count retries before increasing limits.'},
    {'step':'4','check':'Check human handoff points','owner_question':'Where should a person approve, stop, or redirect work before costs continue?','safe_action':'Add review gates for ambiguous, high-volume, risky, or customer-facing paths.'},
    {'step':'5','check':'Protect quality evidence','owner_question':'Are cheaper changes likely to reduce answer quality, traceability, or customer experience?','safe_action':'Keep before-and-after examples, run logs, and owner notes for any change.'},
    {'step':'6','check':'Compare tool-neutral options','owner_question':'Can scope, routing, caching, batching, model choice, or workflow design reduce waste safely?','safe_action':'List design alternatives before switching vendors or cancelling automation.'},
    {'step':'7','check':'Create an owner review loop','owner_question':'Who reviews cost, value, failures, and risk each week until the pattern stabilizes?','safe_action':'Assign an owner, threshold, review cadence, and next decision date.'},
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(str(s), quote=True)

def wrap(text, width=28, max_lines=4):
    words = esc(text).split(); lines=[]; line=''
    for word in words:
        if len((line+' '+word).strip()) > width:
            if line: lines.append(line)
            line = word
        else:
            line = (line+' '+word).strip()
    if line: lines.append(line)
    return lines[:max_lines]

colors = ['#dbeafe','#ede9fe','#ccfbf1','#fef3c7','#fce7f3','#dcfce7','#fee2e2']
strokes = ['#2563eb','#7c3aed','#0f766e','#d97706','#db2777','#16a34a','#dc2626']
positions = [(70,260),(380,260),(690,260),(1000,260),(225,535),(535,535),(845,535)]
cards = []
for i, c in enumerate(checks):
    x,y = positions[i]
    title = ''.join(f"<tspan x='{x+62}' dy='{0 if n==0 else 22}'>{line}</tspan>" for n,line in enumerate(wrap(c['check'],18,2)))
    q = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n,line in enumerate(wrap(c['owner_question'],34,4)))
    action = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n,line in enumerate(wrap(c['safe_action'],34,3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='260' height='222' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+34}' cy='{y+35}' r='22' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+34}' y='{y+43}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+62}' y='{y+32}' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#0f172a'>{title}</text>
    <text x='{x+22}' y='{y+92}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+22}' y='{y+116}' font-family='Inter,Arial,sans-serif' font-size='12.5' font-weight='750' fill='#1e293b'>{q}</text>
    <text x='{x+22}' y='{y+178}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+22}' y='{y+199}' font-family='Inter,Arial,sans-serif' font-size='12' fill='#0f172a'>{action}</text>
  </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1360' height='900' viewBox='0 0 1360 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#0f172a'/><stop offset='.48' stop-color='#4338ca'/><stop offset='1' stop-color='#0891b2'/></linearGradient>
    <filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1360' height='900' fill='#f8fafc'/>
  <rect x='38' y='34' width='1284' height='832' rx='46' fill='white' stroke='#c7d2fe' stroke-width='3'/>
  <rect x='72' y='66' width='1216' height='158' rx='34' fill='url(#hero)'/>
  <text x='108' y='112' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#bae6fd' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='108' y='161' font-family='Inter,Arial,sans-serif' font-size='40' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='108' y='197' font-family='Inter,Arial,sans-serif' font-size='18' fill='#eef2ff'>{esc(HOOK)}</text>
  <g transform='translate(1120 100)'><rect width='118' height='86' rx='22' fill='rgba(255,255,255,.15)' stroke='#a5f3fc'/><text x='59' y='35' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='white'>Cost</text><text x='59' y='61' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='800' fill='#cffafe'>Evidence first</text></g>
  {''.join(cards)}
  <rect x='86' y='812' width='1188' height='50' rx='21' fill='#111827'/>
  <text x='680' y='833' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#c7d2fe'>When AI costs jump, inspect trigger, cost type, retries, handoffs, quality evidence, alternatives, and owner cadence.</text>
  <text x='680' y='853' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='11.5' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
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
<style>body{{margin:0;background:#f8fafc;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f172a,#4338ca,#0891b2);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bae6fd;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #dbeafe;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #c7d2fe}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #dbeafe;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#111827;color:#e5f0ff}}a{{color:#3730a3;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · AI agent cost triage</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Seven checks before scaling or switching tools</h2><table><thead><tr><th>Step</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the AI agent cost triage CSV</a></p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir/f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md = f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\n\n## Seven checks before scaling or switching tools\n\n{list_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir/f'{SLUG}.md').write_text(post_md, encoding='utf-8')

manifest_path = pub_dir/'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest = [m for m in manifest if not (m.get('slot') == SLOT or m.get('slug') == SLUG)]
manifest.append({'slot':SLOT,'slug':SLUG,'title':TITLE,'url':URL,'png':PNG_URL,'svg':SVG_URL,'csv':CSV_URL,'repository':REPO_URL,'boundary':BOUNDARY})
manifest.sort(key=lambda m: {'morning':0,'evening':1}.get(m.get('slot'),9))
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links = ''.join(f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV template</a></li>" for m in manifest)
(pub_dir/'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, medical, financial, security, certification, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
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
- CSV worksheet included for AI agent cost spike triage.

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
(info_dir/'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: AI agent cost spike triage.\n- Data type: educational checklist with seven checks.\n- Layout: bento-grid.\n- Style: corporate Memphis / dashboard cards.\n- Audience: founders and operators reviewing AI agent, chatbot, workflow, or token usage costs.\n- Language: en.\n- Safety: educational only; no legal, compliance, medical, financial, security, savings, ranking, customer, approval, or guaranteed claims.\n", encoding='utf-8')
(info_dir/'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp founders and operators inspect AI agent cost spikes with evidence before scaling, switching tools, or cutting automation.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir/'prompts'/'infographic.md').write_text(f"Create a clean bento-grid corporate Memphis infographic titled '{TITLE}'. Seven rounded cards, numbered 1 to 7, with check, owner question, and safe first action. Use navy, indigo, teal, amber, pink, green, and red accents. Aspect 3:2. Include educational-only truth boundary in footer.\n", encoding='utf-8')

home = REPO/'index.html'
home_text = home.read_text(encoding='utf-8')
new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Trigger</span><i></i><span>Retry</span><i></i><span>Owner</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3><a href="/publications/{DATE}/{SLUG}.html">{TITLE}</a></h3>
            <p>{HOOK}</p>
          </article>

'''
if f'/publications/{DATE}/{SLUG}.html' not in home_text:
    marker = '          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Count</span>'
    if marker in home_text:
        home_text = home_text.replace(marker, new_article + marker, 1)
    else:
        home_text = re.sub(r'(\s*</div>\s*</section>)', new_article + r'\1', home_text, count=1)
home.write_text(home_text, encoding='utf-8')

llms = REPO/'llms.txt'
txt = llms.read_text(encoding='utf-8')
for line in [
    f'- [{TITLE}]({URL}) — safe educational AI agent cost spike triage checklist with infographic.\n',
    f'- [AI agent cost spike triage CSV]({CSV_URL}) — reusable worksheet for evidence-led AI agent cost review.\n',
]:
    link = line.split('](')[1].split(')')[0]
    if link not in txt:
        txt = txt.rstrip() + '\n' + line
llms.write_text(txt, encoding='utf-8')

builder = REPO/'scripts'/'build_sitemap.py'
if builder.exists():
    subprocess.run(['python3', str(builder)], cwd=str(REPO), check=True)

sitemap = REPO/'sitemap.xml'
sitemap_text = sitemap.read_text(encoding='utf-8')
for loc, prio in [
    (URL,'0.6'),
    (PNG_URL,'0.5'),
    (CSV_URL,'0.5'),
    (INDEX_URL,'0.6'),
]:
    if loc not in sitemap_text:
        sitemap_text = sitemap_text.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot':SLOT,'title':TITLE,'url':URL,'png':PNG_URL,'csv':CSV_URL,'repository':REPO_URL}, indent=2))
