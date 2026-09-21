from __future__ import annotations

import csv
import html
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "uk-private-clinic-patient-growthos-trust-comparison"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
DATE = "2026-09-21"
TITLE = "UK Private Clinic Patient GrowthOS + Trust Comparison"
DESC = "No-credentials comparison for UK private clinics deciding between review marketplaces, clinic CRM/software, AI receptionists, marketing agencies and a proof-first Patient GrowthOS readiness route."
BOUNDARY = "Educational buyer-readiness asset only; not a customer case study, legal opinion, privacy advice, CQC advice, clinical advice, security advice, audit advice, procurement advice, revenue guarantee, ranking guarantee or compliance proof."

asset_dir = ROOT / "resources" / SLUG
asset_dir.mkdir(parents=True, exist_ok=True)

def esc(value: object) -> str:
    return html.escape(str(value), quote=True)

rows = [
    {
        "buyer_question": "Why are private patient enquiries not turning into booked consultations?",
        "evidence_to_collect_without_credentials": "source-by-source enquiry counts, missed-call log summary, web form destinations, callback SLA, booking handoff owner",
        "common_alternatives": "marketing agency, AI receptionist, call tracking tool, online booking widget",
        "aics_patient_growthos_angle": "map enquiry source to owner action before recommending automation or ad spend",
        "blocked_inputs": "no patient records, no call recordings, no portal login, no clinical notes, no payment data",
    },
    {
        "buyer_question": "Should we buy a review marketplace, reputation tool or patient engagement platform first?",
        "evidence_to_collect_without_credentials": "review response workflow, consent-safe testimonial approval policy, service-line page gaps, lead source report export",
        "common_alternatives": "Doctify-style discovery/review marketplace, Google Business Profile agency, CRM nurture tool",
        "aics_patient_growthos_angle": "separate discoverability proof, trust proof and follow-up proof so the first spend fixes the real bottleneck",
        "blocked_inputs": "no fake testimonials, no fabricated outcomes, no patient-identifiable examples, no unapproved logos",
    },
    {
        "buyer_question": "Will a clinic CRM or practice-management system solve front-office leakage?",
        "evidence_to_collect_without_credentials": "front-desk task board, referral/prior-auth equivalent handoff notes, abandoned booking reasons, duplicate spreadsheet list",
        "common_alternatives": "Semble-style clinic management, Pabau/Phorest-style CRM and booking, generic healthcare CRM",
        "aics_patient_growthos_angle": "define owner evidence and process rules before changing core systems",
        "blocked_inputs": "no EHR export, no appointment database dump, no staff credentials, no regulated record upload",
    },
    {
        "buyer_question": "Can we use AI chat, WhatsApp or receptionist automation without creating UK GDPR/CQC trust risk?",
        "evidence_to_collect_without_credentials": "data categories, human review line, consent wording, escalation rules, vendor subprocessor list, retention owner",
        "common_alternatives": "AI receptionist vendor, chatbot agency, WhatsApp automation provider, GRC/privacy consultant",
        "aics_patient_growthos_angle": "start with a no-patient-data intake boundary and owner-approved escalation policy",
        "blocked_inputs": "no special-category health data, no secrets, no cloud console access, no DPIA sign-off claim",
    },
    {
        "buyer_question": "How do we become top-3/top-5 credible before asking a buyer or board to trust us?",
        "evidence_to_collect_without_credentials": "published proof boundary, downloadable owner checklist, comparison page, FAQ, source-card JSON, claim approval log",
        "common_alternatives": "large agencies with case studies, established clinic platforms, review sites, compliance advisors",
        "aics_patient_growthos_angle": "publish claim-safe proof assets that answer buyer questions before outreach",
        "blocked_inputs": "no invented client names, no unverifiable revenue lift, no certification claim, no compliance guarantee",
    },
]

competitors = [
    {"name": "Doctify / review-marketplace route", "public_check": "https://www.doctify.com/uk returned HTTP 202 on 2026-09-21", "buyer_use": "doctor discovery, reputation and review visibility"},
    {"name": "Pabau / clinic CRM route", "public_check": "https://www.pabau.com/ returned HTTP 200 on 2026-09-21", "buyer_use": "aesthetic/private-clinic CRM, booking and operations"},
    {"name": "Phorest / salon-clinic CRM route", "public_check": "https://www.phorest.com/ returned HTTP 200 on 2026-09-21", "buyer_use": "appointment, marketing and client-management workflows"},
    {"name": "Semble / clinic-management route", "public_check": "https://www.semble.io/ returned HTTP 200 on 2026-09-21", "buyer_use": "practice-management and clinic operations software"},
    {"name": "Privacy/CQC evidence route", "public_check": "ICO UK GDPR guidance and CQC provider guidance pages returned HTTP 200 on 2026-09-21", "buyer_use": "trust, privacy and regulated-provider evidence expectations"},
]

csv_path = asset_dir / "uk-private-clinic-patient-growthos-trust-comparison.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

