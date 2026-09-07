from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "healthcare-ai-trust-controls" / "index.html"
CSV = ROOT / "resources" / "healthcare-ai-trust-controls" / "healthcare-ai-trust-controls-owner-evidence.csv"
SVG = ROOT / "resources" / "healthcare-ai-trust-controls" / "healthcare-ai-trust-controls-owner-map.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def test_healthcare_ai_trust_controls_page_has_buyer_language_and_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "Healthcare AI trust controls before AI receptionist spend",
        "patient-data automation boundaries",
        "No-patient-data first",
        "Human approval gates",
        "Vendor-evidence map",
        "healthcare-ai-trust-controls-owner-evidence.csv",
        "healthcare-ai-trust-controls-owner-map.svg",
        "synthetic/readiness asset",
        "does not use real clinic, patient, PHI/ePHI, personal data",
        "does not prove DPDP, GDPR, UK GDPR, HIPAA",
        "no ranking, demand, lead, patient, appointment, revenue, savings, ROI",
    ]
    for marker in required:
        assert marker in html


def test_healthcare_ai_trust_controls_artifacts_and_discovery_routes_exist():
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert "control_area,buyer_question,evidence_to_prepare,owner_gate,claim_boundary" in csv
    assert "Patient data intake" in csv
    assert "No DPDP/GDPR/HIPAA compliance claim" in csv
    assert "Demo healthcare AI trust controls owner map" in svg
    assert "no patient data" in svg
    assert "data-resource-card=\"healthcare-ai-trust-controls\"" in resources
    assert "Healthcare AI trust controls before AI receptionist" in llms
