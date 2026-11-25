/**
 * Dense branded SynthoSaaS sample diagnostic PDF.
 * Embeds site fonts: Figtree (body) + Syne (display/headings).
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(__dirname, 'pdf-tools', 'package.json'));
const PDFDocument = require('pdfkit');
const root = path.resolve(__dirname, '..');
const fontsDir = path.join(root, 'assets', 'fonts');
const logoPath = path.join(root, 'assets', 'brand', 'aics-brand-mark-nav.png');
const outPrimary = path.join(root, 'downloads', 'sample-cloud-ai-cost-governance-diagnostic.pdf');
const outSecondary = path.join(root, 'resources', 'sample-diagnostic-deliverable', 'sample-cloud-ai-cost-governance-diagnostic.pdf');
const PRE_STRIP_DEBUG = process.env.PDF_DEBUG_PRESTRIP === '1';

const FIGTREE = path.join(fontsDir, 'Figtree-Regular.ttf');
const FIGTREE_BOLD = path.join(fontsDir, 'Figtree-Bold.ttf');
const SYNE_BOLD = path.join(fontsDir, 'Syne-Bold.ttf');

for (const f of [FIGTREE, FIGTREE_BOLD, SYNE_BOLD, logoPath]) {
  if (!fs.existsSync(f)) throw new Error(`Missing required asset: ${f}`);
}

const PAGE_W = 595.28;
const PAGE_H = 841.89;
const ML = 28;
const MR = 28;
const MT = 40;
const MB = 30;
const CW = PAGE_W - ML - MR;
const TEAL = '#087989';
const INK = '#0a1828';
const MUTED = '#4a5568';
const RULE_COLOR = '#c5d0ce';
const SOFT = '#e8f4f6';

const doc = new PDFDocument({
  size: 'A4',
  margins: { top: MT, bottom: MB, left: ML, right: MR },
  autoFirstPage: false,
  bufferPages: true,
  info: {
    Title: 'Sample Cloud & AI Cost Governance Diagnostic — SynthoSaaS',
    Author: 'AICloudStrategist',
    Subject: 'Synthetic sample diagnostic deliverable',
    Keywords: 'SynthoSaaS, synthetic, cloud cost ownership, diagnostic',
  },
});

const chunks = [];
doc.on('data', (c) => chunks.push(c));

doc.registerFont('Figtree', FIGTREE);
doc.registerFont('FigtreeBold', FIGTREE_BOLD);
doc.registerFont('SyneBold', SYNE_BOLD);

let pageCount = 0;
let pageHasBody = false;
let inManualAddPage = false;
let skippedEmptyBreaks = 0;

function remainingSpace() {
  return PAGE_H - MB - doc.y;
}

function markBody() {
  pageHasBody = true;
}

function drawHeader() {
  const y = 14;
  try {
    doc.image(logoPath, ML, y, { width: 16, height: 16 });
  } catch {
    /* logo optional at runtime */
  }
  // lineBreak:false + explicit position keeps header from auto-paging
  doc.font('SyneBold').fontSize(9).fillColor(INK).text('AICloudStrategist', ML + 22, y + 3, { lineBreak: false });
  doc.font('Figtree').fontSize(6.5).fillColor(MUTED)
    .text('Synthetic data, real structure', PAGE_W - MR - 130, y + 1, { width: 130, align: 'right', lineBreak: false })
    .text('Sample diagnostic deliverable', PAGE_W - MR - 130, y + 10, { width: 130, align: 'right', lineBreak: false });
  doc.moveTo(ML, 34).lineTo(PAGE_W - MR, 34).lineWidth(1.1).strokeColor(TEAL).stroke();
  doc.x = ML;
  doc.y = 42;
  doc.fillColor(INK);
}

function addPage() {
  // Never stack blank pages: if current page has no body yet, reuse it.
  if (pageCount > 0 && !pageHasBody) {
    skippedEmptyBreaks += 1;
    doc.y = Math.max(doc.y, 42);
    return;
  }
  inManualAddPage = true;
  doc.addPage();
  inManualAddPage = false;
  pageCount += 1;
  pageHasBody = false;
  drawHeader();
}

