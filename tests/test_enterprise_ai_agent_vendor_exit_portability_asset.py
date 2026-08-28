from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / "resources" / "global-enterprise-ai-agent-vendor-exit-portability-evidence-checklist"
RESOURCE = RESOURCE_DIR / "index.html"
CSV_TEMPLATE = RESOURCE_DIR / "ai-agent-vendor-exit-portability-evidence-checklist.csv"
RESOURCES_INDEX = ROOT / "resources" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"


def test_ai_agent_vendor_exit_portability_asset_is_discoverable_and_buyer_safe():
    page = RESOURCE.read_text(encoding="utf-8")
    resources = RESOURCES_INDEX.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    url = "https://aicloudstrategist.com/resources/global-enterprise-ai-agent-vendor-exit-portability-evidence-checklist/"
    href = "/resources/global-enterprise-ai-agent-vendor-exit-portability-evidence-checklist/"

    assert "AI agent vendor exit and portability evidence checklist" in page
    assert "AI agent vendor exit checklist" in page
    assert "LLM app portability requirements" in page
    assert "prompt ownership evidence" in page
    assert "model fallback operating plan" in page
    assert "No real customer, migration, cost saving" in page
    assert "not legal, cybersecurity, privacy, financial, clinical, regulatory or procurement advice" in page
    assert f'link rel="canonical" href="{url}"' in page
    assert href in resources
    assert url in llms
    assert "ai-agent-vendor-exit-portability-evidence-checklist.csv" in page


def test_ai_agent_vendor_exit_portability_csv_has_safe_operational_fields():
    rows = list(csv.DictReader(CSV_TEMPLATE.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 1
    assert "Synthetic example row only" in rows[0]["required_proof"]
    assert "No customer, contract, legal or migration outcome claimed" in rows[0]["notes"]
    assert set(rows[0].keys()) == {
        "evidence_area",
        "required_proof",
        "owner",
        "evidence_link",
        "status",
        "notes",
    }


def test_ai_agent_vendor_exit_portability_sitemap_after_build():
    sitemap = SITEMAP.read_text(encoding="utf-8")
    assert "https://aicloudstrategist.com/resources/global-enterprise-ai-agent-vendor-exit-portability-evidence-checklist/" in sitemap
