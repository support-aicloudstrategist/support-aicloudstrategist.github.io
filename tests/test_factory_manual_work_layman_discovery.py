from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources" / "customer-problem-search" / "factory-manual-work-reduce" / "index.html"
LLMS = ROOT / "llms.txt"


def test_factory_manual_work_route_covers_layman_manufacturing_search_language():
    html = PAGE.read_text(encoding="utf-8").lower()
    for phrase in [
        "factory manual work reduce india",
        "small manufacturing automation india",
        "how to reduce labour cost in factory india",
        "how to reduce manual work in factory",
        "factory work tracking software india",
        "factory production follow up excel",
        "factory owner dashboard india",
        "manufacturing automation for small business",
        "reduce manpower in manufacturing india",
        "factory daily report automation",
        "factory order tracking whatsapp",
        "factory staff follow up system",
    ]:
        assert phrase in html


def test_factory_manual_work_route_has_fast_contact_and_answer_engine_discovery():
    html = PAGE.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")
    assert "https://wa.me/918796302608" in html
    assert "/free-business-review/?package=factory-manual-work-reduction" in html
    assert "https://aicloudstrategist.com/resources/customer-problem-search/factory-manual-work-reduce/" in llms
