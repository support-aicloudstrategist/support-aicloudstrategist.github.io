from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-customer-support-ticket-backlog-vs-helpdesk-ai-chatbot-comparison"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "support-ticket-backlog-comparison-matrix.csv"


def test_support_ticket_backlog_asset_has_seo_schema_and_buyer_language():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert source.count('<script type="application/ld+json">') >= 4
    for marker in [
        "Support Ticket Backlog vs Helpdesk AI Chatbot Comparison",
        "customer support ticket backlog",
        "support tickets piling up",
        "helpdesk AI chatbot comparison",
        "support SLA breach owner dashboard",
        "refund escalation follow up",
        "BPO support vs AI automation",
        "Top-3 / top-5 consideration angle",
        "Owner evidence fields before AI support automation",
        "Comparison matrix before spend",
        "Truth boundary",
    ]:
        assert marker in source


def test_support_ticket_backlog_asset_preserves_truth_boundaries_and_routes():
    source = PAGE.read_text(encoding="utf-8")
    for boundary in [
        "synthetic buyer-education comparison",
        "not a real client case study",
        "not customer support data",
        "not ticket data",
        "not helpdesk export data",
        "not refund advice",
        "not legal advice",
        "not privacy advice",
        "not security advice",
        "not customer-success advice",
        "not ticket-deflection evidence",
        "not SLA improvement evidence",
        "not CSAT evidence",
        "not retention evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real customer, prospect, buyer, support ticket, helpdesk export, email thread, chat transcript, refund, chargeback, incident, payment record, testimonial, logo, certification, platform partnership, customer outcome, ranking, demand, lead, customer, revenue, savings, ROI, support cost reduction, ticket-deflection, SLA or CSAT claim is made",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-customer-support-ticket-backlog-vs-helpdesk-ai-chatbot-comparison" in source
    assert "/resources/global-b2b-saas-customer-onboarding-implementation-delay-checklist/" in source
    assert "/resources/global-ai-vendor-security-questionnaire-answer-source-map/" in source
    assert "/growth-control-os/" in source
    assert "/llms.txt" in source


def test_support_ticket_backlog_asset_has_csv_and_discovery_surfaces():
    csv = CSV.read_text(encoding="utf-8")
    assert "AICS owner-evidence review" in csv
    assert "No customer result ticket-deflection SLA CSAT revenue savings ROI ranking demand lead or AI-accuracy claim" in csv
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{REL}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
