from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "india-radiology-mri-ct-referral-followup-dpdp-finops-checklist"
PAGE = (ROOT / "resources" / SLUG / "index.html").read_text(encoding="utf-8")
CSV_PATH = ROOT / "resources" / SLUG / "india-radiology-mri-ct-referral-followup-synthetic.csv"
RESOURCES = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")


def test_india_radiology_checklist_is_indexable_buyer_safe_and_discoverable():
    url = f"https://aicloudstrategist.com/resources/{SLUG}/"
    href = f"/resources/{SLUG}/"
    assert '<meta name="robots" content="index, follow"/>' in PAGE
    assert f'<link rel="canonical" href="{url}"/>' in PAGE
    assert "India Radiology MRI/CT Referral Follow-up DPDP + FinOps Checklist" in PAGE
    assert "MRI/CT referral leakage" in PAGE
    assert "missed callbacks" in PAGE
    assert "report-access queries" in PAGE
    assert "WhatsApp/DPDP evidence gaps" in PAGE
    assert "cloud image-access" in PAGE
    assert "Request no-credentials review" in PAGE
    assert "/free-business-review/?package=india-radiology-mri-ct-referral-followup-dpdp-finops" in PAGE
    assert "not a real customer case study" in PAGE
    assert "No outreach was sent" in PAGE
    assert "no patient data" in PAGE.lower() or "No real radiology centre" in PAGE
    for forbidden_boundary in ("storage-savings claim", "appointment-growth claim", "compliance proof"):
        assert forbidden_boundary in PAGE
    assert href in RESOURCES
    assert "India Radiology MRI/CT Referral Follow-up DPDP + FinOps Checklist" in RESOURCES
    assert url in LLMS
    assert url in SITEMAP


def test_india_radiology_synthetic_csv_is_downloadable_and_consistent():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    assert len(rows) == 24
    assert sum(1 for row in rows if row["followup_risk"] == "High") == 14
    assert sum(1 for row in rows if int(row["age_hours"]) >= 24 and row["status"] != "Resolved") == 16
    assert sum(1 for row in rows if row["consent_notice_evidence"] in {"No", "Partial"}) == 16
    assert sum(1 for row in rows if row["cloud_access_control_evidence"] in {"No", "Partial"}) == 20
    duplicate_gb = sum(float(row["image_storage_gb"]) for row in rows if row["duplicate_image_study"] == "Yes")
    assert round(duplicate_gb, 1) == 10.2
