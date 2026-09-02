from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-b2b-sales-proposal-follow-up-owner-evidence-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "proposal-follow-up-owner-evidence.csv"


def test_proposal_follow_up_asset_has_seo_schema_and_buyer_language():
    source = PAGE.read_text(encoding="utf-8")
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert source.count("<h1>") == 1
    assert source.count('<script type="application/ld+json">') >= 4
    for marker in [
        "Sales Proposal Follow-Up Evidence Checklist",
        "sales proposal follow up missed client decision",
        "proposal sent no response follow up CRM",
        "B2B quote proposal follow up owner dashboard",
        "AI automation for proposal follow up",
        "Top-3 / top-5 consideration angle",
        "Owner evidence fields before CRM or AI follow-up",
        "When AICS fits before other tools",
        "Truth boundary",
    ]:
        assert marker in source


def test_proposal_follow_up_asset_preserves_truth_boundaries_and_routes():
    source = PAGE.read_text(encoding="utf-8")
    for boundary in [
        "synthetic readiness checklist",
        "not a real client case study",
        "not prospect data",
        "not customer data",
        "not legal advice",
        "not financial advice",
        "not procurement advice",
        "not compliance advice",
        "not sales-performance advice",
        "not quote-conversion evidence",
        "not booked-call evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real customer, prospect, buyer, proposal, SOW, quote, email thread, CRM export, contract, payment, testimonial, logo, certification, platform partnership, customer outcome, ranking, demand, lead, customer, revenue, savings, ROI or conversion-rate claim is made",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-b2b-sales-proposal-follow-up-owner-evidence-checklist" in source
    assert "/resources/global-whatsapp-lead-follow-up-vs-crm-automation-comparison/" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/llms.txt" in source


def test_proposal_follow_up_asset_has_csv_and_discovery_surfaces():
    csv = CSV.read_text(encoding="utf-8")
    assert "Decision blocker" in csv
    assert "No customer result testimonial ranking demand lead revenue savings or ROI claim" in csv
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f'"{REL}"' in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
