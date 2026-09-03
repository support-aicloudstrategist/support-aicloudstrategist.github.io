from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "resources/dpdp-compliance-checklist-small-business-india/index.html"
CSV = ROOT / "resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv"
SVG = ROOT / "resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-owner-evidence-map.svg"
LLMS = ROOT / "llms.txt"


def test_dpdp_smb_owner_evidence_page_has_no_credentials_markers():
    html = PAGE.read_text(encoding="utf-8")
    assert 'data-resource="dpdp-smb-owner-evidence-repair-2026-09-03"' in html
    assert "DPDP checklist before WhatsApp, CRM or lead automation spend" in html
    assert "No passwords, production exports, sensitive records or legal guarantees required" in html
    assert "Download synthetic evidence register" in html
    assert "not legal advice, compliance certification" in html
    assert "no real client, customer, patient, personal data" in html


def test_dpdp_smb_supporting_assets_are_linked_and_labelled():
    html = PAGE.read_text(encoding="utf-8")
    csv_text = CSV.read_text(encoding="utf-8")
    svg_text = SVG.read_text(encoding="utf-8")
    llms = LLMS.read_text(encoding="utf-8")

    assert "dpdp-smb-consent-evidence-register.csv" in html
    assert "dpdp-smb-owner-evidence-map.svg" in html
    assert "Synthetic DPDP SMB Consent Evidence Register" in html
    assert "DEMO / SYNTHETIC OWNER MAP" in svg_text
    assert "buyer_question,example_source,owner,green_evidence,red_flag,claim_boundary" in csv_text
    assert "Passwords exports patient reports payment data or secrets requested" in csv_text
    assert "Indian small businesses need DPDP readiness before WhatsApp" in llms
    assert "dpdp-smb-consent-evidence-register.csv" in llms
    assert "dpdp-smb-owner-evidence-map.svg" in llms
