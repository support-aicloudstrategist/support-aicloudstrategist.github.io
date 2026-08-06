import html
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "services" / "cloud-security" / "index.html"
GENERATOR = ROOT / "scripts" / "generate-seo-expansion.py"


def text_content(source):
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(source)).strip()


class AiSecurityFlagshipContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = PAGE.read_text(encoding="utf-8")
        cls.text = text_content(cls.source)

    def test_metadata_and_schema_name_the_flagship_truthfully(self):
        self.assertIn(
            "<title>AI Security, Compliance &amp; Sovereign Platform | AICloudStrategist</title>",
            self.source,
        )
        self.assertIn(
            '<link rel="canonical" href="https://aicloudstrategist.com/services/cloud-security/">',
            self.source,
        )
        self.assertRegex(
            self.source,
            r'<meta name="description" content="[^"]*[Ee]nterprise AI[^"]*security[^"]*compliance[^"]*sovereign[^"]*">',
        )
        block = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            self.source,
            flags=re.S,
        )
        if block is None:
            self.fail("Missing JSON-LD schema")
        graph = json.loads(block.group(1))["@graph"]
        service = next(item for item in graph if item.get("@type") == "Service")
        self.assertEqual(service["name"], "AI Security, Compliance & Sovereign Platform")
        self.assertIn("AI security", service["serviceType"])
        for phrase in ("primary seo target", "money page", "free growth review", "without enterprise bureaucracy"):
            self.assertNotIn(phrase, self.text.lower())

    def test_legacy_generator_cannot_overwrite_the_flagship(self):
        generator = GENERATOR.read_text(encoding="utf-8")
        self.assertIn('HANDCRAFTED_FLAGSHIP_SLUGS = {"ai-automation", "ai-mlops", "cloud-finops", "cloud-security"}', generator)
        self.assertIn('if s["slug"] in HANDCRAFTED_FLAGSHIP_SLUGS:', generator)

    def test_customer_questions_follow_one_decision_journey(self):
        expected = [
            "security-boundary",
            "service-scope",
            "how-it-works",
            "deliverables",
            "fit",
            "why-aics",
            "enterprise-diligence",
            "connected-capabilities",
            "final-cta",
        ]
        positions = []
        for section_id in expected:
            marker = f'id="{section_id}"'
            self.assertEqual(self.source.count(marker), 1)
            positions.append(self.source.index(marker))
        self.assertEqual(positions, sorted(positions))
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", self.source, flags=re.I | re.S)
        self.assertEqual(len(h1s), 1)
        self.assertEqual(
            text_content(h1s[0]),
            "Secure enterprise AI without losing control of data, decisions or deployment.",
        )

    def test_method_and_representative_outputs_are_explicit(self):
        steps = re.findall(
            r'data-security-step="(\d+)"[^>]*>.*?<h3>(.*?)</h3>',
            self.source,
            flags=re.I | re.S,
        )
        self.assertEqual([number for number, _ in steps], [str(i) for i in range(1, 7)])
        self.assertEqual(
            [text_content(label) for _, label in steps],
            ["Understand", "Map", "Assess", "Design", "Verify", "Decide"],
        )
        outputs = re.findall(r'data-representative-output="([^"]+)"', self.source)
        self.assertEqual(
            outputs,
            [
                "Security and Sovereignty Decision Brief",
                "System and Trust Boundary Map",
                "AI and Cloud Risk Register",
                "Identity and Tool Permission Matrix",
                "Data and Residency Record",
                "Control and Evidence Map",
                "Remediation Decision Plan",
                "Release and Operating Conditions",
            ],
        )
        deliverables = self.source[self.source.index('id="deliverables"'):self.source.index('id="fit"')]
        copy = text_content(deliverables).lower()
        self.assertIn("representative outputs", copy)
        self.assertIn("not presented as previous client work", copy)

    def test_scope_trust_and_authority_boundaries_are_clear(self):
        lowered = self.text.lower()
        for phrase in [
            "ai and agent security",
            "cloud and platform controls",
            "compliance evidence",
            "sovereign platform decisions",
            "does not provide legal advice",
            "client approves production change",
            "least privilege",
            "vendor-neutral",
            "can stand alone",
        ]:
            self.assertIn(phrase, lowered)
        for forbidden in [
            "we guarantee compliance",
            "we eliminate risk",
            "certified compliant",
            "industry-leading",
            "world-leading",
            "trusted by thousands",
        ]:
            self.assertNotIn(forbidden, lowered)

    def test_conversion_and_connected_capabilities_preserve_context(self):
        cta = "/contact.html?service=ai-security-sovereignty"
        self.assertGreaterEqual(self.source.count(f'href="{cta}"'), 2)
        self.assertNotIn("/free-business-review/", self.source)
        contact = (ROOT / "contact.html").read_text(encoding="utf-8")
        self.assertIn('value="ai-security-sovereignty"', contact)
        for route in [
            "/services/ai-mlops/",
            "/services/ai-automation/",
            "/services/cloud-finops/",
            "/services/devops-observability/",
        ]:
            self.assertIn(f'href="{route}"', self.source)
            self.assertTrue((ROOT / route.strip("/") / "index.html").exists())

    def test_approved_editorial_refinements_improve_flow_without_scope_drift(self):
        opening = (
            "AICloudStrategist helps leaders decide what AI systems may access, what actions they may take and where they may run. "
            "We turn those decisions into controls and evidence the organisation can use."
        )
        self.assertIn(f'<p class="lead">{opening}</p>', self.source)
        self.assertNotIn("operate across cloud and jurisdictional boundaries", self.source)

        sovereignty = (
            "Define where data and models may run, which providers and jurisdictions are acceptable, who controls encryption keys and operations, "
            "and how the organisation can change or exit the platform."
        )
        self.assertIn(f"<p>{sovereignty}</p>", self.source)

        method = "Each stage clarifies what the system may do, who owns the decision and what evidence is still required."
        self.assertIn(method, self.source)
        self.assertNotIn("Each stage produces a clearer boundary", self.source)

        fit_start = self.source.index('id="fit"')
        fit_end = self.source.index('id="why-aics"')
        fit = self.source[fit_start:fit_end]
        self.assertIn(
            "The work typically brings together the CIO, CISO, CTO or Head of AI with architecture, platform, data, compliance, legal and procurement teams.",
            fit,
        )
        self.assertNotIn("The client retains final risk", fit)
        why = self.source[fit_end:self.source.index('id="enterprise-diligence"')]
        merged = (
            "Recommendations connect to available evidence, explicit assumptions and named gaps. "
            "Credentials and client evidence are used only when verified and approved."
        )
        self.assertIn(f"<p>{merged}</p>", why)
        self.assertNotIn("<h3>Honest claims</h3>", why)
        self.assertEqual(why.count("<article"), 5)

        diligence = self.source[self.source.index('id="enterprise-diligence"'):self.source.index('id="connected-capabilities"')]
        self.assertIn("The client approves production change, accepts residual risk", diligence)

        connected = self.source[self.source.index('id="connected-capabilities"'):self.source.index('id="final-cta"')]
        self.assertIn("can stand alone", text_content(connected).lower())
        self.assertIn("connect only when the system and decision require them", text_content(connected).lower())
        self.assertNotIn("Start with the security decision", connected)


if __name__ == "__main__":
    unittest.main()
