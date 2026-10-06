from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-specialty-clinic-ai-receptionist-no-phi-scope-memo"
PAGE = ROOT / "resources" / SLUG / "index.html"


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_no_phi_scope_memo_has_indexable_seo_and_schema():
    text = html()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/us-specialty-clinic-ai-receptionist-no-phi-scope-memo/"' in text
    assert '<meta name="robots" content="index, follow"' in text
    assert text.count("<h1>") == 1
    assert len(re.findall(r'<script type="application/ld\+json">', text)) >= 4
    for marker in [
        "AI receptionist for medical practice",
        "HIPAA AI receptionist",
        "healthcare voice agent",
        "patient engagement platform",
        "EHR/PMS",
        "medical office call answering",
        "data-proof-marker=\"us-specialty-clinic-ai-receptionist-no-phi-scope-memo\"",
    ]:
        assert marker in text


def test_no_phi_scope_memo_truth_boundaries_are_explicit():
    text = html()
    for marker in [
        "synthetic buyer-education and scoping memo",
        "not legal, privacy, security, clinical, billing or procurement advice",
        "US specialty clinic customer",
        "signed BAA",
        "HIPAA/SOC 2/HITRUST certification",
        "appointment growth",
        "revenue",
        "ROI",
        "AI accuracy",
        "PHI/ePHI",
        "patient lists",
        "call recordings",
        "production API keys",
        "credentials",
    ]:
        assert marker in text


def test_no_phi_scope_memo_is_linked_from_discovery_surfaces():
    rel = f"/resources/{SLUG}/"
    abs_url = "https://aicloudstrategist.com" + rel
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert rel in resources
    assert abs_url in llms
    assert abs_url in sitemap


def test_no_phi_scope_memo_points_to_conversion_and_related_matrix():
    text = html()
    assert "/free-business-review/?package=us-specialty-clinic-ai-receptionist-no-phi-scope-memo" in text
    assert "/resources/us-specialty-clinic-ai-receptionist-vendor-shortlist-evidence-matrix/" in text
