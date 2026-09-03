from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-cost-savings-claim-boundary-worksheet"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV_PATH = ROOT / "resources" / SLUG / f"{SLUG}.csv"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
SITEMAP = ROOT / "sitemap.xml"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
CSV_URL = f"{URL}{SLUG}.csv"


def test_ai_cost_savings_claim_boundary_page_is_buyer_safe_and_sellable():
    html = PAGE.read_text(encoding="utf-8")
    assert "AI Cost Savings Claim Boundary Worksheet" in html
    assert "Request a no-credentials claim boundary review" in html
    assert f"/free-business-review/?package=ai-cost-savings-claim-boundary&amp;source=resource" in html
    assert "not a savings guarantee" in html
    assert "not ROI evidence" in html
    assert "not proof that AICS lowered any customer cost" in html
    assert "Financial, legal, procurement and compliance claims require" in html


def test_ai_cost_savings_claim_boundary_csv_has_pause_triggers_and_owners():
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 4
    assert rows[0].keys() >= {
        "claim_area",
        "claim_requested",
        "evidence_required",
        "pause_trigger",
        "human_owner",
        "safe_note",
    }
    joined = "\n".join(" ".join(row.values()) for row in rows)
    assert "Finance owner + platform owner" in joined
    assert "Commercial owner + legal/procurement adviser" in joined
    assert "Do not promise savings" in joined
    assert "customer proof is approved" in joined


def test_ai_cost_savings_claim_boundary_is_discoverable_from_hub_llms_sitemap():
    resources = RESOURCES.read_text(encoding="utf-8")
    assert f'/resources/{SLUG}/' in resources
    assert f'/resources/{SLUG}/{SLUG}.csv' in resources
    llms = LLMS.read_text(encoding="utf-8")
    assert URL in llms
    assert CSV_URL in llms
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert URL in sitemap
    assert CSV_URL not in sitemap


def test_ai_cost_savings_claim_boundary_json_ld_is_parseable():
    html = PAGE.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html)
    assert blocks
    parsed = [json.loads(block) for block in blocks]
    assert any(block.get("@type") == "FAQPage" for block in parsed if isinstance(block, dict))
