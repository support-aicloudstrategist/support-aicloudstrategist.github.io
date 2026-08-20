from pathlib import Path
import html
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-08-20"
SLUG = "overnight-ai-automation-safety-handoff"
TITLE = "Overnight AI automation safety handoff: 5 owner checks before the team logs off"
DESC = "A safe educational checklist for small teams that run AI, forms, chatbots, reminders, or workflow automation after business hours."
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE_DIR = ROOT / "resources" / SLUG
INFO_DIR = ROOT / "infographic" / SLUG
EVIDENCE_DIR = ROOT / "docs" / "publication-evidence"
PAGE_DIR.mkdir(parents=True, exist_ok=True)
INFO_DIR.mkdir(parents=True, exist_ok=True)
(INFO_DIR / "prompts").mkdir(parents=True, exist_ok=True)
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

source = """Topic: Overnight AI automation safety handoff for small teams.
Audience: business owners, ops managers, clinic/admin teams, agencies, SaaS operators, and local-service teams using AI or automation after hours.
Safe boundaries: educational workflow only; no client claims, no legal/compliance advice, no savings, no medical advice, no guaranteed outcomes.
Core checks: owner, queue, stop rule, customer promise, morning review.
"""
analysis = """# Analysis — Overnight AI automation safety handoff

- Topic: Safe owner-led handoff before AI/automation runs after business hours.
- Data type: Educational checklist and operational control framework.
- Complexity: Low-to-medium; intended for owners and managers, not engineers only.
- Tone: Practical, calm, buyer-safe, non-claim-based.
- Audience: Small teams using forms, chatbots, reminders, workflow tools, CRMs, or AI assistants.
- Language: English.
- Design: bento-grid + corporate-memphis, landscape 16:9, infographic-style SVG.
- Truth boundary: No client claims, legal advice, compliance certification, medical advice, savings, rankings, or guaranteed outcomes.
"""
structured = """# Structured content — Overnight AI automation safety handoff

## Title
Overnight AI automation safety handoff: 5 owner checks before the team logs off

## Learning objectives
- Help owners pause risky automation before staff leave.
- Help teams define a human owner, queue, stop rule, customer promise, and morning review.
- Keep the guidance educational, not legal/compliance/medical/performance advice.

## Sections

### 1. Named owner
Content: Every overnight workflow needs one named owner for escalation.
Visual element: Owner badge with escalation arrow.
Text labels: Named owner; escalation path.

### 2. Visible queue
Content: Keep pending leads, customer questions, failed jobs, and manual reviews in one visible queue.
Visual element: Shared inbox/checklist panel.
Text labels: Pending; failed; manual review.

### 3. Stop rule
Content: Define when automation should stop instead of continuing silently.
Visual element: Red stop switch.
Text labels: Stop; hold; human review.

### 4. Customer promise
Content: Match every automatic reply to a promise the team can actually honour the next business day.
Visual element: Message bubble with calendar.
Text labels: Promise; next business day.

### 5. Morning review
Content: Start the next day by checking exceptions before adding new automation.
Visual element: Sunrise dashboard.
Text labels: Exceptions first; improve later.

## Data points
- No statistics used.
- No customer examples used.
- No performance claims used.

## Boundary label
Educational workflow — no legal, compliance, medical, or performance advice.
"""
prompt = """Create a professional infographic following these specifications:

## Image Specifications
- Type: Infographic
- Layout: bento-grid
- Style: corporate-memphis
- Aspect Ratio: 16:9
- Language: English

## Layout Guidelines
Modular grid layout with varied cell sizes, clear cell boundaries, a hero cell, supporting cells, concise labels, and visual hierarchy through size.

## Style Guidelines
Flat vector corporate Memphis style with white/light pastel background, saturated purple, orange, teal, yellow accents, clean sans-serif typography, abstract geometric elements, friendly business tone.

## Content
Title: Overnight AI automation safety handoff: 5 owner checks before the team logs off
Hero: Before automation runs overnight, confirm who owns exceptions and what must stop for human review.
Cells: Named owner; Visible queue; Stop rule; Customer promise; Morning review.
Boundary: Educational workflow — no legal, compliance, medical, or performance advice.
"""
(INFO_DIR / "source.md").write_text(source, encoding="utf-8")
(INFO_DIR / "analysis.md").write_text(analysis, encoding="utf-8")
(INFO_DIR / "structured-content.md").write_text(structured, encoding="utf-8")
(INFO_DIR / "prompts" / "infographic.md").write_text(prompt, encoding="utf-8")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">Overnight AI automation safety handoff</title>
<desc id="desc">Five owner checks before automation runs after hours: named owner, visible queue, stop rule, customer promise, morning review.</desc>
<rect width="1600" height="900" fill="#f7fbff"/>
<circle cx="1370" cy="120" r="120" fill="#ffe082" opacity="0.75"/>
<circle cx="150" cy="790" r="150" fill="#7c4dff" opacity="0.12"/>
<path d="M1180 740c120-80 220-52 330-122" fill="none" stroke="#00bcd4" stroke-width="20" opacity="0.25" stroke-linecap="round"/>
<text x="80" y="92" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="800" fill="#172033">Overnight AI automation safety handoff</text>
<text x="82" y="140" font-family="Inter,Arial,sans-serif" font-size="26" font-weight="600" fill="#40526b">5 owner checks before the team logs off</text>
<g transform="translate(80 190)">
  <rect x="0" y="0" width="690" height="300" rx="34" fill="#18233a"/>
  <text x="42" y="64" font-family="Inter,Arial,sans-serif" font-size="28" font-weight="800" fill="#ffffff">Before automation runs overnight</text>
  <text x="42" y="112" font-family="Inter,Arial,sans-serif" font-size="25" fill="#dbe7ff">Confirm who owns exceptions,</text>
  <text x="42" y="150" font-family="Inter,Arial,sans-serif" font-size="25" fill="#dbe7ff">where the queue is visible, and</text>
  <text x="42" y="188" font-family="Inter,Arial,sans-serif" font-size="25" fill="#dbe7ff">what must stop for human review.</text>
  <rect x="420" y="86" width="188" height="138" rx="28" fill="#00d4b8"/>
  <circle cx="514" cy="124" r="28" fill="#fff" opacity="0.9"/>
  <rect x="470" y="166" width="88" height="44" rx="22" fill="#fff" opacity="0.9"/>
  <path d="M608 156l42 0" stroke="#ff7a59" stroke-width="14" stroke-linecap="round"/>