let autoPagesAdded = 0;
// PDFKit auto page-breaks need a header; blocking addPage left header-only ghost pages.
doc.on('pageAdded', () => {
  if (inManualAddPage) return;
  autoPagesAdded += 1;
  pageCount += 1;
  pageHasBody = false;
  drawHeader();
});

function drawFooters() {
  const range = doc.bufferedPageRange();
  for (let i = 0; i < range.count; i++) {
    doc.switchToPage(range.start + i);
    const bottomLimit = PAGE_H - MB;
    const ruleY = bottomLimit - 16;
    const fy = bottomLimit - 8;
    doc.moveTo(ML, ruleY).lineTo(PAGE_W - MR, ruleY).lineWidth(0.5).strokeColor(RULE_COLOR).stroke();
    doc.font('Figtree').fontSize(5.5).fillColor(MUTED);
    doc.text('AICLOUDSTRATEGIST PRIVATE LIMITED  |  CIN U62020DC2026PTC470945', ML, fy, { lineBreak: false });
    doc.text(`Page ${i + 1} of ${range.count}  |  aicloudstrategist.com/request-fit-review/`, PAGE_W - MR - 220, fy, {
      width: 220,
      align: 'right',
      lineBreak: false,
    });
  }
}

function ensure(h = 24) {
  if (remainingSpace() < h) addPage();
}

function gap(pts = 3) {
  doc.y += pts;
}

function writeText(font, size, color, text, opts = {}) {
  ensure(opts.minH || size + 4);
  markBody();
  doc.font(font).fontSize(size).fillColor(color);
  // No height cap — capped height made PDFKit open new pages without flowing body text.
  doc.text(text, ML, doc.y, {
    width: CW,
    lineGap: opts.lineGap ?? 1,
    ...(opts.lineBreak === false ? { lineBreak: false } : {}),
  });
}

function eyebrow(t) {
  writeText('SyneBold', 7, TEAL, t, { minH: 12, lineGap: 0 });
}

function h1(t) {
  writeText('SyneBold', 13, INK, t, { minH: 18, lineGap: 0 });
  gap(2);
}

function h2(t) {
  writeText('SyneBold', 10, INK, t, { minH: 14, lineGap: 0 });
  gap(1);
}

function section(label, title) {
  ensure(36);
  markBody();
  doc.font('SyneBold').fontSize(7).fillColor(TEAL).text(label, ML, doc.y, { width: CW, lineGap: 0 });
  doc.font('SyneBold').fontSize(13).fillColor(INK).text(title, ML, doc.y, { width: CW, lineGap: 0 });
  gap(2);
}

function body(t) {
  let remaining = t;
  while (remaining) {
    if (remainingSpace() < 14) addPage();
    doc.font('Figtree').fontSize(8);
    const fullH = doc.heightOfString(remaining, { width: CW, lineGap: 1.2 });
    const avail = remainingSpace() - 2;
    markBody();
    if (fullH <= avail) {
      doc.fillColor(INK).text(remaining, ML, doc.y, { width: CW, lineGap: 1.2 });
      remaining = '';
    } else {
      // Fit as many words as possible on this page; continue on next (no blank page).
      const words = remaining.split(/\s+/);
      let lo = 1;
      let hi = words.length;
      let best = 1;
      while (lo <= hi) {
        const mid = Math.floor((lo + hi) / 2);
        const trial = words.slice(0, mid).join(' ');
        const th = doc.heightOfString(trial, { width: CW, lineGap: 1.2 });
        if (th <= avail) {
          best = mid;
          lo = mid + 1;
        } else {
          hi = mid - 1;
        }
      }
      const chunk = words.slice(0, Math.max(1, best)).join(' ');
      doc.fillColor(INK).text(chunk, ML, doc.y, { width: CW, lineGap: 1.2 });
      remaining = words.slice(Math.max(1, best)).join(' ');
      if (remaining) addPage();
    }
  }
  gap(2);
}

