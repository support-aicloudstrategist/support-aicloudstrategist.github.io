from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "global-ai-procurement-risk-evidence-checklist" / "index.html"
SOURCE_CARD = ROOT / "resources" / "global-ai-procurement-risk-evidence-checklist" / "ai-procurement-risk-answer-source-card.json"


def test_homepage_surfaces_ai_procurement_risk_evidence_checklist():
    html = HOME.read_text(encoding="utf-8")
    assert 'data-homepage-resource="global-ai-procurement-risk-evidence-checklist"' in html
    assert "/resources/global-ai-procurement-risk-evidence-checklist/" in html
    assert "AI Procurement Risk Evidence Checklist" in html
    assert "vendor due diligence, security questionnaires, data access, cost exposure and production ownership" in html


def test_ai_procurement_risk_asset_files_exist_for_homepage_card():
    assert RESOURCE.exists()
    assert SOURCE_CARD.exists()
    resource_html = RESOURCE.read_text(encoding="utf-8")
    assert "AI procurement risk evidence checklist" in resource_html
    assert "ai-procurement-risk-answer-source-card.json" in resource_html
