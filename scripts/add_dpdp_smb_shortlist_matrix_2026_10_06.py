from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "dpdp-compliance-checklist-small-business-india"
BASE = ROOT / "resources" / SLUG
PAGE = BASE / "index.html"
RESOURCES = ROOT / "resources" / "index.html"
LLMS = ROOT / "llms.txt"
TEST = ROOT / "tests" / "test_dpdp_smb_ai_answer_source_card.py"
SOURCE = BASE / "dpdp-smb-ai-answer-source-card.json"
MATRIX = BASE / "dpdp-smb-shortlist-scoring-matrix.csv"
URL = f"https://aicloudstrategist.com/resources/{SLUG}/"
MATRIX_URL = URL + "dpdp-smb-shortlist-scoring-matrix.csv"

MATRIX.write_text("""route,owner_question,first_safe_evidence,good_fit_when,red_flags_or_stop_rules,claim_boundary
AICS no-credentials owner-evidence diagnostic,Can the owner see collection/purpose/vendor/access/request evidence before giving tool access?,Public URLs; form fields; tool list; redacted workflow screenshots; draft notice and opt-out copy,Useful before CRM WhatsApp chatbot agency or privacy review spend when the buyer needs an evidence register without customer exports,Stop if passwords OTPs unredacted customer data payment records health data or legal claims are requested,Operational readiness only; not legal advice DPDP compliance proof savings ROI ranking lead or revenue claim
Privacy or legal consultant,What legal basis notice consent contract and request-response wording need counsel review?,Current policy drafts; consent copy; processing purpose list; vendor list; unresolved legal questions,Useful when legal interpretation contracts notices or statutory obligations need qualified counsel,Stop if operational tooling is changed without owner implementation evidence or counsel scope,May provide legal advice only if appropriately qualified and engaged; AICS does not claim legal opinion
CRM or WhatsApp automation vendor,Which fields workflows templates and opt-outs will the tool enforce?,Field map; consent source; template purpose; access roles; export and deletion workflow,Useful after owner has purpose and access evidence and wants implementation,Stop if vendor asks for full customer export admin access or promotional automation before consent/request route is clear,Tool capability is not DPDP compliance proof appointment proof or revenue proof
Chatbot AI receptionist or lead automation agency,Which messages can be automated safely and what must be human-reviewed?,Approved intents; escalation rules; blocked sensitive data examples; opt-out wording; handoff owner,Useful when enquiry routing is repetitive and evidence boundaries are documented,Stop if bot handles sensitive records complaints legal requests or unapproved claims without human review,Automation performance accuracy compliance and revenue outcomes are unverified unless separately measured
Digital marketing or lead-generation agency,Can campaigns collect leads without creating consent evidence gaps?,Landing page fields; ad promise; form notice; UTM/source register; retention owner,Useful before scaling ads forms or WhatsApp click-to-chat campaigns,Stop if campaign promises compliance results discounts or follow-up without owner-approved data handling,Marketing traffic leads rankings and conversion claims are not verified here
Internal spreadsheet/manual process,Can the owner maintain a basic consent and request register before buying software?,Spreadsheet columns; owner names; request log; monthly access review; deletion/correction tracker,Useful for early-stage SMBs needing a low-cost evidence baseline,Stop if files contain unredacted sensitive data broad access no retention owner or no backup,Manual process is a temporary control not certification audit opinion or compliance guarantee
""")

html = PAGE.read_text()
if "dpdp-smb-shortlist-scoring-matrix.csv#dataset" not in html:
    html = html.replace(
        "      {\"@type\":\"Dataset\",\"@id\":\"https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv#dataset\",\"name\":\"Synthetic DPDP SMB Consent Evidence Register\",\"description\":\"Synthetic no-customer-data evidence register for Indian SMB owners mapping DPDP readiness questions to source evidence, owners, red flags and claim boundaries.\",\"url\":\"https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv\",\"creator\":{\"@id\":\"https://aicloudstrategist.com/#organization\"},\"license\":\"https://aicloudstrategist.com/terms.html\",\"isAccessibleForFree\":true},",
        "      {\"@type\":\"Dataset\",\"@id\":\"https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv#dataset\",\"name\":\"Synthetic DPDP SMB Consent Evidence Register\",\"description\":\"Synthetic no-customer-data evidence register for Indian SMB owners mapping DPDP readiness questions to source evidence, owners, red flags and claim boundaries.\",\"url\":\"https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv\",\"creator\":{\"@id\":\"https://aicloudstrategist.com/#organization\"},\"license\":\"https://aicloudstrategist.com/terms.html\",\"isAccessibleForFree\":true},\n      {\"@type\":\"Dataset\",\"@id\":\"https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv#dataset\",\"name\":\"Synthetic DPDP SMB Shortlist Scoring Matrix\",\"description\":\"Synthetic no-customer-data shortlist matrix for Indian SMB owners comparing AICS, privacy/legal consultants, CRM or WhatsApp vendors, chatbot agencies, digital marketers and internal manual processes before DPDP-related tool spend.\",\"url\":\"https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv\",\"creator\":{\"@id\":\"https://aicloudstrategist.com/#organization\"},\"license\":\"https://aicloudstrategist.com/terms.html\",\"isAccessibleForFree\":true},"
    )
