import html
import json
import re
import unittest
from pathlib import Path

import tinycss2


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "devops-observability" / "index.html"
STYLES = ROOT / "css" / "ai-platform-reliability-operations.css"
SCRIPT = ROOT / "js" / "ai-platform-reliability-operations.js"
COPY_FIXTURE = ROOT / "tests" / "fixtures" / "ai-platform-reliability-operations-copy.json"
GENERATOR = ROOT / "scripts" / "generate-seo-expansion.py"
PEER_PAGE = ROOT / "services" / "cloud-security" / "index.html"


def text_content(source):
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(source)).strip()


def between(source, start, end):
    start_index = source.index(start)
    return source[start_index:source.index(end, start_index)]


class AiPlatformReliabilityOperationsPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PAGE.read_text(encoding="utf-8")
        cls.text = text_content(cls.source)
        cls.fixture = json.loads(COPY_FIXTURE.read_text(encoding="utf-8"))

    def test_metadata_schema_and_page_identity_match_the_frozen_service(self):
        self.assertIn(
            "<title>AI Platform Reliability &amp; Operations | AICloudStrategist</title>",
            self.source,
        )
        self.assertIn(
            '<link rel="canonical" href="https://aicloudstrategist.com/services/devops-observability/">',
            self.source,
        )
        self.assertIn('<body class="ai-reliability-page">', self.source)
        block = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            self.source,
            flags=re.S,
        )
        self.assertIsNotNone(block, "Missing JSON-LD")
        assert block is not None
        graph = json.loads(block.group(1))["@graph"]
        service = next(item for item in graph if item.get("@type") == "Service")
        self.assertEqual(service["name"], "AI Platform Reliability & Operations")
        self.assertIn("AI service reliability", service["serviceType"])
        for forbidden in [
            "DevOps & Observability Services",
            "Primary SEO target",
            "money page",
            "Get free growth review",
        ]:
            self.assertNotIn(forbidden, self.text)

    def test_page_uses_only_dedicated_versioned_runtime_assets(self):
        self.assertIn(
            '<link rel="stylesheet" href="/css/ai-platform-reliability-operations.css?v=20260806-1">',
            self.source,
        )
        self.assertIn(
            '<script defer src="/js/ai-platform-reliability-operations.js?v=20260806-1"></script>',
            self.source,
        )
        self.assertNotRegex(self.source, r"<style\b")
        self.assertTrue(STYLES.exists(), "Dedicated page stylesheet is missing")
        self.assertTrue(SCRIPT.exists(), "Dedicated artifact-browser script is missing")

    def test_shared_navigation_footer_and_shell_contracts_are_unchanged(self):
        self.assertIn('class="air-skip-link" href="#main-content"', self.source)
        self.assertEqual(len(re.findall(r"<main\b", self.source, flags=re.I)), 1)
        self.assertIn('<main id="main-content">', self.source)
        self.assertIn('data-aics-navigation-mount', self.source)
        self.assertEqual(self.source.count('data-aics-global-footer'), 1)
        self.assertIn('href="/css/site-navigation.css?v=premium-shell-20260727"', self.source)
        self.assertIn('src="/js/site-navigation.js?v=premium-shell-20260727"', self.source)
        target_footer = re.search(r'(<footer class="aics-global-footer".*?</footer>)', self.source, flags=re.S)
        peer_footer = re.search(
            r'(<footer class="aics-global-footer".*?</footer>)',
            PEER_PAGE.read_text(encoding="utf-8"),
            flags=re.S,
        )
        self.assertIsNotNone(target_footer)
        self.assertIsNotNone(peer_footer)
        assert target_footer is not None
        assert peer_footer is not None
        self.assertEqual(target_footer.group(1), peer_footer.group(1))

    def test_exactly_eleven_sections_follow_the_frozen_order(self):
        expected = [
            "executive-orientation",
            "production-operating-gap",
            "aics-operating-model",
            "continuity-mechanism",
            "responsibility-boundary",
            "representative-artifacts",
            "reliability-baseline",
            "sustained-operation",
            "enterprise-diligence",
            "portfolio-handoffs",
            "final-conversion",
        ]
        actual = re.findall(
            r'<section\b[^>]*class="[^"]*air-section[^"]*"[^>]*id="([^"]+)"',
            self.source,
        )
        self.assertEqual(actual, expected)
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", self.source, flags=re.I | re.S)
        self.assertEqual([text_content(item) for item in h1s], [
            "Keep live AI services observable, recoverable and accountable"
        ])
        h2s = [text_content(item) for item in re.findall(
            r"<h2\b[^>]*>(.*?)</h2>",
            between(self.source, '<main id="main-content">', '</main>'),
            flags=re.I | re.S,
        )]
        self.assertEqual(h2s, [
            "Infrastructure health does not prove that the AI service is working",
            "Operate the service, not only its components",
            "Turn production signals into controlled action",
            "Clear responsibility before an incident",
            "See what the work produces",
            "Start with one service and one operating decision",
            "Move forward only when the evidence supports it",
            "Define the delivery conditions before work begins",
            "Route each decision to the right authority",
            "Start with one named AI service",
        ])

    def test_every_frozen_copy_block_is_present_in_order(self):
        ids = [
            "executive-orientation",
            "production-operating-gap",
            "aics-operating-model",
            "continuity-mechanism",
            "responsibility-boundary",
            "representative-artifacts",
            "reliability-baseline",
            "sustained-operation",
            "enterprise-diligence",
            "portfolio-handoffs",
            "final-conversion",
        ]
        for index, frozen in enumerate(self.fixture["sections"]):
            start = f'id="{ids[index]}"'
            end = f'id="{ids[index + 1]}"' if index + 1 < len(ids) else "</main>"
            section_text = text_content(between(self.source, start, end))
            position = -1
            for exact in frozen["content"]:
                found = section_text.find(exact, position + 1)
                self.assertGreaterEqual(
                    found,
                    0,
                    f"Section {index + 1} missing or reordered frozen copy: {exact}",
                )
                position = found

    def test_diagrams_matrices_artifacts_and_progressions_match_the_approved_counts(self):
        self.assertEqual(self.source.count("data-spine-layer="), 7)
        self.assertEqual(self.source.count("data-continuity-stage="), 5)
        self.assertEqual(self.source.count("data-responsibility-row="), 7)
        self.assertEqual(self.source.count("data-representative-artifact="), 4)
        self.assertEqual(self.source.count("data-baseline-step="), 5)
        self.assertEqual(self.source.count("data-engagement-stage="), 3)
        self.assertEqual(self.source.count("data-diligence-item="), 6)
        self.assertEqual(self.source.count("data-handoff-route="), 4)
        for component in [
            "air-category-model",
            "air-failure-chain",
            "air-production-spine",
            "air-continuity-loop",
            "air-responsibility-matrix",
            "air-artifact-browser",
            "air-baseline-chain",
            "air-engagement-progression",
            "air-diligence-index",
            "air-handoff-map",
            "air-decision-summary",
        ]:
            self.assertIn(component, self.source)

    def test_representative_evidence_is_explicit_and_not_presented_as_customer_proof(self):
        evidence = between(self.source, 'id="representative-artifacts"', 'id="reliability-baseline"')
        self.assertEqual(evidence.count("data-representative-artifact="), 4)
        for phrase in [
            "These representative artifacts show the expected structure",
            "They are not customer results, production records or evidence of measured client outcomes.",
            "Representative artifact",
            "Assumptions",
            "Evidence provenance",
            "Owner",
            "Decision use",
        ]:
            self.assertIn(phrase, evidence)
        for forbidden in ["customer result", "live uptime", "trusted by", "industry-leading"]:
            if forbidden == "customer result":
                continue
            self.assertNotIn(forbidden, evidence.lower())

    def test_conversion_context_and_related_routes_are_preserved(self):
        cta = (
            "/contact.html?service=managed-ai-operations&amp;"
            "engagement=ai-service-reliability-baseline&amp;"
            "utm_source=ai-platform-reliability-operations&amp;"
            "utm_medium=flagship-service-page&amp;"
            "utm_campaign=ai-service-reliability-baseline"
        )
        self.assertEqual(self.source.count(f'href="{cta}"'), 4)
        self.assertIn('href="#representative-artifacts"', self.source)
        self.assertNotIn("/free-business-review/", self.source)
        contact = (ROOT / "contact.html").read_text(encoding="utf-8")
        self.assertIn('value="managed-ai-operations"', contact)
        self.assertIn('name="engagement" type="hidden"', contact)
        self.assertIn('params.get("engagement")', contact)
        self.assertIn("'ai-service-reliability-baseline'", contact)
        self.assertIn('engagement: payload.engagement', contact)
        self.assertIn('`Engagement: ${payload.engagement}`', contact)
        for field in ["utm_source", "utm_medium", "utm_campaign"]:
            self.assertIn(f'name="{field}"', contact)
            self.assertIn(f'{field}: payload.{field}', contact)
        for route in [
            "/services/ai-automation/",
            "/services/ai-mlops/",
            "/services/cloud-finops/",
            "/services/cloud-security/",
        ]:
            self.assertIn(f'href="{route}"', self.source)
            self.assertTrue((ROOT / route.strip("/") / "index.html").exists())

    def test_mobile_authority_labels_and_final_source_order_are_explicit(self):
        responsibility = between(
            self.source,
            '<div class="air-responsibility-matrix">',
            '</table></div>',
        )
        self.assertIn('<table aria-label="Responsibility and escalation matrix">', responsibility)
        for label in ["AICS-owned", "Shared", "Client-retained", "Specialist trigger"]:
            self.assertIn(f'<th scope="col">{label}</th>', responsibility)
            self.assertEqual(responsibility.count(f'data-label="{label}"'), 7)
        self.assertEqual(responsibility.count('data-responsibility-row="'), 7)
        self.assertIn("content: attr(data-label)", STYLES.read_text(encoding="utf-8"))

        final = between(
            self.source,
            '<section class="air-section air-section--final" id="final-conversion"',
            '</section>',
        )
        order = [
            "Start with one named AI service",
            "The AI Service Reliability Baseline gives the accountable technology owner",
            "Selected engagement",
            "The initial scoping conversation confirms:",
            "After the inquiry, AICS confirms whether the service fits the Baseline",
            "Discuss an AI Service Reliability Baseline",
            "The Baseline is the first purchase.",
        ]
        positions = [final.index(item) for item in order]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("Preselect AI Platform Reliability", final)

    def test_authority_access_and_service_boundaries_remain_explicit(self):
        lowered = self.text.lower()
        for phrase in [
            "does not imply universal 24/7 support",
            "independent evaluation of output correctness",
            "business-risk acceptance",
            "release approval",
            "read-only by default",
            "does not change production",
            "not an incident-response retainer",
            "does not commit the customer to implementation or managed operations",
        ]:
            self.assertIn(phrase, lowered)
        for forbidden in [
            "guaranteed uptime",
            "we guarantee",
            "unlimited incident response",
            "zero downtime",
            "fully autonomous remediation",
        ]:
            self.assertNotIn(forbidden, lowered)

    def test_css_is_scoped_responsive_static_and_accessible(self):
        css = STYLES.read_text(encoding="utf-8")
        self.assertGreater(len(css), 20000)
        for selector in [
            "body.ai-reliability-page",
            ".ai-reliability-page .air-hero-grid",
            ".ai-reliability-page .air-production-spine",
            ".ai-reliability-page .air-continuity-loop",
            ".ai-reliability-page .air-responsibility-matrix",
            ".ai-reliability-page .air-artifact-browser",
            ".ai-reliability-page .air-baseline-grid",
            ".ai-reliability-page .air-engagement-progression",
            ".ai-reliability-page .air-handoff-map",
            ".ai-reliability-page .air-final-decision",
        ]:
            self.assertIn(selector, css)
        for contract in [
            "@media (max-width: 1199px)",
            "@media (max-width: 959px)",
            "@media (max-width: 767px)",
            "@media (max-width: 430px)",
            "@media (prefers-reduced-motion: reduce)",
            "@media (prefers-contrast: more)",
            "@media print",
            ":focus-visible",
        ]:
            self.assertIn(contract, css)
        self.assertNotIn("@keyframes", css)
        self.assertNotRegex(css, r"\banimation(?:-name)?\s*:")
        self.assertNotRegex(css, r"url\(\s*['\"]?https?://")

        def selectors(rules):
            for rule in rules:
                if rule.type == "qualified-rule":
                    yield tinycss2.serialize(rule.prelude).strip()
                elif rule.type == "at-rule" and rule.content is not None:
                    nested = tinycss2.parse_rule_list(
                        rule.content,
                        skip_comments=True,
                        skip_whitespace=True,
                    )
                    yield from selectors(nested)

        rules = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
        for selector_group in selectors(rules):
            for selector in selector_group.split(","):
                selector = selector.strip()
                self.assertIn(
                    ".ai-reliability-page",
                    selector,
                    f"Unscoped selector could affect another page: {selector}",
                )

    def test_artifact_browser_progressively_enhances_without_hiding_mobile_content(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for contract in [
            'matchMedia("(max-width: 767px)")',
            'role="tab"',
            'aria-selected',
            'ArrowRight',
            'ArrowLeft',
            'Home',
            'End',
        ]:
            self.assertIn(contract, script)
        self.assertNotIn("innerHTML", script)
        self.assertNotIn("setInterval", script)

    def test_legacy_generator_cannot_overwrite_the_new_flagship(self):
        generator = GENERATOR.read_text(encoding="utf-8")
        match = re.search(r"HANDCRAFTED_FLAGSHIP_SLUGS\s*=\s*\{([^}]+)\}", generator)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertIn('HANDCRAFTED_FLAGSHIP_SLUGS.add("devops-observability")', generator)
        self.assertIn('if s["slug"] in HANDCRAFTED_FLAGSHIP_SLUGS:', generator)


if __name__ == "__main__":
    unittest.main()
