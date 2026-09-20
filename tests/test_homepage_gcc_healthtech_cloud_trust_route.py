from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
RESOURCE = ROOT / "resources" / "gcc-healthtech-cross-border-patient-data-cloud-trust-faq" / "index.html"
CARD = RESOURCE.parent / "gcc-healthtech-cross-border-ai-answer-source-card.json"


def test_homepage_promotes_gcc_healthtech_cloud_trust_route_once():
    source = HOME.read_text(encoding="utf-8")
    route = "/resources/gcc-healthtech-cross-border-patient-data-cloud-trust-faq/"

    assert source.count('data-homepage-resource="gcc-healthtech-cross-border-patient-data-cloud-trust-faq"') == 1
    assert source.count(f'href="{route}"') == 2
    assert "GCC Healthtech Cross-Border Patient Data Cloud Trust FAQ" in source
    assert "before sharing patient data or credentials" in source
    assert "Open the GCC healthtech cross-border Cloud Trust FAQ" in source


def test_gcc_healthtech_route_has_claim_safe_source_card():
    page = RESOURCE.read_text(encoding="utf-8")
    card = CARD.read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

    assert "gcc-healthtech-cross-border-ai-answer-source-card.json" in page
    assert "No. Use redacted workflow names" in page
    assert "No outreach was sent" in page
    assert "customer" in card and "revenue" in card and "ROI" in card
    assert "gcc-healthtech-cross-border-ai-answer-source-card.json" in llms
