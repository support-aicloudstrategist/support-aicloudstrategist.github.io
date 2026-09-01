from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist" / "index.html"
CSV = ROOT / "resources" / "global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist" / "restaurant-food-cost-wastage-synthetic.csv"
HUB = ROOT / "resources" / "index.html"


def test_restaurant_food_cost_asset_exists_with_truth_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "Restaurant Food Cost Too High? POS + Inventory Owner Evidence Checklist" in html
    assert "restaurant food cost too high" in html.lower()
    assert "simulated proof-of-method" in html
    assert "not a real customer case study" in html
    assert "No outreach was sent" in html
    assert "Request no-credentials review" in html
    assert "FAQPage" in html
    assert "Dataset" in html


def test_restaurant_food_cost_csv_is_synthetic_and_linked():
    csv = CSV.read_text(encoding="utf-8")
    assert "buyer_pain_phrase" in csv
    assert "synthetic_not_real_loss" in csv
    assert csv.count("\n") >= 14
    html = PAGE.read_text(encoding="utf-8")
    assert "restaurant-food-cost-wastage-synthetic.csv" in html


def test_resources_hub_links_restaurant_food_cost_asset():
    hub = HUB.read_text(encoding="utf-8")
    assert "/resources/global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist/" in hub
    assert "food-cost leakage" in hub
