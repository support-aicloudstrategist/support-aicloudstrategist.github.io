from pathlib import Path
import html
import json
import re
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-28'
SLOT = 'evening'
SLUG = 'automation-readiness-traffic-light'
TITLE = 'The Automation Readiness Traffic Light'
HOOK = 'A safe educational worksheet for deciding whether a workflow is ready for automation, needs human review, or should stay manual until facts are clearer.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

lanes = [
    ('RED', 'Keep manual', '#dc2626', 'Use manual handling when the input is sensitive, the rule is unclear, the impact is external, or the owner cannot explain the decision path.'),
    ('AMBER', 'Human review first', '#f59e0b', 'Use assisted drafts only when a responsible reviewer can inspect the facts, approve the wording, and record unresolved questions.'),
    ('GREEN', 'Automate carefully', '#16a34a', 'Automate only when the trigger, allowed data, owner, exception path, audit log, and rollback step are documented.'),
]
checks = [
    ('Trigger', 'What event starts the workflow, and can it be detected reliably?'),
    ('Data', 'Which fields are allowed, necessary, and safe to process?'),
    ('Owner', 'Who owns approval, exception handling, and rollback?'),
    ('Evidence', 'What log proves what happened and why?'),
    ('Exit', 'How does a person pause or reverse the automation?'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def wrap(text, width=42, max_lines=5):
    words = html.escape(text).split()
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

lane_svg=[]
for i,(name,label,color,text) in enumerate(lanes):
    x=86+i*365
    text_lines=''.join(f"<tspan x='{x+32}' dy='{0 if n==0 else 23}'>{ln}</tspan>" for n,ln in enumerate(wrap(text)))
    lane_svg.append(f"""
    <g filter='url(#shadow)'>
      <rect x='{x}' y='302' width='318' height='338' rx='34' fill='#ffffff' stroke='{color}' stroke-width='4'/>
      <circle cx='{x+72}' cy='374' r='42' fill='{color}'/>
      <text x='{x+72}' y='384' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='20' font-weight='950' fill='#fff'>{name}</text>
      <text x='{x+32}' y='464' font-family='Inter,Arial,sans-serif' font-size='31' font-weight='950' fill='#111827'>{html.escape(label)}</text>
      <text x='{x+32}' y='522' font-family='Inter,Arial,sans-serif' font-size='18' fill='#334155'>{text_lines}</text>
    </g>""")

check_svg=[]
for i,(label,text) in enumerate(checks):
    x=68+i*224
    check_svg.append(f"""
      <g>
        <rect x='{x}' y='742' width='190' height='116' rx='24' fill='#f8fafc' stroke='#cbd5e1'/>
        <text x='{x+95}' y='783' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='950' fill='#0f172a'>{html.escape(label)}</text>
        <text x='{x+16}' y='816' font-family='Inter,Arial,sans-serif' font-size='12.4' fill='#475569'>{html.escape(text[:68])}</text>
      </g>""")

svg=f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='940' viewBox='0 0 1200 940'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#fef2f2'/><stop offset='50%' stop-color='#fffbeb'/><stop offset='100%' stop-color='#ecfdf5'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='16' stdDeviation='13' flood-color='#0f172a' flood-opacity='.14'/></filter>
  </defs>
  <rect width='1200' height='940' fill='url(#bg)'/>
  <rect x='44' y='44' width='1112' height='852' rx='44' fill='rgba(255,255,255,.80)' stroke='#fde68a'/>
  <text x='76' y='106' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#92400e' letter-spacing='3'>AICLOUDSTRATEGIST · EVENING AUTOMATION WORKSHEET</text>
  <text x='76' y='166' font-family='Inter,Arial,sans-serif' font-size='54' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='76' y='214' font-family='Inter,Arial,sans-serif' font-size='21' fill='#334155'>{html.escape(HOOK)}</text>
  <rect x='86' y='250' width='1028' height='12' rx='6' fill='#e5e7eb'/>
  <circle cx='245' cy='256' r='28' fill='#dc2626'/><circle cx='610' cy='256' r='28' fill='#f59e0b'/><circle cx='975' cy='256' r='28' fill='#16a34a'/>
  {''.join(lane_svg)}
  <text x='76' y='712' font-family='Inter,Arial,sans-serif' font-size='23' font-weight='950' fill='#0f172a'>Five checks before changing the light to green</text>
  {''.join(check_svg)}
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

lanes_html=''.join(f"<li><strong>{html.escape(name)} — {html.escape(label)}:</strong> {html.escape(text)}</li>" for name,label,_,text in lanes)
checks_html=''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for label,text in checks)
lanes_md=''.join(f"- **{name} — {label}:** {text}\n" for name,label,_,text in lanes)
checks_md=''.join(f"- **{label}:** {text}\n" for label,text in checks)
page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='{URL}'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='{PNG_URL}'>
<meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#fffdf6;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#991b1b,#a16207,#166534);color:white;border-radius:30px;padding:36px}}.kicker{{color:#fde68a;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #f5ddb0;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #f5ddb0}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Evening publication · automation readiness</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Three readiness lights</h2><ul>{lanes_html}</ul></section><section class='card'><h2>Five checks before green</h2><ul>{checks_html}</ul></section><section class='card'><h2>How to use this worksheet</h2><p>Use the traffic light when a team wants to automate a repeatable workflow but has not yet agreed on evidence, ownership, exceptions, and rollback. The worksheet keeps automation decisions visible and reversible before a workflow affects customers, staff, or public messages.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')
post_md=f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Three readiness lights\n\n{lanes_md}\n## Five checks before green\n\n{checks_md}\n## How to use it\n\nUse the traffic light when a team wants to automate a repeatable workflow but has not yet agreed on evidence, ownership, exceptions, and rollback. The worksheet keeps automation decisions visible and reversible before a workflow affects customers, staff, or public messages.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic worksheet and infographic: {URL}\n"""
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')
manifest_path=pub_dir / 'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
manifest=[m for m in manifest if m.get('slot') != SLOT and m.get('slug') != SLUG]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get('slot') == 'morning' else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
links=''.join(f"<li><a href='{html.escape(m['slug'])}.html'>{html.escape(m['slot'].title())}: {html.escape(m['title'])}</a></li>" for m in manifest)
index=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>"""
(pub_dir / 'index.html').write_text(index, encoding='utf-8')
log=pub_dir / 'publish-log.md'
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n""" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + f"\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')
evidence_dir=REPO / 'docs' / 'publication-evidence'
evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`\n\nLive targets after deployment:\n- {URL}\n- {PNG_URL}\n- {REPO_URL}\n""", encoding='utf-8')
info_dir=REPO / 'infographic' / SLUG
(info_dir / 'prompts').mkdir(parents=True, exist_ok=True)
(info_dir / 'source.md').write_text(post_md, encoding='utf-8')
(info_dir / 'analysis.md').write_text(f"# Analysis — {TITLE}\n\n- Topic: automation readiness and safe workflow ownership.\n- Layout: dashboard traffic-light / bento worksheet.\n- Style: corporate Memphis with clear red/amber/green decision cards.\n- Audience: business operators adopting AI and automation.\n- Language: en.\n- Safety: educational only; no customer, legal, compliance, savings, ranking, or guaranteed claims.\n", encoding='utf-8')
(info_dir / 'structured-content.md').write_text(f"# Structured content — {TITLE}\n\n## Learning objective\nHelp teams classify automation readiness as manual, human-review, or carefully automated.\n\n## Sections\n{lanes_md}\n## Review checks\n{checks_md}\n\n## Boundary\n{BOUNDARY}\n", encoding='utf-8')
(info_dir / 'prompts' / 'infographic.md').write_text(f"Create a clean corporate Memphis traffic-light dashboard infographic titled '{TITLE}' using the three lights and five checks from structured-content.md. Aspect 16:9-ish wide educational worksheet. Keep all claims educational and avoid client/result/legal/compliance claims.\n", encoding='utf-8')
home=REPO / 'index.html'
home_text=home.read_text(encoding='utf-8')
new_article=f'''          <article class="ea-evidence-item">
            <div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Red</span><i></i><span>Amber</span><i></i><span>Green</span></div>
            <span class="ea-evidence-type">Public educational asset · {DATE}</span>
            <h3>{TITLE}</h3>
            <p>{HOOK}</p>
          </article>'''
home_text=re.sub(r'          <article class="ea-evidence-item">\n            <div class="ea-mini-art ea-architecture-art" aria-hidden="true">.*?</article>', new_article, home_text, count=1, flags=re.S)
home_text=re.sub(r'/publications/\d{4}-\d{2}-\d{2}/[^"<>]+\.html">Review the [^<]+', f'/publications/{DATE}/{SLUG}.html">Review the automation readiness traffic light', home_text, count=1)
home.write_text(home_text, encoding='utf-8')
sitemap=REPO / 'sitemap.xml'
sitemap_text=sitemap.read_text(encoding='utf-8')
index_entry=f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
page_entry=f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
if f'https://aicloudstrategist.com/publications/{DATE}/' not in sitemap_text:
    sitemap_text=sitemap_text.replace('</urlset>', index_entry + '</urlset>')
if URL not in sitemap_text:
    sitemap_text=sitemap_text.replace(index_entry, page_entry + index_entry)
sitemap.write_text(sitemap_text, encoding='utf-8')
print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
