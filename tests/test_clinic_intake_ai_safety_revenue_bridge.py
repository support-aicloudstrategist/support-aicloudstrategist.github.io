from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "publications" / "2026-09-10" / "clinic-intake-ai-safety-card.html"


def test_clinic_intake_publication_has_no_credentials_revenue_bridge():
    html = PAGE.read_text(encoding="utf-8")
    cta = "/free-business-review/?package=clinic-intake-ai-safety-review&amp;source=publication-clinic-intake-ai-safety-card"
    assert cta in html
    assert "Request a no-credentials clinic intake automation review" in html
    assert "No patient records, PHI, credentials or payment are needed" in html
    assert "Educational operations guide only" in html
