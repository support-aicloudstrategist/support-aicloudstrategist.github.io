from pathlib import Path
from urllib.parse import urlsplit
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HOST = "aicloudstrategist.com"


class LlmsLocalLinkIntegrityTests(unittest.TestCase):
    def test_every_canonical_llms_url_maps_to_a_published_local_asset(self):
        source = (ROOT / "llms.txt").read_text(encoding="utf-8")
        urls = sorted(
            set(re.findall(r"https://aicloudstrategist\.com/[^\s)>]+", source))
        )
        self.assertGreater(len(urls), 0)

        missing = []
        for raw_url in urls:
            url = raw_url.rstrip(".,;:")
            parsed = urlsplit(url)
            self.assertEqual(parsed.netloc, CANONICAL_HOST, url)
            route = parsed.path or "/"
            candidates = []
            if route.endswith("/"):
                candidates.append(ROOT / route.lstrip("/") / "index.html")
            else:
                candidates.extend(
                    [
                        ROOT / route.lstrip("/"),
                        ROOT / route.lstrip("/") / "index.html",
                    ]
                )
            if not any(candidate.is_file() for candidate in candidates):
                missing.append(url)

        self.assertEqual([], missing, f"llms.txt contains unpublished local routes: {missing}")


if __name__ == "__main__":
    unittest.main()