function bullet(t) {
  writeText('Figtree', 7.5, INK, `•  ${t}`, { minH: 11, lineGap: 0.5 });
}

function subhead(t) {
  writeText('FigtreeBold', 8, INK, t, { minH: 12, lineGap: 0 });
  gap(1);
}

function table(headers, rows, widths) {
  const rowH = 12.5;
  const headerH = 13;
  ensure(headerH + rowH + 4);

  const drawHeaderRow = () => {
    markBody();
    const top = doc.y;
    doc.rect(ML, top, CW, headerH).fill(INK);
    let x = ML + 3;
    headers.forEach((h, i) => {
      doc.font('FigtreeBold').fontSize(6).fillColor('#ffffff')
        .text(h, x, top + 3.5, { width: widths[i] - 4, lineBreak: false });
      x += widths[i];
    });
    doc.y = top + headerH;
  };

  drawHeaderRow();
  rows.forEach((row, idx) => {
    if (remainingSpace() < rowH + 4) {
      addPage();
      drawHeaderRow();
    }
    markBody();
    const top = doc.y;
    if (idx % 2 === 0) doc.rect(ML, top, CW, rowH).fill('#f4f7f8');
    doc.rect(ML, top, CW, rowH).lineWidth(0.4).strokeColor('#d0d7dc').stroke();
    let x = ML + 3;
    row.forEach((cell, i) => {
      const s = String(cell);
      doc.font('Figtree').fontSize(6.2).fillColor(INK)
        .text(s.length > 52 ? `${s.slice(0, 50)}..` : s, x, top + 3, { width: widths[i] - 4, lineBreak: false });
      x += widths[i];
    });
    doc.y = top + rowH;
  });
  gap(3);
}

function kpiBoxes(items) {
  ensure(42);
  markBody();
  const boxW = (CW - 8) / items.length;
  const y = doc.y;
  items.forEach((it, i) => {
    const x = ML + i * (boxW + 4);
    doc.roundedRect(x, y, boxW, 36, 3).fillAndStroke(SOFT, TEAL);
    doc.font('SyneBold').fontSize(8).fillColor(INK).text(it[0], x + 5, y + 6, { width: boxW - 10, lineBreak: false });
    doc.font('Figtree').fontSize(6.5).fillColor(MUTED).text(it[1], x + 5, y + 20, { width: boxW - 10, lineBreak: false });
  });
  doc.y = y + 40;
}

// -------- Document --------
addPage();

eyebrow('CLOUD & AI COST GOVERNANCE DIAGNOSTIC');
h1('Sample diagnostic pack — SynthoSaaS (synthetic estate)');
kpiBoxes([
  ['SynthoSaaS', 'Series B SaaS — fictional'],
  ['USD 186,400', 'Synthetic Aug 2026 bill'],
  ['AWS + Azure', 'EKS / GPU / LLM APIs'],
]);

subhead('Pack contents (7 sections)');
[
  '01  Executive summary — buyer answers first',
  '02  Evidence register — what was reviewed',
  '03  Cost ownership map — who owns each dollar',
  '04  Allocation-gap table — contested / unallocated spend',
  '05  Risk and confidence matrix — what is safe to cut',
  '06  Act / Investigate / Hold register — decisions with owners',
  '07  30-day action plan — client-owned next moves',
].forEach(bullet);
gap(3);
body('Currency note: All dollar amounts are synthetic USD for one illustrative billing period (1–31 Aug 2026). Not benchmarks, forecasts, or savings guarantees. Label: Synthetic data, real structure.');