</g>
<g font-family="Inter,Arial,sans-serif">
  <g transform="translate(810 190)"><rect width="300" height="300" rx="32" fill="#ffffff" stroke="#d9e3f0"/><circle cx="82" cy="86" r="42" fill="#7c4dff"/><text x="142" y="76" font-size="25" font-weight="800" fill="#172033">1. Named owner</text><text x="36" y="152" font-size="22" fill="#46566c">One person owns</text><text x="36" y="184" font-size="22" fill="#46566c">escalation tonight.</text><path d="M65 226h150l-34-34" fill="none" stroke="#ff7a59" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>
  <g transform="translate(1140 190)"><rect width="380" height="300" rx="32" fill="#ffffff" stroke="#d9e3f0"/><rect x="44" y="52" width="96" height="118" rx="18" fill="#00bcd4" opacity="0.22"/><path d="M66 88h52M66 122h52M66 156h38" stroke="#00a4b8" stroke-width="10" stroke-linecap="round"/><text x="164" y="76" font-size="25" font-weight="800" fill="#172033">2. Visible queue</text><text x="164" y="126" font-size="22" fill="#46566c">Pending, failed, and</text><text x="164" y="158" font-size="22" fill="#46566c">manual-review items</text><text x="164" y="190" font-size="22" fill="#46566c">stay in one place.</text></g>
  <g transform="translate(80 530)"><rect width="440" height="250" rx="32" fill="#ffffff" stroke="#d9e3f0"/><circle cx="88" cy="94" r="48" fill="#ff7a59"/><rect x="58" y="86" width="60" height="16" rx="8" fill="#fff"/><text x="162" y="78" font-size="25" font-weight="800" fill="#172033">3. Stop rule</text><text x="42" y="158" font-size="22" fill="#46566c">Define when automation must</text><text x="42" y="190" font-size="22" fill="#46566c">hold instead of continuing silently.</text></g>
  <g transform="translate(555 530)"><rect width="440" height="250" rx="32" fill="#ffffff" stroke="#d9e3f0"/><path d="M54 64h148a34 34 0 0134 34v38a34 34 0 01-34 34h-74l-52 42v-42H54a34 34 0 01-34-34V98a34 34 0 0134-34z" fill="#ffe082"/><text x="262" y="78" font-size="25" font-weight="800" fill="#172033">4. Customer promise</text><text x="262" y="126" font-size="22" fill="#46566c">Only promise what</text><text x="262" y="158" font-size="22" fill="#46566c">the team can honour</text><text x="262" y="190" font-size="22" fill="#46566c">next business day.</text></g>
  <g transform="translate(1030 530)"><rect width="490" height="250" rx="32" fill="#ffffff" stroke="#d9e3f0"/><circle cx="100" cy="112" r="54" fill="#ffca28"/><rect x="52" y="116" width="96" height="42" fill="#ffffff" opacity="0.7"/><path d="M220 92h185M220 132h142M220 172h205" stroke="#00d4b8" stroke-width="13" stroke-linecap="round"/><text x="42" y="214" font-size="25" font-weight="800" fill="#172033">5. Morning review</text></g>
