from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-ent-audiology-hearing-aid-trial-followup-checklist"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
CSV = (ROOT / "resources" / SLUG / "india-ent-audiology-hearing-aid-followup-synthetic.csv").read_text(encoding="utf-8")
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_ent_audiology_checklist_is_indexable_and_buyer_safe():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "ENT / Audiology Missed Calls + Hearing Aid Trial Follow-up Checklist" in PAGE
    assert "ENT clinic missed patient calls" in PAGE
    assert "audiology clinic missed calls" in PAGE
    assert "hearing aid trial follow up" in PAGE
    assert "synthetic readiness checklist" in PAGE
    assert "No outreach was sent" in PAGE
    assert "Rankings, AI-answer inclusion, impressions, clicks, demand, leads, customers and revenue remain unverified" in PAGE
    assert "No real clinic, patient, doctor, audiologist" in PAGE
    assert url in SITEMAP


def test_ent_audiology_csv_and_discovery_links_exist():
    href = f"/resources/{SLUG}/"
    csv_href = f"/resources/{SLUG}/india-ent-audiology-hearing-aid-followup-synthetic.csv"
    assert href in RESOURCES
    assert "hearing-aid trial follow-up" in RESOURCES
    assert f"https://aicloudstrategist.com{href}" in LLMS
    assert f"https://aicloudstrategist.com{csv_href}" in LLMS
    assert "lane,example_safe_evidence,owner_to_confirm,human_review_gate,claim_boundary" in CSV
    assert "hearing_aid_trial_follow_up" in CSV
    assert "No DPDP compliance, legal/privacy advice or certification claim" in CSV
