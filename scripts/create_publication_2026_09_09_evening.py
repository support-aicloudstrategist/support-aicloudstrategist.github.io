from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-09'
SLOT = 'evening'
SLUG = 'ecommerce-abandoned-cart-whatsapp-followup'
TITLE = 'E-commerce Abandoned Cart WhatsApp Follow-up: 7 Checks Before You Automate'
HOOK = 'A safe educational checklist for store owners before using WhatsApp, SMS, email, or AI workflows to follow up on abandoned carts.'
BOUNDARY = 'Educational operations guide only — not legal, privacy, marketing, financial, compliance, certification, savings, ranking, customer-result, approval, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
SVG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.svg'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
INDEX_URL = f'https://aicloudstrategist.com/publications/{DATE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'
ANSWER_CARD_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}-answer-card.json'

checks = [
    {'step':'1','check':'Confirm consent source','owner_question':'Where did the shopper agree to receive WhatsApp, SMS, email, or cart follow-up messages?','safe_action':'Keep a visible consent/source note before adding any automated reminder.'},
    {'step':'2','check':'Separate help from pressure','owner_question':'Is the message useful, or does it feel like a pushy sales chase?','safe_action':'Start with one helpful reminder, clear context, and an easy way to stop.'},
    {'step':'3','check':'Check timing windows','owner_question':'When is the cart still relevant without disturbing the buyer?','safe_action':'Test a small manual timing window before adding repeated automations.'},
    {'step':'4','check':'Match product context','owner_question':'Does the follow-up reference the right item, stock status, delivery concern, or checkout issue?','safe_action':'Use product-safe placeholders and avoid guessing reasons the buyer left.'},
    {'step':'5','check':'Protect support capacity','owner_question':'Who answers if the buyer replies with a question, complaint, cancellation, or delivery issue?','safe_action':'Route replies to an owner before increasing message volume.'},
    {'step':'6','check':'Limit discount leakage','owner_question':'Will automatic discounts train buyers to abandon carts to get offers?','safe_action':'Separate service reminders from discount rules and review margin impact manually.'},
    {'step':'7','check':'Review evidence weekly','owner_question':'Which messages helped, which annoyed buyers, and which created support work?','safe_action':'Track sent count, reply themes, stops/opt-outs, and owner notes before scaling.'},
]

def esc(value):
    return html.escape(str(value), quote=True)

def wrap(text, width=28, max_lines=4):
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

