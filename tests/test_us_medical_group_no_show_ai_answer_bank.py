from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SLUG = "us-medical-group-no-show-recovery-vs-patient-engagement-ai-receptionist-comparison"
PAGE = ROOT / "resources" / SLUG / "index.html"
ANSWER_BANK = ROOT / "resources" / SLUG / "us-medical-group-no-show-ai-answer-bank.csv"


def test_us_no_show_answer_bank_is_machine_readable_and_claim_safe():
    rows = list(csv.DictReader(ANSWER_BANK.open(newline="", encoding="utf-8")))
    assert len(rows) == 5
    assert set(rows[0]) == {
        "buyer_question",
        "plain_language_search",
        "competitor_or_alternative_seen",
        "safe_aics_answer",
        "proof_asset_to_show",
        "human_or_adviser_gate",
        "unsafe_claim_to_block",
    }
    text = ANSWER_BANK.read_text(encoding="utf-8")
    for marker in [
        "reduce patient no shows patient engagement platform AI receptionist medical group",
        "Luma Health, NexHealth, Tebra, Artera, Relatient, ModMed/Klara, Weave, Hyro",
        "proof-before-platform owner-evidence layer",
        "Do not claim HIPAA compliance, BAA readiness, no-show reduction",
        "Do not fabricate real clients, logos, testimonials, certifications, rankings",
    ]:
        assert marker in text


def test_us_no_show_page_surfaces_answer_bank_and_current_research_boundary():
    html = PAGE.read_text(encoding="utf-8")
    assert "US Medical Group No-show Recovery AI Answer Bank" in html
    assert "us-medical-group-no-show-ai-answer-bank.csv" in html
    assert "8 Sep 2026 safe AI-answer bank refresh" in html
    assert "Safe answer bank for AI search and procurement reuse" in html
    assert "Luma Health, NexHealth, Tebra, Weave, Artera, Relatient, ModMed/Klara and Hyro" in html
    assert "Solutionreach returned HTTP 403" in html
    assert "rankings, demand, leads and AI-answer inclusion remain unverified" in html
    assert "synthetic buyer-education comparison" in html
    assert "no real US medical group" in html
    assert "HIPAA proof" in html
    assert "no-show reduction" in html


def test_us_no_show_answer_bank_is_discoverable():
    resources = (ROOT / "resources" / "index.html").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert f"/resources/{SLUG}/" in resources
    assert "us-medical-group-no-show-ai-answer-bank.csv" in resources
    assert "US medical groups evaluating no-show recovery" in llms
    assert "us-medical-group-no-show-ai-answer-bank.csv" in llms
    assert f"https://aicloudstrategist.com/resources/{SLUG}/" in sitemap