subhead('Fictional estate snapshot (SynthoSaaS)');
table(
  ['Dimension', 'Synthetic value', 'Notes'],
  [
    ['Headcount band', '~180 FTE', 'Product-led SaaS; eng-heavy'],
    ['Primary workloads', 'API + data plane', 'EKS-hosted microservices'],
    ['ML footprint', 'GPU pool + LLM APIs', '23% of Aug bill combined'],
    ['Forecast discipline', 'Monthly', 'MoM +12% triggered diagnostic'],
    ['Tagging maturity', 'Partial', 'Azure stronger than shared EKS'],
    ['Buyer sponsor', 'CTO + CFO joint', 'Ownership before cuts'],
  ],
  [120, 120, CW - 240],
);

section('01  EXECUTIVE SUMMARY', 'What finance and engineering should see first');
body('Decision question: Who owns the month-over-month cloud and GPU rise before SynthoSaaS cuts anything?');
body('Synthetic MoM spend rose about 12%. Growth concentrates in shared EKS, GPU retention after experiments, and LLM inference without a clear product owner. Checkout/API compute is owned and actionable. Production downsizing without SLO evidence stays on Hold.');
table(
  ['Signal', 'Synthetic figure', 'Buyer takeaway'],
  [
    ['Reconciled bill', 'USD 186,400', 'Single-period baseline for ownership work'],
    ['Assigned ownership', '61%', 'Bankable only where owner + confidence exist'],
    ['Shared / contested', '24%', 'Investigate before forecasting cuts'],
    ['Unallocated gap', '15%', 'Name the gap — do not average it away'],
    ['Register posture', '4 Act / 4 Inv / 3 Hold', 'Hold stays visible under pressure'],
  ],
  [115, 105, CW - 220],
);
table(
  ['MoM driver', 'Synthetic delta', 'Primary evidence'],
  [
    ['Shared EKS growth', '+USD 3,100', 'E-02, E-03'],
    ['GPU retention', '+USD 2,400', 'E-04'],
    ['LLM inference', '+USD 1,800', 'E-05'],
    ['Non-prod idle', '+USD 1,200', 'E-01'],
    ['Product API (owned)', '+USD 900', 'E-02'],
    ['Networking egress', '+USD 650', 'E-02'],
  ],
  [130, 95, CW - 225],
);
subhead('Where waste shows up');
['Non-prod overnight idle without a product owner', 'Orphaned GPU volumes after experiment end dates', 'Sandbox accounts without budget caps'].forEach(bullet);
gap(2);
subhead('30-day posture');
['Act on high-confidence idle waste', 'Investigate EKS split rules and LLM token owners', 'Hold prod/GPU cuts until evidence holds'].forEach(bullet);
gap(3);
table(
  ['Deliverable', 'Audience', 'Format in pack'],
  [
    ['Executive + registers', 'CTO / CFO', 'Tables + short narrative'],
    ['Ownership + gap tables', 'FinOps + platform', 'Bankable vs contested USD'],
    ['Act / Inv / Hold', 'Engineering leads', 'Owner + evidence ID per row'],
    ['30-day plan', 'Client PMO', 'Client-owned milestones only'],
  ],
  [155, 130, CW - 285],
);

