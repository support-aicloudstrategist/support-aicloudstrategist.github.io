import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTACT = ROOT / "contact.html"
ENDPOINT = ROOT / "functions" / "api" / "contact.ts"


class ContactReliabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTACT.read_text(encoding="utf-8")
        cls.endpoint = ENDPOINT.read_text(encoding="utf-8")

    def test_contact_form_posts_to_the_durable_endpoint(self):
        form = re.search(r'<form\b[^>]*id="contactForm"[^>]*>', self.source, flags=re.I)
        if form is None:
            self.fail("Contact form is missing")
        self.assertIn('action="/api/contact"', form.group(0))
        self.assertIn('method="POST"', form.group(0))
        self.assertIn("fetch('/api/contact'", self.source)
        self.assertIn("method: 'POST'", self.source)
        self.assertIn("'Content-Type': 'application/json'", self.source)

    def test_success_is_gated_on_confirmed_delivery(self):
        handler = re.search(
            r"contactForm\.addEventListener\('submit'.*?\n\s*// reveal \+ timeline draw",
            self.source,
            flags=re.S,
        )
        if handler is None:
            self.fail("Contact submit handler is missing")
        script = handler.group(0)
        self.assertIn("if (!response.ok || !result.ok)", script)
        self.assertIn("contactSuccess.style.display = 'block'", script)
        self.assertIn("contactError.style.display = 'block'", script)
        self.assertNotIn("window.location.href = 'mailto:", script)

    def test_server_endpoint_validates_and_returns_a_contact_reference(self):
        self.assertIn('Missing required field(s)', self.endpoint)
        self.assertIn('contact_id: contactId', self.endpoint)
        self.assertIn('JSON.stringify({ ok: true, contact_id: contactId, notification_sent: false, notification_mode: "manual-review" })', self.endpoint)

    def test_contact_form_has_clear_low_friction_requirements(self):
        required_fields = re.findall(r'<(?:input|select)\b[^>]*\brequired\b[^>]*>', self.source, flags=re.I)
        required_names = {
            match.group(1)
            for field in required_fields
            if (match := re.search(r'\bname="([^"]+)"', field, flags=re.I))
        }
        self.assertEqual(required_names, {"name", "email", "company", "service", "stage"})
        self.assertRegex(
            self.source,
            r'<select\b[^>]*name="stage"[^>]*required[^>]*>\s*<option value="" selected disabled>',
        )
        self.assertIn('Initiative brief <span aria-hidden="true">(optional)</span>', self.source)
        self.assertIn('This usually takes about two minutes.', self.source)

    def test_privacy_and_safe_disclosure_guidance_is_adjacent_to_submit(self):
        privacy_position = self.source.index('class="privacy-note"')
        submit_position = self.source.index('id="contactSubmitButton"')
        self.assertLess(privacy_position, submit_position)
        self.assertIn('Do not include passwords, credentials, personal data or sensitive production information.', self.source)
        self.assertIn('href="/privacy.html"', self.source[privacy_position:submit_position])

    def test_mobile_prioritizes_the_form_and_response_expectation_is_visible(self):
        self.assertIn('.contact-layout .form-wrap{order:-1}', self.source)
        self.assertIn('reply within one business day', self.source.lower())
        self.assertNotIn('id="response-time-sla"', self.source)
        self.assertNotIn('class="channels"', self.source)

    def test_click_to_call_and_contact_schema_use_dialable_phone_number(self):
        self.assertNotIn('tel:+918****0898', self.source)
        self.assertNotIn('telephone":"+918****0898', self.source)
        self.assertEqual(self.source.count('tel:+918065480898'), 2)
        self.assertEqual(self.source.count('telephone":"+918065480898'), 2)


if __name__ == "__main__":
    unittest.main()
