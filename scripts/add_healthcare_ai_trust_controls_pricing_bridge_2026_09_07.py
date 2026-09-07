from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRICING = ROOT / "pricing.html"

BRIDGE = '''<aside class="card" data-revenue-bridge="healthcare-ai-trust-controls"><h3>Healthcare AI trust controls first-review diagnostic bridge</h3><p><strong>Scope before AI receptionist, patient engagement, chatbot, CRM/PMS/EHR workflow or cloud automation spend</strong> for clinics and healthtech teams that need a no-patient-data view of patient-data boundaries, human approval gates, audit logs, vendor evidence, rollback ownership and public-claim approval before platform or automation decisions. Starts from the synthetic owner-evidence CSV and demo owner map; no real clinic, patient, PHI/ePHI, health record, personal data, vendor export, credential, production access, DPDP/GDPR/UK GDPR/HIPAA compliance proof, legal/privacy/security/medical advice, ranking, demand, lead, appointment, patient, revenue, savings, ROI or automation-performance claim.</p><p><a class="btn btn-light" href="/resources/healthcare-ai-trust-controls/">View trust controls</a> <a class="btn btn-light" href="/resources/healthcare-ai-trust-controls/healthcare-ai-trust-controls-owner-evidence.csv">Download CSV</a> <a class="btn btn-light" href="/free-business-review/?package=healthcare-ai-trust-controls&amp;source=pricing-fixed-scope">Request fit check</a></p></aside>'''
MARKER = '<aside class="card" data-revenue-bridge="india-healthcare-dpdp-cloud-trust-evidence-source-map">'


def main() -> None:
    html = PRICING.read_text(encoding="utf-8")
    if 'data-revenue-bridge="healthcare-ai-trust-controls"' in html:
        return
    if MARKER not in html:
        raise SystemExit("pricing bridge insertion marker missing")
    PRICING.write_text(html.replace(MARKER, BRIDGE + MARKER, 1), encoding="utf-8")


if __name__ == "__main__":
    main()
