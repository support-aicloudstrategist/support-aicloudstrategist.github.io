from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "global-ai-tool-sprawl-no-credentials-intake-policy"
URL = "https://aicloudstrategist.com/resources/global-ai-tool-sprawl-no-credentials-intake-policy/"
PAGE = ROOT / "resources" / SLUG / "index.html"
CSV = ROOT / "resources" / SLUG / "ai-tool-sprawl-no-credentials-intake-policy.csv"
CARD = ROOT / "resources" / SLUG / "ai-tool-sprawl-no-credentials-answer-source-card.json"


def test_ai_tool_sprawl_no_credentials_policy_asset_exists_and_is_claim_safe():
    html = PAGE.read_text(encoding="utf-8")
    csv = CSV.read_text(encoding="utf-8")
    card = CARD.read_text(encoding="utf-8")
    assert "AI tool sprawl no-credentials intake policy" in html
    assert "Download CSV policy" in html
    assert "customer data, employee data, credentials, production access" in html
    assert "not a customer case study" in html
    assert "savings, revenue, ROI or productivity claim" in html
    assert "No outreach was sent" in html
    assert "intake_area,safe_to_share_first,do_not_share_first" in csv
    assert "Credentials; API keys" in csv
    assert '"blocked_claims"' in card
    assert "savings guarantee" in card


def test_ai_tool_sprawl_no_credentials_policy_discoverability():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_script = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    assert f'/resources/{SLUG}/' in resources
    assert URL in llms
    assert f'https://aicloudstrategist.com/resources/global-ai-tool-sprawl-no-credentials-intake-policy/ai-tool-sprawl-no-credentials-intake-policy.csv' in llms
    assert f'https://aicloudstrategist.com/resources/global-ai-tool-sprawl-no-credentials-intake-policy/ai-tool-sprawl-no-credentials-answer-source-card.json' in llms
    assert '"/resources/global-ai-tool-sprawl-no-credentials-intake-policy/"' in sitemap_script

