from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-10'
SLOT = 'morning'
SLUG = 'clinic-intake-ai-safety-card'
TITLE = 'Clinic Intake AI Safety Card: 7 Checks Before Automating Patient Questions'
HOOK = 'A safe educational checklist for clinic owners before using AI chat, forms, WhatsApp, or email to handle patient intake questions.'
BOUNDARY = 'Educational operations guide only — not medical, legal, privacy, compliance, diagnosis, treatment, certification, savings, ranking, customer-result, approval, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
SVG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.svg'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
INDEX_URL = f'https://aicloudstrategist.com/publications/{DATE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'
ANSWER_CARD_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}-answer-card.json'

checks = [
    {'step':'1','check':'Define allowed questions','owner_question':'Which intake questions are administrative only, such as location, hours, appointment type, documents, or callback preference?','safe_action':'Keep medical symptoms, diagnosis, treatment, urgency, and medication questions routed to humans.'},
    {'step':'2','check':'Show the handoff rule','owner_question':'When must the AI stop and send the person to staff or emergency guidance already approved by the clinic?','safe_action':'Write a visible handoff rule before connecting the intake tool to patients.'},
    {'step':'3','check':'Protect sensitive details','owner_question':'What personal or health details should not be typed into a public chat or unmanaged form?','safe_action':'Collect the minimum needed and avoid free-text medical history in low-control channels.'},
    {'step':'4','check':'Use approved wording','owner_question':'Has the clinic owner reviewed the exact phrases patients will see?','safe_action':'Use simple scripted wording and avoid advice, reassurance, diagnosis, or promise language.'},
    {'step':'5','check':'Assign a response owner','owner_question':'Who reads escalated messages, missed calls, incomplete forms, and confused replies each business day?','safe_action':'Name a staff owner before increasing intake automation volume.'},
    {'step':'6','check':'Test edge cases manually','owner_question':'What happens for urgent symptoms, angry patients, minors, billing concerns, language gaps, or repeated messages?','safe_action':'Run a small internal test log and fix unsafe flows before public use.'},
    {'step':'7','check':'Review weekly evidence','owner_question':'Which questions repeated, which handoffs worked, and where did patients still need help?','safe_action':'Track themes, handoffs, unanswered items, and owner notes before expanding automation.'},
]

def esc(value):
    return html.escape(str(value), quote=True)

def wrap(text, width=31, max_lines=4):
    words = esc(text).split()
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

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

colors = ['#ecfeff','#f0fdf4','#eef2ff','#fdf2f8','#fff7ed','#fefce8','#f0f9ff']
strokes = ['#0891b2','#16a34a','#4f46e5','#db2777','#ea580c','#ca8a04','#0284c7']
positions = [(72,276),(384,276),(696,276),(1008,276),(228,552),(540,552),(852,552)]
cards = []
for i, c in enumerate(checks):
    x, y = positions[i]
    title_lines = ''.join(f"<tspan x='{x+62}' dy='{0 if n==0 else 22}'>{line}</tspan>" for n, line in enumerate(wrap(c['check'], 18, 2)))
    q_lines = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n, line in enumerate(wrap(c['owner_question'], 35, 4)))
    a_lines = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n, line in enumerate(wrap(c['safe_action'], 35, 3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='260' height='222' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+34}' cy='{y+35}' r='22' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+34}' y='{y+43}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+62}' y='{y+32}' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#0f172a'>{title_lines}</text>
    <text x='{x+22}' y='{y+92}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+22}' y='{y+116}' font-family='Inter,Arial,sans-serif' font-size='12.3' font-weight='750' fill='#1e293b'>{q_lines}</text>
    <text x='{x+22}' y='{y+178}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+22}' y='{y+199}' font-family='Inter,Arial,sans-serif' font-size='11.8' fill='#0f172a'>{a_lines}</text>
  </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1360' height='900' viewBox='0 0 1360 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#0f172a'/><stop offset='.52' stop-color='#0369a1'/><stop offset='1' stop-color='#16a34a'/></linearGradient>
    <filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1360' height='900' fill='#f0f9ff'/>
  <rect x='38' y='34' width='1284' height='832' rx='46' fill='white' stroke='#bae6fd' stroke-width='3'/>
  <rect x='72' y='66' width='1216' height='168' rx='34' fill='url(#hero)'/>
  <text x='108' y='112' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#bbf7d0' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING INFOGRAPHIC</text>
  <text x='108' y='160' font-family='Inter,Arial,sans-serif' font-size='37' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='108' y='199' font-family='Inter,Arial,sans-serif' font-size='18' fill='#e0f2fe'>{esc(HOOK)}</text>
  <g transform='translate(1128 98)'><rect width='118' height='94' rx='24' fill='rgba(255,255,255,.16)' stroke='#bbf7d0'/><text x='59' y='37' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='white'>Clinic</text><text x='59' y='64' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='850' fill='#dcfce7'>Safe intake</text></g>
  {''.join(cards)}
  <rect x='86' y='812' width='1188' height='50' rx='21' fill='#0f172a'/>
  <text x='680' y='833' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#bbf7d0'>Before clinic intake automation, check scope, handoff, sensitivity, wording, owner, edge cases, and evidence.</text>
  <text x='680' y='853' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='11.5' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(checks[0].keys()))
    writer.writeheader(); writer.writerows(checks)

