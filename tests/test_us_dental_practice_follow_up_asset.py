from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-dental-practice-missed-call-treatment-plan-follow-up-checklist"
REL = f"/resources/{SLUG}/"
URL = f"https://aicloudstrategist.com{REL}"
PAGE = ROOT / "resources" / SLUG / "index.html"


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_us_dental_follow_up_asset_is_buyer_safe_and_indexable():
    html = source(PAGE)
    assert '<meta name="robots" content="index, follow"' in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert "US Dental Practice Missed Call + Treatment Plan Follow-Up Checklist" in html
    assert "missed calls" in html
    assert "new-patient enquiries" in html
    assert "insurance checks" in html
    assert "hygiene recall" in html
    assert "treatment-plan follow-up" in html
    assert "AI receptionist" in html
    assert "HIPAA-aware" in html
    assert "/free-business-review/?service=us-dental-growthos-checklist" in html


def test_us_dental_follow_up_asset_keeps_claim_boundaries_clear():
    html = source(PAGE).lower()
    assert "not a client case study" in html
    assert "not a client case study, medical recommendation, legal opinion, hipaa compliance certification" in html
    assert "does not guarantee bookings, revenue, treatment acceptance, rankings or compliance" in html
    prohibited = ["certified hipaa compliant", "guaranteed patients", "guaranteed revenue", "proven results"]
    for phrase in prohibited:
        assert phrase not in html


def test_us_dental_follow_up_asset_is_on_discovery_surfaces():
    assert REL in source(ROOT / "resources" / "index.html")
    assert URL in source(ROOT / "llms.txt")
    assert URL in source(ROOT / "sitemap.xml")
    assert REL in source(ROOT / "scripts" / "build_sitemap.py")
    assert REL in source(ROOT / "pricing.html")
