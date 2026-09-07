import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "47-cloud-cost-checks-before-finops-consultant"
RESOURCE = ROOT / "resources" / SLUG


def test_cloud_cost_checks_resource_has_owner_evidence_and_boundaries():
    html = (RESOURCE / "index.html").read_text(encoding="utf-8")

    assert "Evidence status:" in html
    assert "synthetic owner-readiness template" in html
    assert "not a client case study" in html
    assert "href=\"cloud-cost-owner-review-checklist.csv\"" in html
    assert "href=\"cloud-cost-owner-board.svg\"" in html
    assert "no real client or customer evidence" in html
    assert "No cloud bill, invoice, personal data, customer data, production data, credentials" in html
    assert "no rankings, demand, leads, customers, revenue, savings, ROI" in html
    assert "No legal, privacy, security, procurement, tax, financial, architecture or FinOps advice" in html
    assert "Owner review / approval gate" in html
    assert "free-business-review" in html


def test_cloud_cost_owner_review_csv_blocks_fake_savings_and_unsafe_access():
    rows = list(csv.DictReader((RESOURCE / "cloud-cost-owner-review-checklist.csv").open(encoding="utf-8")))
    assert len(rows) >= 8
    gates = {row["gate"] for row in rows}
    assert {"scope", "data", "visibility", "waste", "claims", "advice", "commercial", "proof_boundary"}.issubset(gates)

    proof_boundary = next(row for row in rows if row["gate"] == "proof_boundary")
    assert "Synthetic/readiness template only" in proof_boundary["evidence_to_collect"]
    assert "No real client" in proof_boundary["stop_rule"]
    assert "savings" in proof_boundary["stop_rule"]
    assert "ROI" in proof_boundary["stop_rule"]

    data_gate = next(row for row in rows if row["gate"] == "data")
    assert "credentials" in data_gate["stop_rule"]
    assert "API keys" in data_gate["stop_rule"]


def test_cloud_cost_owner_board_is_clearly_demo_labelled():
    svg = (RESOURCE / "cloud-cost-owner-board.svg").read_text(encoding="utf-8")
    assert "Demo cloud cost owner board" in svg
    assert "Demo/synthetic" in svg
    assert "no real client" in svg
    assert "savings or ROI proof" in svg
    assert "not legal, privacy, security, procurement, tax, financial, architecture or FinOps advice" in svg
