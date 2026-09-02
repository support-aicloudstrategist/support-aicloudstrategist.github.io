from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EUROPE_SAAS_AI_EVIDENCE_URLS = [
    "https://aicloudstrategist.com/resources/europe-saas-ai-evidence-room-faq/",
    "https://aicloudstrategist.com/resources/europe-saas-ai-evidence-room-template/",
    "https://aicloudstrategist.com/resources/europe-saas-ai-finops-allocation-checklist/",
    "https://aicloudstrategist.com/resources/europe-saas-ai-governance-evidence-diagnostic-package/",
    "https://aicloudstrategist.com/resources/europe-saas-security-questionnaire-ai-evidence-comparison/",
]


def test_europe_saas_ai_evidence_cluster_is_llm_discoverable():
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

    assert "Europe SaaS teams preparing AI governance" in llms
    assert "security-questionnaire" in llms
    assert "GDPR-aware evidence" in llms
    assert "FinOps owner packs" in llms
    for url in EUROPE_SAAS_AI_EVIDENCE_URLS:
        assert url in llms


def test_europe_saas_ai_evidence_cluster_pages_are_indexable_and_sitemapped():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

    for url in EUROPE_SAAS_AI_EVIDENCE_URLS:
        slug = url.rstrip("/").split("/")[-1]
        page = (ROOT / "resources" / slug / "index.html").read_text(encoding="utf-8")
        assert 'name="robots" content="index, follow' in page
        assert f"<loc>{url}</loc>" in sitemap
        assert 'href="/free-business-review/' in page
