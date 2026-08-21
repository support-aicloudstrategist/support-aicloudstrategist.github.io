from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "veterinary-clinic-missed-calls-after-hours-follow-up-checklist" / "index.html"


def source() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_veterinary_asset_has_public_seo_and_schema_markers():
    html = source()
    assert '<link rel="canonical" href="https://aicloudstrategist.com/resources/veterinary-clinic-missed-calls-after-hours-follow-up-checklist/"' in html
    assert '<meta name="robots" content="index, follow"' in html
    assert len(re.findall(r'<script type="application/ld\+json">', html)) >= 4
    assert html.count("<h1>") == 1
    for marker in [
        "veterinary clinic missed calls",
        "after-hours vet appointment requests",
        "animal hospital phone answering",
        "vet clinic client communication software",
        "owner dashboard",
        "Truth boundary",
    ]:
        assert marker in html


def test_veterinary_asset_has_truth_boundaries_and_conversion_route():
    html = source()
    for forbidden_claim_boundary in [
        "No real veterinary clinic",
        "no testimonial",
        "no ranking claim",
        "not proof of pet-owner growth",
        "revenue or ROI",
        "AI-accuracy claim",
        "not veterinary, medical, legal, privacy or compliance advice",
    ]:
        assert forbidden_claim_boundary in html
    assert "/free-business-review/?package=veterinary-clinic-missed-calls-after-hours-follow-up" in html
    assert "/resources/" in html
    assert "/llms.txt" in html


def test_veterinary_asset_is_linked_from_discovery_surfaces():
    rel = "/resources/veterinary-clinic-missed-calls-after-hours-follow-up-checklist/"
    assert rel in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com" + rel in (ROOT / "llms.txt").read_text(encoding="utf-8")
