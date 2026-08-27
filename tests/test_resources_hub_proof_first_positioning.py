from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "index.html"


def test_resources_hub_positions_proof_first_ai_trust_entry_point():
    source = PAGE.read_text(encoding="utf-8")
    description = (
        "Proof-first AI, cloud trust, FinOps and growth-system resources for buyers who need evidence, "
        "owner handoff and safe next steps before platform or automation commitments."
    )
    social_description = (
        "AICloudStrategist proof-first resource hub for AI trust, healthtech evidence rooms, "
        "cloud/LLM spend ownership, human review and growth-system readiness."
    )
    assert f'<meta name="description" content="{description}"/>' in source
    assert f'<meta property="og:description" content="{social_description}">' in source
    assert f'<meta name="twitter:description" content="{social_description}">' in source
    assert f'<p>{description}</p>' in source
    assert source.find("/resources/north-america-healthtech-ai-trust-first-review/") < source.find("/resources/north-america-healthtech-ai-human-review-escalation-policy-template/")


def test_resources_hub_schema_uses_current_resource_language_without_overclaiming():
    source = PAGE.read_text(encoding="utf-8")
    assert "AICloudStrategist proof-first resource hub for AI trust" in source
    for forbidden in ["trusted by", "guaranteed compliance", "real client results", "increased revenue"]:
        assert forbidden not in source.lower()
