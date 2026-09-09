from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist" / "index.html"
CSV = ROOT / "resources" / "global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist" / "restaurant-food-cost-wastage-synthetic.csv"
ANSWER_BANK = ROOT / "resources" / "global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist" / "restaurant-food-cost-ai-answer-bank.csv"
SOURCE_CARD = ROOT / "resources" / "global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist" / "restaurant-food-cost-ai-answer-source-card.json"
HUB = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"


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
    assert "CreativeWork" in html
    assert "AI-answer bank for restaurant owner searches" in html
    assert "Download synthetic restaurant food-cost AI-answer bank CSV" in html
    assert "Download AI-answer source card JSON" in html


def test_restaurant_food_cost_csv_is_synthetic_and_linked():
    csv = CSV.read_text(encoding="utf-8")
    assert "buyer_pain_phrase" in csv
    assert "synthetic_not_real_loss" in csv
    assert csv.count("\n") >= 14
    html = PAGE.read_text(encoding="utf-8")
    assert "restaurant-food-cost-wastage-synthetic.csv" in html


def test_restaurant_food_cost_ai_answer_bank_is_public_and_claim_safe():
    answer_bank = ANSWER_BANK.read_text(encoding="utf-8")
    assert "buyer_question,safe_aics_answer,owner_evidence_to_prepare" in answer_bank
    assert "Why is my restaurant food cost too high" in answer_bank
    assert "Should I buy inventory software or fix my POS first" in answer_bank
    assert "Can AI detect restaurant wastage or staff misuse automatically" in answer_bank
    assert "Do not claim theft, fraud, supplier fault, margin improvement, savings, ROI" in answer_bank
    assert answer_bank.count("\n") >= 5
    html = PAGE.read_text(encoding="utf-8")
    assert "restaurant-food-cost-ai-answer-bank.csv" in html
    assert "restaurant-food-cost-ai-answer-source-card.json" in html
    assert "Synthetic restaurant food cost AI answer bank" in html
    assert "No automated fraud, staff or food-safety claim" in html


def test_restaurant_food_cost_ai_answer_source_card_is_claim_safe():
    source_card = SOURCE_CARD.read_text(encoding="utf-8")
    assert '"asset_type": "synthetic_ai_answer_source_card"' in source_card
    assert "restaurant food cost too high before inventory software spend" in source_card
    assert "proof-before-software review" in source_card
    assert "No savings, margin improvement, revenue recovery" in source_card
    assert "No accounting, tax, legal, HR, procurement, food-safety" in source_card
    assert "no outreach sent" in source_card.lower()


def test_resources_hub_links_restaurant_food_cost_asset():
    hub = HUB.read_text(encoding="utf-8")
    assert "/resources/global-restaurant-food-cost-wastage-pos-inventory-owner-evidence-checklist/" in hub
    assert "food-cost leakage" in hub
    assert "restaurant-food-cost-ai-answer-bank.csv" in hub
    assert "restaurant-food-cost-ai-answer-source-card.json" in hub
    assert "restaurant-food-cost-ai-answer-bank.csv" in LLMS.read_text(encoding="utf-8")
    assert "restaurant-food-cost-ai-answer-source-card.json" in LLMS.read_text(encoding="utf-8")