</g>
<text x="80" y="842" font-family="Inter,Arial,sans-serif" font-size="20" font-weight="700" fill="#5a6778">Educational workflow — no legal, compliance, medical, or performance advice.</text>
</svg>'''
(PAGE_DIR / "infographic.svg").write_text(svg, encoding="utf-8")

page = f'''<!doctype html><html lang="en-IN"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(TITLE)} | AICloudStrategist</title>
<meta name="description" content="{html.escape(DESC)}"/>
<link rel="canonical" href="{URL}"/>
<meta property="og:type" content="article"/><meta property="og:site_name" content="AICloudStrategist"/>
<meta property="og:title" content="{html.escape(TITLE)}"/><meta property="og:description" content="{html.escape(DESC)}"/>
<meta property="og:url" content="{URL}"/><meta property="og:image" content="{URL}infographic.svg"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="{html.escape(TITLE)}"/><meta name="twitter:description" content="{html.escape(DESC)}"/><meta name="twitter:image" content="{URL}infographic.svg"/>
<link rel="stylesheet" href="/css/styles.css?v=clean-navbar-20260604"/>
<link rel="stylesheet" href="/css/site-navigation.css?v=premium-shell-20260727"><script defer src="/js/site-navigation.js?v=premium-shell-20260727"></script>
<script defer src="/js/aics-analytics-shim.js"></script><script defer src="/js/aics-conversion-tracking.js"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{html.escape(TITLE)}","description":"{html.escape(DESC)}","url":"{URL}","image":"{URL}infographic.svg","author":{{"@type":"Organization","name":"AICloudStrategist","url":"https://aicloudstrategist.com/"}},"publisher":{{"@type":"Organization","name":"AICloudStrategist","url":"https://aicloudstrategist.com/","logo":{{"@type":"ImageObject","url":"https://aicloudstrategist.com/assets/brand/aics-logo.svg"}}}},"datePublished":"{TODAY}","dateModified":"{TODAY}","inLanguage":"en-IN"}}</script>
</head><body class="reform-site"><div data-aics-navigation-mount></div>
<main>
<section class="page-hero"><div class="container"><p class="section-tag">Evening publication · Safe educational workflow</p><h1>{html.escape(TITLE)}</h1><p>{html.escape(DESC)}</p><p><strong>Boundary:</strong> Educational workflow — no legal, compliance, medical, or performance advice.</p></div></section>
<section class="section"><div class="container"><img src="infographic.svg" alt="Overnight AI automation safety handoff infographic showing five owner checks" style="width:100%;height:auto;border-radius:24px;box-shadow:0 18px 50px rgba(15,23,42,.12);background:#f7fbff"/></div></section>
<section class="section"><div class="container grid2">
<article class="card"><h2>1. Name the owner</h2><p>Every overnight workflow needs one named owner for escalation. If nobody owns exceptions, the automation is not ready to run unattended.</p></article>
<article class="card"><h2>2. Keep one visible queue</h2><p>Pending leads, customer questions, failed jobs, and manual reviews should land in one visible queue the next team member can check.</p></article>
<article class="card"><h2>3. Define the stop rule</h2><p>Decide which signals should make automation hold for human review instead of continuing silently.</p></article>
<article class="card"><h2>4. Match the customer promise</h2><p>Automatic replies should only make promises the team can honour on the next business day.</p></article>
<article class="card"><h2>5. Review exceptions first</h2><p>Start the next morning by checking exceptions, failed messages, and manual-review items before adding new automation.</p></article>
<article class="card"><h2>Use this before adding tools</h2><p>This is a simple operating checklist for owners and managers. It does not replace professional legal, compliance, medical, security, or platform-specific advice.</p></article>
</div></section>
<section class="section band"><div class="container"><h2>Copy-paste handoff note</h2><p><strong>Tonight's automation owner:</strong> ____ · <strong>Queue:</strong> ____ · <strong>Stop rule:</strong> ____ · <strong>Customer promise:</strong> ____ · <strong>Morning reviewer:</strong> ____</p></div></section>
</main>
<footer class="aics-footer"><div class="container"><div class="aics-footer-bottom"><span>© AICloudStrategist</span><span class="aics-footer-legal"><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></span><span>Enterprise-grade, not enterprise-exclusive.</span></div></div></footer>
</body></html>'''
(PAGE_DIR / "index.html").write_text(page, encoding="utf-8")

evidence = f"""# Publication evidence — {TODAY} evening

Post: {TITLE}

Safe educational boundaries:
- No client names or testimonials.
- No savings, ranking, booking, revenue, legal, medical, compliance, certification, or guaranteed-performance claims.
- Infographic-style visual included as local SVG.

Published surfaces in this repository:
- Website/GitHub Pages page: `/resources/{SLUG}/`
- Infographic asset: `/resources/{SLUG}/infographic.svg`
- Sitemap entry added: `/sitemap.xml`
- Repository/deployment evidence: this file.

Verification markers:
- Page title: `{TITLE}`
- Visual marker: `Overnight AI automation safety handoff`
- Boundary marker: `Educational workflow — no legal, compliance, medical, or performance advice`
"""
(EVIDENCE_DIR / f"{TODAY}-evening-{SLUG}.md").write_text(evidence, encoding="utf-8")

# Insert resource card if absent
res = ROOT / "resources" / "index.html"
text = res.read_text(encoding="utf-8")
card = f'<article class="card"><h2><a href="/resources/{SLUG}/">{html.escape(TITLE)}</a></h2><p>{html.escape(DESC)}</p></article>'
if f'/resources/{SLUG}/' not in text:
    marker = '<main><section class="page-hero"><div class="container"><h1>Resources</h1><p>Guides for websites, enquiry capture, automation, trust basics, AI creatives and practical business growth.</p>'
    text = text.replace(marker, marker + card, 1)
    res.write_text(text, encoding="utf-8")

# Add sitemap URL before closing tag if absent
site = ROOT / "sitemap.xml"
s = site.read_text(encoding="utf-8")
entry = f'  <url><loc>{URL}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
if URL not in s:
    s = s.replace('</urlset>', entry + '</urlset>')
    site.write_text(s, encoding="utf-8")

print(URL)
