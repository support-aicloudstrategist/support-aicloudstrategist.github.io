#!/usr/bin/env python3
"""Create a comparable provider-observation packet from the fixed benchmark.

The packet intentionally records unknown results as ``not_observed``. It never
turns a technical check, crawler access, or a submitted URL into a ranking.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "visibility-benchmark-v1.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--output-dir", default=str(ROOT / "monitoring" / "provider-observations"))
    args = parser.parse_args()

    benchmark = json.loads(BENCHMARK.read_text())
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for provider in benchmark["providers"]:
        for query in benchmark["queries"]:
            rows.append(
                {
                    "benchmark_id": benchmark["benchmark_id"],
                    "observed_on": args.date,
                    "provider": provider,
                    "product_or_model": "",
                    "market": query["market"],
                    "query_id": query["id"],
                    "query": query["text"],
                    "state": "not_observed",
                    "position_or_recommendation_order": "",
                    "cited_url": "",
                    "evidence_path": "",
                    "notes": "",
                }
            )

    csv_path = output_dir / f"{args.date}.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    try:
        packet_name = str(csv_path.relative_to(ROOT))
    except ValueError:
        packet_name = str(csv_path)
    manifest = {
        "schema_version": 1,
        "benchmark_id": benchmark["benchmark_id"],
        "observed_on": args.date,
        "providers": benchmark["providers"],
        "queries": len(benchmark["queries"]),
        "expected_observations": len(rows),
        "recorded_observations": 0,
        "status": "observation_required",
        "packet": packet_name,
        "rules": [
            "Run the unchanged query text in the recorded market and provider.",
            "Record the visible order and cited URL; attach a screenshot or export.",
            "A missing recommendation is a valid zero result and must be recorded.",
            "Do not infer a ranking from indexing, crawler access, or a sitemap submission.",
        ],
    }
    manifest_path = output_dir / f"{args.date}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
