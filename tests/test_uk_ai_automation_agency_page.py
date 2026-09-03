from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = "/ai-automation-agency-uk/"
URL = "https://aicloudstrategist.com" + REL
PAGE = ROOT / "ai-automation-agency-uk" / "index.html"


def test_uk_ai_automation_agency_page_is_buyer_safe_and_indexable():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="index, follow"' in html
    assert f'<link rel="canonical" href="{URL}"' in html
    assert html.count("<h1") == 1
    assert "AI automation agency UK" in html
    assert "/free-business-review/?market=uk-ai-automation" in html
    assert "/resources/uk-private-clinic-owner-evidence-decision-memo/" in html
    assert "UK clinic buyer proof path" in html
    assert "forwardable owner memo" in html
    assert "before sharing patient data or committing to platform spend" in html
    assert "UK GDPR-aware operational prompts" in html
    assert "not legal advice" in html.lower()
    assert "does not guarantee" in html.lower()
    proof_boundary_terms = [
        "guaranteed leads",
        "revenue",
        "UK client results",
        "local certification",
        "official platform partnership",
    ]
    for term in proof_boundary_terms:
        assert term in html


def test_uk_ai_automation_agency_discovery_surfaces_are_updated():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap_builder = (ROOT / "scripts" / "build_sitemap.py").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert URL in llms
    assert f'"{REL}"' in sitemap_builder
    assert URL in sitemap
