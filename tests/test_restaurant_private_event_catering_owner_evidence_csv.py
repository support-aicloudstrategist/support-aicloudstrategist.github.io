from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "restaurant-missed-bookings-whatsapp-follow-up-checklist"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "restaurant-private-event-catering-owner-evidence.csv"
LLMS = ROOT / "llms.txt"


def test_restaurant_page_links_private_event_catering_csv_and_boundaries():
    html = PAGE.read_text()
    for marker in [
        "Downloadable private-event and catering owner-evidence matrix",
        "Restaurant Private Event + Catering Owner Evidence CSV",
        f"/resources/{SLUG}/restaurant-private-event-catering-owner-evidence.csv",
        "synthetic examples only; no real restaurant",
        "private-event leads",
        "Top-3/top-5 consideration signals",
    ]:
        assert marker in html


def test_restaurant_private_event_csv_has_owner_handoff_rows():
    with CSV.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 8
    assert rows[0].keys() >= {
        "enquiry_source",
        "lead_type",
        "owner_evidence_needed",
        "common_blocker",
        "review_gate",
        "next_owner",
        "unsafe_claim_to_avoid",
    }
    joined = "\n".join(row["unsafe_claim_to_avoid"] for row in rows)
    assert "more bookings guaranteed" in joined
    assert "revenue increase achieved" in joined
    assert "ROI from WhatsApp automation" in joined


def test_restaurant_private_event_csv_discovery_in_llms():
    llms = LLMS.read_text()
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/restaurant-private-event-catering-owner-evidence.csv" in llms
    assert "private-event enquiries, catering leads" in llms
