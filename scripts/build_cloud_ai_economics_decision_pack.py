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

PACK_URL = "https://aicloudstrategist.com/resources/cloud-ai-economics-decision-pack/"
SERVICE_URL = "https://aicloudstrategist.com/cloud-ai-cost-governance-diagnostic/"
CONTACT_URL = "https://aicloudstrategist.com/request-fit-review/"

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


def build_html() -> str:
    """Validate the committed browser artifact instead of overwriting it from stale copy."""
    html = HTML_PATH.read_text(encoding="utf-8")
    required = [
        "Representative synthetic scenario",
        "30-day customer action plan",
        "/request-fit-review/",
        "/cloud-ai-cost-governance-diagnostic/",
        "/downloads/cloud-ai-economics-decision-pack.pdf",
        *OUTPUTS,
    ]
    missing = [marker for marker in required if marker not in html]
    if missing:
        raise RuntimeError(f"Decision Pack HTML is missing required release markers: {missing}")
    retired = ["/contact.html?service=", "/services/" + "cloud-finops/"]
    present = [marker for marker in retired if marker in html]
    if present:
        raise RuntimeError(f"Decision Pack HTML contains retired routes: {present}")
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
        canvas.drawString(19 * mm, 8.5 * mm, "AICloudStrategist · Cloud & AI Cost Governance Diagnostic")
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
        p("aicloudstrategist.com/cloud-ai-cost-governance-diagnostic/", styles["small"]),
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
    story += [p("30-day customer action plan: establish allocation policy, resolve owner gaps and qualify the accepted AI outcome unit before later gates.", styles["body"]), panel_table([("D+15 · Allocation policy", "Owner: Technology Finance · dependency: product/shared mapping · accept/reject 72% coverage"), ("D+30 · AI outcome unit", "Owner: AI Product Leader · dependency: task-success telemetry · accept/revise/hold USD 0.083 unit"), ("D+45 · Kubernetes allocation", "Owner: Cloud Architect · dependency: namespace, idle and SLO evidence"), ("D+60 · Commitment readiness", "Owner: CFO Delegate + Procurement · dependency: demand confidence and terms"), ("D+75 · Legacy retirement", "Owner: Engineering Director · dependency: business confirmation and rollback"), ("D+90 · Value verification", "Owner: Technology Finance · dependency: baseline, counterfactual and evidence owner")], styles), Spacer(1, 5 * mm), p("Each action has an explicit owner, dependency and decision date. Technical approval, procurement authority and rollback conditions remain visible.", styles["body"]), PageBreak()]

    story += heading(9, OUTPUTS[8], styles)
    proof_data = [[p(x, styles["center"]) for x in ["Observed", "Qualified", "Approved", "Implemented", "Measured", "Finance-accepted", "Sustained"]]]
    proof = Table(proof_data, colWidths=[22.4 * mm] * 7)
    proof.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PANEL_2), ("BOX", (0, 0), (-1, -1), 0.5, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE), ("TOPPADDING", (0, 0), (-1, -1), 4 * mm), ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm)]))
    story += [proof, Spacer(1, 5 * mm), p("Synthetic planning record—not realised value", styles["h2"]), panel_table([("Action", "Retire the representative legacy analytics workload"), ("Baseline", "USD 86k monthly · synthetic 90-day observed run-rate"), ("Counterfactual", "USD 84k–90k monthly if no action occurs"), ("Expected-value range", "USD 62k–74k monthly cashable reduction · before USD 18k–26k one-time cost"), ("Evidence state", "Qualified—not implemented · CUR-SYN-01 + SYN-WL-17"), ("Finance acceptance", "Pending"), ("Persistence window", "90 days after implementation")], styles), Spacer(1, 4 * mm), p("Value classes remain separate", styles["h2"]), panel_table([("Cashable reduction", "Separate from avoided future cost"), ("Cost avoidance", "Requires an agreed counterfactual"), ("Negotiated rate improvement", "Separate from demand or architecture effects"), ("Capacity released", "Engineering or infrastructure capacity, not automatic cash"), ("Reliability or risk improvement", "Accepted through the relevant owner"), ("Revenue or throughput effect", "Requires business evidence; no automatic attribution"), ("Unit-margin improvement", "Requires accepted unit and finance classification")], styles), Spacer(1, 3 * mm), p("No amount advances to finance-accepted until implementation, measurement and persistence evidence exist.", styles["small"]), PageBreak()]

    story += heading(10, OUTPUTS[9], styles)
    story += [panel_table([("Decision now", "Approve evidence resolution and bounded technical qualification"), ("Why", "Material ownership and unit-evidence gaps remain"), ("Owners", "CTO/CIO, finance, FinOps, architecture, product and procurement"), ("Next gate", "Decision workshop with approved source and constraint register")], styles), Spacer(1, 7 * mm), p("Commercial next step", styles["h2"]), p("Inspect this method before sharing sensitive data. If a material decision exists, request a fit and scope conversation. No billing files, credentials or commitment to proceed are required for the first conversation.", styles["body"]), Spacer(1, 7 * mm), link_table([("Cloud & AI Cost Governance Diagnostic", SERVICE_URL), ("Request a review", CONTACT_URL), ("Public Decision Pack", PACK_URL)], styles), Spacer(1, 7 * mm), p("AICloudStrategist · accountable cloud and AI economics supported by decision-ready evidence.", styles["body"])]

    doc.build(story)
    return PDF_PATH


if __name__ == "__main__":
    build_html()
    build_pdf()
    print(f"Validated {HTML_PATH.relative_to(ROOT)}")
    print(f"Built {PDF_PATH.relative_to(ROOT)}")
