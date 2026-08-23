import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "canada-clinic-missed-calls-appointment-follow-up-checklist" / "index.html"


def _jsonld_blocks(html: str):
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html):
        yield json.loads(block)


def test_canada_clinic_asset_has_refreshed_buyer_language_and_market_signals():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        "Jane App alternative",
        "Juvonno alternative",
        "ClinicSense alternative",
        "OceanMD patient engagement",
        "PIPEDA questions",
        "PHIPA questions",
        "Accessible market signals sampled on 2026-08-23",
        "did not show a readable AICloudStrategist marker",
        "TELUS Health EMR page returned HTTP 403",
        "source-to-owner queues",
    ]
    for marker in required:
        assert marker in html


def test_canada_clinic_asset_routes_to_diagnostic_and_keeps_claim_boundaries():
    html = PAGE.read_text(encoding="utf-8")
    assert "/resources/canada-clinic-missed-calls-appointment-follow-up-diagnostic-package/" in html
    boundaries = [
        "not a real Canadian clinic case study",
        "not a testimonial",
        "not proof of patient growth",
        "No real Canadian clinic",
        "No real Canadian clinic, patient, PHI",
        "no-show reduction",
        "revenue, ROI, ranking",
        "AI-accuracy claim",
    ]
    for marker in boundaries:
        assert marker in html
    forbidden_claims = [
        "guaranteed appointments",
        "guaranteed compliance",
        "certified PHIPA",
        "certified PIPEDA",
        "official Jane partner",
    ]
    lowered = html.lower()
    for claim in forbidden_claims:
        assert claim.lower() not in lowered


def test_canada_clinic_jsonld_remains_parseable_and_current():
    html = PAGE.read_text(encoding="utf-8")
    blocks = list(_jsonld_blocks(html))
    assert len(blocks) >= 4
    article = next(block for block in blocks if block.get("@type") == "Article")
    assert article["dateModified"] == "2026-08-23"
    about = " ".join(article["about"])
    assert "PIPEDA PHIPA questions" in about
    assert "Jane App alternative" in about
