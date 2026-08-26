from pathlib import Path
import html
import json
import subprocess

REPO = Path('/home/agent/work/support-aicloudstrategist.github.io')
DATE = '2026-08-26'
SLOT = 'morning'
SLUG = 'ai-customer-data-redaction-ladder'
TITLE = 'The AI Customer Data Redaction Ladder'
HOOK = 'A safe educational checklist for reducing sensitive customer details before using AI-assisted drafting, sorting, or analysis.'
BOUNDARY = 'Educational workflow only — not legal, compliance, medical, financial, security, certification, savings, ranking, revenue, booking, or guaranteed-performance advice.'
URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.html'
PNG_URL = f'https://aicloudstrategist.com/publications/{DATE}/{SLUG}.png'
REPO_URL = f'https://github.com/support-aicloudstrategist/support-aicloudstrategist.github.io/tree/main/publications/{DATE}'

levels = [
    ('1', 'Remove direct identifiers', '#0ea5e9', 'Names, phone numbers, email addresses, IDs, booking references, addresses, photos, and exact account labels.'),
    ('2', 'Generalise context', '#6366f1', 'Replace exact dates, locations, employee names, case numbers, prices, and unusually specific events with safer ranges.'),
    ('3', 'Limit business facts', '#f97316', 'Share only the minimum product, process, queue, or policy detail needed for the AI task to work.'),
    ('4', 'Keep a human gate', '#16a34a', 'Require a named owner to review anything customer-facing, uncertain, emotional, regulated, or commercially sensitive.'),
]
checks = [
    ('Purpose', 'Is the AI task narrow, internal, and necessary?'),
    ('Minimum', 'Can the example be synthetic, sampled, or shortened?'),
    ('Access', 'Who can see prompts, files, outputs, and logs?'),
    ('Review', 'Who approves before a message, report, or change leaves the business?'),
    ('Record', 'Where is the redaction decision saved for later review?'),
]

pub_dir = REPO / 'publications' / DATE
pub_dir.mkdir(parents=True, exist_ok=True)

def wrap_svg_text(text, width=44, max_lines=3):
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

level_cards = []
y_positions = [280, 405, 530, 655]
for (num, label, color, text), y in zip(levels, y_positions):
    tspans = ''.join(f"<tspan x='265' dy='{0 if j == 0 else 22}'>{ln}</tspan>" for j, ln in enumerate(wrap_svg_text(text, 70)))
    level_cards.append(f"""
    <g filter='url(#shadow)'>
      <rect x='92' y='{y}' width='1016' height='94' rx='28' fill='#ffffff' stroke='#dbeafe'/>
      <circle cx='152' cy='{y+47}' r='35' fill='{color}'/>
      <text x='152' y='{y+59}' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='34' font-weight='950' fill='#fff'>{num}</text>
      <text x='215' y='{y+42}' font-family='Inter,Arial,sans-serif' font-size='26' font-weight='950' fill='#132033'>{html.escape(label)}</text>
      <text x='265' y='{y+71}' font-family='Inter,Arial,sans-serif' font-size='16.5' fill='#334155'>{tspans}</text>
    </g>""")

check_items = []
for i, (label, text) in enumerate(checks):
    x = 72 + i * 214
    check_items.append(f"""
      <g>
        <rect x='{x}' y='794' width='186' height='76' rx='19' fill='#f8fafc' stroke='#cbd5e1'/>
        <text x='{x+93}' y='823' text-anchor='middle' font-family='Inter,Arial,sans-serif' font-size='17' font-weight='950' fill='#0f172a'>{html.escape(label)}</text>
        <text x='{x+14}' y='851' font-family='Inter,Arial,sans-serif' font-size='12.4' fill='#475569'>{html.escape(text[:58])}</text>
      </g>""")

svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='900' viewBox='0 0 1200 900'>
  <defs>
    <linearGradient id='bg' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#eff6ff'/><stop offset='48%' stop-color='#ecfeff'/><stop offset='100%' stop-color='#f0fdf4'/></linearGradient>
    <filter id='shadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='13' stdDeviation='13' flood-color='#0f172a' flood-opacity='.13'/></filter>
  </defs>
  <rect width='1200' height='900' fill='url(#bg)'/>
  <rect x='42' y='42' width='1116' height='816' rx='42' fill='rgba(255,255,255,.80)' stroke='#bae6fd'/>
  <text x='75' y='104' font-family='Inter,Arial,sans-serif' font-size='18' font-weight='900' fill='#0369a1' letter-spacing='3'>AICLOUDSTRATEGIST · MORNING DATA MINIMISATION CHECKLIST</text>
  <text x='75' y='166' font-family='Inter,Arial,sans-serif' font-size='54' font-weight='950' fill='#111827'>{html.escape(TITLE)}</text>
  <text x='75' y='211' font-family='Inter,Arial,sans-serif' font-size='22' fill='#334155'>{html.escape(HOOK)}</text>
  <path d='M152 247 L152 760' stroke='#cbd5e1' stroke-width='5' stroke-linecap='round' stroke-dasharray='12 16'/>
  {''.join(level_cards)}
  <text x='78' y='762' font-family='Inter,Arial,sans-serif' font-size='21' font-weight='950' fill='#0f172a'>Five questions before using real customer examples with AI</text>
  {''.join(check_items)}
