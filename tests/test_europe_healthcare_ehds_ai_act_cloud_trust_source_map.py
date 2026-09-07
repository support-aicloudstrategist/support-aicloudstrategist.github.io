from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "europe-healthcare-ehds-ai-act-cloud-trust-source-map"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "europe-healthcare-ehds-ai-act-cloud-trust-source-map.csv"
SVG = ROOT / "resources" / SLUG / "europe-healthcare-ehds-ai-act-cloud-trust-owner-map.svg"


def test_europe_healthcare_ehds_ai_act_cloud_trust_asset_exists_and_is_safe():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    svg = SVG.read_text(encoding="utf-8")

    assert "Europe healthcare EHDS + EU AI Act cloud trust source map" in html
    assert "European Health Data Space readiness" in html
    assert "EU AI Act healthcare AI high-risk questions" in html
    assert "NIS2 supplier evidence" in html
    assert "cloud/AI FinOps ownership" in html
    assert "Accurx" in html and "DrDoctor" in html and "Doctolib" in html
    assert "Vanta" in html and "Drata" in html
    assert "synthetic/readiness asset" in html
    assert "does not use real healthcare" in html
    assert "does not prove EHDS" in html
    assert "no ranking" in html and "revenue" in html and "ROI" in html
    assert "not legal, privacy, security, medical" in html
    assert "europe-healthcare-ehds-ai-act-cloud-trust-source-map.csv" in html
    assert "europe-healthcare-ehds-ai-act-cloud-trust-owner-map.svg" in html
    assert "EHDS source inventory" in csv
    assert "EU AI Act use-case classification" in csv
    assert "Do not claim GDPR or UK GDPR compliance" in csv
    assert "Do not claim savings ROI cost reduction or payback" in csv
    assert "Synthetic/readiness asset only" in svg


def test_discovery_surfaces_europe_healthcare_ehds_source_map():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")

    assert f'data-resource-card="{SLUG}"' in resources
    assert f"/resources/{SLUG}/" in resources
    assert "EHDS, EU AI Act, GDPR/DPIA, NIS2 supplier evidence" in llms
    assert f'"/resources/{SLUG}/"' in sitemap_script