colors = ['#ecfeff','#eef2ff','#f0fdf4','#fff7ed','#fdf2f8','#fefce8','#fef2f2']
strokes = ['#0891b2','#4f46e5','#16a34a','#ea580c','#db2777','#ca8a04','#dc2626']
positions = [(70,270),(380,270),(690,270),(1000,270),(225,545),(535,545),(845,545)]
cards = []
for i, c in enumerate(checks):
    x, y = positions[i]
    title_lines = ''.join(f"<tspan x='{x+62}' dy='{0 if n==0 else 22}'>{line}</tspan>" for n, line in enumerate(wrap(c['check'], 19, 2)))
    q_lines = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n, line in enumerate(wrap(c['owner_question'], 34, 4)))
    a_lines = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n, line in enumerate(wrap(c['safe_action'], 34, 3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='260' height='222' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+34}' cy='{y+35}' r='22' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+34}' y='{y+43}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+62}' y='{y+32}' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#0f172a'>{title_lines}</text>
    <text x='{x+22}' y='{y+92}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+22}' y='{y+116}' font-family='Inter,Arial,sans-serif' font-size='12.5' font-weight='750' fill='#1e293b'>{q_lines}</text>
    <text x='{x+22}' y='{y+178}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+22}' y='{y+199}' font-family='Inter,Arial,sans-serif' font-size='12' fill='#0f172a'>{a_lines}</text>
  </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1360' height='900' viewBox='0 0 1360 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#111827'/><stop offset='.52' stop-color='#0f766e'/><stop offset='1' stop-color='#f97316'/></linearGradient>
    <filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1360' height='900' fill='#fff7ed'/>
  <rect x='38' y='34' width='1284' height='832' rx='46' fill='white' stroke='#fed7aa' stroke-width='3'/>
  <rect x='72' y='66' width='1216' height='168' rx='34' fill='url(#hero)'/>
  <text x='108' y='112' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#ccfbf1' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='108' y='160' font-family='Inter,Arial,sans-serif' font-size='38' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='108' y='199' font-family='Inter,Arial,sans-serif' font-size='18' fill='#fff7ed'>{esc(HOOK)}</text>
  <g transform='translate(1120 103)'><rect width='118' height='86' rx='22' fill='rgba(255,255,255,.16)' stroke='#fed7aa'/><text x='59' y='35' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='white'>Cart</text><text x='59' y='61' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='800' fill='#ffedd5'>Trust first</text></g>
  {''.join(cards)}
  <rect x='86' y='812' width='1188' height='50' rx='21' fill='#111827'/>
  <text x='680' y='833' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#fed7aa'>Before automating abandoned-cart follow-up, check consent, tone, timing, context, support, discounts, and review evidence.</text>
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
<style>body{{margin:0;background:#fff7ed;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#111827,#0f766e,#f97316);color:white;border-radius:30px;padding:36px}}.kicker{{color:#ccfbf1;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #fed7aa;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #fed7aa}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #fed7aa;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#111827;color:#e5f0ff}}a{{color:#0f766e;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · abandoned cart follow-up</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Seven checks before automating abandoned cart follow-up</h2><table><thead><tr><th>Step</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table><p><a href='{SLUG}.csv'>Download the abandoned cart follow-up CSV</a> · <a href='{SLUG}-answer-card.json'>LLM-readable answer card</a></p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md = f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\nLLM-readable answer card: {ANSWER_CARD_URL}\n\n## Seven checks before automating abandoned cart follow-up\n\n{list_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer = {'topic': TITLE, 'date': DATE, 'slot': SLOT, 'url': URL, 'infographic': PNG_URL, 'csv': CSV_URL, 'boundary': BOUNDARY, 'checks': checks, 'safe_scope': 'Uses consent/source notes, tone review, timing windows, product context, support routing, discount review, and weekly owner evidence review; no customer data, credentials, legal advice, privacy advice, guaranteed revenue, or result claims.'}
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
links = ''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a></li>" for m in manifest)
(pub_dir / 'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#0f766e;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, medical, financial, security, certification, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir / 'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')

mirror = Path('/home/agent/.hermes/aicloudstrategist/publications') / DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror / 'publish-log.md').write_text((pub_dir / 'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

info_dir = REPO / 'infographic' / SLUG
(info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: e-commerce abandoned cart WhatsApp follow-up.\n- Data type: educational checklist with seven checks.\n- Layout: bento-grid.\n- Style: corporate Memphis / warm commerce cards.\n- Audience: store owners and operators considering WhatsApp, SMS, email, or AI follow-up workflows.\n- Language: en.\n- Safety: educational only; no legal, privacy, marketing, financial, compliance, certification, savings, ranking, customer-result, approval, or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp store owners inspect abandoned cart follow-up automation safely before increasing message volume.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean bento-grid corporate Memphis infographic titled '{TITLE}'. Seven rounded cards, numbered 1 to 7, with check, owner question, and safe first action. Use warm commerce colors: navy, teal, orange, mint, indigo, rose, and amber accents. Aspect 3:2. Include educational-only truth boundary in footer.\n", encoding='utf-8')

home = REPO / 'index.html'
if home.exists():
    home_text = home.read_text(encoding='utf-8')
    new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Consent</span><i></i><span>Timing</span><i></i><span>Owner</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h3>
            <p>{esc(HOOK)}</p>
          </article>

'''
    if f'/publications/{DATE}/{SLUG}.html' not in home_text:
        marker = '          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Count</span>'
        if marker in home_text:
            home_text = home_text.replace(marker, new_article + marker, 1)
        else:
            home_text = re.sub(r'(\s*</div>\s*</section>)', new_article + r'\1', home_text, count=1)
        home.write_text(home_text, encoding='utf-8')

llms = REPO / 'llms.txt'
if llms.exists():
    txt = llms.read_text(encoding='utf-8')
    for line in [
        f'- [{TITLE}]({URL}) — safe educational abandoned-cart follow-up checklist with infographic.\n',
        f'- [Abandoned cart follow-up CSV]({CSV_URL}) — reusable worksheet for consent, timing, owner review, and support routing.\n',
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
