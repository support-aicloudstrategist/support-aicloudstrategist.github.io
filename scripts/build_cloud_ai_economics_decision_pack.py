#!/usr/bin/env python3
"""Build the public Cloud & AI Economics Decision Pack HTML and PDF.

The scenario is explicitly synthetic. It demonstrates decision evidence without
claiming client work, market benchmarks, realised savings, or live system data.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "resources" / "cloud-ai-economics-decision-pack" / "index.html"
PDF_PATH = ROOT / "downloads" / "cloud-ai-economics-decision-pack.pdf"
SERVICE_PATH = ROOT / "services" / "cloud-finops" / "index.html"

PACK_URL = "https://aicloudstrategist.com/resources/cloud-ai-economics-decision-pack/"
SERVICE_URL = "https://aicloudstrategist.com/services/cloud-finops/"
CONTACT_URL = "https://aicloudstrategist.com/contact.html?service=ai-finops-cloud-economics"

OUTPUTS = [
    "Economic Baseline and Confidence Statement",
    "Allocation and Ownership Map",
    "Cloud and AI Unit Economics Tree",
    "Quality Reliability and Risk Constraint Record",
    "Portfolio Decision Register",
    "Forecast and Scenario Comparison",
    "Commitment Readiness Record",
    "90-Day Action Portfolio",
    "Value Realisation Entry",
    "Executive Decision Summary",
]

ACCENT = colors.HexColor("#55D9E8")
ACCENT_2 = colors.HexColor("#7EF0D0")
INK = colors.HexColor("#EAF7FA")
MUTED = colors.HexColor("#A7C0C8")
BG = colors.HexColor("#061218")
PANEL = colors.HexColor("#0A1E26")
PANEL_2 = colors.HexColor("#0C2932")
LINE = colors.HexColor("#244651")
DARK_INK = colors.HexColor("#061218")


def shared_footer() -> str:
    source = SERVICE_PATH.read_text(encoding="utf-8")
    start = source.index('<footer class="aics-global-footer"')
    end = source.index("</footer>", start) + len("</footer>")
    return source[start:end]


def output_section(number: int, title: str, eyebrow: str, body: str) -> str:
    body = body.strip()
    return f'''\n      <section class="pack-section" id="output-{number:02d}" data-decision-output="{escape(title)}" aria-labelledby="output-{number:02d}-title">
        <div class="pack-output-heading"><span>{number:02d}</span><div><p>{eyebrow}</p><h2 id="output-{number:02d}-title">{escape(title)}</h2></div></div>
        {body}
      </section>'''


def build_html() -> str:
    sections = [
        output_section(1, OUTPUTS[0], "Decision evidence · baseline", '''
        <div class="pack-split">
          <article class="pack-panel"><h3>Representative estate boundary</h3><dl class="pack-facts"><div><dt>Business context</dt><dd>Global digital-services portfolio with customer-facing SaaS and AI-assisted workflows</dd></div><div><dt>Technology scope</dt><dd>AWS, Azure, Google Cloud, Kubernetes and two AI-provider usage exports</dd></div><div><dt>Baseline</dt><dd>USD 2.47m monthly · USD 29.64m annualised</dd></div><div><dt>Allocation</dt><dd>72% allocation coverage · 18% shared · 10% unallocated</dd></div><div><dt>Decision window</dt><dd>Next two planning quarters</dd></div><div><dt>Currency</dt><dd>USD, synthetic planning values only</dd></div></dl></article>
          <article class="pack-panel pack-confidence"><h3>Confidence: moderate</h3><p>Provider totals are 96% reconciled in the synthetic source register. Product allocation is 72% covered; the successful-outcome denominator is 64% evidenced and still requires owner acceptance.</p><ul><li>Allocated product consumption: USD 1.78m monthly</li><li>Shared platform pool: USD 0.44m monthly</li><li>Unallocated evidence backlog: USD 0.25m monthly</li></ul></article>
        </div>
        <div class="pack-register"><h3>Source register</h3><div class="pack-register-row"><span>AWS Cost and Usage Report</span><strong>Observed</strong><small>USD 1.12m monthly · synthetic</small></div><div class="pack-register-row"><span>Azure Cost Management export</span><strong>Observed</strong><small>USD 0.62m monthly · synthetic</small></div><div class="pack-register-row"><span>Google Cloud billing export</span><strong>Observed</strong><small>USD 0.31m monthly · synthetic</small></div><div class="pack-register-row"><span>Kubernetes allocation export</span><strong>Qualified</strong><small>USD 0.71m provider-cost subset</small></div><div class="pack-register-row"><span>AI provider usage export</span><strong>Qualified</strong><small>USD 0.42m monthly · synthetic</small></div></div>
        <aside class="pack-callout" aria-label="Unresolved evidence"><strong>Unresolved evidence</strong><p>Customer-level allocation, AI task-success denominator, commitment portability and finance acceptance remain open. No value claim advances until the relevant owner approves the evidence.</p></aside>'''),
        output_section(2, OUTPUTS[1], "Accountability · allocation", '''
        <ul class="ownership-map" aria-label="Representative allocation and ownership path">
          <li><span>Provider</span><strong>Cloud and AI vendors</strong><small>Invoice and usage origin</small></li><li class="map-arrow" aria-hidden="true">→</li>
          <li><span>Platform</span><strong>Accounts, clusters, models</strong><small>Technical control boundary</small></li><li class="map-arrow" aria-hidden="true">→</li>
          <li><span>Product</span><strong>SaaS and AI workflows</strong><small>Allocation destination</small></li><li class="map-arrow" aria-hidden="true">→</li>
          <li><span>Owner</span><strong>Technology + finance</strong><small>Decision and acceptance rights</small></li>
        </ul>
        <div class="pack-grid-three"><article class="pack-panel"><h3>Direct consumption</h3><p>Assigned from provider evidence to a product, environment and accountable technical owner.</p></article><article class="pack-panel"><h3>Shared platforms</h3><p>Allocated through an approved driver; unallocated remainder stays visible rather than disappearing into averages.</p></article><article class="pack-panel"><h3>Owner exception</h3><p>Any material spend without a decision owner enters the evidence backlog before optimisation.</p></article></div>
        <p class="pack-decision-note"><strong>Client approval required:</strong> allocation policy, product-value definition and financial reporting treatment remain client-owned.</p>'''),
        output_section(3, OUTPUTS[2], "Unit economics · cloud and AI", '''
        <div class="unit-tree">
          <div class="unit-root"><span>Business outcome</span><strong>Successful customer workflow</strong><small>8.0m attempted tasks · 7.2m successful tasks · synthetic month</small></div>
          <div class="unit-branches"><article><span>Product unit</span><strong>Completed workflow</strong><small>Accepted by product owner</small></article><article><span>AI unit</span><strong>Quality-qualified task</strong><small>Includes retry and review</small></article><article><span>Technology unit</span><strong>Cloud + model consumption</strong><small>Includes shared allocation</small></article></div>
        </div>
        <table class="pack-table" tabindex="0" aria-label="Representative cloud and AI unit economics definitions"><thead><tr><th>Unit layer</th><th>Numerator</th><th>Denominator</th><th>Representative unit</th><th>Guardrail</th></tr></thead><tbody><tr><td>Cloud-native product</td><td>USD 1.20m allocated cloud</td><td>24.0m transactions</td><td>USD 0.050 per transaction</td><td>99.9% service objective</td></tr><tr><td>AI workflow</td><td>USD 0.60m model, data, platform and review</td><td>7.2m successful tasks</td><td>USD 0.083 per successful AI task</td><td>≥89% accepted quality; observed 90%</td></tr><tr><td>Customer economics</td><td>USD 1.78m attributed technology</td><td>180k active accounts</td><td>USD 9.89 per active account</td><td>Finance-approved allocation policy</td></tr></tbody></table>
        <p class="pack-decision-note">The pack does not present a universal unit cost. The unit is only valid after product, finance and technical owners accept its definition and constraints.</p>'''),
        output_section(4, OUTPUTS[3], "Guardrails · decision admissibility", '''
        <div class="constraint-grid"><article><span>Quality</span><strong>Task success remains above the agreed acceptance threshold</strong><small>Owner: product or AI programme</small></article><article><span>Reliability</span><strong>Availability and recovery objectives remain protected</strong><small>Owner: platform or service</small></article><article><span>Security</span><strong>Controls, residency and access boundaries are not traded away</strong><small>Owner: security and risk</small></article><article><span>Commercial</span><strong>Contract, lock-in and exit exposure are visible before approval</strong><small>Owner: procurement and finance</small></article></div>
        <aside class="pack-callout" aria-label="Decision rule"><strong>Decision rule</strong><p>An option that reduces theoretical spend but breaches an accepted quality, reliability, security or commercial constraint is not an admissible optimisation.</p></aside>'''),
        output_section(5, OUTPUTS[4], "Decision portfolio · accountable action", '''
        <div class="pack-register decision-register"><div class="pack-register-row"><span>Shared Kubernetes platform</span><strong>Optimise safely</strong><small>Qualified · owner assigned · reliability guardrail open</small></div><div class="pack-register-row"><span>AI routing policy</span><strong>Rearchitect</strong><small>Observed · quality comparison required</small></div><div class="pack-register-row"><span>Database commitment</span><strong>Hold</strong><small>Demand confidence below approval boundary</small></div><div class="pack-register-row"><span>Legacy analytics workload</span><strong>Retire</strong><small>Qualified · business owner confirmation required</small></div><div class="pack-register-row"><span>Customer-facing inference</span><strong>Scale</strong><small>Unit economics acceptable · capacity decision pending</small></div></div>
        <p class="pack-decision-note">Representative decisions show the method. They are not recommendations for any real estate and do not imply realised outcomes.</p>'''),
        output_section(6, OUTPUTS[5], "Planning · scenario comparison", '''
        <table class="pack-table scenario-table" tabindex="0" aria-label="Representative forecast and scenario comparison"><thead><tr><th>Scenario</th><th>Quantified assumption</th><th>Monthly planning range</th><th>Variance from base</th><th>Decision consequence</th></tr></thead><tbody><tr><td>Base</td><td>Approved product forecast</td><td>USD 2.47m</td><td>Reference</td><td>Maintain flexibility</td></tr><tr><td>Growth</td><td>Successful-task demand +18%</td><td>USD 2.74m–2.82m after qualified decisions</td><td>Growth counterfactual: USD 2.91m monthly</td><td>Stage commitment after evidence</td></tr><tr><td>Downside</td><td>Demand −15%</td><td>USD 2.18m–2.28m</td><td>−8% to −12%</td><td>Preserve exit options</td></tr><tr><td>Quality shift</td><td>Accepted quality 90% → 94%</td><td>USD 2.55m–2.63m</td><td>+3% to +6%</td><td>Revalidate AI architecture</td></tr></tbody></table>
        <div class="pack-split"><article class="pack-panel"><h3>Assumptions and exclusions</h3><ul><li>No tax, accounting or FX treatment.</li><li>No provider-price forecast.</li><li>No revenue or savings guarantee.</li><li>No production change authority.</li></ul></article><article class="pack-panel"><h3>Confidence boundary</h3><p>Scenario confidence depends on workload seasonality, demand ownership, contract terms, architecture feasibility and accepted business units.</p></article></div>
        <aside class="pack-callout" aria-label="Synthetic expected value range"><strong>Expected-value range: USD 0.09m–0.17m monthly cost avoidance</strong><p>Qualified decision range: USD 2.74m–2.82m monthly. Low-confidence synthetic range against the USD 2.91m growth counterfactual, only if the qualified decisions are approved and quality, reliability and security constraints remain satisfied. It is not realised value or a client savings claim.</p></aside>'''),
        output_section(7, OUTPUTS[6], "Commercial exposure · commitment", '''
        <div class="commitment-boundary"><div><span>Demand confidence</span><strong>Is material usage sufficiently stable?</strong></div><div><span>Coverage</span><strong>Which usage should remain flexible?</strong></div><div><span>Utilisation</span><strong>Can the organisation operate the commitment?</strong></div><div><span>Downside</span><strong>What happens if demand or architecture changes?</strong></div><div><span>Authority</span><strong>Who can approve the commercial exposure?</strong></div></div>
        <aside class="pack-callout pack-warning" aria-label="Representative commitment disposition"><strong>Representative disposition: hold</strong><p>Commitment approval is withheld until demand confidence, portability and authorised owner evidence are complete. AICS does not broker, resell or automatically recommend provider commitments.</p></aside>'''),
        output_section(8, OUTPUTS[7], "Execution · 90-day portfolio", '''
        <div class="action-portfolio">
          <article data-action-record="allocation-policy"><span>D+15</span><h3>Approve allocation policy</h3><p>Owner: Technology Finance<br>Dependency: product and shared-platform mapping<br>Decision date: day 15</p><small>Exit: 72% coverage policy accepted or rejected</small></article>
          <article data-action-record="ai-unit"><span>D+30</span><h3>Qualify the AI outcome unit</h3><p>Owner: AI Product Leader<br>Dependency: task-success and review telemetry<br>Decision date: day 30</p><small>Exit: USD 0.083 unit accepted, revised or held</small></article>
          <article data-action-record="kubernetes"><span>D+45</span><h3>Test Kubernetes allocation</h3><p>Owner: Cloud Architect<br>Dependency: namespace, idle and SLO evidence<br>Decision date: day 45</p><small>Exit: safe action candidates with guardrails</small></article>
          <article data-action-record="commitment"><span>D+60</span><h3>Resolve commitment readiness</h3><p>Owner: CFO Delegate + Procurement<br>Dependency: demand confidence and provider terms<br>Decision date: day 60</p><small>Exit: approve, resize or hold record</small></article>
          <article data-action-record="retirement"><span>D+75</span><h3>Decide legacy workload retirement</h3><p>Owner: Engineering Director<br>Dependency: business-owner confirmation and rollback<br>Decision date: day 75</p><small>Exit: implementation approval or no-action record</small></article>
          <article data-action-record="verification"><span>D+90</span><h3>Approve value verification design</h3><p>Owner: Technology Finance<br>Dependency: baseline, counterfactual and evidence owner<br>Decision date: day 90</p><small>Exit: finance acceptance and persistence plan</small></article>
        </div>
        <p class="pack-decision-note">Dependencies, technical approval, procurement authority and rollback conditions remain visible for every action.</p>'''),
        output_section(9, OUTPUTS[8], "Proof · realised value", '''
        <ol class="proof-chain" aria-label="Value proof stages"><li>Observed</li><li>Qualified</li><li>Approved</li><li>Implemented</li><li>Measured</li><li>Finance-accepted</li><li>Sustained</li></ol>
        <div class="value-classes"><span>Cashable reduction</span><span>Cost avoidance</span><span>Negotiated rate improvement</span><span>Capacity released</span><span>Reliability or risk improvement</span><span>Revenue or throughput effect</span><span>Unit-margin improvement</span></div>
        <div class="pack-split"><article class="pack-panel"><h3>Synthetic planning record—not realised value</h3><ul class="value-entry-fields"><li><strong>Action:</strong> retire the representative legacy analytics workload</li><li><strong>Baseline: USD 86k monthly</strong> · synthetic 90-day observed run-rate</li><li><strong>Counterfactual: USD 84k–90k monthly</strong> · seasonality range if no action occurs</li><li><strong>Expected-value range: USD 62k–74k monthly cashable reduction</strong> · before one-time migration cost of USD 18k–26k</li><li><strong>Evidence state: qualified—not implemented</strong></li><li><strong>Finance acceptance: pending</strong></li><li><strong>Persistence window: 90 days after implementation</strong></li></ul></article><article class="pack-panel"><h3>Evidence record and counterfactual</h3><p>Source IDs: CUR-SYN-01, workload inventory SYN-WL-17 and business-owner confirmation pending. The counterfactual uses the synthetic workload's trailing range; it is not an external benchmark.</p><p>An opportunity estimate is not delivered value. No amount advances to finance-accepted until implementation, measurement and persistence evidence exist.</p></article></div>'''),
        output_section(10, OUTPUTS[9], "Executive brief · unresolved approvals", '''
        <div class="executive-brief"><article><span>Decision now</span><h3>Approve evidence resolution and bounded technical qualification</h3><p>Do not approve a broad commitment or claim value yet.</p></article><article><span>Why</span><h3>Material ownership and unit-evidence gaps remain</h3><p>The estate can be governed without pretending uncertainty has disappeared.</p></article><article><span>Owners required</span><h3>CTO/CIO, finance, FinOps, architecture, product and procurement</h3><p>Each retains the authority defined for its decision boundary.</p></article><article><span>Next gate</span><h3>Decision workshop with approved source and constraint register</h3><p>Outcome may be action, hold, referral or no further work.</p></article></div>
        <aside class="pack-callout" aria-label="First conversation boundary"><strong>First conversation boundary</strong><p>No billing files, credentials or work email are required to inspect this pack. A review conversation validates fit, decision urgency, stakeholders and scope before any data-access agreement.</p></aside>'''),
    ]

    toc = "".join(f'<a href="#output-{i:02d}"><span>{i:02d}</span>{escape(title)}</a>' for i, title in enumerate(OUTPUTS, 1))
    footer = shared_footer()
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cloud &amp; AI Economics Decision Pack | AICloudStrategist</title>
<meta name="description" content="Inspect a clearly labelled synthetic Cloud and AI Economics decision dossier: baseline, ownership, unit economics, commitments, decision records and value verification.">
<link rel="canonical" href="{PACK_URL}">
<link rel="stylesheet" href="/css/site-navigation.css?v=premium-shell-20260727">
<link rel="stylesheet" href="/css/cloud-ai-economics-decision-pack.css?v=20260803-1">
<script defer src="/js/site-navigation.js?v=premium-shell-20260727"></script>
<script defer src="/js/aics-analytics-shim.js"></script>
<script defer src="/js/aics-conversion-tracking.js"></script>
</head>
<body class="economics-pack-page">
<a class="pack-skip-link" href="#main-content">Skip to decision evidence</a>
<div data-aics-navigation-mount></div>
<main id="main-content">
  <header class="pack-hero">
    <div class="pack-shell pack-hero-grid">
      <div>
        <p class="pack-eyebrow">Representative evidence · synthetic scenario</p>
        <h1>Cloud &amp; AI Economics Decision Pack</h1>
        <p class="pack-lead">Inspect how AICloudStrategist turns multicloud and AI consumption into accountable decisions, owner-approved constraints and a finance-accepted evidence trail.</p>
        <div class="pack-actions"><a class="pack-button pack-button-primary" href="/downloads/cloud-ai-economics-decision-pack.pdf" download="Cloud-and-AI-Economics-Decision-Pack.pdf" data-aics-cta="decision-pack-pdf">Download the PDF dossier</a><a class="pack-button" href="{SERVICE_URL.replace('https://aicloudstrategist.com', '')}">Review the advisory service</a></div>
      </div>
      <aside class="pack-boundary" aria-label="Evidence boundary"><strong>Evidence boundary</strong><p>This is not client work, not a case study, not a benchmark and not a savings promise. Every value, organisation and decision state is synthetic and exists only to demonstrate the AICS method.</p><dl><div><dt>Data</dt><dd>Synthetic</dd></div><div><dt>Claims</dt><dd>Representative only</dd></div><div><dt>Access</dt><dd>Ungated</dd></div></dl></aside>
    </div>
  </header>
  <div class="pack-shell pack-layout">
    <nav class="pack-contents" aria-label="Decision Pack contents"><p>Decision dossier</p>{toc}</nav>
    <article class="pack-document">
      <section class="pack-intro" aria-labelledby="scenario-title"><p class="pack-eyebrow">How to read this evidence</p><h2 id="scenario-title">A decision dossier—not a dashboard or sales brochure</h2><p>The representative scenario shows ten connected outputs. Sources, assumptions, confidence, owners, unresolved evidence and approval boundaries stay visible so an executive can distinguish a signal from an accepted decision.</p></section>
      {''.join(sections)}
      <section class="pack-final" aria-labelledby="pack-next-title"><p class="pack-eyebrow">Commercial next step</p><h2 id="pack-next-title">Use the method before sharing sensitive data</h2><p>Inspect the complete evidence architecture first. If a material cloud or AI economic decision exists, the next step is a fit and scope conversation—not a free audit or an immediate data upload.</p><div class="pack-actions"><a class="pack-button pack-button-primary" href="/contact.html?service=ai-finops-cloud-economics" data-aics-cta="economics-review">Request a Cloud &amp; AI Economics Review</a><a class="pack-button" href="/services/cloud-finops/">Return to Enterprise FinOps Advisory</a></div></section>
    </article>
  </div>
</main>
{footer}
</body>
</html>
'''
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(html, encoding="utf-8")
    return html


def pdf_styles():
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    pdfmetrics.registerFont(TTFont("AICS", font_path))
    pdfmetrics.registerFont(TTFont("AICS-Bold", bold_path))
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=styles["Title"], fontName="AICS-Bold", fontSize=29, leading=34, textColor=INK, alignment=TA_LEFT, spaceAfter=8 * mm),
        "h1": ParagraphStyle("H1", parent=styles["Heading1"], fontName="AICS-Bold", fontSize=21, leading=25, textColor=INK, spaceBefore=4 * mm, spaceAfter=5 * mm),
        "h2": ParagraphStyle("H2", parent=styles["Heading2"], fontName="AICS-Bold", fontSize=13, leading=16, textColor=ACCENT, spaceBefore=3 * mm, spaceAfter=2 * mm),
        "body": ParagraphStyle("Body", parent=styles["BodyText"], fontName="AICS", fontSize=9.2, leading=14, textColor=MUTED, spaceAfter=3 * mm),
        "small": ParagraphStyle("Small", parent=styles["BodyText"], fontName="AICS", fontSize=7.5, leading=11, textColor=MUTED),
        "label": ParagraphStyle("Label", parent=styles["BodyText"], fontName="AICS-Bold", fontSize=7.2, leading=9, textColor=ACCENT_2, uppercase=True, spaceAfter=2 * mm),
        "cover": ParagraphStyle("Cover", parent=styles["BodyText"], fontName="AICS", fontSize=12, leading=18, textColor=MUTED, spaceAfter=4 * mm),
        "center": ParagraphStyle("Center", parent=styles["BodyText"], fontName="AICS", fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER),
    }


class PackDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(19 * mm, 20 * mm, A4[0] - 38 * mm, A4[1] - 39 * mm, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="pack", frames=[frame], onPage=self.draw_page)])

    def draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.line(19 * mm, 14 * mm, A4[0] - 19 * mm, 14 * mm)
        canvas.setFont("AICS", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(19 * mm, 8.5 * mm, "AICloudStrategist · Enterprise FinOps Advisory")
        canvas.drawRightString(A4[0] - 19 * mm, 8.5 * mm, f"Representative evidence · {doc.page}")
        canvas.restoreState()


def p(text: str, style) -> Paragraph:
    return Paragraph(escape(text), style)


def panel_table(rows, styles, widths=None):
    data = [[p(str(a), styles["small"]), p(str(b), styles["small"])] for a, b in rows]
    table = Table(data, colWidths=widths or [48 * mm, 110 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    return table


def link_table(rows, styles):
    data = [
        [
            p(label, styles["small"]),
            Paragraph(
                f'<link href="{escape(url)}" color="#55D9E8">{escape(url)}</link>',
                styles["small"],
            ),
        ]
        for label, url in rows
    ]
    table = Table(data, colWidths=[48 * mm, 110 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    return table


def heading(number: int, title: str, styles):
    return [p(f"OUTPUT {number:02d}", styles["label"]), p(title, styles["h1"])]


def build_pdf():
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    styles = pdf_styles()
    doc = PackDocTemplate(str(PDF_PATH), pagesize=A4, pageCompression=0, invariant=1, title="Cloud & AI Economics Decision Pack", author="AICloudStrategist", subject="Representative synthetic Enterprise FinOps decision evidence", creator="AICloudStrategist deterministic pack builder")
    story = [
        Spacer(1, 18 * mm), p("REPRESENTATIVE EVIDENCE · SYNTHETIC SCENARIO", styles["label"]),
        p("Cloud & AI Economics Decision Pack", styles["title"]),
        p("A browser-inspectable decision dossier showing how cloud and AI consumption can move from source evidence to accountable ownership, risk-governed decisions and finance-accepted value.", styles["cover"]),
        Spacer(1, 8 * mm),
        panel_table([
            ("Evidence boundary", "Not client work, not a case study, not a benchmark and not a savings promise."),
            ("Scenario", "Synthetic global digital-services portfolio using multicloud, Kubernetes and AI providers."),
            ("Access", "Ungated. No work email, credentials or billing files required."),
            ("Method", "Visibility → ownership → risk-constrained decision → verified value."),
        ], styles),
        Spacer(1, 12 * mm),
        p("What this pack proves", styles["h2"]),
        p("It proves that AICS can structure a decision evidence trail. It does not prove a customer outcome, certification, platform partnership, realised saving or production capability beyond the explicit method shown.", styles["body"]),
        Spacer(1, 6 * mm),
        p("aicloudstrategist.com/services/cloud-finops/", styles["small"]),
        PageBreak(),
    ]

    story += heading(1, OUTPUTS[0], styles)
    story += [p("Representative estate boundary", styles["h2"]), panel_table([("Business context", "Global digital-services portfolio with SaaS and AI-assisted workflows"), ("Technology", "AWS, Azure, Google Cloud, Kubernetes and two AI providers"), ("Baseline", "USD 2.47m monthly · USD 29.64m annualised"), ("Allocation", "72% allocation coverage · 18% shared · 10% unallocated"), ("Decision window", "Two planning quarters"), ("Confidence", "Moderate · 96% source reconciliation · 64% outcome-unit evidence")], styles), Spacer(1, 5 * mm), p("Source register", styles["h2"]), panel_table([("AWS Cost and Usage Report", "Observed · USD 1.12m monthly · synthetic"), ("Azure Cost Management export", "Observed · USD 0.62m monthly · synthetic"), ("Google Cloud billing export", "Observed · USD 0.31m monthly · synthetic"), ("Kubernetes allocation export", "Qualified · USD 0.71m provider-cost subset"), ("AI provider usage export", "Qualified · USD 0.42m monthly · synthetic")], styles), Spacer(1, 4 * mm), p("Allocation record: USD 1.78m allocated, USD 0.44m shared and USD 0.25m unallocated per synthetic month. Unresolved evidence: customer allocation, AI task-success denominator, commitment portability and finance acceptance.", styles["body"]), PageBreak()]

    story += heading(2, OUTPUTS[1], styles)
    story += [panel_table([("Provider", "Cloud and AI vendors · invoice and usage origin"), ("Platform", "Accounts, clusters and models · technical control boundary"), ("Product", "SaaS and AI workflows · allocation destination"), ("Owner", "Technology and finance · decision and acceptance rights")], styles), Spacer(1, 5 * mm), p("Allocation rules", styles["h2"]), panel_table([("Direct consumption", "Assigned to product, environment and accountable technical owner"), ("Shared platform", "Allocated through an approved driver; remainder stays visible"), ("Owner exception", "Material spend without an owner enters the evidence backlog")], styles), Spacer(1, 4 * mm), p("Client approval required: allocation policy, product-value definition and financial-reporting treatment remain client-owned.", styles["body"]), PageBreak()]

    story += heading(3, OUTPUTS[2], styles)
    story += [p("8.0m attempted tasks → 7.2m successful tasks in the synthetic month. The method connects business outcome → product unit → quality-qualified AI task → allocated technology consumption.", styles["body"]), panel_table([("Cloud-native product", "USD 1.20m ÷ 24.0m transactions = USD 0.050 · 99.9% service objective"), ("AI workflow", "USD 0.60m ÷ 7.2m successful tasks = USD 0.083 · ≥89% accepted quality; observed 90%"), ("Customer economics", "USD 1.78m ÷ 180k active accounts = USD 9.89 · finance-approved policy pending")], styles), Spacer(1, 4 * mm), p("These are synthetic planning units, not benchmarks. Product, finance and technical owners must accept the definitions and constraints before use.", styles["body"]), PageBreak()]

    story += heading(4, OUTPUTS[3], styles)
    story += [panel_table([("Quality", "Task success remains above the accepted threshold · product/AI owner"), ("Reliability", "Availability and recovery objectives remain protected · platform owner"), ("Security", "Controls, residency and access boundaries are not traded away · security owner"), ("Commercial", "Contract, lock-in and exit exposure remain visible · procurement/finance owner")], styles), Spacer(1, 5 * mm), p("Decision rule", styles["h2"]), p("An option that reduces theoretical spend but breaches an accepted quality, reliability, security or commercial constraint is not an admissible optimisation.", styles["body"]), PageBreak()]

    story += heading(5, OUTPUTS[4], styles)
    story += [panel_table([("Shared Kubernetes platform", "OPTIMISE SAFELY · qualified; reliability guardrail open"), ("AI routing policy", "REARCHITECT · observed; quality comparison required"), ("Database commitment", "HOLD · demand confidence below approval boundary"), ("Legacy analytics workload", "RETIRE · business owner confirmation required"), ("Customer-facing inference", "SCALE · unit economics acceptable; capacity decision pending")], styles), Spacer(1, 4 * mm), p("These representative states show the method. They are not recommendations for a real estate and do not imply realised outcomes.", styles["body"]), PageBreak()]

    story += heading(6, OUTPUTS[5], styles)
    story += [panel_table([("Base", "USD 2.47m monthly · approved synthetic product forecast"), ("Growth", "+18% successful-task demand · USD 2.91m counterfactual · USD 2.74m–2.82m qualified range"), ("Downside", "−15% demand · USD 2.18m–2.28m range · preserve exit options"), ("Quality shift", "90% → 94% accepted quality · USD 2.55m–2.63m range · revalidate architecture")], styles), Spacer(1, 5 * mm), p("Expected-value range", styles["h2"]), p("USD 0.09m–0.17m monthly cost avoidance against the synthetic growth counterfactual, at low confidence and only if decisions are approved and guardrails remain satisfied. This is not realised value or a client savings claim.", styles["body"]), p("Exclusions: no tax, accounting, foreign-exchange, provider-price, revenue or guaranteed-savings forecast.", styles["small"]), PageBreak()]

    story += heading(7, OUTPUTS[6], styles)
    story += [panel_table([("Demand confidence", "Is material usage sufficiently stable?"), ("Coverage", "Which usage should remain flexible?"), ("Utilisation", "Can the organisation operate the commitment?"), ("Downside", "What happens if demand or architecture changes?"), ("Authority", "Who can approve the commercial exposure?")], styles), Spacer(1, 5 * mm), p("Representative disposition: HOLD", styles["h2"]), p("Approval is withheld until demand confidence, portability and authorised-owner evidence are complete. AICS does not broker, resell or automatically recommend provider commitments.", styles["body"]), PageBreak()]

    story += heading(8, OUTPUTS[7], styles)
    story += [panel_table([("D+15 · Allocation policy", "Owner: Technology Finance · dependency: product/shared mapping · accept/reject 72% coverage"), ("D+30 · AI outcome unit", "Owner: AI Product Leader · dependency: task-success telemetry · accept/revise/hold USD 0.083 unit"), ("D+45 · Kubernetes allocation", "Owner: Cloud Architect · dependency: namespace, idle and SLO evidence"), ("D+60 · Commitment readiness", "Owner: CFO Delegate + Procurement · dependency: demand confidence and terms"), ("D+75 · Legacy retirement", "Owner: Engineering Director · dependency: business confirmation and rollback"), ("D+90 · Value verification", "Owner: Technology Finance · dependency: baseline, counterfactual and evidence owner")], styles), Spacer(1, 5 * mm), p("Each action has an explicit owner, dependency and decision date. Technical approval, procurement authority and rollback conditions remain visible.", styles["body"]), PageBreak()]

    story += heading(9, OUTPUTS[8], styles)
    proof_data = [[p(x, styles["center"]) for x in ["Observed", "Qualified", "Approved", "Implemented", "Measured", "Finance-accepted", "Sustained"]]]
    proof = Table(proof_data, colWidths=[22.4 * mm] * 7)
    proof.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PANEL_2), ("BOX", (0, 0), (-1, -1), 0.5, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE), ("TOPPADDING", (0, 0), (-1, -1), 4 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm)]))
    story += [proof, Spacer(1, 5 * mm), p("Synthetic planning record—not realised value", styles["h2"]), panel_table([("Action", "Retire the representative legacy analytics workload"), ("Baseline", "USD 86k monthly · synthetic 90-day observed run-rate"), ("Counterfactual", "USD 84k–90k monthly if no action occurs"), ("Expected-value range", "USD 62k–74k monthly cashable reduction · before USD 18k–26k one-time cost"), ("Evidence state", "Qualified—not implemented · CUR-SYN-01 + SYN-WL-17"), ("Finance acceptance", "Pending"), ("Persistence window", "90 days after implementation")], styles), Spacer(1, 4 * mm), p("Value classes remain separate", styles["h2"]), panel_table([("Cashable reduction", "Separate from avoided future cost"), ("Cost avoidance", "Requires an agreed counterfactual"), ("Negotiated rate improvement", "Separate from demand or architecture effects"), ("Capacity released", "Engineering or infrastructure capacity, not automatic cash"), ("Reliability or risk improvement", "Accepted through the relevant owner"), ("Revenue or throughput effect", "Requires business evidence; no automatic attribution"), ("Unit-margin improvement", "Requires accepted unit and finance classification")], styles), Spacer(1, 3 * mm), p("No amount advances to finance-accepted until implementation, measurement and persistence evidence exist.", styles["small"]), PageBreak()]

    story += heading(10, OUTPUTS[9], styles)
    story += [panel_table([("Decision now", "Approve evidence resolution and bounded technical qualification"), ("Why", "Material ownership and unit-evidence gaps remain"), ("Owners", "CTO/CIO, finance, FinOps, architecture, product and procurement"), ("Next gate", "Decision workshop with approved source and constraint register")], styles), Spacer(1, 7 * mm), p("Commercial next step", styles["h2"]), p("Inspect this method before sharing sensitive data. If a material decision exists, request a fit and scope conversation. No billing files, credentials or commitment to proceed are required for the first conversation.", styles["body"]), Spacer(1, 7 * mm), link_table([("Enterprise FinOps Advisory", SERVICE_URL), ("Request a review", CONTACT_URL), ("Public Decision Pack", PACK_URL)], styles), Spacer(1, 7 * mm), p("AICloudStrategist · accountable cloud and AI economics supported by decision-ready evidence.", styles["body"])]

    doc.build(story)
    return PDF_PATH


if __name__ == "__main__":
    build_html()
    build_pdf()
    print(f"Built {HTML_PATH.relative_to(ROOT)}")
    print(f"Built {PDF_PATH.relative_to(ROOT)}")
