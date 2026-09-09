import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLICATION = ROOT / "publications" / "2026-09-09" / "saas-security-questionnaire-evidence-pack.html"
URL = "https://aicloudstrategist.com/publications/2026-09-09/saas-security-questionnaire-evidence-pack.html"


def json_ld_documents(html: str):
    return [json.loads(raw) for raw in re.findall(r"<script\s+type=['\"]application/ld\+json['\"]>(.*?)</script>", html, re.I | re.S)]


def graph_nodes(docs):
    nodes = []
    for doc in docs:
        nodes.extend(doc.get("@graph", [doc]))
    return nodes


def test_latest_saas_security_publication_has_article_and_faq_jsonld():
    html = PUBLICATION.read_text(encoding="utf-8")
    nodes = graph_nodes(json_ld_documents(html))
    article = next(node for node in nodes if node.get("@type") == "Article")
    faq = next(node for node in nodes if node.get("@type") == "FAQPage")

    assert article["mainEntityOfPage"] == URL
    assert article["headline"] == "SaaS Security Questionnaire Evidence Pack: 7 Red Flags Before AI Answers"
    assert article["isAccessibleForFree"] is True
    assert "AI answer evidence" in article["about"]

    questions = [item["name"] for item in faq["mainEntity"]]
    assert "Can AI answer our SaaS security questionnaire?" in questions
    assert "When should this become a paid diagnostic?" in questions
    assert "invent" in json.dumps(faq).lower()
    assert "guaranteed compliance" not in json.dumps(faq).lower()