rows = ''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['check'])}</strong></td><td>{esc(c['owner_question'])}</td><td>{esc(c['safe_action'])}</td></tr>" for c in checks)
list_md = ''.join(f"- **{c['step']}. {c['check']}:** Owner question: {c['owner_question']} Safe first action: {c['safe_action']}\n" for c in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f0f9ff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f172a,#0369a1,#16a34a);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bbf7d0;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #bae6fd;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bae6fd}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #bae6fd;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#0f172a;color:#e5f0ff}}a{{color:#0369a1;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · clinic intake AI safety</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Seven checks before automating clinic intake questions</h2><table><thead><tr><th>Step</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the clinic intake AI safety CSV</a> · <a href='{SLUG}-answer-card.json'>LLM-readable answer card</a></p></section><section class='card'><h2>Turn this into a safe first review</h2><p>Use this card to scope what a clinic intake AI flow may answer, where it must stop, and which owner reviews handoffs before any public automation expands.</p><p>No patient records, PHI, credentials or payment are needed for the first review.</p><p><a href='/free-business-review/?package=clinic-intake-ai-safety-review&amp;source=publication-clinic-intake-ai-safety-card'>Request a no-credentials clinic intake automation review</a></p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md = f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\nLLM-readable answer card: {ANSWER_CARD_URL}\n\n## Seven checks before automating clinic intake questions\n\n{list_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer = {'topic': TITLE, 'date': DATE, 'slot': SLOT, 'url': URL, 'infographic': PNG_URL, 'csv': CSV_URL, 'boundary': BOUNDARY, 'checks': checks, 'safe_scope': 'Uses administrative-scope boundaries, handoff rules, minimal collection, approved wording, response ownership, edge-case testing, and weekly owner evidence review; no patient data, credentials, medical advice, legal advice, privacy advice, compliance approval, guaranteed growth, or result claims.'}
(pub_dir / f'{SLUG}-answer-card.json').write_text(json.dumps(answer, indent=2), encoding='utf-8')

manifest_path = pub_dir / 'manifest.json'
if manifest_path.exists():
    raw = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest = raw.get('posts', raw) if isinstance(raw, dict) else raw
else:
    manifest = []
manifest = [m for m in manifest if not (m.get('slot') == SLOT or m.get('slug') == SLUG)]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'svg': SVG_URL, 'csv': CSV_URL, 'answer_card': ANSWER_CARD_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: {'morning': 0, 'evening': 1}.get(m.get('slot'), 9))
manifest_path.write_text(json.dumps({'date': DATE, 'posts': manifest}, indent=2), encoding='utf-8')
links = ''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a> · <a href='{esc(m['answer_card'].split('/')[-1])}'>answer card</a></li>" for m in manifest)
(pub_dir / 'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#0369a1;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, medical, financial, security, certification, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir / 'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')

mirror = Path('/home/agent/.hermes/aicloudstrategist/publications') / DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror / 'publish-log.md').write_text((pub_dir / 'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

info_dir = REPO / 'infographic' / SLUG
(info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: clinic intake AI safety.\n- Data type: educational checklist with seven checks.\n- Layout: bento-grid.\n- Style: corporate Memphis / healthcare-safe cards.\n- Audience: clinic owners and operators considering AI chat, forms, WhatsApp, or email for patient intake questions.\n- Language: en.\n- Safety: educational only; no medical, legal, privacy, compliance, diagnosis, treatment, certification, savings, ranking, customer-result, approval, or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp clinic owners inspect patient-intake automation boundaries safely before increasing public-facing automation.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean bento-grid corporate Memphis infographic titled '{TITLE}'. Seven rounded cards, numbered 1 to 7, with check, owner question, and safe first action. Use clinical-safe colors: navy, sky blue, teal, green, indigo, rose, and amber accents. Aspect 3:2. Include educational-only truth boundary in footer.\n", encoding='utf-8')

home = REPO / 'index.html'
if home.exists():
    home_text = home.read_text(encoding='utf-8')
    new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Scope</span><i></i><span>Handoff</span><i></i><span>Owner</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h3>
            <p>{esc(HOOK)}</p>
          </article>

'''
    if f'/publications/{DATE}/{SLUG}.html' not in home_text:
        marker = '          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Cart</span>'
        if marker in home_text:
            home_text = home_text.replace(marker, new_article + marker, 1)
        else:
            home_text = re.sub(r'(\s*</div>\s*</section>)', new_article + r'\1', home_text, count=1)
        home.write_text(home_text, encoding='utf-8')

llms = REPO / 'llms.txt'
if llms.exists():
    txt = llms.read_text(encoding='utf-8')
    for line in [
        f'- [{TITLE}]({URL}) — safe educational clinic-intake AI checklist with infographic.\n',
        f'- [Clinic intake AI safety CSV]({CSV_URL}) — reusable worksheet for scope, handoff, sensitive-detail, wording, owner and evidence review.\n',
    ]:
        link = line.split('](')[1].split(')')[0]
        if link not in txt:
            txt = txt.rstrip() + '\n' + line
    llms.write_text(txt, encoding='utf-8')

builder = REPO / 'scripts' / 'build_sitemap.py'
if builder.exists():
    subprocess.run(['python3', str(builder)], cwd=str(REPO), check=True)
sitemap = REPO / 'sitemap.xml'
if sitemap.exists():
    sitemap_text = sitemap.read_text(encoding='utf-8')
    for loc, prio in [(URL, '0.6'), (PNG_URL, '0.5'), (CSV_URL, '0.5'), (ANSWER_CARD_URL, '0.5'), (INDEX_URL, '0.6')]:
        if loc not in sitemap_text:
            sitemap_text = sitemap_text.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
    sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'csv': CSV_URL, 'answer_card': ANSWER_CARD_URL, 'repository': REPO_URL}, indent=2))
