from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-10'
SLOT = 'night'
SLUG = 'support-ticket-ai-reply-boundary-card'
TITLE = 'Support Ticket AI Reply Boundary Card: 7 Checks Before Automating Helpdesk Responses'
HOOK = 'A safe educational checklist for support, SaaS and ecommerce teams before letting AI draft or send replies on refunds, outages, access, bugs or customer escalations.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, security, support-SLA, customer-result, revenue, savings, refund, incident-resolution, ranking, certification, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
SVG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.svg'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
INDEX_URL = f'https://aicloudstrategist.com/publications/{DATE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'
ANSWER_CARD_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}-answer-card.json'

checks = [
    {'step':'1','check':'Classify the ticket risk','owner_question':'Is this a routine question, refund dispute, outage, access problem, data request, bug, complaint or legal/compliance issue?','safe_action':'Let AI draft only low-risk replies; route risky tickets to the named human owner.'},
    {'step':'2','check':'Verify the source of truth','owner_question':'Which help article, policy, order record, incident note or product owner update supports the reply?','safe_action':'Do not answer from memory or model confidence when the current source is missing.'},
    {'step':'3','check':'Protect sensitive data','owner_question':'Could the reply expose credentials, payment data, health/legal details, customer records, logs or another customer’s information?','safe_action':'Mask sensitive details and ask for secure-channel handling before sharing records.'},
    {'step':'4','check':'Separate apology from promise','owner_question':'Does the wording promise a refund, fix date, SLA credit, legal position, security outcome or future feature?','safe_action':'Use bounded status language and require owner approval for commitments.'},
    {'step':'5','check':'Add escalation stop rules','owner_question':'What words or conditions force handoff: angry customer, chargeback, outage, repeated failure, data deletion, account lockout or regulated request?','safe_action':'Make stop rules visible inside the helpdesk workflow before automation is enabled.'},
    {'step':'6','check':'Record human approval','owner_question':'Who reviewed the reply pattern, when, and what evidence link shows approval?','safe_action':'Keep an approval register for templates, macros, AI prompts and high-risk examples.'},
    {'step':'7','check':'Review failed replies weekly','owner_question':'Which AI drafts were edited, rejected, escalated or caused follow-up confusion?','safe_action':'Feed review findings into updated templates, source articles and routing rules.'},
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
colors = ['#eff6ff','#f0fdf4','#f5f3ff','#fff7ed','#fef2f2','#ecfeff','#f8fafc']
strokes = ['#2563eb','#16a34a','#7c3aed','#ea580c','#dc2626','#0891b2','#475569']
positions = [(72,278),(384,278),(696,278),(1008,278),(228,558),(540,558),(852,558)]
cards = []
for i, c in enumerate(checks):
    x, y = positions[i]
    title_lines = ''.join(f"<tspan x='{x+62}' dy='{0 if n==0 else 22}'>{line}</tspan>" for n, line in enumerate(wrap(c['check'], 18, 2)))
    q_lines = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n, line in enumerate(wrap(c['owner_question'], 36, 4)))
    a_lines = ''.join(f"<tspan x='{x+22}' dy='{0 if n==0 else 16}'>{line}</tspan>" for n, line in enumerate(wrap(c['safe_action'], 36, 3)))
    cards.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x}' y='{y}' width='260' height='226' rx='28' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+34}' cy='{y+35}' r='22' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+34}' y='{y+43}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='{strokes[i]}'>{c['step']}</text>
    <text x='{x+62}' y='{y+32}' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#0f172a'>{title_lines}</text>
    <text x='{x+22}' y='{y+94}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>OWNER QUESTION</text>
    <text x='{x+22}' y='{y+118}' font-family='Inter,Arial,sans-serif' font-size='12.1' font-weight='750' fill='#1e293b'>{q_lines}</text>
    <text x='{x+22}' y='{y+182}' font-family='Inter,Arial,sans-serif' font-size='11' font-weight='900' fill='#475569'>SAFE FIRST ACTION</text>
    <text x='{x+22}' y='{y+203}' font-family='Inter,Arial,sans-serif' font-size='11.5' fill='#0f172a'>{a_lines}</text>
  </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1360' height='900' viewBox='0 0 1360 900'>
  <defs><linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#111827'/><stop offset='.5' stop-color='#1d4ed8'/><stop offset='1' stop-color='#0d9488'/></linearGradient><filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='9' flood-color='#0f172a' flood-opacity='.14'/></filter></defs>
  <rect width='1360' height='900' fill='#eef6ff'/><rect x='38' y='34' width='1284' height='832' rx='46' fill='white' stroke='#bfdbfe' stroke-width='3'/>
  <rect x='72' y='66' width='1216' height='170' rx='34' fill='url(#hero)'/>
  <text x='108' y='112' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#a7f3d0' letter-spacing='3'>AICLOUDSTRATEGIST · NIGHT INFOGRAPHIC</text>
  <text x='108' y='160' font-family='Inter,Arial,sans-serif' font-size='34' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='108' y='200' font-family='Inter,Arial,sans-serif' font-size='18' fill='#dbeafe'>{esc(HOOK)}</text>
  <g transform='translate(1128 98)'><rect width='118' height='94' rx='24' fill='rgba(255,255,255,.16)' stroke='#a7f3d0'/><text x='59' y='37' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='white'>AI</text><text x='59' y='64' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='850' fill='#dbeafe'>Reply Gate</text></g>
  {''.join(cards)}
  <rect x='86' y='818' width='1188' height='44' rx='21' fill='#0f172a'/><text x='680' y='837' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='850' fill='#a7f3d0'>Before automating helpdesk replies, verify risk, source, sensitive data, commitments, stop rules, human approval and weekly failures.</text><text x='680' y='856' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='11.5' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(checks[0].keys()))
    writer.writeheader(); writer.writerows(checks)