section('02  EVIDENCE REGISTER', 'What was reviewed (synthetic exports only)');
body('No production credentials. Evidence IDs are fictional labels showing how a real pack cites sources so finance and engineering argue from the same record.');
table(
  ['ID', 'Source', 'Scope', 'Period', 'Conf'],
  [
    ['E-01', 'AWS CUR export (synthetic)', 'All linked accounts', 'Aug 2026', 'High'],
    ['E-02', 'Cost Explorer by service', 'MoM delta view', 'Jul–Aug 2026', 'High'],
    ['E-03', 'EKS namespace label dump', 'Shared platform cluster', '2026-08-28', 'Med'],
    ['E-04', 'GPU job metadata CSV', 'Training pool', 'Aug 2026', 'Med'],
    ['E-05', 'LLM API vendor invoice', 'Inference tokens', 'Aug 2026', 'High'],
    ['E-06', 'Azure subscription export', 'Secondary region apps', 'Aug 2026', 'Med'],
    ['E-07', 'Owner roster (notes)', 'Product / platform / ML', 'Intake', 'Med'],
  ],
  [34, 150, 120, 80, CW - 384],
);
body('FinOps note: Tools can show the bill. This register shows which exports underpin each decision.');
table(
  ['Stakeholder', 'Care about', 'Section to open first'],
  [
    ['CFO', 'Bankable vs contested USD', 'Exec summary + ownership map'],
    ['CTO', 'Blast radius of Acts', 'Risk matrix + Hold register'],
    ['Platform lead', 'EKS + sandbox gaps', 'Allocation-gap table'],
    ['ML Ops', 'GPU idle policy', 'Ownership map + register A3/H2'],
    ['FinOps analyst', 'Evidence trail', 'Evidence register + Act rows'],
  ],
  [95, 155, CW - 250],
);
table(
  ['Handling rule', 'Applies to', 'Rationale'],
  [
    ['Single billing period lock', 'All USD rows', 'Avoid MoM noise in ownership %'],
    ['Evidence ID on every Act row', 'Register section', 'Audit trail for finance sign-off'],
    ['No credential collection in sample', 'This PDF', 'Real pack uses client-owned exports'],
    ['Hold list is published', 'Week 1 governance', 'Prevents silent scope creep on cuts'],
  ],
  [145, 115, CW - 260],
);

section('03  COST OWNERSHIP MAP', 'Who owns every material dollar');
body('Synthetic multi-cloud estate: AWS-primary (~88%) + Azure secondary (~12%). Totals reconcile to USD 186,400.');
table(
  ['Cost pool', 'Cloud', 'Owner class', 'USD', 'Share', 'Status'],
  [
    ['Product API — prod compute', 'AWS', 'Assigned / Product Eng', '52,100', '28%', 'Assigned'],
    ['Customer data plane', 'AWS', 'Assigned / Data', '31,400', '17%', 'Assigned'],
    ['Shared EKS platform', 'AWS', 'Shared / Platform', '28,900', '16%', 'Contested'],
    ['GPU training pool', 'AWS', 'Shared / ML Ops', '24,700', '13%', 'Policy gap'],
    ['LLM inference APIs', 'Vendor', 'Assigned / AI Prod', '18,200', '10%', 'Owner thin'],
    ['Non-prod + sandbox', 'AWS', 'Unallocated gap', '16,800', '9%', 'Gap'],
    ['Networking / egress', 'AWS', 'Shared / Platform', '8,600', '5%', 'Investigate'],
    ['Azure app / misc', 'Azure', 'Assigned / Product', '5,700', '3%', 'Assigned'],
  ],
  [135, 45, 120, 48, 40, CW - 388],
);
subhead('Buyer answers this map unlocks');
body('Ownership: 61% named; 39% shared or gap — not one “cloud waste” number. GPU / AI spend: Training + LLM APIs = 23% of bill; idle policy and token ownership are blockers. Multi-cloud: Azure is small but tagged; AWS shared platform is where attribution breaks.');
table(
  ['Status', 'Meaning for finance', 'Typical next step'],
  [
    ['Assigned', 'Forecastable with named owner', 'Track in unit economics'],
    ['Contested', 'USD real; split rule missing', 'Investigate before target setting'],
    ['Gap', 'No owner class', 'Name owner in intake workshop'],
    ['Policy gap', 'Technical owner; policy thin', 'ML/platform policy ticket'],
  ],
  [72, 175, CW - 247],
);

section('04  ALLOCATION-GAP TABLE', 'Contested and unallocated spend — named, not averaged');
table(
  ['Gap', 'Est. USD', 'Why it blocks cuts', 'Owner to name', 'Ev'],
  [
    ['EKS namespaces w/o chargeback', '14,200', '3 products share ingress; no split', 'Platform + FinOps', 'E-03'],
    ['GPU nodes past experiment end', '9,800', 'Jobs owned; idle policy is not', 'ML Ops', 'E-04'],
    ['Non-prod overnight idle', '7,400', 'No product accountable for schedule', 'Platform Eng', 'E-01'],
    ['LLM tokens without SKU map', '6,100', 'Invoice exists; commercial owner thin', 'AI Prod + Fin', 'E-05'],
    ['Sandbox accounts uncapped', '4,900', 'Spend drifts outside forecast', 'FinOps', 'E-01'],
    ['Egress spike — service unknown', '3,200', 'Cannot assign without path attribution', 'Networking', 'E-02'],
  ],
  [138, 50, 155, 95, CW - 438],
);
body('FinOps vs diagnostic: A FinOps tool surfaces anomalies. This table decides which dollars are not yet bankable until an owner and rule exist.');

