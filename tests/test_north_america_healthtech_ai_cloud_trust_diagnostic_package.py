import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/index.html"
URL = "https://aicloudstrategist.com/resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def json_ld_objects(html: str):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return [json.loads(block) for block in blocks]


def test_page_is_indexable_with_canonical_and_metadata():
    html = read(PAGE)
    assert '<meta name="robots" content="index, follow"/>' in html
    assert f'<link rel="canonical" href="{URL}"/>' in html
    assert "North America Healthtech AI Cloud Trust Diagnostic Package" in html
    assert "HIPAA-style questionnaire" in html
    assert "vendor-risk and FinOps evidence" in html


def test_structured_data_supports_article_service_and_faq():
    data = json_ld_objects(read(PAGE))
    types = {item["@type"] for item in data}
    assert {"Article", "Service", "FAQPage"}.issubset(types)
    article = next(item for item in data if item["@type"] == "Article")
    assert article["mainEntityOfPage"] == URL
    assert "healthtech AI cloud trust diagnostic" in article["about"]
    service = next(item for item in data if item["@type"] == "Service")
    assert service["areaServed"] == ["United States", "Canada"]
    faq = next(item for item in data if item["@type"] == "FAQPage")
    assert "HIPAA, SOC 2 or HITRUST" in faq["mainEntity"][0]["name"]


def test_truth_boundaries_and_no_forbidden_real_claims():
    html = read(PAGE)
    required = [
        "not a real client case study",
        "not a real client case study, testimonial",
        "No patient data, PHI, customer data, cloud credentials or real bills",
        "not a compliance automation platform or hyperscaler",
        "No outreach was sent",
    ]
    for phrase in required:
        assert phrase in html
    forbidden = ["guaranteed savings", "certified partner", "client logo", "proven ROI"]
    lowered = html.lower()
    for phrase in forbidden:
        assert phrase not in lowered


def test_discovery_wiring_resources_sitemap_llms_and_backlink():
    resources = read(ROOT / "resources/index.html")
    sitemap_builder = read(ROOT / "scripts/build_sitemap.py")
    llms = read(ROOT / "llms.txt")
    evidence_room = read(ROOT / "resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/index.html")
    assert "/resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/" in resources
    assert "/resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/" in sitemap_builder
    assert URL in llms
    assert "/resources/north-america-healthtech-ai-cloud-trust-diagnostic-package/" in evidence_room


def test_related_cluster_links_exist():
    html = read(PAGE)
    for href in [
        "/resources/north-america-healthtech-ai-cloud-finops-trust-evidence-room/",
        "/resources/us-healthtech-growthos-vs-patient-engagement-grc-finops-comparison/",
        "/resources/us-healthtech-ai-vendor-risk-cloud-cost-evidence-checklist/",
        "/services/cloud-security/",
        "/services/cloud-finops/",
        "/healthcare-growthos/",
        "/case-studies/",
    ]:
        assert href in html