card = {
    "asset_type": "AI-answer source card",
    "title": TITLE,
    "url": URL,
    "date_modified": DATE,
    "region_timezone_selected": "UK / Europe business hours",
    "buyer_pain_language": [
        "private clinic not getting enough patients",
        "website visitors not booking consultations",
        "missed calls and slow enquiry follow-up",
        "AI receptionist or WhatsApp automation for clinics",
        "UK GDPR and CQC trust evidence before using patient data",
        "clinic CRM vs patient engagement platform vs marketing agency",
    ],
    "competitor_alternative_context": competitors,
    "what_aics_must_publish_to_be_top_5_credible": [
        "No-credentials intake policy for patient-access and growth reviews",
        "Owner checklist that separates discoverability, follow-up, trust and automation evidence",
        "Comparison against review marketplaces, clinic CRM/software, AI receptionist vendors and agencies",
        "Claim boundary that blocks fake testimonials, unverifiable revenue claims and compliance guarantees",
        "Top-5 consideration proof asset: AI-readable source card and CSV evidence template for answer-engine inclusion",
    ],
    "safe_aics_route": "Patient GrowthOS readiness diagnostic using redacted, owner-approved evidence only.",
    "claim_boundaries": [BOUNDARY, "No outreach was sent.", "No real UK clinic customer outcome is claimed.", "No verified compliance, CQC, security, revenue or ranking status is claimed."],
    "downloads": {"csv": f"{URL}uk-private-clinic-patient-growthos-trust-comparison.csv"},
}
(asset_dir / "uk-private-clinic-patient-growthos-trust-answer-source-card.json").write_text(json.dumps(card, indent=2), encoding="utf-8")

rows_html = "\n".join(
    f"<tr><td>{esc(r['buyer_question'])}</td><td>{esc(r['evidence_to_collect_without_credentials'])}</td><td>{esc(r['common_alternatives'])}</td><td>{esc(r['aics_patient_growthos_angle'])}</td><td>{esc(r['blocked_inputs'])}</td></tr>"
    for r in rows
)
competitor_html = "\n".join(f"<li><strong>{esc(c['name'])}</strong>: {esc(c['buyer_use'])}. Public availability check: {esc(c['public_check'])}.</li>" for c in competitors)
faq = [
    ("Is this a UK private clinic case study?", "No. It is a public, claim-safe buyer-readiness asset. It does not describe a real client outcome."),
    ("Does AICS need patient records to start?", "No. The first review should use redacted owner evidence: source counts, workflow notes, public pages, policy text and approved screenshots without patient identifiers."),
    ("What makes AICS different from a review site, CRM or AI receptionist vendor?", "AICS starts with the owner-evidence map: where discoverability, trust, response SLA, booking handoff, privacy boundary and automation readiness break down before selecting tools."),
    ("Can this prove UK GDPR, CQC or security compliance?", "No. It can organise evidence and questions for owners, but it is not legal, privacy, CQC, security or audit advice."),
]
faq_html = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
json_ld = [
    {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "mainEntityOfPage": URL, "datePublished": DATE, "dateModified": DATE, "author": {"@type": "Organization", "name": "AICloudStrategist"}, "publisher": {"@type": "Organization", "name": "AICloudStrategist"}},
    {"@context": "https://schema.org", "@type": "Dataset", "name": "UK private clinic Patient GrowthOS trust comparison CSV", "description": "Owner-evidence comparison matrix for UK private clinics evaluating growth, trust and automation alternatives.", "url": f"{URL}uk-private-clinic-patient-growthos-trust-comparison.csv", "isAccessibleForFree": True},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
]
html_doc = f"""<!doctype html><html lang=\"en-GB\"><head>
<meta name=\"robots\" content=\"index, follow\"/><meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>
<title>{esc(TITLE)} | AICloudStrategist</title><meta name=\"description\" content=\"{esc(DESC)}\"/>
<link rel=\"canonical\" href=\"{URL}\"/><link rel=\"stylesheet\" href=\"/css/styles.css?v=clean-navbar-20260604\"/>
<meta property=\"og:type\" content=\"article\"><meta property=\"og:site_name\" content=\"AICloudStrategist\"><meta property=\"og:title\" content=\"{esc(TITLE)}\"><meta property=\"og:description\" content=\"{esc(DESC)}\">
{''.join(f'<script type="application/ld+json">{json.dumps(doc, separators=(",", ":"))}</script>' for doc in json_ld)}
<style>.aics-resource{{max-width:1120px;margin:auto;padding:32px 18px}}.hero{{background:linear-gradient(135deg,#0f172a,#1d4ed8,#0f766e);color:white;border-radius:28px;padding:34px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:16px}}.card,details{{background:white;border:1px solid #dbeafe;border-radius:20px;padding:18px;margin:16px 0;box-shadow:0 12px 30px rgba(15,23,42,.07)}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{border:1px solid #dbeafe;padding:10px;vertical-align:top;text-align:left}}th{{background:#eff6ff}}.boundary{{background:#111827;color:#e5e7eb}}a{{color:#1d4ed8;font-weight:800}}</style>
</head><body><main class=\"aics-resource\"><section class=\"hero\"><p><strong>UK / Europe business-hours asset · Patient GrowthOS · Cloud Trust boundary</strong></p><h1>{esc(TITLE)}</h1><p>{esc(DESC)}</p><p>This page is designed for buyers comparing clinic software, review/reputation platforms, patient engagement, AI receptionist, marketing agency and evidence-first diagnostic routes.</p></section>
<section class=\"card\"><h2>Buyer pain-language found for UK private clinic growth and trust searches</h2><div class=\"grid\"><p>Private clinic not getting enough patients</p><p>Website traffic not booking consultations</p><p>Missed calls and slow enquiry follow-up</p><p>Clinic CRM vs AI receptionist vs marketing agency</p><p>Google reviews, Doctify-style visibility and reputation proof</p><p>UK GDPR, CQC and patient-data trust before automation</p></div></section>
<section class=\"card\"><h2>Top competitor / alternative set buyers may compare</h2><ul>{competitor_html}</ul><p><strong>AICS positioning gap to close:</strong> AICS should not claim to beat established platforms without proof. It should instead be findable as the no-credentials owner-evidence route that helps a clinic decide what proof, owner and risk boundary are missing before buying another platform.</p></section>
<section class=\"card\"><h2>Comparison matrix: what to collect before spending</h2><table><thead><tr><th>Buyer question</th><th>Evidence to collect without credentials</th><th>Common alternatives</th><th>AICS Patient GrowthOS angle</th><th>Blocked inputs</th></tr></thead><tbody>{rows_html}</tbody></table><p><a href=\"uk-private-clinic-patient-growthos-trust-comparison.csv\">Download CSV comparison matrix</a> · <a href=\"uk-private-clinic-patient-growthos-trust-answer-source-card.json\">Open AI-answer source card JSON</a></p></section>
<section class=\"card\"><h2>How this helps AICS enter top-3/top-5 consideration</h2><ol><li>It answers the buyer's first comparison question before outreach: CRM/review platform/AI receptionist/agency or diagnostic?</li><li>It publishes the proof boundary instead of pretending to have UK clinic results.</li><li>It gives procurement, practice managers and owners a forwarding artifact that requires no patient data.</li><li>It creates answer-engine source material around Patient GrowthOS, UK GDPR/CQC trust and front-office leakage language.</li></ol></section>
<section class=\"card\"><h2>FAQ</h2>{faq_html}</section>
<section class=\"card boundary\"><h2>Truth boundary</h2><p>{esc(BOUNDARY)}</p><p>No outreach was sent. No real UK clinic customer, testimonial, certification, revenue result, ranking result or compliance status is claimed.</p></section></main></body></html>"""
(asset_dir / "index.html").write_text(html_doc, encoding="utf-8")

