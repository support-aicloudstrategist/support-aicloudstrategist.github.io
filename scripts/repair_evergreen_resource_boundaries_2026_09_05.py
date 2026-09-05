#!/usr/bin/env python3
"""Add proof-boundary repair blocks and owner-review CSV artifacts to older evergreen resources.

This is intentionally conservative: it does not add client proof, outcomes, rankings,
or compliance claims. It adds reusable buyer-safety language and a simple downloadable
checklist so broad entry pages are safer to discover and forward.
"""
from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

PAGES = {
    "ai-automation-small-business-use-cases": {
        "title": "AI automation use-case proof boundary",
        "topic": "AI automation use cases for small businesses",
        "service": "/services/ai-automation/",
        "label": "AI automation owner review checklist",
    },
    "ai-chatbot-development-cost-india": {
        "title": "AI chatbot cost proof boundary",
        "topic": "AI chatbot cost planning in India",
        "service": "/services/ai-automation/",
        "label": "AI chatbot cost owner review checklist",
    },
    "ai-voice-agents-appointment-booking": {
        "title": "AI voice appointment proof boundary",
        "topic": "AI voice agents for appointment booking",
        "service": "/services/ai-automation/",
        "label": "AI voice appointment owner review checklist",
    },
    "aics-vs-alternatives-comparison": {
        "title": "AICS alternatives comparison proof boundary",
        "topic": "AICS alternative/vendor comparison",
        "service": "/pricing.html#fixed-scope-diagnostics",
        "label": "Alternative comparison owner review checklist",
    },
    "first-customer-proof-protocol": {
        "title": "First-customer proof protocol boundary",
        "topic": "first-customer proof before outreach",
        "service": "/free-business-review/",
        "label": "First-customer proof owner review checklist",
    },
    "global-ai-pilot-tools-vs-assurance-led-review-comparison": {
        "title": "AI pilot tools comparison proof boundary",
        "topic": "AI pilot tool versus assurance-led review decisions",
        "service": "/pricing.html#fixed-scope-diagnostics",
        "label": "AI pilot comparison owner review checklist",
    },
    "lead-follow-up-automation-guide": {
        "title": "Lead follow-up automation proof boundary",
        "topic": "lead follow-up automation for owner-led businesses",
        "service": "/services/whatsapp-automation/lead-management/",
        "label": "Lead follow-up owner review checklist",
    },
    "small-business-website-checklist-india": {
        "title": "Small-business website proof boundary",
        "topic": "small-business website readiness in India",
        "service": "/free-business-review/",
        "label": "Website readiness owner review checklist",
    },
    "whatsapp-business-api-vs-direct-whatsapp-india": {
        "title": "WhatsApp route comparison proof boundary",
        "topic": "WhatsApp Business API versus direct WhatsApp choices in India",
        "service": "/services/whatsapp-automation/lead-management/",
        "label": "WhatsApp route owner review checklist",
    },
    "custom-ai-solutions-vs-off-the-shelf-ai-tools-guide": {
        "title": "Custom AI versus tools proof boundary",
        "topic": "custom AI solutions versus off-the-shelf AI tools",
        "service": "/services/ai-automation/",
        "label": "Custom AI decision owner review checklist",
    },
}

CSV_NAME = "proof-boundary-owner-review-checklist.csv"
CSV_ROWS = [
    ["gate", "owner_question", "safe_evidence", "stop_rule"],
    ["scope", "Which workflow, audience and owner decision is this page supporting?", "A named use case, owner and next review step.", "Do not imply a full implementation or production result."],
    ["data", "Can this be reviewed without customer, patient, personal, production, credential or billing data?", "Use synthetic, sample or redacted planning notes only.", "Stop before uploading sensitive or live data."],
    ["claims", "Are rankings, leads, revenue, savings, ROI, appointment growth and AI accuracy still unverified?", "Keep claims as hypotheses or review criteria until independently measured.", "Do not publish outcome numbers without source evidence."],
    ["advice", "Does a qualified human need to review legal, privacy, security, medical, financial or procurement implications?", "Route specialist decisions to qualified review before action.", "Do not treat this guide as professional advice."],
    ["commercial", "Is there a no-credentials diagnostic path if the owner wants help?", "Use the linked AICS free review or fixed-scope diagnostic path.", "Do not request production access before scope and evidence boundaries are agreed."],
]


def csv_text(topic: str) -> str:
    lines = [",".join(CSV_ROWS[0])]
    for row in CSV_ROWS[1:]:
        safe = [cell.replace("\"", "\"\"") for cell in row]
        lines.append(",".join(f'"{cell}"' for cell in safe))
    lines.append(f'"proof_boundary","This checklist is a template for {topic}; it is not client proof.","Synthetic/sample planning evidence only.","No real client, customer, patient, personal, production, credential, cloud bill, revenue, savings, ROI, ranking, demand, lead, customer, appointment-growth, outcome or AI-accuracy claim."')
    return "\n".join(lines) + "\n"


def boundary_section(slug: str, meta: dict[str, str]) -> str:
    return f'''
<section class="section"><h2>{meta["title"]}</h2><div class="card"><p><strong>Evidence status:</strong> This is a buyer-education and readiness guide for {meta["topic"]}. It is not a client case study, testimonial, certification, partnership proof or production-result claim.</p><ul><li><strong>Data boundary:</strong> use synthetic, sample or owner-supplied planning notes only; no real client, customer, clinic, patient, no personal data, no health data, no production data, no credentials, no CRM export, no WhatsApp export, no call recording, no invoice and no cloud bill is required for this first review.</li><li><strong>Outcome boundary:</strong> rankings, demand, leads, customers, revenue, savings, ROI, appointment growth, cost reduction, performance gains, outcomes and AI accuracy remain unverified until independently measured and documented.</li><li><strong>Advice boundary:</strong> this page is not legal, privacy, security, medical, clinical, billing, coding, tax, financial, procurement or FinOps advice; route those decisions to qualified review.</li><li><strong>Human stop rule:</strong> pause before automation or publication when a claim lacks source evidence, when sensitive data is requested, or when an owner review / approval gate is missing.</li></ul><p><a href="{CSV_NAME}">Download the {meta["label"]} CSV</a> before forwarding this guide or requesting a <a href="{meta["service"]}">no-credentials AICS diagnostic</a>.</p></div></section>
'''.strip()


def repair_page(slug: str, meta: dict[str, str]) -> None:
    page = BASE / "resources" / slug / "index.html"
    if not page.exists():
        raise FileNotFoundError(page)
    text = page.read_text(encoding="utf-8")
    marker = f"<h2>{meta['title']}</h2>"
    if marker not in text:
        section = boundary_section(slug, meta)
        insert_before = "<section class=\"section\"><h2>Related reading</h2>"
        if insert_before in text:
            text = text.replace(insert_before, section + "\n" + insert_before, 1)
        else:
            text = text.replace("</main>", section + "\n</main>", 1)
        page.write_text(text, encoding="utf-8")
    csv_path = page.parent / CSV_NAME
    csv_path.write_text(csv_text(meta["topic"]), encoding="utf-8")


def main() -> None:
    for slug, meta in PAGES.items():
        repair_page(slug, meta)
    print(f"Repaired {len(PAGES)} evergreen resource pages with proof-boundary sections and CSV artifacts.")


if __name__ == "__main__":
    main()