section('05  RISK & CONFIDENCE MATRIX', 'What is safe to cut — and what is not');
body('Act only when confidence is high and residual risk is low. Hold is a first-class outcome.');
table(
  ['Candidate action', 'Conf', 'Risk', 'Safe now?', 'Rationale'],
  [
    ['Stop idle non-prod nights', 'High', 'Low', 'Yes — Act', 'Clear schedule gap; easy rollback'],
    ['Rightsize oversized API ASGs', 'High', 'Low', 'Yes — Act', 'Utilization evidence; Product-owned'],
    ['Delete orphaned GPU volumes', 'High', 'Low', 'Yes — Act', 'Past end date; no active jobs'],
    ['Cap sandbox budgets', 'Med', 'Low', 'Yes — Act', 'Policy change; low blast radius'],
    ['Allocate shared EKS costs', 'Med', 'Med', 'No — Investigate', 'Needs split rule before banking'],
    ['Trace egress to service', 'Med', 'Med', 'No — Investigate', 'Attribution incomplete'],
    ['Map LLM tokens to SKU', 'Med', 'Med', 'No — Investigate', 'Owner roster incomplete'],
    ['Buy RIs / Savings Plans now', 'Low', 'High', 'No — Hold', 'Commitment before ownership clear'],
    ['Prod downsize without SLO', 'Low', 'High', 'No — Hold', 'Reliability risk > bill optics'],
    ['Collapse multi-AZ for savings', 'Low', 'High', 'No — Hold', 'Architecture / DR risk'],
  ],
  [150, 36, 36, 78, CW - 300],
);
table(
  ['Confidence', 'Definition in this pack', 'When to use'],
  [
    ['High', 'Export + owner agree', 'Act candidates A1–A3'],
    ['Med', 'Export solid; owner/rule partial', 'Investigate I1–I3'],
    ['Low', 'Commitment or SLO unknown', 'Hold H1–H3 until clarity'],
  ],
  [70, 210, CW - 280],
);

section('06  ACT / INVESTIGATE / HOLD REGISTER', 'Decisions with confidence, risk, and owner');
table(
  ['ID', 'Finding', 'Conf', 'Risk', 'Owner', 'Next', 'Ev'],
  [
    ['A1', 'Stop idle non-prod nights', 'High', 'Low', 'Platform Eng', 'Act', 'E-01'],
    ['A2', 'Rightsize oversized API ASGs', 'High', 'Low', 'Product Eng', 'Act', 'E-02'],
    ['A3', 'Delete orphaned GPU volumes', 'High', 'Low', 'ML Ops', 'Act', 'E-04'],
    ['A4', 'Cap sandbox account budgets', 'Med', 'Low', 'FinOps', 'Act', 'E-01'],
    ['I1', 'Allocate shared EKS costs', 'Med', 'Med', 'Platform + Fin', 'Investigate', 'E-03'],
    ['I2', 'Trace egress spike to service', 'Med', 'Med', 'Networking', 'Investigate', 'E-02'],
    ['I3', 'LLM token owner unclear', 'Med', 'Med', 'AI Prod + Fin', 'Investigate', 'E-05'],
    ['I4', 'Spot interruption impact', 'Low', 'Med', 'Platform Eng', 'Investigate', 'E-01'],
    ['H1', 'RI / SP purchase now', 'Low', 'High', 'FinOps', 'Hold', 'E-01'],
    ['H2', 'Prod downsize without SLO', 'Low', 'High', 'SRE', 'Hold', 'E-07'],
    ['H3', 'Multi-AZ collapse proposal', 'Low', 'High', 'Architecture', 'Hold', 'E-07'],
  ],
  [26, 140, 32, 32, 85, 68, CW - 383],
);
body('Illustrative near-term Act candidates (not a savings promise): ASG floors ~USD 28–36k/yr teaching range; orphan cleanup ~USD 9–14k; non-prod idle ~USD 12–18k. Real estates differ.');
table(
  ['Posture', 'Count', 'USD band (synthetic)', 'Finance treatment'],
  [
    ['Act', '4', '~USD 42–68k annualized equiv.', 'Include after owner sign-off'],
    ['Investigate', '4', '~USD 38–51k contested', 'Exclude from forecast'],
    ['Hold', '3', 'Commitment / SLO exposure', 'Disclose; no target'],
  ],
  [70, 42, 155, CW - 267],
);

