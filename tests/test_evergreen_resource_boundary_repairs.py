import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
    "ai-automation-small-business-use-cases",
    "ai-chatbot-development-cost-india",
    "ai-voice-agents-appointment-booking",
    "aics-vs-alternatives-comparison",
    "first-customer-proof-protocol",
    "global-ai-pilot-tools-vs-assurance-led-review-comparison",
    "lead-follow-up-automation-guide",
    "small-business-website-checklist-india",
    "whatsapp-business-api-vs-direct-whatsapp-india",
    "custom-ai-solutions-vs-off-the-shelf-ai-tools-guide",
]
CSV_NAME = "proof-boundary-owner-review-checklist.csv"


def test_top_evergreen_resource_pages_have_explicit_proof_boundaries_and_csv_artifacts():
    for slug in SLUGS:
        html = (ROOT / "resources" / slug / "index.html").read_text(encoding="utf-8")
        assert "Evidence status:" in html, slug
        assert "not a client case study" in html, slug
        assert "no real client, customer" in html, slug
        assert "personal data" in html, slug
        assert "production data" in html, slug
        assert "rankings, demand, leads, customers, revenue, savings, ROI" in html, slug
        assert "not legal, privacy, security, medical" in html, slug
        assert "owner review / approval gate" in html, slug
        assert f"href=\"{CSV_NAME}\"" in html, slug
        assert "free-business-review" in html or "pricing.html#fixed-scope-diagnostics" in html or "/services/" in html, slug


def test_top_evergreen_resource_csv_artifacts_encode_owner_stop_rules():
    for slug in SLUGS:
        path = ROOT / "resources" / slug / CSV_NAME
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        assert len(rows) >= 6, slug
        gates = {row["gate"] for row in rows}
        assert {"scope", "data", "claims", "advice", "commercial", "proof_boundary"}.issubset(gates), slug
        boundary = next(row for row in rows if row["gate"] == "proof_boundary")
        assert "not client proof" in boundary["owner_question"], slug
        assert "No real client" in boundary["stop_rule"], slug
        assert "ROI" in boundary["stop_rule"], slug