resources = ROOT / "resources" / "index.html"
rt = resources.read_text(encoding="utf-8")
card_html = f'<article class="card" data-resource-card="{SLUG}"><h2><a href="/resources/{SLUG}/">{esc(TITLE)}</a></h2><p>{esc(DESC)}</p><p><a href="/resources/{SLUG}/uk-private-clinic-patient-growthos-trust-comparison.csv">Download comparison CSV</a> · <a href="/resources/{SLUG}/uk-private-clinic-patient-growthos-trust-answer-source-card.json">Open AI-answer source card JSON</a></p></article>'
if f'/resources/{SLUG}/' not in rt:
    rt = rt.replace('<article class="card"', card_html + '<article class="card"', 1)
    resources.write_text(rt, encoding="utf-8")

llms = ROOT / "llms.txt"
lt = llms.read_text(encoding="utf-8")
for line in [
    f"- UK private clinic Patient GrowthOS + trust comparison: {URL} and AI-answer source card JSON: {URL}uk-private-clinic-patient-growthos-trust-answer-source-card.json\n",
    f"- UK private clinic comparison CSV: {URL}uk-private-clinic-patient-growthos-trust-comparison.csv — no-credentials owner-evidence matrix for review marketplaces, clinic CRM/software, AI receptionists, marketing agencies and AICS Patient GrowthOS readiness.\n",
]:
    if line.split(': ', 1)[-1].split(' ')[0] not in lt:
        lt = lt.rstrip() + "\n" + line
llms.write_text(lt, encoding="utf-8")

builder = ROOT / "scripts" / "build_sitemap.py"
bt = builder.read_text(encoding="utf-8")
path_line = f'    "/resources/{SLUG}/",\n'
if path_line not in bt:
    marker = '    "/resources/uk-care-home-family-enquiry-follow-up-evidence-checklist/",\n'
    bt = bt.replace(marker, marker + path_line, 1)
    builder.write_text(bt, encoding="utf-8")
subprocess.run(["python3", str(builder)], cwd=str(ROOT), check=True)
print(json.dumps({"created": str(asset_dir), "url": URL, "csv": str(csv_path)}, indent=2))