</svg>"""
(pub_dir / f'{SLUG}.svg').write_text(svg, encoding='utf-8')
subprocess.run(['convert', str(pub_dir / f'{SLUG}.svg'), str(pub_dir / f'{SLUG}.png')], check=True)

levels_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for _, label, _, text in levels)
checks_html = ''.join(f"<li><strong>{html.escape(label)}:</strong> {html.escape(text)}</li>" for label, text in checks)
levels_md = ''.join(f"- **{label}:** {text}\n" for _, label, _, text in levels)
checks_md = ''.join(f"- **{label}:** {text}\n" for label, text in checks)
page = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(TITLE)} | AICloudStrategist</title><meta name='description' content='{html.escape(HOOK)}'>
<link rel='canonical' href='{URL}'>
<meta property='og:type' content='article'><meta property='og:site_name' content='AICloudStrategist'><meta property='og:title' content='{html.escape(TITLE)}'><meta property='og:description' content='{html.escape(HOOK)}'><meta property='og:image' content='{PNG_URL}'>
<meta name='twitter:card' content='summary_large_image'>
<script type='application/ld+json'>{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(HOOK)}","image":"{PNG_URL}","datePublished":"{DATE}","dateModified":"{DATE}","author":{{"@type":"Organization","name":"AICloudStrategist"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist"}}}}</script>
<style>body{{margin:0;background:#f6fbff;color:#152033;font-family:Inter,Segoe UI,Arial,sans-serif}}.wrap{{max-width:1080px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f766e,#0369a1);color:white;border-radius:30px;padding:36px}}.kicker{{color:#bae6fd;text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:900}}h1{{font-size:43px;line-height:1.08;margin:14px 0}}.hook{{font-size:20px;line-height:1.45}}.card{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px;margin:22px 0;box-shadow:0 14px 35px rgba(15,23,42,.08)}}img{{max-width:100%;border-radius:24px;border:1px solid #d8e6f3}}li{{margin:12px 0;line-height:1.6}}.boundary{{background:#0f172a;color:#e5f0ff}}</style></head><body><main class='wrap'><section class='hero'><div class='kicker'>Morning publication · AI data minimisation</div><h1>{html.escape(TITLE)}</h1><p class='hook'>{html.escape(HOOK)}</p></section><section class='card'><img src='{SLUG}.png' alt='Infographic: {html.escape(TITLE)}'></section><section class='card'><h2>Four redaction levels</h2><ul>{levels_html}</ul></section><section class='card'><h2>Five questions before using customer examples</h2><ul>{checks_html}</ul></section><section class='card'><h2>How to use this ladder</h2><p>Use this ladder before pasting real messages, tickets, exports, notes, recordings, transcripts, or reports into any AI-assisted workflow. Start with synthetic or redacted examples, keep the AI task narrow, and pause customer-facing outputs for human review.</p></section><section class='card boundary'><h2>Truth boundary</h2><p>{html.escape(BOUNDARY)}</p></section></main></body></html>"""
(pub_dir / f'{SLUG}.html').write_text(page, encoding='utf-8')

post_md = f"""# {TITLE}\n\n![Infographic: {TITLE}]({PNG_URL})\n\n{HOOK}\n\n## Four redaction levels\n\n{levels_md}\n## Five questions before using customer examples\n\n{checks_md}\n## How to use it\n\nUse this ladder before pasting real messages, tickets, exports, notes, recordings, transcripts, or reports into any AI-assisted workflow. Start with synthetic or redacted examples, keep the AI task narrow, and pause customer-facing outputs for human review.\n\n**Truth boundary:** {BOUNDARY}\n\nPublic checklist and infographic: {URL}\n"""
(pub_dir / f'{SLUG}.md').write_text(post_md, encoding='utf-8')

manifest_path = pub_dir / 'manifest.json'
manifest = []
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest = [m for m in manifest if m.get('slot') != SLOT and m.get('slug') != SLUG]
manifest.append({'slot': SLOT, 'slug': SLUG, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL, 'boundary': BOUNDARY})
manifest.sort(key=lambda m: 0 if m.get('slot') == 'morning' else 1)
manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

