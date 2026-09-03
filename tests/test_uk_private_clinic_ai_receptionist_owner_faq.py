from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-ai-receptionist-owner-faq"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
MEMO = (ROOT / "resources" / "uk-private-clinic-owner-evidence-decision-memo" / "index.html").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_uk_private_clinic_ai_receptionist_owner_faq_is_indexable_and_buyer_safe():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "UK private clinic AI receptionist owner FAQ" in PAGE
    assert "practice-management" in PAGE
    assert "patient engagement" in PAGE
    assert "no-credentials review route" in PAGE
    assert "AI receptionist human handover" in PAGE
    assert "No for first scoping" in PAGE
    assert "Do not claim GDPR, CQC, DTAC, DSPT or clinical readiness" in PAGE
    assert "not a real clinic case study" in PAGE
    assert "No outreach was sent" in PAGE
    assert "makes no claim of appointment growth, no-show reduction, booking conversion, revenue, savings, ROI" in PAGE
    assert "FAQPage" in PAGE


def test_uk_private_clinic_ai_receptionist_owner_faq_discovery_links_exist():
    href = f"/resources/{SLUG}/"
    assert href in RESOURCES
    assert "UK Private Clinic AI Receptionist Owner FAQ" in RESOURCES
    assert href in MEMO
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{href}" in SITEMAP