section('07  30-DAY ACTION PLAN', 'What the client owns next');
body('Implementation stays with SynthoSaaS. AICloudStrategist does not execute production changes as part of the diagnostic fee.');
const weeks = [
  ['Days 1–7 — Confirm owners', 'Lock owners for Act items A1–A4. Freeze the Hold list so commercial pressure cannot erase H1–H3. Name the EKS split-rule owner.'],
  ['Days 8–14 — Execute high-confidence Acts', 'Run A1/A3 in non-prod with rollback notes. Open Investigate tickets I1–I3. No production GPU changes.'],
  ['Days 15–21 — Investigate shared platform', 'Draft EKS namespace/ingress allocation options. Keep contested dollars out of finance forecasts until the rule is agreed.'],
  ['Days 22–30 — Hold review + re-measure', 'GPU idle policy workshop. Re-measure baseline. Promote Investigate to Act only where evidence and owners now exist.'],
];
for (const [t, p] of weeks) {
  writeText('FigtreeBold', 7.5, TEAL, t, { minH: 12, lineGap: 0 });
  body(p);
}
table(
  ['Week', 'Client deliverable', 'Success signal'],
  [
    ['1', 'Signed owner list A1–A4', 'No anonymous infra spend in forecast'],
    ['2', 'Rollback notes for A1/A3', 'Change tickets linked to evidence'],
    ['3', 'EKS split options memo', 'Finance stops allocating contested 16%'],
    ['4', 'Re-measured Aug-equivalent', 'Investigate rows promoted or closed'],
  ],
  [40, 230, CW - 270],
);
subhead('What we typically need from the client');
table(
  ['Input', 'Why', 'When'],
  [
    ['Billing export / CUR-equivalent', 'Reconcile ownership to one period', 'After fit, under NDA'],
    ['Account list + known product owners', 'Seed the ownership map', 'Intake'],
    ['Optional: labels, GPU jobs, model bills', 'GPU / LLM attribution', 'If in scope'],
  ],
  [170, 190, CW - 360],
);
table(
  ['Checkpoint', 'Owner', 'Exit criteria'],
  [
    ['Act owners confirmed', 'Client PMO', 'A1–A4 named in writing'],
    ['Investigate tickets opened', 'Platform + Fin', 'I1–I3 in backlog with dates'],
    ['Hold list ratified', 'CTO / CFO', 'H1–H3 unchanged in forecast deck'],
    ['Baseline re-measure', 'FinOps', 'Same period definition as diagnostic'],
  ],
  [130, 115, CW - 245],
);

