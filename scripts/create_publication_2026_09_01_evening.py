from pathlib import Path
import html, json, re, subprocess

REPO = Path('/home/agent/.hermes/aicloudstrategist/repos/support-aicloudstrategist.github.io')
DATE = '2026-09-01'
SLOT = 'evening'
SLUG = 'missed-lead-follow-up-ladder'
TITLE = 'The Missed Lead Follow-Up Ladder'
HOOK = 'A safe educational infographic for turning unanswered calls, forms, and WhatsApp enquiries into an owner-visible follow-up rhythm without over-automating customer promises.'
BOUNDARY = 'Educational operations guide only — not legal, compliance, medical, financial, security, certification, revenue, savings, ranking, customer-result, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

ladder = [
    ('1', 'Capture the source', 'Record where the enquiry came from: phone, website form, WhatsApp, referral, marketplace, or ad click.'),
    ('2', 'Send a safe acknowledgement', 'Confirm the message was received and set a realistic response expectation without promising outcomes or prices.'),
    ('3', 'Route by urgency', 'Separate routine questions, owner review, sensitive topics, payment requests, and complaint or risk items.'),
    ('4', 'Show the owner queue', 'Give the business owner one daily view of open leads, stuck leads, unanswered replies, and ageing items.'),
    ('5', 'Close the loop', 'Mark each item as answered, waiting, booked, not relevant, duplicate, or needs human follow-up.'),
]
owner_checks = [
    'Do not let AI invent price, availability, guarantees, discounts, legal terms, or professional advice.',
    'Escalate sensitive messages before replying: payment, credentials, medical, legal, compliance, identity, complaint, or contract topics.',
    'Keep a visible correction log when a template or AI draft is edited by a human.',
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def esc(s): return html.escape(s, quote=True)
def wrap(text, width=42, max_lines=5):
    words = esc(text).split(); lines=[]; line=''
    for word in words:
        if len((line + ' ' + word).strip()) > width:
            if line: lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    if line: lines.append(line)
    return lines[:max_lines]

rungs=[]
colors=['#dbeafe','#ccfbf1','#dcfce7','#fef3c7','#ede9fe']
inks=['#1d4ed8','#0f766e','#166534','#92400e','#6d28d9']
for i,(num,label,text) in enumerate(ladder):
    y=276+i*104
    fill=colors[i]; ink=inks[i]
    lines=''.join(f"<tspan x='292' dy='{0 if n==0 else 21}'>{ln}</tspan>" for n,ln in enumerate(wrap(text, 64, 3)))
    rungs.append(f"""
    <g filter='url(#shadow)'>
      <rect x='196' y='{y}' width='812' height='82' rx='25' fill='white' stroke='{ink}' stroke-opacity='.28' stroke-width='2'/>
      <circle cx='244' cy='{y+41}' r='30' fill='{fill}' stroke='{ink}' stroke-width='3'/>
      <text x='244' y='{y+51}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='28' font-weight='950' fill='{ink}'>{num}</text>
      <text x='292' y='{y+30}' font-family='Inter,Arial,sans-serif' font-size='25' font-weight='950' fill='#0f172a'>{esc(label)}</text>
      <text x='292' y='{y+58}' font-family='Inter,Arial,sans-serif' font-size='17' fill='#334155'>{lines}</text>
    </g>""")

check_svg=[]
for i,check in enumerate(owner_checks):
    x=102+i*336
    lines=''.join(f"<tspan x='{x+24}' dy='{0 if n==0 else 19}'>{ln}</tspan>" for n,ln in enumerate(wrap(check, 31, 4)))
    check_svg.append(f"""
    <g>
      <rect x='{x}' y='812' width='302' height='106' rx='24' fill='#f8fafc' stroke='#cbd5e1'/>
      <text x='{x+24}' y='844' font-family='Inter,Arial,sans-serif' font-size='15' font-weight='950' fill='#2563eb' letter-spacing='1.4'>OWNER CHECK {i+1}</text>
      <text x='{x+24}' y='874' font-family='Inter,Arial,sans-serif' font-size='16' fill='#334155'>{lines}</text>
    </g>""")

svg=f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='960' viewBox='0 0 1200 960'>
  <defs>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'><stop stop-color='#111827'/><stop offset='.52' stop-color='#0f766e'/><stop offset='1' stop-color='#2563eb'/></linearGradient>
    <filter id='shadow' x='-10%' y='-20%' width='120%' height='150%'><feDropShadow dx='0' dy='12' stdDeviation='10' flood-color='#0f172a' flood-opacity='.12'/></filter>
  </defs>
  <rect width='1200' height='960' fill='#f8fbff'/>
  <rect x='42' y='36' width='1116' height='890' rx='44' fill='white' stroke='#bae6fd' stroke-width='3'/>
  <rect x='76' y='70' width='1048' height='166' rx='36' fill='url(#hero)'/>
  <text x='108' y='116' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#ccfbf1' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING INFOGRAPHIC GUIDE</text>
  <text x='108' y='171' font-family='Inter,Arial,sans-serif' font-size='50' font-weight='950' fill='white'>{esc(TITLE)}</text>
  <text x='108' y='212' font-family='Inter,Arial,sans-serif' font-size='20' fill='#dbeafe'>{esc(HOOK)}</text>
  <text x='100' y='258' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>Five rungs from missed enquiry to owner-visible action</text>
  <line x1='244' y1='260' x2='244' y2='790' stroke='#93c5fd' stroke-width='9' stroke-linecap='round'/>
  {''.join(rungs)}
  {''.join(check_svg)}
  <text x='92' y='944' font-family='Inter,Arial,sans-serif' font-size='13' fill='#64748b'>{esc(BOUNDARY)}</text>
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

ladder_html=''.join(f"<li><strong>{esc(label)}:</strong> {esc(text)}</li>" for _,label,text in ladder)
checks_html=''.join(f"<li>{esc(check)}</li>" for check in owner_checks)
ladder_md=''.join(f"- **{label}:** {text}\n" for _,label,text in ladder)
checks_md=''.join(f"- {check}\n" for check in owner_checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name='description' content='{esc(HOOK)}'>
<link rel='canonical' href='{URL}'><meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{esc(TITLE)}'><meta property='og:description' content='{esc(HOOK)}'><meta property='og:image' content='{PNG_URL}'><meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{esc(TITLE)}","description":"{esc(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f8fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#111827,#0f766e,#2563eb);color:white;border-radius:30px;padding:36px}}.kicker{{color:#ccfbf1;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #bae6fd}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#111827;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · lead follow-up operations</div><h1>{esc(TITLE)}</h1><p class='hook'>{esc(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {esc(TITLE)}'></section><section class='card'><h2>Five-rung follow-up ladder</h2><ol>{ladder_html}</ol></section><section class='card'><h2>Owner checks</h2><ul>{checks_html}</ul></section><section class='card boundary'><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Five-rung follow-up ladder\n\n{ladder_md}\n## Owner checks\n\n{checks_md}\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"""
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
manifest_path=pub_dir / 'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest=[m for m in manifest if m.get('slot') != SLOT and m.get('slug') != SLUG]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get('slot') == 'morning' else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links=''.join(f"<li><a href='{esc(m['slug'])}.html'>{esc(m['slot'].title())}: {esc(m['title'])}</a></li>" for m in manifest)
index=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>"""
(pub_dir / 'index.html').write_text(index, encoding='utf-8')
log=pub_dir / 'publish-log.md'
log.write_text(f"# Publish log — {DATE}\n\n## Assets\n" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + "\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
evidence_dir=REPO / 'docs' / 'publication-evidence'; evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`\n\nLive targets after deployment:\n- {URL}\n- {PNG_URL}\n- {REPO_URL}\n""", encoding='utf-8')
info_dir=REPO / 'infographic' / SLUG; (info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: missed lead follow-up operating rhythm.\n- Data type: educational ladder plus owner checks.\n- Layout: linear-progression ladder with modular checks.\n- Style: corporate Memphis / clean infographic.\n- Audience: business owners and operators handling phone, website form, and WhatsApp enquiries.\n- Language: en.\n- Safety: educational only; no client, legal, compliance, medical, savings, ranking, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp operators convert missed enquiries into a visible follow-up rhythm while preserving human approval for sensitive topics.\n\n## Five-rung follow-up ladder\n{ladder_md}\n## Owner checks\n{checks_md}\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean corporate Memphis linear-progression ladder infographic titled '{TITLE}' using five rungs and three owner checks from structured-content.md. Use blue, teal, green, amber, and violet modular cards, numbered circles, clear owner-queue visual hierarchy, and safe educational language. Aspect landscape.\n", encoding='utf-8')
# homepage latest card and link
home=REPO / 'index.html'
home_text=home.read_text(encoding='utf-8')
new_article=f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Capture</span><i></i><span>Route</span><i></i><span>Close</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3>{TITLE}</h3>
            <p>{HOOK}</p>
          </article>'''
home_text=re.sub(r'          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true">.*?</article>', new_article, home_text, count=1, flags=re.S)
home_text=re.sub(r'/publications/\d{4}-\d{2}-\d{2}/[^"<>]+\.html">Review the [^<]+', f'/publications/{DATE}/{SLUG}.html">Review the missed lead follow-up ladder', home_text, count=1)
home.write_text(home_text, encoding='utf-8')
# sitemap + llms
sitemap=REPO / 'sitemap.xml'; sitemap_text=sitemap.read_text(encoding='utf-8')
index_entry=f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
page_entry=f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
if f'https://aicloudstrategist.com/publications/{DATE}/' not in sitemap_text:
    sitemap_text=sitemap_text.replace('</urlset>', index_entry + '</urlset>')
if URL not in sitemap_text:
    sitemap_text=sitemap_text.replace(index_entry, page_entry + index_entry)
sitemap.write_text(sitemap_text, encoding='utf-8')
llms=REPO/'llms.txt'
if llms.exists():
    txt=llms.read_text(encoding='utf-8')
    line=f'- [{TITLE}]({URL}) — safe educational missed-lead follow-up ladder with infographic.\n'
    if URL not in txt:
        llms.write_text(txt.rstrip()+"\n"+line, encoding='utf-8')
print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
