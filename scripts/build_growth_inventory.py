#!/usr/bin/env python3
"""Classify every public HTML route for the content-quality cleanup ledger."""
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
CORE={"index.html","about/index.html","contact/index.html","pricing/index.html","free-business-review/index.html","how-we-work/index.html","case-studies/index.html","case-studies/aicloudstrategist-geo-turnaround/index.html","services/production-ai-readiness/index.html","services/cloud-ai-economics/index.html","resources/index.html"}

def decision(path:str):
    if path in CORE:return "keep","commercial/proof priority"
    if path.endswith('.html') and (ROOT/path[:-5]/'index.html').exists():return "redirect","duplicate extension variant"
    if path.startswith('ai-automation-agency-') or path=='ai-automation-agency/index.html':return "redirect","generic geography offer consolidated"
    if path.startswith('case-studies/simulated-'):return "noindex","synthetic method example, not search acquisition"
    if path.startswith('webinars/'):return "noindex","event not currently scheduled"
    if path.startswith('resources/') or path.startswith('publications/'):return "improve","retain only with original buyer value and evidence"
    if any(path.startswith(p) for p in ('scripts/','tests/','preview/','reports/','seo/','docs/')):return "remove_from_public","internal artifact"
    return "improve","review metadata, originality and commercial role"

rows=[]
for file in sorted(ROOT.rglob('*.html')):
    rel=file.relative_to(ROOT).as_posix()
    if '/.git/' in rel:continue
    action,reason=decision(rel)
    rows.append((rel,action,reason,'Growth operations','2026-10-06'))
out=ROOT/'seo'/'editorial-decisions-2026-10-06.csv';out.parent.mkdir(exist_ok=True)
with out.open('w',newline='',encoding='utf-8') as handle:
    writer=csv.writer(handle,lineterminator='\n');writer.writerow(('source_file','decision','reason','owner','review_date'));writer.writerows(rows)
print(f"Classified {len(rows)} HTML files in {out.relative_to(ROOT)}")
