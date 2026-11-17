#!/usr/bin/env python3
"""Build gated FinOps one-pager PDFs from Markdown (ReportLab, OSS)."""
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "downloads" / "gated"
OUT.mkdir(parents=True, exist_ok=True)

JOBS = [
    (
        ROOT / "content/onepagers/finops-diagnostic-vs-cloud-cost-tools.md",
        OUT / "finops-diagnostic-vs-cloud-cost-tools.pdf",
        "FinOps diagnostic vs cloud cost tools",
    ),
    (
        ROOT / "content/onepagers/cloud-cost-alert-triage-board.md",
        OUT / "cloud-cost-alert-triage-board.pdf",
        "Cloud cost alert triage board",
    ),
]

styles = {
    "title": ParagraphStyle(
        "Title",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=10,
        textColor=colors.HexColor("#0f2a32"),
    ),
    "heading": ParagraphStyle(
        "Heading",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
        textColor=colors.HexColor("#1a5a66"),
    ),
    "body": ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        spaceAfter=5,
        textColor=colors.HexColor("#1c2a30"),
    ),
}


def linked_text(text):
    return re.sub(
        r"https://[^\s<>]+",
        lambda m: '<link href="' + m[0] + '" color="#1a5a66">' + m[0] + "</link>",
        escape(text),
    )


def footer(canvas, document):
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawString(18 * mm, 12 * mm, "AICloudStrategist | One-pager | aicloudstrategist.com")
    canvas.drawRightString(192 * mm, 12 * mm, str(document.page))


def build(source: Path, target: Path, title: str):
    story = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        if line.startswith("# "):
            kind = "title"
            text = line[2:]
        elif line.startswith("## ") or line.startswith("### "):
            kind = "heading"
            text = line.lstrip("# ").strip()
        else:
            kind = "body"
            text = line
        story.append(Paragraph(linked_text(text), styles[kind]))
    doc = SimpleDocTemplate(
        str(target),
        pagesize=(210 * mm, 297 * mm),
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=22 * mm,
        title=title,
        author="AICloudStrategist",
        invariant=1,
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(target)


if __name__ == "__main__":
    for src, dst, title in JOBS:
        build(src, dst, title)