links = ''.join(f"<li><a href='{html.escape(m['slug'])}.html'>{html.escape(m['slot'].title())}: {html.escape(m['title'])}</a></li>" for m in manifest)
index = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>AICS publications {DATE}</title><meta name='description' content='AICloudStrategist safe educational publications for {DATE}, with infographic-style visuals.'><link rel='canonical' href='https://aicloudstrategist.com/publications/{DATE}/'><style>body{{font-family:Inter,Segoe UI,Arial,sans-serif;background:#f8fbff;color:#152033;margin:0}}main{{max-width:900px;margin:auto;padding:40px 18px}}section{{background:white;border:1px solid #d8e6f3;border-radius:24px;padding:24px}}</style></head><body><main><section><h1>AICS publications — {DATE}</h1><p>Safe educational posts with infographic-style visuals.</p><ul>{links}</ul></section></main></body></html>"""
(pub_dir / 'index.html').write_text(index, encoding='utf-8')

log = pub_dir / 'publish-log.md'
log.write_text(f"""# Publish log — {DATE}\n\n## Assets\n""" + ''.join(f"- {m['slot'].title()} — {m['title']}: {m['url']}\n- {m['slot'].title()} PNG: {m['png']}\n" for m in manifest) + f"\n## Published / verified\n" + ''.join(f"- AICS website / GitHub Pages — {m['slot'].title()}: {m['url']}\n- GitHub repository / deployment evidence — {m['slot'].title()}: {m['repository']}\n" for m in manifest) + f"\n## Verification boundary\n{BOUNDARY}\n", encoding='utf-8')

evidence_dir = REPO / 'docs' / 'publication-evidence'
evidence_dir.mkdir(parents=True, exist_ok=True)
(evidence_dir / f'{DATE}-{SLOT}-{SLUG}.md').write_text(f"""# Publication evidence — {DATE} {SLOT}\n\nPost: {TITLE}\n\nSafe educational boundaries:\n- No client names, testimonials, savings, rankings, booking, revenue, legal, medical, compliance, security, certification, or guaranteed-performance claims.\n- Infographic-style visual included as SVG and PNG.\n\nPublished surfaces in this repository:\n- Website/GitHub Pages page: `/publications/{DATE}/{SLUG}.html`\n- Infographic assets: `/publications/{DATE}/{SLUG}.svg` and `/publications/{DATE}/{SLUG}.png`\n- Markdown cross-post copy: `/publications/{DATE}/{SLUG}.md`\n\nLive targets after deployment:\n- {URL}\n- {PNG_URL}\n- {REPO_URL}\n""", encoding='utf-8')

home = REPO / 'index.html'
home_text = home.read_text(encoding='utf-8')
old_card = '<div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Need</span><i></i><span>Data</span><i></i><span>Access</span></div>\n            <span class="ea-evidence-type">Public educational asset · 2026-08-25</span>\n            <h3>The AI Vendor Access Review Board</h3>\n            <p>A safe checklist for reviewing what an AI vendor or tool may access before it touches business data.</p>'
new_card = '<div class="ea-mini-art ea-architecture-art" aria-hidden="true"><span>Mask</span><i></i><span>Limit</span><i></i><span>Review</span></div>\n            <span class="ea-evidence-type">Public educational asset · 2026-08-26</span>\n            <h3>The AI Customer Data Redaction Ladder</h3>\n            <p>A safe checklist for reducing sensitive customer details before using AI-assisted drafting, sorting, or analysis.</p>'
if old_card in home_text:
    home_text = home_text.replace(old_card, new_card)
home_text = home_text.replace('/publications/2026-08-25/ai-vendor-access-review-board.html">Review the AI vendor access review board', '/publications/2026-08-26/ai-customer-data-redaction-ladder.html">Review the AI customer data redaction ladder')
home.write_text(home_text, encoding='utf-8')

sitemap = REPO / 'sitemap.xml'
sitemap_text = sitemap.read_text(encoding='utf-8')
index_entry = f'  <url><loc>https://aicloudstrategist.com/publications/{DATE}/</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
page_entry = f'  <url><loc>{URL}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
if f'https://aicloudstrategist.com/publications/{DATE}/' not in sitemap_text:
    sitemap_text = sitemap_text.replace('</urlset>', index_entry + '</urlset>')
if URL not in sitemap_text:
    sitemap_text = sitemap_text.replace(index_entry, page_entry + index_entry)
sitemap.write_text(sitemap_text, encoding='utf-8')

print(json.dumps({'slot': SLOT, 'title': TITLE, 'url': URL, 'png': PNG_URL, 'repository': REPO_URL}, indent=2))
