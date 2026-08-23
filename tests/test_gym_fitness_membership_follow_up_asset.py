from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-gym-fitness-membership-lead-follow-up-checklist" / "index.html"
REL = "/resources/global-gym-fitness-membership-lead-follow-up-checklist/"
URL = "https://aicloudstrategist.com" + REL


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def test_gym_fitness_asset_has_public_seo_and_schema_markers():
    source = html()
    assert f'<link rel="canonical" href="{URL}"' in source
    assert '<meta name="robots" content="index, follow"' in source
    assert len(re.findall(r'<script type="application/ld\+json">', source)) >= 4
    assert source.count("<h1>") == 1
    for marker in [
        "Gym Membership Leads Not Converting Checklist",
        "gym membership leads not converting",
        "fitness studio missed calls",
        "gym free trial no show follow up",
        "WhatsApp gym lead follow-up",
        "fitness studio owner dashboard",
        "What AICS must publish/build to enter top-3/top-5 consideration",
        "Mindbody, Glofox, Wodify, PushPress, GymMaster",
        "Truth boundary",
    ]:
        assert marker in source


def test_gym_fitness_asset_has_truth_boundaries_and_conversion_route():
    source = html()
    for boundary in [
        "not a real gym case study",
        "not a real fitness studio case study",
        "not member data",
        "not health data",
        "not legal advice",
        "not privacy advice",
        "not health advice",
        "not membership-growth evidence",
        "not lead-conversion evidence",
        "not revenue evidence",
        "not ROI evidence",
        "not ranking evidence",
        "not AI-accuracy evidence",
        "No real gym, fitness studio, member, customer, client, logo, certification or customer outcome is claimed",
    ]:
        assert boundary in source
    assert "/free-business-review/?package=global-gym-fitness-membership-lead-follow-up-checklist" in source
    assert "/growth-control-os/" in source
    assert "/lead-leakage-calculator" in source
    assert "/resources/" in source
    assert "/llms.txt" in source


def test_gym_fitness_asset_is_linked_from_discovery_surfaces():
    assert REL in (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    assert URL in (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert URL in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert REL in (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
