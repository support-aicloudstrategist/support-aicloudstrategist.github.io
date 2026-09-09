import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING_PAGES = [ROOT / "pricing.html", ROOT / "pricing" / "index.html"]


class PricingFixedScopeCountConsistencyTests(unittest.TestCase):
    def test_fixed_scope_offer_count_matches_schema_and_buyer_copy(self):
        for pricing_page in PRICING_PAGES:
            with self.subTest(page=pricing_page.relative_to(ROOT)):
                html = pricing_page.read_text(encoding="utf-8")
                itemlist_json = next(
                    match.group(1)
                    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html)
                    if 'pricing#fixed-scope-diagnostics' in match.group(1)
                )
                itemlist = json.loads(itemlist_json)
                offers = itemlist["itemListElement"]

                self.assertEqual(40, itemlist["numberOfItems"])
                self.assertEqual(40, len(offers))
                self.assertEqual("40 fixed-scope AICS diagnostic offers", itemlist["name"])
                self.assertIn(
                    "Forty structured fixed-scope diagnostic offers buyers can understand before a custom build.",
                    html,
                )
                self.assertNotIn("39 fixed-scope AICS diagnostic offers", html)
                self.assertNotIn("Forty-one structured fixed-scope diagnostic offers", html)


if __name__ == "__main__":
    unittest.main()
