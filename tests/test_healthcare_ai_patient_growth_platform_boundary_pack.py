from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "index.html"
CSV = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "healthcare-ai-patient-growth-owner-evidence.csv"
SVG = ROOT / "resources" / "healthcare-ai-patient-growth-platform" / "healthcare-ai-patient-growth-owner-map.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_healthcare_ai_patient_growth_platform_boundary_pack():
    html = PAGE.read_text(encoding="utf-8")
    assert "Healthcare AI Patient GrowthOS evidence checklist" in html
    assert "healthcare-ai-patient-growth-owner-evidence.csv" in html
    assert "healthcare-ai-patient-growth-owner-map.svg" in html
    assert "synthetic readiness assets" in html
    assert "not a real healthcare client case study" in html
    assert "not patient data" in html
    assert "not GDPR/UK GDPR/DPIA/NIS2/ISO/SOC2/HIPAA compliance proof" in html
    assert "not evidence of demand, leads, booked appointments, patients, revenue, savings, ROI" in html
    assert "/free-business-review/?source=healthcare-ai-patient-growth-platform" in html
    assert "/pricing.html#fixed-scope-diagnostics" in html


def test_healthcare_ai_patient_growth_platform_artifacts_and_discovery_routes():
    csv = CSV.read_text(encoding="utf-8")
    assert "Synthetic owner-evidence template only; no real clinic patient or revenue data" in csv
    assert "Cloud trust and FinOps" in csv
    assert "Do not send patient data to new tools or automation" in csv

    svg = SVG.read_text(encoding="utf-8")
    assert "Synthetic / no-patient-data visual" in svg
    assert "No client, ranking, compliance, revenue, savings or appointment-growth claim" in svg

    resources = RESOURCES.read_text(encoding="utf-8")
    assert 'data-resource-card="healthcare-ai-patient-growth-platform"' in resources
    assert "/resources/healthcare-ai-patient-growth-platform/healthcare-ai-patient-growth-owner-evidence.csv" in resources

    llms = LLMS.read_text(encoding="utf-8")
    assert "Healthcare AI Patient GrowthOS evidence checklist" in llms
    assert "healthcare-ai-patient-growth-owner-map.svg" in llms

    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/healthcare-ai-patient-growth-platform/" in sitemap
