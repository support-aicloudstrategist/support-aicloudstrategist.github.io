from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")


def test_pricing_surfaces_canada_clinic_diagnostic_as_revenue_entry_point():
    assert "Eight concrete first offers" in PRICING
    assert "Canada clinic missed-call follow-up diagnostic" in PRICING
    assert "/resources/canada-clinic-missed-calls-appointment-follow-up-diagnostic-package/" in PRICING
    assert "without patient-growth, privacy, compliance or revenue claims" in PRICING
    assert "No revenue, ranking, lead volume or business outcome is guaranteed" in PRICING

def test_pricing_surfaces_europe_saas_security_questionnaire_evidence_room_as_revenue_entry_point():
    assert "Europe SaaS security-questionnaire evidence-room diagnostic" in PRICING
    assert "/resources/europe-saas-eu-ai-act-security-questionnaire-evidence-room/" in PRICING
    assert "AI-use inventory, EU AI Act/GDPR adviser-question queues" in PRICING
    assert "without compliance, procurement, legal, security, ranking or revenue claims" in PRICING


def test_pricing_surfaces_ecommerce_abandoned_cart_diagnostic_as_revenue_entry_point():
    assert "Ecommerce abandoned-cart follow-up diagnostic" in PRICING
    assert "/resources/global-ecommerce-abandoned-cart-whatsapp-follow-up-evidence-checklist/" in PRICING
    assert "abandoned-cart, COD confirmation, WhatsApp opt-in, payment-failure" in PRICING
    assert "without revenue, conversion-rate, recovery or ad-performance claims" in PRICING


def test_pricing_surfaces_us_ai_startup_finops_as_revenue_entry_point():
    assert "US AI startup LLM/GPU FinOps diagnostic" in PRICING
    assert "/resources/us-ai-startup-llm-gpu-finops-diagnostic-package/" in PRICING
    assert "CFO/CTO decision queues" in PRICING
    assert "without savings, runway, compliance, security or revenue claims" in PRICING


def test_pricing_surfaces_us_law_firm_intake_as_revenue_entry_point():
    assert "US law firm intake evidence diagnostic" in PRICING
    assert "/services/us-law-firm-ai-intake-answering-service/" in PRICING
    assert "conflict-screening prompts" in PRICING
    assert "without signed-client, legal-advice, compliance, confidentiality or revenue claims" in PRICING


def test_canada_clinic_diagnostic_package_has_buyer_safe_conversion_boundaries():
    page = (ROOT / "resources/canada-clinic-missed-calls-appointment-follow-up-diagnostic-package/index.html").read_text(encoding="utf-8")
    assert "Canada Clinic Missed-Call Follow-Up Diagnostic Package" in page
    assert "fixed-scope operating diagnostic" in page
    assert "Start with a free review" in page
    assert "does not claim a real Canadian clinic client result" in page
    assert "No production access or sensitive patient data is required" in page
