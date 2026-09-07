from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/australia-ndis-intake-vs-answering-service-crm-comparison/index.html"
CSV = ROOT / "resources/australia-ndis-intake-vs-answering-service-crm-comparison/australia-ndis-intake-comparison-matrix.csv"
SVG = ROOT / "resources/australia-ndis-intake-vs-answering-service-crm-comparison/australia-ndis-intake-comparison-map.svg"
RESOURCES = ROOT / "resources/index.html"
LLMS = ROOT / "llms.txt"


def test_australia_ndis_comparison_public_asset_exists_with_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "NDIS provider participant enquiry follow up" in html
    assert "Answering Service vs CRM vs Rostering vs AICS Owner-Evidence Review" in html
    assert "Visibility check" in html
    assert "sampled result HTML did not show AICS markers" in html
    assert "Rankings, AI-answer inclusion, impressions, clicks, demand" in html
    assert "No real Australian NDIS provider" in html
    assert "No outreach was sent" in html
    assert "australia-ndis-intake-comparison-matrix.csv" in html
    assert "australia-ndis-intake-comparison-map.svg" in html
    assert "https://schema.org" in html


def test_australia_ndis_comparison_downloads_and_discovery_links():
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")
    resources = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert "AICS owner-evidence review" in csv
    assert "Synthetic row only" in csv
    assert "Demo-labelled readiness map" in svg
    assert "data-resource-card=\"australia-ndis-intake-vs-answering-service-crm-comparison\"" in resources
    assert "australia-ndis-intake-vs-answering-service-crm-comparison" in llms
