from pathlib import Path
import html, json, re, subprocess, csv

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-03'
SLOT = 'evening'
SLUG = 'ai-decision-trace-card'
TITLE = 'The AI Decision Trace Card'
HOOK = 'A safe educational worksheet for recording why an AI-assisted business decision was made, which source supported it, and when a human owner must review it.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, medical, financial, security, certification, revenue, savings, ranking, customer-result, decision-approval, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
CSV_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.csv'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

checks = [
    ('Decision named', 'Write the exact decision, draft, recommendation, or workflow change being considered.'),
    ('Source evidence', 'Attach the approved page, record, policy, data extract, or owner note the AI response relied on.'),
    ('Reason captured', 'Record the short reason the option was chosen, rejected, or sent back for more evidence.'),
    ('Risk label', 'Mark brand, legal, privacy, security, pricing, customer-specific, payment, or operational risk before action.'),
    ('Owner checkpoint', 'Route sensitive, uncertain, external-facing, or commitment-making decisions to the accountable human owner.'),
    ('Trace saved', 'Save prompt, source, AI draft, reviewer note, final decision, date, and correction trail together.'),
]
rows = [
    {'decision_area':'External customer answer','decision_example':'Send, edit, pause, or route a drafted answer','evidence_required':'Approved source page or owner note','risk_label':'Brand / customer-specific / commercial','owner_checkpoint':'Account owner before commitments','safe_note':'Do not invent claims, prices, results, or approvals'},
    {'decision_area':'Operational automation','decision_example':'Automate, partially automate, or keep manual review','evidence_required':'Process owner note and sample edge cases','risk_label':'Operational / privacy / security','owner_checkpoint':'Process and data owner','safe_note':'Keep a human review path for uncertain cases'},
    {'decision_area':'Policy-sensitive draft','decision_example':'Answer privacy, security, legal, or compliance-like questions','evidence_required':'Current approved policy or adviser-reviewed text','risk_label':'Legal / privacy / security','owner_checkpoint':'Appropriate adviser or accountable owner','safe_note':'Educational workflow only; not adviser replacement'},
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(str(s), quote=True)
def wrap(text, width=36, max_lines=4):
    words = esc(text).split(); lines=[]; line=''
    for word in words:
        if len((line + ' ' + word).strip()) > width:
            if line: lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line: lines.append(line)
    return lines[:max_lines]

cards=[]
icons = ['Name', 'Src', 'Why', 'Risk', 'Own', 'Log']
for i,(head,body) in enumerate(checks):
    col=i%3; row=i//3
    x=74+col*364; y=294+row*250
    body_lines=''.join(f"<tspan x='{x+32}' dy='{0 if n==0 else 22}'>{ln}</tspan>" for n,ln in enumerate(wrap(body)))
    cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='{y}' width='320' height='206' rx='30' fill='white' stroke='#d7e3f4' stroke-width='2'/>
      <rect x='{x+28}' y='{y+28}' width='62' height='54' rx='18' fill='#fef3c7' stroke='#f59e0b'/>
      <text x='{x+59}' y='{y+63}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='16' font-weight='950' fill='#92400e'>{icons[i]}</text>
      <text x='{x+104}' y='{y+60}' font-family='Inter,Arial,sans-serif' font-size='22' font-weight='950' fill='#0f172a'>{esc(head)}</text>
      <text x='{x+32}' y='{y+118}' font-family='Inter,Arial,sans-serif' font-size='18' fill='#334155'>{body_lines}</text>
    </g>""")

svg=f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#1e1b4b'/><stop offset='.52' stop-color='#7c2d12'/><stop offset='1' stop-color='#0f766e'/></linearGradient>
    <filter id='shadow' x='-15%' y='-20%' width='130%' height='150%'><feDropShadow dx='0' dy='16' stdDeviation='11' flood-color='#0f172a' flood-opacity='.12'/></filter>
  </defs>
  <rect width='1200' height='900' fill='#fffbeb'/>
  <rect x='36' y='34' width='1128' height='832' rx='44' fill='white' stroke='#fde68a' stroke-width='3'/>
  <rect x='70' y='68' width='1060' height='168' rx='36' fill='url(#hero)'/>
  <text x='106' y='116' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='900' fill='#fde68a' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC</text>
  <text x='106' y='174' font-family='Inter,Arial,sans-serif' font-size='52' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='106' y='214' font-family='Inter,Arial,sans-serif' font-size='19' fill='#ccfbf1'>{esc(HOOK)}</text>
  <text x='80' y='270' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>Six trace checks before AI-assisted decisions become business actions</text>
  {''.join(cards)}
  <rect x='78' y='812' width='1044' height='36' rx='18' fill='#f8fafc' stroke='#cbd5e1'/>
  <text x='600' y='836' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='13' fill='#64748b'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

with (pub_dir / f'{SLUG}.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

checks_html=''.join(f"<li><strong>{esc(h)}:</strong> {esc(b)}</li>" for h,b in checks)
rows_html=''.join(f"<tr><td>{esc(r['decision_area'])}</td><td>{esc(r['decision_example'])}</td><td>{esc(r['evidence_required'])}</td><td>{esc(r['owner_checkpoint'])}</td></tr>" for r in rows)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#fffbeb;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#1e1b4b,#7c2d12,#0f766e);color:white;border-radius:30px;padding:36px}}.kicker{{color:#fde68a;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:42px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #fde68a;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #fcd34d}}li{{margin:12px 0;line-height:1.6}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #f8dd8d;padding:12px;text-align:left;vertical-align:top}}.boundary{{background:#0f172a;color:#e5f0ff}}a{{color:#075985;font-weight:800}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · decision trace</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Six AI decision-trace checks</h2><ul>{checks_html}</ul><p><a href='{SLUG}.csv'>Download the decision trace CSV</a></p></section><section class='card'><h2>Reusable trace examples</h2><table><thead><tr><th>Decision area</th><th>Decision example</th><th>Evidence required</th><th>Owner checkpoint</th></tr></thead><tbody>{rows_html}</tbody></table></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\nDownload the CSV: {CSV_URL}\n\n## Six AI decision-trace checks\n\n" + ''.join(f"- **{h}:** {b}\n" for h,b in checks) + f"\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
manifest_path=pub_dir / 'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest=[m for m in manifest if not (m.get('slot') == SLOT or m.get('slug') == SLUG)]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'csv': CSV_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
order={'morning':0,'afternoon':1,'evening':2}
manifest.sort(key=lambda m: order.get(m.get('slot'),9))
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links=''.join(
    f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a>"
    + (f" · <a href='{esc(m['csv'].split('/')[-1])}'>CSV template</a>" if m.get('csv') else "")
    + (" · <a href='ai-source-evidence-register-template.csv'>source evidence register template</a>" if m.get('slug') == 'ai-source-evidence-card' else "")
    + "</li>"
    for m in manifest
)
(pub_dir / 'index.html').write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals and downloadable owner-evidence templates.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals and downloadable owner-evidence templates; not legal, compliance, medical, financial, security, or guaranteed-performance advice.</p><ul>{links}</ul></section></main></body></html>", encoding='utf-8')
(pub_dir / 'publish-log.md').write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" + (f"- {m['slot'].title()} CSV: {m['csv']}\n" if m.get('csv') else '') for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest if m.get('slot') in ['morning','evening']) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
mirror = Path('/home/agent/.hermes/aicloudstrategist/publications') / DATE
mirror.mkdir(parents=True, exist_ok=True)
(mirror / 'publish-log.md').write_text((pub_dir / 'publish-log.md').read_text(encoding='utf-8'), encoding='utf-8')

evidence_dir=REPO / 'docs' / 'publication-evidence'; evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}

Post: {TITLE}

Safe educational boundaries:
- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, decision-approval, or guaranteed-performance claims.
- Infographic-style visual included as SVG and PNG.
- CSV worksheet included for operational trace use.

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
info_dir=REPO / 'infographic' / SLUG; (info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: safe AI-assisted decision traceability.\n- Data type: educational checklist with six decision-trace checks and CSV worksheet.\n- Layout: bento-grid / dense modular cards.\n- Style: warm corporate Memphis with amber, indigo, and teal colors.\n- Audience: business operators using AI assistants.\n- Language: en.\n- Safety: educational only; no client, legal, compliance, medical, savings, ranking, decision-approval, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators record why an AI-assisted business decision was made, which source supported it, and when a human owner must review it.\n\n## Six decision-trace checks\n" + ''.join(f"- **{h}:** {b}\n" for h,b in checks) + f"\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean warm corporate Memphis bento-grid infographic titled '{TITLE}' using six numbered decision-trace cards, amber/indigo/teal trust colors, rounded modular cards, clear hierarchy, and safe educational language. Aspect 4:3 worksheet.\n", encoding='utf-8')

home=REPO/'index.html'
home_text=home.read_text(encoding='utf-8')
new_article=f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Decision</span><i></i><span>Source</span><i></i><span>Owner</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3><a href="/publications/{DATE}/{SLUG}.html">{TITLE}</a></h3>
            <p>{HOOK}</p>
          </article>

'''
insert_before='          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Question</span>'
if f'/publications/{DATE}/{SLUG}.html' not in home_text:
    if insert_before in home_text:
        home_text=home_text.replace(insert_before, new_article + insert_before, 1)
    else:
        home_text=re.sub(r'(\s*</div>\s*</section>)', new_article + r'\1', home_text, count=1)
home.write_text(home_text, encoding='utf-8')

sitemap=REPO/'sitemap.xml'; sitemap_text=sitemap.read_text(encoding='utf-8')
for loc,prio in [(URL,'0.6'),(CSV_URL,'0.5'),(f'https://aicloudstrategist.com/publications/{DATE}/','0.6')]:
    if loc not in sitemap_text:
        sitemap_text=sitemap_text.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>{prio}</priority></url>\n</urlset>')
sitemap.write_text(sitemap_text, encoding='utf-8')
llms=REPO/'llms.txt'
txt=llms.read_text(encoding='utf-8')
for line in [
    f'- [{TITLE}]({URL}) — safe educational AI decision trace checklist with infographic.\n',
    f'- [AI decision trace CSV]({CSV_URL}) — reusable worksheet for evidence, risk labels, owner checkpoints, and correction trails.\n',
]:
    link=line.split('](')[1].split(')')[0]
    if link not in txt:
        txt=txt.rstrip()+"\n"+line
llms.write_text(txt, encoding='utf-8')
print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'csv': CSV_URL, 'repository': REPO_URL}, indent=2))
