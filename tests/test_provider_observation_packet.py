import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_packet_covers_every_provider_query_pair_without_inventing_results(tmp_path):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_provider_observation_packet.py"),
            "--date",
            "2026-10-06",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
    )
    benchmark = json.loads((ROOT / "visibility-benchmark-v1.json").read_text())
    rows = list(csv.DictReader((tmp_path / "2026-10-06.csv").open()))
    assert len(rows) == len(benchmark["providers"]) * len(benchmark["queries"])
    assert {row["state"] for row in rows} == {"not_observed"}
    assert all(not row["position_or_recommendation_order"] for row in rows)
    manifest = json.loads((tmp_path / "2026-10-06.json").read_text())
    assert manifest["expected_observations"] == len(rows)
    assert manifest["recorded_observations"] == 0


def test_sitemap_builder_cannot_reintroduce_the_legacy_catalogue(tmp_path):
    routes = [
        line.strip()
        for line in (ROOT / "seo" / "indexable-routes.txt").read_text().splitlines()
        if line.strip()
    ]
    source = (ROOT / "scripts" / "build_sitemap.py").read_text()
    assert "for page in html_pages()" not in source
    assert "EXTERNAL_SUPPORT_URLS" not in source
    assert len(routes) == 26
