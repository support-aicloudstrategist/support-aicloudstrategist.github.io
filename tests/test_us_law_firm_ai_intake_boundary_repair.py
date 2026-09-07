from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "resources/us-law-firm-ai-intake-confidentiality-checklist/index.html").read_text(encoding="utf-8")
CSV = ROOT / "resources/us-law-firm-ai-intake-confidentiality-checklist/us-law-firm-ai-intake-owner-evidence.csv"


def test_us_law_firm_intake_page_has_downloadable_owner_evidence_template():
    assert "Downloadable owner-evidence template" in PAGE
    assert "/resources/us-law-firm-ai-intake-confidentiality-checklist/us-law-firm-ai-intake-owner-evidence.csv" in PAGE
    assert "conflict-screening handoffs" in PAGE
    assert CSV.exists()
    csv_text = CSV.read_text(encoding="utf-8")
    assert "No-advice boundary" in csv_text
    assert "Conflict-screening handoff" in csv_text
    assert "Owner dashboard" in csv_text


def test_us_law_firm_intake_page_has_buyer_safe_boundaries():
    assert "no real client" in PAGE
    assert "no customer data" in PAGE
    assert "no personal data" in PAGE
    assert "no production data" in PAGE
    assert "not legal advice" in PAGE
    assert "No ranking, no demand, no lead volume, no customer, no revenue, no ROI" in PAGE
    assert "Human firm leadership and qualified counsel should approve" in PAGE