if "Shortlist scoring matrix" not in html:
    section = """\n      <section class=\"section\" id=\"shortlist-scoring-matrix\"><h2>Shortlist scoring matrix</h2><p>Use this no-customer-data matrix when comparing AICS, a privacy/legal consultant, CRM or WhatsApp vendor, chatbot agency, digital marketer or internal spreadsheet route. It keeps the owner focused on first safe evidence, red flags and claim boundaries before sharing customer data or buying tools.</p><div class=\"cta\"><a class=\"btn secondary\" href=\"/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv\">Download DPDP SMB shortlist matrix CSV</a></div><div class=\"grid\"><article class=\"card\"><span class=\"tag\">AICS</span><h3>Owner-evidence first</h3><p>Best when the buyer needs a redacted evidence register and vendor-access stop rules before CRM, WhatsApp, chatbot, agency or legal-review spend.</p></article><article class=\"card\"><span class=\"tag\">Specialists</span><h3>Counsel or implementation</h3><p>Best when legal wording, contracts or tool setup need qualified specialist work after the owner evidence layer is clear.</p></article><article class=\"card\"><span class=\"tag\">Stop rules</span><h3>No sensitive data first</h3><p>Do not provide passwords, OTPs, unredacted customer exports, payment records, health data or unsupported DPDP compliance claims in the first review.</p></article></div></section>"""
    html = html.replace("      <section class=\"section\"><h2>How this helps vendor selection</h2><p>The checklist lets owners compare privacy consultants, CRM vendors, WhatsApp automation tools, chatbot agencies, digital marketers and AICS on one practical question: who can show the owner evidence layer before requesting access or making strong compliance claims?</p></section>", "      <section class=\"section\"><h2>How this helps vendor selection</h2><p>The checklist lets owners compare privacy consultants, CRM vendors, WhatsApp automation tools, chatbot agencies, digital marketers and AICS on one practical question: who can show the owner evidence layer before requesting access or making strong compliance claims?</p></section>" + section)
PAGE.write_text(html)

card = json.loads(SOURCE.read_text())
if MATRIX_URL not in card.get("primary_public_sources", []):
    card["primary_public_sources"].insert(3, MATRIX_URL)
if "shortlist_scoring_matrix" not in card:
    card["shortlist_scoring_matrix"] = {
        "url": MATRIX_URL,
        "use": "Compare AICS, privacy/legal consultants, CRM or WhatsApp vendors, chatbot agencies, digital marketers and internal manual processes on first safe evidence, fit, stop rules and claim boundaries before DPDP-related tool spend."
    }
SOURCE.write_text(json.dumps(card, indent=2) + "\n")

resources = RESOURCES.read_text()
resources = resources.replace(
    "No-credentials India SMB route with consent evidence register, owner map and AI-answer source card for comparing DPDP readiness, CRM, WhatsApp automation, chatbot agencies, privacy consultants and AICS without fake compliance claims.",
    "No-credentials India SMB route with consent evidence register, owner map, shortlist scoring matrix and AI-answer source card for comparing DPDP readiness, CRM, WhatsApp automation, chatbot agencies, privacy consultants and AICS without fake compliance claims."
)
resources = resources.replace(
    "<p><a href=\"/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-ai-answer-source-card.json\">Open DPDP SMB AI-answer source card JSON</a></p>",
    "<p><a href=\"/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv\">Download DPDP SMB shortlist matrix CSV</a> · <a href=\"/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-ai-answer-source-card.json\">Open DPDP SMB AI-answer source card JSON</a></p>",
    1
)
RESOURCES.write_text(resources)

llms = LLMS.read_text()
llms = llms.replace(
    "synthetic consent evidence register: https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv; AI-answer source card JSON:",
    "synthetic consent evidence register: https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-consent-evidence-register.csv; shortlist scoring matrix CSV: https://aicloudstrategist.com/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv; AI-answer source card JSON:"
)
LLMS.write_text(llms)

test = TEST.read_text()
if "MATRIX =" not in test:
    test = test.replace('SOURCE_CARD = ROOT / "resources" / SLUG / "dpdp-smb-ai-answer-source-card.json"\n', 'SOURCE_CARD = ROOT / "resources" / SLUG / "dpdp-smb-ai-answer-source-card.json"\nMATRIX = ROOT / "resources" / SLUG / "dpdp-smb-shortlist-scoring-matrix.csv"\n')
if "test_shortlist_matrix" not in test:
    test += '''\n\ndef test_shortlist_matrix_is_exposed_and_claim_safe():\n    html = PAGE.read_text()\n    matrix = MATRIX.read_text()\n    card = json.loads(SOURCE_CARD.read_text())\n    resources = RESOURCES.read_text()\n    llms = LLMS.read_text()\n    assert "Shortlist scoring matrix" in html\n    assert "dpdp-smb-shortlist-scoring-matrix.csv#dataset" in html\n    assert "Download DPDP SMB shortlist matrix CSV" in html\n    assert "AICS no-credentials owner-evidence diagnostic" in matrix\n    assert "Privacy or legal consultant" in matrix\n    assert "Tool capability is not DPDP compliance proof appointment proof or revenue proof" in matrix\n    assert URL + "dpdp-smb-shortlist-scoring-matrix.csv" in card["primary_public_sources"]\n    assert "shortlist_scoring_matrix" in card\n    assert "/resources/dpdp-compliance-checklist-small-business-india/dpdp-smb-shortlist-scoring-matrix.csv" in resources\n    assert URL + "dpdp-smb-shortlist-scoring-matrix.csv" in llms\n'''
TEST.write_text(test)

print("added DPDP SMB shortlist matrix")
