#!/usr/bin/env python3
"""Weekly public technical checks for the focused organic acquisition path."""
from pathlib import Path
import json, sys, urllib.request, urllib.error
from xml.etree import ElementTree as ET

BASE = "https://aicloudstrategist.com"
ROOT = Path(__file__).resolve().parents[1]
ROUTES = [line.strip() for line in (ROOT / "seo/indexable-routes.txt").read_text().splitlines() if line.strip()]

def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent":"AICloudStrategistTechnicalMonitor/1.0","Accept":"text/html,application/json"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.status, dict(response.headers), response.read().decode("utf-8", "replace")

results=[]
for route in ROUTES:
    try:
        status, headers, body = get(route)
        robots = headers.get("X-Robots-Tag", "").lower()
        results.append({"route":route,"status":status,"indexable_header":"noindex" not in robots,"body_bytes":len(body.encode())})
    except Exception as exc:
        results.append({"route":route,"status":0,"indexable_header":False,"error":type(exc).__name__})

status, _, sitemap = get("/sitemap.xml")
root = ET.fromstring(sitemap)
ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
listed={node.text.replace(BASE,"") for node in root.findall("s:url/s:loc",ns)}
expected=set(ROUTES)
failures=[r for r in results if r["status"] != 200 or not r["indexable_header"]]
if listed != expected:
    failures.append({"sitemap_missing":sorted(expected-listed),"sitemap_extra":sorted(listed-expected)})

report={"ok":not failures,"base":BASE,"routes_checked":len(results),"results":results,"failures":failures}
out=ROOT / "monitoring" / "latest-technical.json"; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"ok":report["ok"],"routes_checked":len(results),"failure_count":len(failures)}))
sys.exit(0 if report["ok"] else 1)
