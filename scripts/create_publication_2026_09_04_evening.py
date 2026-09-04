from pathlib import Path
import csv, html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-04'
SLOT = 'evening'
SLUG = 'ai-output-risk-ladder'
TITLE = 'The AI Output Risk Ladder'
HOOK = 'A safe educational checklist for deciding when an AI-assisted draft can be used as-is, when it needs owner review, and when it must stop before becoming a business action.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, medical, financial, security, certification, revenue, savings, ranking, customer-result, approval, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
SVG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.svg'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
INDEX_URL = f'https://aicloudstrategist.com/publications/{DATE}/'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

levels = [
    {'level':'1','name':'Safe note','use':'Internal reminder, summary, or personal checklist','review':'Self-check sources and wording before saving','stop':'No stop if it stays internal and non-sensitive'},
    {'level':'2','name':'Team draft','use':'Draft for a colleague, task, or operating note','review':'Named owner checks facts and missing context','stop':'Stop if the draft assigns blame or changes process without owner consent'},
    {'level':'3','name':'Customer-facing draft','use':'Website copy, support reply, proposal note, or FAQ','review':'Accountable owner checks claims, prices, scope, exclusions, and proof boundary','stop':'Stop if it mentions results, clients, savings, rankings, or approvals without evidence'},
    {'level':'4','name':'Sensitive-domain answer','use':'Privacy, security, health, finance, legal, compliance, or HR-like topics','review':'Route to the right accountable owner or qualified adviser before use','stop':'Stop if it could be interpreted as professional advice or a formal compliance/security decision'},
    {'level':'5','name':'External commitment','use':'Contract-like promise, spend decision, guarantee, customer send, or production change','review':'Formal approval path before action; keep source, reviewer, date, and final text','stop':'Stop unless the owner, authority, payment, risk, and audit trail are explicit'},
]
checks = [
    ('Source named', 'The answer points to a visible source, owner note, approved record, or labelled assumption.'),
    ('Claim type known', 'The draft separates education, opinion, internal benchmark, demo, and real approved proof.'),
    ('Risk domain marked', 'Brand, customer-specific, privacy, security, legal, pricing, payment, or production risk is labelled.'),
    ('Owner route set', 'A named human owner can approve, edit, pause, or reject before external action.'),
    ('Stop rule clear', 'The draft says what must not be sent, automated, paid for, or promised without evidence.'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s):
    return html.escape(str(s), quote=True)

def wrap(text, width=42, max_lines=4):
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

rungs = []
colors = ['#dcfce7', '#dbeafe', '#fef3c7', '#ffedd5', '#fee2e2']
strokes = ['#16a34a', '#2563eb', '#d97706', '#ea580c', '#dc2626']
for i, item in enumerate(levels):
    y = 690 - i * 118
    w = 520 + i * 100
    x = 600 - w / 2
    name_lines = ''.join(f"<tspan x='{x+92}' dy='{0 if n == 0 else 22}'>{line}</tspan>" for n, line in enumerate(wrap(item['name'], 18, 2)))
    use_lines = ''.join(f"<tspan x='{x+250}' dy='{0 if n == 0 else 18}'>{line}</tspan>" for n, line in enumerate(wrap(item['use'], 44, 3)))
    rungs.append(f"""
  <g filter='url(#shadow)'>
    <rect x='{x:.0f}' y='{y}' width='{w:.0f}' height='88' rx='26' fill='{colors[i]}' stroke='{strokes[i]}' stroke-width='3'/>
    <circle cx='{x+48:.0f}' cy='{y+44}' r='29' fill='white' stroke='{strokes[i]}' stroke-width='3'/>
    <text x='{x+48:.0f}' y='{y+53}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='28' font-weight='950' fill='{strokes[i]}'>{item['level']}</text>
    <text x='{x+92:.0f}' y='{y+37}' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='#0f172a'>{name_lines}</text>
    <text x='{x+250:.0f}' y='{y+34}' font-family='Inter,Arial,sans-serif' font-size='15' fill='#334155'>{use_lines}</text>
  </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#0f172a'/><stop offset='.5' stop-color='#1d4ed8'/><stop offset='1' stop-color='#991b1b'/></linearGradient>
    <filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='14' stdDeviation='9' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1200' height='900' fill='#f8fafc'/>
  <rect x='36' y='34' width='1128' height='832' rx='44' fill='white' stroke='#dbeafe' stroke-width='3'/>
  <rect x='70' y='68' width='1060' height='150' rx='34' fill='url(#hero)'/>
  <text x='106' y='112' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#bfdbfe' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='106' y='166' font-family='Inter,Arial,sans-serif' font-size='54' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='106' y='202' font-family='Inter,Arial,sans-serif' font-size='18' fill='#e0f2fe'>{esc(HOOK)}</text>
  <text x='600' y='264' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='24' font-weight='950' fill='#0f172a'>Five levels for deciding use, review, or stop</text>
  {''.join(rungs)}
  <rect x='78' y='802' width='1044' height='52' rx='22' fill='#0f172a'/>
  <text x='600' y='824' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' font-weight='800' fill='#bfdbfe'>Before publishing or acting: source named · claim type known · risk marked · owner route set · stop rule clear</text>
  <text x='600' y='844' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='12' fill='#e5e7eb'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(levels[0].keys()))
    writer.writeheader(); writer.writerows(levels)

level_html = ''.join(f"<tr><td>{esc(r['level'])}</td><td><strong>{esc(r['name'])}</strong></td><td>{esc(r['use'])}</td><td>{esc(r['review'])}</td><td>{esc(r['stop'])}</td></tr>" for r in levels)
check_html = ''.join(f"<li><strong>{esc(h)}:</strong> {esc(b)}</li>" for h, b in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":["{PNG_URL}","{SVG_URL}"],"datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f8fafc;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f172a,#1d4ed8,#991b1b);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bfdbfe;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #dbeafe;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #c7d2fe}}li{{margin:12px 0;line-height:1.6}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #dbeafe;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#0f172a;color:#e5f0ff}}a{{color:#075985;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · AI governance</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Five output-risk levels</h2><table><thead><tr><th>Level</th><th>Name</th><th>Use</th><th>Review</th><th>Stop rule</th></tr></thead><tbody>{level_html}</tbody></table><p><a href='{SLUG}.csv'>Download the risk ladder CSV</a></p></section><section class='card'><h2>Five checks before an AI output becomes an action</h2><ul>{check_html}</ul></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\n\n## Five AI output-risk levels\n\n" + ''.join(f"- **Level {r['level']} — {r['name']}:** Use: {r['use']} Review: {r['review']} Stop: {r['stop']}\n" for r in levels) + f"\n## Five checks\n\n" + ''.join(f"- **{h}:** {b}\n" for h, b in checks) + f"\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')

manifest_path = pub_dir / 'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest = [m for m in manifest if not (m.get('slot') == SLOT or m.get('slug') == SLUG)]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'svg': SVG_URL, 'csv': CSV_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
order = {'morning': 0, 'evening': 1}
manifest.sort(key=lambda m: order.get(m.get('slot'), 9))
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links = ''.join(f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a> · <a href='{esc(m['csv'].split('/')[-1])}'>CSV template</a></li>" for m in manifest)
(pub_dir / 'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='{INDEX_URL}'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable templates; not legal, compliance, medical, financial, security, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir / 'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n- {m['slot'].title()} CSV: {m['csv']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest if m.get('slot') in ['morning', 'evening']) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror = Path('/home/agent/.hermes/aicloudstrategist/publications') / DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror / 'publish-log.md').write_text((pub_dir / 'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

evidence_dir = REPO / 'docs' / 'publication-evidence'
evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}

Post: {TITLE}

Safe educational boundaries:
- No client names, testimonials, savings, rankings, bookings, revenue, legal, medical, compliance, security, certification, approval, or guaranteed-performance claims.
- Infographic-style visual included as SVG and PNG.
- CSV worksheet included for operational risk-ladder use.

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

info_dir = REPO / 'infographic' / SLUG
(info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: safe AI output risk triage.\n- Data type: educational risk ladder with five levels, checks, and CSV worksheet.\n- Layout: hierarchical-layers / ladder.\n- Style: corporate Memphis with risk-gradient colors.\n- Audience: business operators using AI-assisted drafts.\n- Language: en.\n- Safety: educational only; no client, legal, compliance, medical, savings, ranking, approval, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators decide when an AI-assisted draft can be used as-is, when it needs owner review, and when it must stop before action.\n\n## Five levels\n" + ''.join(f"- **Level {r['level']} — {r['name']}:** Use: {r['use']} Review: {r['review']} Stop: {r['stop']}\n" for r in levels) + f"\n## Checks\n" + ''.join(f"- **{h}:** {b}\n" for h, b in checks) + f"\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean corporate Memphis hierarchical-layers infographic titled '{TITLE}' as a five-step risk ladder. Use navy, blue, amber, orange, and red progression colors, rounded cards, large level numbers, concise labels, and safe educational wording. Aspect 4:3 worksheet.\n", encoding='utf-8')

home = REPO / 'index.html'
home_text = home.read_text(encoding='utf-8')
new_article = f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Draft</span><i></i><span>Review</span><i></i><span>Stop</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3><a href="/publications/{DATE}/{SLUG}.html">{TITLE}</a></h3>
            <p>{HOOK}</p>
          </article>

'''
insert_before = '          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Question</span>'
if f'/publications/{DATE}/{SLUG}.html' not in home_text:
    if insert_before in home_text:
        home_text = home_text.replace(insert_before, new_article + insert_before, 1)
    else:
        home_text = re.sub(r'(\s*</div>\s*</section>)', new_article + r'\1', home_text, count=1)
home.write_text(home_text, encoding='utf-8')

llms = REPO / 'llms.txt'
txt = llms.read_text(encoding='utf-8')
for line in [
    f'- [{TITLE}]({URL}) — safe educational AI output risk ladder with infographic.\n',
    f'- [AI output risk ladder CSV]({CSV_URL}) — reusable worksheet for use, review, and stop rules.\n',
]:
    link = line.split('](')[1].split(')')[0]
    if link not in txt:
        txt = txt.rstrip() + '\n' + line
llms.write_text(txt, encoding='utf-8')

# Rebuild sitemap if the site helper exists; otherwise add essential URLs directly.
builder = REPO / 'scripts' / 'build_sitemap.py'
if builder.exists():
    subprocess.run(['python3', str(builder)], cwd=str(REPO), check=True)
else:
    sitemap = REPO / 'sitemap.xml'
    sitemap_text = sitemap.read_text(encoding='utf-8')
    for loc, prio in [(URL, '0.6'), (CSV_URL, '0.5'), (INDEX_URL, '0.6')]:
        if loc not in sitemap_text:
            sitemap_text = sitemap_text.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
    sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'csv': CSV_URL, 'repository': REPO_URL}, indent=2))