section('BOUNDARIES & NEXT STEP', 'Synthetic data, real structure');
subhead('What this diagnostic does NOT do');
[
  'No production login or credentials required to start',
  'No savings-share contract and no savings guarantee',
  'No implementation of cuts inside the diagnostic fee',
  'Not a statutory financial audit or certification',
].forEach(bullet);
gap(4);
subhead('Primary CTA');
writeText('SyneBold', 11, INK, 'Request a diagnostic fit check', { minH: 16, lineGap: 0 });
gap(2);
body('Free suitability call. About two minutes on the form. No billing files required. We respond within one business day (IST).');
writeText('Figtree', 8, TEAL, 'https://aicloudstrategist.com/request-fit-review/', { minH: 12, lineGap: 0 });
gap(3);
body('SynthoSaaS is fictional. This pack demonstrates deliverable shape for fit-review buyers — not a client endorsement, case study, or promised outcome.');
gap(3);
writeText('Figtree', 7, MUTED, 'AICLOUDSTRATEGIST PRIVATE LIMITED  |  contact@aicloudstrategist.com  |  +91 87963 02608', { minH: 10, lineGap: 0 });

const rangeBeforeFooters = doc.bufferedPageRange();
if (PRE_STRIP_DEBUG || process.env.PDF_LOG_BUFFER === '1') {
  console.error('buffered pages before footers:', JSON.stringify(rangeBeforeFooters));
}
drawFooters();
if (process.env.PDF_LOG_BUFFER === '1') {
  console.error('buffered pages after footers:', JSON.stringify(doc.bufferedPageRange()));
}
doc.end();

await new Promise((resolve) => doc.on('end', resolve));
let buf = Buffer.concat(chunks);
if (PRE_STRIP_DEBUG) {
  fs.writeFileSync(path.join(root, 'downloads', '.prestrip-debug.pdf'), buf);
}

// Verify only — pdf-lib copyPages strips embedded Figtree/Syne (pages look blank in viewers).
const pdfjs = await import(pathToFileURL(path.join(__dirname, 'pdf-tools/node_modules/pdfjs-dist/legacy/build/pdf.mjs')).href);
const parsed = await pdfjs.getDocument({ data: new Uint8Array(buf), useSystemFonts: true }).promise;
const headerNoise = /AICloudStrategist|Synthetic data, real structure|Sample diagnostic deliverable|AICLOUDSTRATEGIST PRIVATE LIMITED|Page \d+ of \d+|aicloudstrategist\.com\/request-fit-review\/|CIN U62020DC2026PTC470945|\|/g;
const emptyPageReport = [];
for (let i = 1; i <= parsed.numPages; i++) {
  const page = await parsed.getPage(i);
  const tc = await page.getTextContent();
  const text = tc.items.map((x) => x.str).join(' ');
  const bodyText = text.replace(headerNoise, ' ').replace(/\s+/g, ' ').trim();
  if (bodyText.length < 40) {
    emptyPageReport.push({ page: i, bodyChars: bodyText.length, preview: bodyText.slice(0, 80) });
  }
}
if (emptyPageReport.length) {
  console.error('EMPTY_PAGES_DETECTED', JSON.stringify(emptyPageReport));
  throw new Error(`PDF has ${emptyPageReport.length} empty page(s): ${emptyPageReport.map((p) => p.page).join(', ')}`);
}

fs.mkdirSync(path.dirname(outPrimary), { recursive: true });
fs.mkdirSync(path.dirname(outSecondary), { recursive: true });
fs.writeFileSync(outPrimary, buf);
fs.writeFileSync(outSecondary, buf);

const verifyDoc = await pdfjs.getDocument({ data: new Uint8Array(buf), useSystemFonts: true }).promise;
const ascii = buf.toString('latin1');
const hasFigtree = /Figtree/i.test(ascii);
const hasSyne = /Syne/i.test(ascii);
const hasFontFile = /\/FontFile2\b/.test(ascii);
const secondaryMatch = fs.readFileSync(outSecondary).equals(buf);
console.log(JSON.stringify({
  primary: outPrimary,
  secondary: outSecondary,
  bytes: buf.length,
  pages: verifyDoc.numPages,
  emptyPages: emptyPageReport.length,
  skippedEmptyBreaks,
  autoPagesAdded,
  hasFigtree,
  hasSyne,
  hasFontFile,
  localCopiesMatch: fs.readFileSync(outPrimary).equals(buf) && secondaryMatch,
}, null, 2));
