from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]

def extract(pattern, source):
    m = re.search(pattern, source, re.I | re.S)
    return m.group(1) if m else None

# Refresh premium shell baseline for currently indexable pages with navigation mount.
pages = {}
for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    source = path.read_text(errors="replace")
    if "data-aics-navigation-mount" not in source:
        continue
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', source, re.I):
        continue
    rel = path.relative_to(ROOT).as_posix()
    main = re.search(r"<main\b[^>]*>.*?</main\s*>", source, re.I | re.S)
    forms = re.findall(r"<form\b[^>]*>.*?</form\s*>", source, re.I | re.S)
    pages[rel] = {
        "canonical": extract(r"<link\b(?=[^>]*\brel=[\"'][^\"']*canonical[^\"']*[\"'])(?=[^>]*\bhref=[\"']([^\"']+)[\"'])[^>]*>", source),
        "forms": len(forms),
        "forms_sha256": hashlib.sha256("".join(forms).encode()).hexdigest(),
        "main_sha256": hashlib.sha256(main.group(0).encode()).hexdigest() if main else None,
        "title": extract(r"<title\b[^>]*>(.*?)</title\s*>", source),
    }

baseline = {"pages": pages}
(ROOT / "tests" / "fixtures" / "premium-shell-baseline.json").write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")

# Update Cloud FinOps release provenance for discovery files changed by curated sitemap/llms/resource-hub edits.
manifest_path = ROOT / "release" / "cloud-finops-phase4-release.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
for rel in ["sitemap.xml", "llms.txt", "resources/index.html", "scripts/build_sitemap.py"]:
    manifest["sha256"][rel] = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("refreshed premium shell baseline pages", len(pages), "and release hashes")