rows = ''.join(f"<tr><td>{esc(c['step'])}</td><td><strong>{esc(c['check'])}</strong></td><td>{esc(c['owner_question'])}</td><td>{esc(c['safe_action'])}</td></tr>" for c in checks)
list_md = ''.join(f"- **{c['step']}. {c['check']}:** Owner question: {c['owner_question']} Safe first action: {c['safe_action']}\n" for c in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'><link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'><script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script><style>body{{margin:0;background:#eef6ff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#111827,#1d4ed8,#0d9488);color:white;border-radius:30px;padding:36px}}.kicker{{color:#a7f3d0;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #bfdbfe;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bfdbfe}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #bfdbfe;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#0f172a;color:#e5f0ff}}a{{color:#1d4ed8;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Night publication · support ticket AI reply boundary</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{esc(SLUG)}.png' alt='Infographic: {esc(TITLE)}'><p><a href='{esc(SLUG)}.csv'>Download CSV worksheet</a> · <a href='{esc(SLUG)}-answer-card.json'>Open AI-answer source card JSON</a></p></section><section class='card'><h2>Seven checks before AI sends or drafts support replies</h2><table><thead><tr><th>#</th><th>Check</th><th>Owner question</th><th>Safe first action</th></tr></thead><tbody>{rows}</tbody></table></section><section class='card'><h2>When this should become a paid diagnostic</h2><p>If support tickets, refunds, outages, account access, sensitive data, manual macros or AI chatbot drafts are creating risk or delays, AICS can review sources, stop rules, owner approvals and weekly failure evidence without asking for credentials or customer data in the first review.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p><p>No customer, SLA, revenue, savings, compliance, legal, refund, security, ranking or incident-resolution claims are made by this publication.</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md = f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\nLLM-readable answer card: {ANSWER_CARD_URL}\n\n## Seven checks before AI sends or drafts support replies\n\n{list_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
answer = {'topic': TITLE, 'date': DATE, 'slot': SLOT, 'url': URL, 'infographic': PNG_URL, 'csv': CSV_URL, 'boundary': BOUNDARY, 'checks': checks, 'safe_scope': 'Uses ticket-risk classification, source-of-truth verification, sensitive-data masking, commitment boundaries, escalation stop rules, human approval records and weekly failure review; no legal, compliance, security, support-SLA, customer-result, revenue, savings, refund, incident-resolution, ranking, certification or performance guarantees.'}
(pub_dir / f'{SLUG}-answer-card.json').write_text(json.dumps(answer, indent=2), encoding='utf-8')

manifest_path = pub_dir / 'manifest.json'
raw = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'date': DATE, 'posts': []}
manifest = raw.get('posts', raw) if isinstance(raw, dict) else raw
manifest = [m for m in manifest if not (m.get('slot') == SLOT or m.get('slug') == SLUG)]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'svg': SVG_URL, 'csv': CSV_URL, 'answer_card': ANSWER_CARD_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: {'morning': 0, 'evening': 1, 'night': 2}.get(m.get('slot'), 9))
manifest_path.write_text(json.dumps({'date': DATE, 'posts': manifest}, indent=2), encoding='utf-8')
links = ''.join(f"<li>{esc(m['slot'].title())}: <a href='{esc(m['slug'])}.html'>{esc(m['title'])}</a> · <a href='{esc(m['png'].split('/')[-1])}'>infographic</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV</a> · <a href='{esc(m['answer_card'].split('/')[-1])}'>answer card</a></li>" for m in manifest)
(pub_dir / 'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}a{{color:#0369a1;font-weight:800}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, medical, financial, security, certification, support-SLA, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir / 'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m.get('repository', REPO_URL)}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror = Path('/home/agent/.hermes/aicloudstrategist/publications') / DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror / 'publish-log.md').write_text((pub_dir / 'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

info_dir = REPO / 'infographic' / SLUG
(info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: support ticket AI reply boundary.\n- Data type: educational checklist with seven checks.\n- Layout: bento-grid.\n- Audience: support, SaaS, ecommerce and operations teams using AI drafts, macros or chatbot replies.\n- Safety: educational only; no legal, compliance, security, support-SLA, customer-result, revenue, savings, refund, incident-resolution, ranking, certification or guaranteed-performance claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp teams avoid unsafe AI helpdesk replies by checking ticket risk, source evidence, sensitive data, commitments, escalation stop rules, human approval and failure review.\n\n## Checks\n{list_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean bento-grid corporate infographic titled '{TITLE}'. Seven rounded cards, numbered 1 to 7, with check, owner question, and safe first action. Use navy, blue, teal, green, indigo and amber accents. Aspect 3:2. Include educational-only truth boundary in footer.\n", encoding='utf-8')

resources = REPO / 'resources' / 'index.html'
if resources.exists():
    resources_text = resources.read_text(encoding='utf-8')
    resource_card = f'''<article class="card" data-resource-card="{SLUG}"><h2><a href="/publications/{DATE}/{SLUG}.html">{esc(TITLE)}</a></h2><p>{esc(HOOK)}</p><p><a href="/publications/{DATE}/{SLUG}.csv">Download helpdesk reply-boundary worksheet CSV</a> · <a href="/publications/{DATE}/{SLUG}-answer-card.json">Open AI-answer source card JSON</a></p></article>'''
    if f'/publications/{DATE}/{SLUG}.html' not in resources_text:
        marker = '<article class="card" data-resource-card="ai-procurement-answer-boundary-card">'
        if marker in resources_text:
            resources_text = resources_text.replace(marker, resource_card + marker, 1)
        else:
            resources_text = resources_text.replace('<article class="card"', resource_card + '<article class="card"', 1)
        resources.write_text(resources_text, encoding='utf-8')

llms = REPO / 'llms.txt'
if llms.exists():
    txt = llms.read_text(encoding='utf-8')
    insert_lines = [
        f'- [{TITLE}]({URL}) — safe educational support-ticket AI reply boundary checklist with infographic.\n',
        f'- [Support ticket AI reply boundary CSV]({CSV_URL}) — reusable worksheet for ticket risk, source, sensitive-data, commitment, stop-rule and approval review.\n',
        f'- [Support ticket AI reply boundary card JSON]({ANSWER_CARD_URL}) — concise LLM-readable safe route and blocked claim boundaries for helpdesk AI reply automation.\n',
    ]
    for line in insert_lines:
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
    asset_urls = [(INDEX_URL, '0.6')]
    for m in manifest:
        asset_urls.extend([
            (m['url'], '0.6'),
            (m['png'], '0.5'),
            (m['svg'], '0.5'),
            (m['csv'], '0.5'),
            (m['answer_card'], '0.5'),
        ])
    for loc, prio in asset_urls:
        if loc not in sitemap_text:
            sitemap_text = sitemap_text.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
    sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'csv': CSV_URL, 'answer_card': ANSWER_CARD_URL, 'repository': REPO_URL}, indent=2))
