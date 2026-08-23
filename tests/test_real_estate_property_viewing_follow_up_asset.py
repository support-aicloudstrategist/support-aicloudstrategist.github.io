from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REL = "/resources/global-real-estate-property-viewing-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / REL.strip("/") / "index.html"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_real_estate_asset_exists_with_canonical_and_indexable_markers():
    html = text(PAGE)
    assert '<meta name="robots" content="index, follow"' in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert html.count("<h1") == 1
    assert "Real Estate Property Viewing Follow-Up Checklist" in html
    assert "real estate leads not followed up" in html
    assert "estate agent missed calls property viewing follow up" in html
    assert "property portal lead response checklist" in html
    assert "WhatsApp property enquiry follow-up" in html
    assert "AI receptionist boundary for real estate" in html


def test_real_estate_asset_has_proof_before_platform_sections_and_boundaries():
    html = text(PAGE)
    required = [
        "Missed-call register",
        "Portal lead queue",
        "Viewing follow-up SLA",
        "WhatsApp and email handoff",
        "Human review boundary",
        "Weekly owner dashboard",
        "proof-before-platform filter",
        "No real real-estate agency",
        "no legal, property, tenancy, tax, privacy, security, fair-housing, anti-discrimination or valuation advice",
    ]
    for marker in required:
        assert marker in html
    forbidden_claims = [
        "we increased",
        "guaranteed",
        "certified",
        "client result",
    ]
    lowered = html.lower()
    for phrase in forbidden_claims:
        assert phrase not in lowered


def test_real_estate_asset_is_linked_from_discovery_surfaces():
    assert REL in text(ROOT / "resources" / "index.html")
    assert URL in text(ROOT / "llms.txt")
    # The page is linked from the resources hub and llms.txt. It is intentionally
    # outside the capped 50-URL sitemap queue until promoted over an older route.


def test_real_estate_asset_has_structured_data():
    html = text(PAGE)
    assert '"@type":"Article"' in html
    assert '"@type":"FAQPage"' in html
    assert '"@type":"BreadcrumbList"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 5
