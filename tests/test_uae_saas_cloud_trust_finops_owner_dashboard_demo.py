import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uae-saas-cloud-trust-finops-readiness-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
DASHBOARD = ROOT / "resources" / SLUG / "uae-saas-cloud-trust-finops-owner-dashboard-demo.svg"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


def _json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.I | re.S)]


def test_uae_saas_page_exposes_demo_dashboard_and_schema():
    html = PAGE.read_text(encoding="utf-8")
    docs = _json_ld_documents(html)
    image = next(
        doc for doc in docs
        if doc.get("@type") == "ImageObject"
        and doc.get("name") == "Synthetic UAE SaaS Cloud Trust and FinOps owner dashboard demo"
    )

    assert image["url"].endswith("/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg")
    assert "Synthetic examples only" in image["description"]
    assert "data-demo-owner-dashboard=\"uae-saas-cloud-trust-finops\"" in html
    assert "uses no real UAE SaaS customer, cloud bill, account, vendor file" in html


def test_uae_saas_owner_dashboard_svg_is_demo_labelled_and_claim_safe():
    svg = DASHBOARD.read_text(encoding="utf-8")

    assert "Synthetic UAE SaaS Cloud Trust and FinOps owner dashboard demo" in svg
    assert "NO REAL CUSTOMER DATA" in svg
    assert "Unexplained spend spike" in svg
    assert "AI spend approval gaps" in svg
    assert "not proof of savings, compliance, ranking, revenue, customer demand or AI accuracy" in svg
    assert "Not a case study" in svg


def test_uae_saas_owner_dashboard_is_discoverable_from_hub_and_llms():
    resources_html = RESOURCES.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    marker = "/resources/uae-saas-cloud-trust-finops-readiness-checklist/uae-saas-cloud-trust-finops-owner-dashboard-demo.svg"

    assert marker in resources_html
    assert "Open demo owner dashboard SVG" in resources_html
    assert f"https://aicloudstrategist.com{marker}" in llms
