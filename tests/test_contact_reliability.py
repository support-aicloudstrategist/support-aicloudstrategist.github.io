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
        self.assertIn('JSON.stringify({ ok: true, contact_id: contactId })', self.endpoint)


if __name__ == "__main__":
    unittest.main()
