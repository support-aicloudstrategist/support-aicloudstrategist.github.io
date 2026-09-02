from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-construction-project-delay-daily-progress-owner-evidence-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "construction-daily-progress-owner-evidence.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"


def test_construction_progress_page_contains_buyer_language_and_boundaries():
    html = PAGE.read_text()
    for marker in [
        "Construction Project Delay Daily Progress Evidence Checklist",
        "construction project delays due to manual updates",
        "project status updates taking too long construction",
        "site progress report automation construction",
        "contractor change order follow up",
        "Top-3 / top-5 consideration angle",
        "This is a synthetic readiness checklist, not a real client case study.",
        "No outreach was sent.",
        f"/resources/{SLUG}/construction-daily-progress-owner-evidence.csv",
    ]:
        assert marker in html


def test_construction_progress_csv_has_owner_evidence_rows():
    with CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 8
    assert rows[0].keys() >= {
        "work_package",
        "owner_evidence_needed",
        "common_blocker",
        "review_gate",
        "next_owner",
        "unsafe_claim_to_avoid",
    }
    joined = "\n".join(row["unsafe_claim_to_avoid"] for row in rows)
    assert "schedule recovery guaranteed" in joined
    assert "cost savings achieved" in joined


def test_construction_progress_discovery_surfaces():
    resources = RESOURCES.read_text()
    llms = LLMS.read_text()
    sitemap = SITEMAP.read_text()
    assert f"/resources/{SLUG}/" in resources
    assert "Construction Project Delay Daily Progress Evidence Checklist" in resources
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert "Construction project delays due to manual updates" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
