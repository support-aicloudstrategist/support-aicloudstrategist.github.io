from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-owner-evidence-decision-memo"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
CSV = (ROOT / "resources" / SLUG / "uk-private-clinic-owner-evidence-decision-memo.csv").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_uk_private_clinic_owner_memo_is_indexable_and_buyer_safe():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "UK private clinic owner evidence decision memo" in PAGE
    assert "AI receptionist for clinics UK" in PAGE
    assert "private practice-management software" in PAGE
    assert "GDPR appointment communication evidence" in PAGE
    assert "no-credentials first review" in PAGE
    assert "not a real client case study" in PAGE
    assert "No outreach was sent" in PAGE
    assert "No appointment growth, no-show reduction, revenue, savings or ROI claim" in PAGE
    assert "No medical advice, clinical-safety proof or AI-accuracy claim" in PAGE
    assert "No vendor superiority, ranking, replacement or partnership claim" in PAGE
    assert url in SITEMAP


def test_uk_private_clinic_owner_memo_csv_and_discovery_links_exist():
    href = f"/resources/{SLUG}/"
    csv_href = f"/resources/{SLUG}/uk-private-clinic-owner-evidence-decision-memo.csv"
    assert href in RESOURCES
    assert "UK Private Clinic Owner Evidence Decision Memo" in RESOURCES
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{csv_href}" in LLMS
    assert "section,owner_question,evidence_to_attach,unsafe_claim_boundary,safe_next_step" in CSV
    assert "AI and human-handover stop rules" in CSV
    assert "GDPR and evidence owner questions" in CSV
    assert "No legal, privacy, security or GDPR compliance conclusion" in CSV
    assert "No promise that review delivers compliance, growth, savings, bookings or implementation success" in CSV
