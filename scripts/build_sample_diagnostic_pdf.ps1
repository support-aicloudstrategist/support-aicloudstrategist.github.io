# Build branded SynthoSaaS sample diagnostic PDF (no Python required).
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outPdf = Join-Path $root "downloads\sample-cloud-ai-cost-governance-diagnostic.pdf"
$logoPath = Join-Path $root "assets\brand\aics-brand-mark-nav.png"

# --- Logo bytes (nav teal mark; embed as JPEG on white for PDF simplicity) ---
$img = [System.Drawing.Image]::FromFile($logoPath)
[int]$logoW = $img.Width
[int]$logoH = $img.Height
$ms = New-Object System.IO.MemoryStream
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
$ep = New-Object System.Drawing.Imaging.EncoderParameters(1)
$ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 92L)
[int]$embedW = [Math]::Max($logoW, 320)
[int]$embedH = [Math]::Max($logoH, 320)
$bmp = New-Object System.Drawing.Bitmap($embedW, $embedH)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.Clear([System.Drawing.Color]::White)
$g.DrawImage($img, 0, 0, $embedW, $embedH)
$logoW = $embedW
$logoH = $embedH
$g.Dispose()
$bmp.Save($ms, $codec, $ep)
$logoBytes = $ms.ToArray()
$bmp.Dispose(); $img.Dispose(); $ms.Dispose()

function Esc([string]$s) {
  return ($s -replace '\\', '\\' -replace '\(', '\(' -replace '\)', '\)')
}

[double]$pageWidth = 595.28
[double]$pageHeight = 841.89
[double]$marginL = 36
[double]$marginR = 36
[double]$marginT = 56
[double]$marginB = 40
[double]$contentW = $pageWidth - $marginL - $marginR

$script:allPages = New-Object System.Collections.Generic.List[object]
$script:pb = $null

function New-PageBuilder {
  return [ordered]@{ lines = New-Object System.Collections.Generic.List[string]; y = ($pageHeight - $marginT) }
}

function Add-Raw($pb, [string]$op) { [void]$pb.lines.Add($op) }

function Ensure-Space($pb, [double]$need) {
  if ($pb.y - $need -lt $marginB + 12) { return $false }
  return $true
}

function Start-Document {
  $script:pb = New-PageBuilder
  Draw-Header $script:pb
}

function Flush-Page {
  if ($script:pb -and $script:pb.lines.Count -gt 0) {
    [void]$script:allPages.Add($script:pb)
  }
}

function New-Page {
  Flush-Page
  $script:pb = New-PageBuilder
  Draw-Header $script:pb
}

function Need-Space([double]$need) {
  if (-not (Ensure-Space $script:pb $need)) { New-Page }
}

function Draw-Header($pb) {
  [double]$logoSize = 20
  [double]$lx = $marginL
  [double]$ly = $pageHeight - 32
  Add-Raw $pb "q"
  Add-Raw $pb ("{0:0.###} 0 0 {0:0.###} {1:0.###} {2:0.###} cm" -f $logoSize, $lx, ($ly - $logoSize))
  Add-Raw $pb "/ImLogo Do"
  Add-Raw $pb "Q"
  Text $pb "F2" 10 ($lx + 26) ($ly - 13) "AICloudStrategist"
  [double]$metaX = $pageWidth - $marginR - 125
  Text $pb "F1" 7 $metaX ($ly - 8) "Synthetic data, real structure"
  Text $pb "F1" 7 $metaX ($ly - 17) "Sample diagnostic deliverable"
  Add-Raw $pb "0.033 0.475 0.537 RG 1.2 w"
  Add-Raw $pb ("{0:0.###} {1:0.###} m {2:0.###} {1:0.###} l S" -f $marginL, ($ly - 22), ($pageWidth - $marginR))
  Add-Raw $pb "0 0 0 RG"
  $pb.y = $ly - 32
}

function Draw-Footer($pb, [int]$pageNum, [int]$pageCount) {
  $fy = 26
  Add-Raw $pb "0.6 w 0.55 0.6 0.65 RG"
  Add-Raw $pb ("{0:0.###} {1:0.###} m {2:0.###} {1:0.###} l S" -f $marginL, 36, ($pageWidth - $marginR))
  Add-Raw $pb "0 0 0 RG"
  Text $pb "F1" 6 $marginL $fy "AICLOUDSTRATEGIST PRIVATE LIMITED  |  CIN U62020DC2026PTC470945"
  Text $pb "F1" 6 ($pageWidth - $marginR - 210) $fy ("Page {0} of {1}  |  aicloudstrategist.com/request-fit-review/" -f $pageNum, $pageCount)
}

function Text($pb, [string]$font, [double]$size, [double]$x, [double]$y, [string]$text, [double[]]$rgb = $null) {
  if ($rgb) {
    Add-Raw $pb ("BT /{0} {1:0.###} Tf {2:0.###} {3:0.###} {4:0.###} rg {5:0.###} {6:0.###} Td ({7}) Tj 0 0 0 rg ET" -f $font, $size, $rgb[0], $rgb[1], $rgb[2], $x, $y, (Esc $text))
  } else {
    Add-Raw $pb ("BT /{0} {1:0.###} Tf {2:0.###} {3:0.###} Td ({4}) Tj ET" -f $font, $size, $x, $y, (Esc $text))
  }
}

function Wrap-Lines([string]$text, [int]$maxChars) {
  $words = $text -split '\s+'
  $lines = New-Object System.Collections.Generic.List[string]
  $cur = ""
  foreach ($w in $words) {
    $trial = if ($cur) { "$cur $w" } else { $w }
    if ($trial.Length -gt $maxChars -and $cur) {
      [void]$lines.Add($cur)
      $cur = $w
    } else { $cur = $trial }
  }
  if ($cur) { [void]$lines.Add($cur) }
  return $lines
}

function Para([string]$text, [double]$size = 9, [string]$font = "F1", [int]$maxChars = 94, [double]$leading = 11) {
  foreach ($line in (Wrap-Lines $text $maxChars)) {
    Need-Space $leading
    Text $script:pb $font $size $marginL $script:pb.y $line
    $script:pb.y -= $leading
  }
}

function Spacer([double]$pts) { $script:pb.y -= $pts }

function Heading([string]$eyebrow, [string]$title) {
  $remaining = $script:pb.y - $marginB
  if ($remaining -lt 420) { New-Page }
  Need-Space 40
  Text $script:pb "F2" 7.5 $marginL $script:pb.y $eyebrow @(0.033, 0.475, 0.537)
  $script:pb.y -= 11
  Text $script:pb "F2" 12.5 $marginL $script:pb.y $title @(0.039, 0.094, 0.157)
  $script:pb.y -= 14
}

function Bullet([string]$text, [double]$leading = 10) {
  Need-Space $leading
  Text $script:pb "F1" 8.5 $marginL $script:pb.y $text
  $script:pb.y -= $leading
}

function Subhead([string]$text) {
  Need-Space 14
  Text $script:pb "F2" 8.5 $marginL $script:pb.y $text
  $script:pb.y -= 11
}

function Draw-Table([string[]]$headers, [object[][]]$rows, [double[]]$colWidths) {
  $rowH = 16
  $headerH = 17
  $x0 = $marginL
  $minNeed = $headerH + [Math]::Min($rows.Count * $rowH, 80) + 6
  Need-Space $minNeed

  function Draw-TableHeader {
    param($top)
    $bottom = $top - $headerH
    Add-Raw $script:pb "0.039 0.094 0.157 rg"
    Add-Raw $script:pb "{0:0.###} {1:0.###} {2:0.###} {3:0.###} re f" -f $x0, $bottom, $contentW, $headerH
    Add-Raw $script:pb "1 1 1 rg"
    $x = $x0 + 3
    for ($i = 0; $i -lt $headers.Count; $i++) {
      Text $script:pb "F2" 6.5 $x ($bottom + 4) $headers[$i]
      $x += $colWidths[$i]
    }
    Add-Raw $script:pb "0 0 0 rg"
    $script:pb.y = $bottom
  }

  Draw-TableHeader $script:pb.y

  $rIdx = 0
  foreach ($row in $rows) {
    if (-not (Ensure-Space $script:pb ($rowH + 8))) {
      New-Page
      Draw-TableHeader $script:pb.y
    }
    $top = $script:pb.y
    $bottom = $top - $rowH
    if ($rIdx % 2 -eq 0) {
      Add-Raw $script:pb "0.96 0.97 0.98 rg"
      Add-Raw $script:pb "{0:0.###} {1:0.###} {2:0.###} {3:0.###} re f" -f $x0, $bottom, $contentW, $rowH
      Add-Raw $script:pb "0 0 0 rg"
    }
    Add-Raw $script:pb "0.6 w 0.7 0.75 0.8 RG"
    Add-Raw $script:pb "{0:0.###} {1:0.###} {2:0.###} {3:0.###} re S" -f $x0, $bottom, $contentW, $rowH
    Add-Raw $script:pb "0 0 0 RG"
    $x = $x0 + 3
    for ($i = 0; $i -lt $row.Count; $i++) {
      $cell = [string]$row[$i]
      if ($cell.Length -gt 48) { $cell = $cell.Substring(0, 46) + ".." }
      Text $script:pb "F1" 6.5 $x ($bottom + 3.5) $cell
      $x += $colWidths[$i]
    }
    $script:pb.y = $bottom
    $rIdx++
  }
  $script:pb.y -= 6
}

# -------- Dense continuous document --------
Start-Document

Text $script:pb "F2" 7.5 $marginL $script:pb.y "CLOUD & AI COST GOVERNANCE DIAGNOSTIC" @(0.033, 0.475, 0.537)
$script:pb.y -= 12
Text $script:pb "F2" 16 $marginL $script:pb.y "Sample diagnostic pack"
$script:pb.y -= 16
Text $script:pb "F2" 16 $marginL $script:pb.y "SynthoSaaS (synthetic estate)"
$script:pb.y -= 18
Para "Fixed-fee illustrative deliverable for CTO / CFO buyers. Shows ownership, waste, safe cuts, GPU/LLM spend, and multi-cloud gaps using one fictional company. Structure matches a real engagement."
Spacer 4

$boxY = $script:pb.y - 44
$boxW = ($contentW - 12) / 3
$labels = @(
  @("SynthoSaaS", "Series B SaaS - fictional"),
  @("USD 186,400", "Synthetic Aug 2026 bill"),
  @("AWS + Azure", "EKS / GPU / LLM APIs")
)
for ($i = 0; $i -lt 3; $i++) {
  $bx = $marginL + $i * ($boxW + 6)
  Add-Raw $script:pb "0.91 0.96 0.97 rg"
  Add-Raw $script:pb "0.033 0.475 0.537 RG 0.8 w"
  Add-Raw $script:pb "{0:0.###} {1:0.###} {2:0.###} 44 re B" -f $bx, $boxY, $boxW
  Add-Raw $script:pb "0 0 0 rg 0 0 0 RG"
  Text $script:pb "F2" 10 ($bx + 6) ($boxY + 26) $labels[$i][0]
  Text $script:pb "F1" 6.5 ($bx + 6) ($boxY + 12) $labels[$i][1]
}
$script:pb.y = $boxY - 14

Subhead "Pack contents (7 sections)"
foreach ($t in @(
  "01  Executive summary - buyer answers first",
  "02  Evidence register - what was reviewed",
  "03  Cost ownership map - who owns each dollar",
  "04  Allocation-gap table - contested / unallocated spend",
  "05  Risk and confidence matrix - what is safe to cut",
  "06  Act / Investigate / Hold register - decisions with owners",
  "07  30-day action plan - client-owned next moves"
)) { Bullet $t 10 }
Spacer 6
Para "Currency note: All dollar amounts are synthetic USD for one illustrative billing period (1-31 Aug 2026). Not benchmarks, forecasts, or savings guarantees."
Spacer 4
Para "Label: Synthetic data, real structure."
Spacer 6
Subhead "Fictional estate snapshot (SynthoSaaS)"
Draw-Table @("Dimension","Synthetic value","Notes") @(
  @("Headcount band","~180 FTE","Product-led SaaS; eng-heavy"),
  @("Primary workloads","API + data plane","EKS-hosted microservices"),
  @("ML footprint","GPU pool + LLM APIs","23% of Aug bill combined"),
  @("Forecast discipline","Monthly","MoM +12% triggered diagnostic"),
  @("Tagging maturity","Partial","Azure stronger than shared EKS"),
  @("Buyer sponsor","CTO + CFO joint","Ownership before cuts")
) @(115, 115, 274)

Spacer 10
Heading "01  EXECUTIVE SUMMARY" "What finance and engineering should see first"
Para "Decision question: Who owns the month-over-month cloud and GPU rise before SynthoSaaS cuts anything?"
Spacer 3
Para "Synthetic MoM spend rose about 12%. Growth concentrates in shared EKS, GPU retention after experiments, and LLM inference without a clear product owner. Checkout/API compute is owned and actionable. Production downsizing without SLO evidence stays on Hold."
Spacer 3
Draw-Table @("Signal","Synthetic figure","Buyer takeaway") @(
  @("Reconciled bill","USD 186,400","Single-period baseline for ownership work"),
  @("Assigned ownership","61%","Bankable only where owner + confidence exist"),
  @("Shared / contested","24%","Investigate before forecasting cuts"),
  @("Unallocated gap","15%","Name the gap - do not average it away"),
  @("Register posture","4 Act / 4 Inv / 3 Hold","Hold stays visible under pressure")
) @(115, 105, 289)
Spacer 4
Draw-Table @("MoM driver","Synthetic delta","Primary evidence") @(
  @("Shared EKS growth","+USD 3,100","E-02, E-03"),
  @("GPU retention","+USD 2,400","E-04"),
  @("LLM inference","+USD 1,800","E-05"),
  @("Non-prod idle","+USD 1,200","E-01"),
  @("Product API (owned)","+USD 900","E-02"),
  @("Networking egress","+USD 650","E-02")
) @(125, 95, 289)
Subhead "Where waste shows up"
foreach ($b in @(
  "- Non-prod overnight idle without a product owner",
  "- Orphaned GPU volumes after experiment end dates",
  "- Sandbox accounts without budget caps"
)) { Bullet $b 10 }
Spacer 2
Subhead "30-day posture"
foreach ($b in @(
  "- Act on high-confidence idle waste",
  "- Investigate EKS split rules and LLM token owners",
  "- Hold prod/GPU cuts until evidence holds"
)) { Bullet $b 10 }

Spacer 10
Draw-Table @("Deliverable","Audience","Format in pack") @(
  @("Executive + registers","CTO / CFO","Tables + short narrative"),
  @("Ownership + gap tables","FinOps + platform","Bankable vs contested USD"),
  @("Act / Inv / Hold","Engineering leads","Owner + evidence ID per row"),
  @("30-day plan","Client PMO","Client-owned milestones only")
) @(155, 130, 244)
Spacer 8
Heading "02  EVIDENCE REGISTER" "What was reviewed (synthetic exports only)"
Para "No production credentials. Evidence IDs are fictional labels showing how a real pack cites sources so finance and engineering argue from the same record."
Spacer 3
Draw-Table @("ID","Source","Scope","Period","Conf") @(
  @("E-01","AWS CUR export (synthetic)","All linked accounts","Aug 2026","High"),
  @("E-02","Cost Explorer by service","MoM delta view","Jul-Aug 2026","High"),
  @("E-03","EKS namespace label dump","Shared platform cluster","2026-08-28","Med"),
  @("E-04","GPU job metadata CSV","Training pool","Aug 2026","Med"),
  @("E-05","LLM API vendor invoice","Inference tokens","Aug 2026","High"),
  @("E-06","Azure subscription export","Secondary region apps","Aug 2026","Med"),
  @("E-07","Owner roster (notes)","Product / platform / ML","Intake","Med")
) @(34, 158, 128, 88, 92)
Spacer 3
Para "FinOps note: Tools can show the bill. This register shows which exports underpin each decision."
Spacer 4
Draw-Table @("Stakeholder","Care about","Section to open first") @(
  @("CFO","Bankable vs contested USD","Exec summary + ownership map"),
  @("CTO","Blast radius of Acts","Risk matrix + Hold register"),
  @("Platform lead","EKS + sandbox gaps","Allocation-gap table"),
  @("ML Ops","GPU idle policy","Ownership map + register A3/H2"),
  @("FinOps analyst","Evidence trail","Evidence register + Act rows")
) @(95, 155, 264)
Spacer 4
Draw-Table @("Handling rule","Applies to","Rationale") @(
  @("Single billing period lock","All USD rows","Avoid MoM noise in ownership %"),
  @("Evidence ID on every Act row","Register section","Audit trail for finance sign-off"),
  @("No credential collection in sample","This PDF","Real pack uses client-owned exports"),
  @("Hold list is published","Week 1 governance","Prevents silent scope creep on cuts")
) @(130, 115, 254)
Spacer 8
Heading "03  COST OWNERSHIP MAP" "Who owns every material dollar"
Para "Synthetic multi-cloud estate: AWS-primary (~88%) + Azure secondary (~12%). Totals reconcile to USD 186,400."
Spacer 3
Draw-Table @("Cost pool","Cloud","Owner class","USD","Share","Status") @(
  @("Product API - prod compute","AWS","Assigned / Product Eng","52,100","28%","Assigned"),
  @("Customer data plane","AWS","Assigned / Data","31,400","17%","Assigned"),
  @("Shared EKS platform","AWS","Shared / Platform","28,900","16%","Contested"),
  @("GPU training pool","AWS","Shared / ML Ops","24,700","13%","Policy gap"),
  @("LLM inference APIs","Vendor","Assigned / AI Prod","18,200","10%","Owner thin"),
  @("Non-prod + sandbox","AWS","Unallocated gap","16,800","9%","Gap"),
  @("Networking / egress","AWS","Shared / Platform","8,600","5%","Investigate"),
  @("Azure app / misc","Azure","Assigned / Product","5,700","3%","Assigned")
) @(138, 48, 128, 50, 40, 86)
Spacer 2
Subhead "Buyer answers this map unlocks"
Para "Ownership: 61% named; 39% shared or gap - not one 'cloud waste' number."
Para "GPU / AI spend: Training + LLM APIs = 23% of bill; idle policy and token ownership are blockers."
Para "Multi-cloud: Azure is small but tagged; AWS shared platform is where attribution breaks."
Spacer 4
Draw-Table @("Status","Meaning for finance","Typical next step") @(
  @("Assigned","Forecastable with named owner","Track in unit economics"),
  @("Contested","USD real; split rule missing","Investigate before target setting"),
  @("Gap","No owner class","Name owner in intake workshop"),
  @("Policy gap","Technical owner; policy thin","ML/platform policy ticket")
) @(72, 175, 266)
Spacer 8
Heading "04  ALLOCATION-GAP TABLE" "Contested and unallocated spend - named, not averaged"
Draw-Table @("Gap","Est. USD","Why it blocks cuts","Owner to name","Ev") @(
  @("EKS namespaces w/o chargeback","14,200","3 products share ingress; no split","Platform + FinOps","E-03"),
  @("GPU nodes past experiment end","9,800","Jobs owned; idle policy is not","ML Ops","E-04"),
  @("Non-prod overnight idle","7,400","No product accountable for schedule","Platform Eng","E-01"),
  @("LLM tokens without SKU map","6,100","Invoice exists; commercial owner thin","AI Prod + Fin","E-05"),
  @("Sandbox accounts uncapped","4,900","Spend drifts outside forecast","FinOps","E-01"),
  @("Egress spike - service unknown","3,200","Cannot assign without path attribution","Networking","E-02")
) @(142, 52, 168, 98, 44)
Spacer 3
Para "FinOps vs diagnostic: A FinOps tool surfaces anomalies. This table decides which dollars are not yet bankable until an owner and rule exist."

Spacer 6
Heading "05  RISK & CONFIDENCE MATRIX" "What is safe to cut - and what is not"
Para "Act only when confidence is high and residual risk is low. Hold is a first-class outcome."
Spacer 3
Draw-Table @("Candidate action","Conf","Risk","Safe now?","Rationale") @(
  @("Stop idle non-prod nights","High","Low","Yes - Act","Clear schedule gap; easy rollback"),
  @("Rightsize oversized API ASGs","High","Low","Yes - Act","Utilization evidence; Product-owned"),
  @("Delete orphaned GPU volumes","High","Low","Yes - Act","Past end date; no active jobs"),
  @("Cap sandbox budgets","Med","Low","Yes - Act","Policy change; low blast radius"),
  @("Allocate shared EKS costs","Med","Med","No - Investigate","Needs split rule before banking"),
  @("Trace egress to service","Med","Med","No - Investigate","Attribution incomplete"),
  @("Map LLM tokens to SKU","Med","Med","No - Investigate","Owner roster incomplete"),
  @("Buy RIs / Savings Plans now","Low","High","No - Hold","Commitment before ownership clear"),
  @("Prod downsize without SLO","Low","High","No - Hold","Reliability risk > bill optics"),
  @("Collapse multi-AZ for savings","Low","High","No - Hold","Architecture / DR risk")
) @(158, 38, 38, 82, 191)
Spacer 4
Draw-Table @("Confidence","Definition in this pack","When to use") @(
  @("High","Export + owner agree","Act candidates A1-A3"),
  @("Med","Export solid; owner/rule partial","Investigate I1-I3"),
  @("Low","Commitment or SLO unknown","Hold H1-H3 until clarity")
) @(80, 210, 223)
Spacer 8
Heading "06  ACT / INVESTIGATE / HOLD REGISTER" "Decisions with confidence, risk, and owner"
Draw-Table @("ID","Finding","Conf","Risk","Owner","Next","Ev") @(
  @("A1","Stop idle non-prod nights","High","Low","Platform Eng","Act","E-01"),
  @("A2","Rightsize oversized API ASGs","High","Low","Product Eng","Act","E-02"),
  @("A3","Delete orphaned GPU volumes","High","Low","ML Ops","Act","E-04"),
  @("A4","Cap sandbox account budgets","Med","Low","FinOps","Act","E-01"),
  @("I1","Allocate shared EKS costs","Med","Med","Platform + Fin","Investigate","E-03"),
  @("I2","Trace egress spike to service","Med","Med","Networking","Investigate","E-02"),
  @("I3","LLM token owner unclear","Med","Med","AI Prod + Fin","Investigate","E-05"),
  @("I4","Spot interruption impact","Low","Med","Platform Eng","Investigate","E-01"),
  @("H1","RI / SP purchase now","Low","High","FinOps","Hold","E-01"),
  @("H2","Prod downsize without SLO","Low","High","SRE","Hold","E-07"),
  @("H3","Multi-AZ collapse proposal","Low","High","Architecture","Hold","E-07")
) @(26, 152, 33, 33, 92, 72, 87)
Spacer 2
Para "Illustrative near-term Act candidates (not a savings promise): ASG floors ~USD 28-36k/yr teaching range; orphan cleanup ~USD 9-14k; non-prod idle ~USD 12-18k. Real estates differ."
Spacer 4
Draw-Table @("Posture","Count","USD band (synthetic)","Finance treatment") @(
  @("Act","4","~USD 42-68k annualized equiv.","Include after owner sign-off"),
  @("Investigate","4","~USD 38-51k contested","Exclude from forecast"),
  @("Hold","3","Commitment / SLO exposure","Disclose; no target")
) @(70, 48, 155, 232)

Spacer 10
Heading "07  30-DAY ACTION PLAN" "What the client owns next"
Para "Implementation stays with SynthoSaaS. AICloudStrategist does not execute production changes as part of the diagnostic fee."
Spacer 4
$weeks = @(
  @("Days 1-7  Confirm owners", "Lock owners for Act items A1-A4. Freeze the Hold list so commercial pressure cannot erase H1-H3. Name the EKS split-rule owner."),
  @("Days 8-14  Execute high-confidence Acts", "Run A1/A3 in non-prod with rollback notes. Open Investigate tickets I1-I3. No production GPU changes."),
  @("Days 15-21  Investigate shared platform", "Draft EKS namespace/ingress allocation options. Keep contested dollars out of finance forecasts until the rule is agreed."),
  @("Days 22-30  Hold review + re-measure", "GPU idle policy workshop. Re-measure baseline. Promote Investigate to Act only where evidence and owners now exist.")
)
foreach ($w in $weeks) {
  Need-Space 22
  Text $script:pb "F2" 8.5 $marginL $script:pb.y $w[0] @(0.033, 0.475, 0.537)
  $script:pb.y -= 10
  Para $w[1]
  Spacer 3
}
Draw-Table @("Week","Client deliverable","Success signal") @(
  @("1","Signed owner list A1-A4","No anonymous infra spend in forecast"),
  @("2","Rollback notes for A1/A3","Change tickets linked to evidence"),
  @("3","EKS split options memo","Finance stops allocating contested 16%"),
  @("4","Re-measured Aug-equivalent","Investigate rows promoted or closed")
) @(52, 248, 209)
Subhead "What we typically need from the client"
Draw-Table @("Input","Why","When") @(
  @("Billing export / CUR-equivalent","Reconcile ownership to one period","After fit, under NDA"),
  @("Account list + known product owners","Seed the ownership map","Intake"),
  @("Optional: labels, GPU jobs, model bills","GPU / LLM attribution","If in scope")
) @(175, 198, 136)
Spacer 4
Draw-Table @("Checkpoint","Owner","Exit criteria") @(
  @("Act owners confirmed","Client PMO","A1-A4 named in writing"),
  @("Investigate tickets opened","Platform + Fin","I1-I3 in backlog with dates"),
  @("Hold list ratified","CTO / CFO","H1-H3 unchanged in forecast deck"),
  @("Baseline re-measure","FinOps","Same period definition as diagnostic")
) @(130, 125, 248)

Spacer 10
Heading "BOUNDARIES & NEXT STEP" "Synthetic data, real structure"
Subhead "What this diagnostic does NOT do"
foreach ($b in @(
  "- No production login or credentials required to start",
  "- No savings-share contract and no savings guarantee",
  "- No implementation of cuts inside the diagnostic fee",
  "- Not a statutory financial audit or certification"
)) { Bullet $b 10 }
Spacer 6
Subhead "Primary CTA"
Text $script:pb "F2" 11 $marginL $script:pb.y "Request a diagnostic fit check"
$script:pb.y -= 14
Para "Free suitability call. About two minutes on the form. No billing files required. We respond within one business day (IST)."
Text $script:pb "F1" 8.5 $marginL $script:pb.y "https://aicloudstrategist.com/request-fit-review/" @(0.033, 0.475, 0.537)
$script:pb.y -= 14
Para "SynthoSaaS is fictional. This pack demonstrates deliverable shape for fit-review buyers - not a client endorsement, case study, or promised outcome."
Spacer 6
Need-Space 12
Text $script:pb "F1" 7.5 $marginL $script:pb.y "AICLOUDSTRATEGIST PRIVATE LIMITED  |  contact@aicloudstrategist.com  |  +91 87963 02608"

Flush-Page
$pages = $script:allPages
$pageCount = $pages.Count

for ($i = 0; $i -lt $pageCount; $i++) {
  Draw-Footer $pages[$i] ($i + 1) $pageCount
}

# -------- Assemble PDF --------
function To-Ascii([string]$s) { [System.Text.Encoding]::ASCII.GetBytes($s) }

$objects = New-Object System.Collections.Generic.List[byte[]]
[void]$objects.Add((To-Ascii "<< /Type /Catalog /Pages 2 0 R >>"))
[void]$objects.Add((To-Ascii "PLACEHOLDER_PAGES"))
[void]$objects.Add((To-Ascii "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"))
[void]$objects.Add((To-Ascii "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"))
$imgDict = "<< /Type /XObject /Subtype /Image /Width $logoW /Height $logoH /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length $($logoBytes.Length) >>`nstream`n"
$imgEnd = "`nendstream"
$imgObj = New-Object byte[] ($imgDict.Length + $logoBytes.Length + $imgEnd.Length)
[System.Text.Encoding]::ASCII.GetBytes($imgDict).CopyTo($imgObj, 0)
$logoBytes.CopyTo($imgObj, $imgDict.Length)
[System.Text.Encoding]::ASCII.GetBytes($imgEnd).CopyTo($imgObj, $imgDict.Length + $logoBytes.Length)
[void]$objects.Add($imgObj)

$pageObjIds = New-Object System.Collections.Generic.List[int]

foreach ($pb in $pages) {
  $streamText = $pb.lines -join "`n"
  $streamBytes = [System.Text.Encoding]::ASCII.GetBytes($streamText)
  $content = "<< /Length $($streamBytes.Length) >>`nstream`n" + $streamText + "`nendstream"
  [void]$objects.Add((To-Ascii $content))
  $contentId = $objects.Count

  $pageDict = @"
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 $pageWidth $pageHeight]
/Resources << /Font << /F1 3 0 R /F2 4 0 R >> /XObject << /ImLogo 5 0 R >> >>
/Contents $contentId 0 R >>
"@
  [void]$objects.Add((To-Ascii $pageDict))
  [void]$pageObjIds.Add($objects.Count)
}

$kids = ($pageObjIds | ForEach-Object { "$_ 0 R" }) -join " "
$objects[1] = To-Ascii "<< /Type /Pages /Kids [ $kids ] /Count $($pageObjIds.Count) >>"

$msOut = New-Object System.IO.MemoryStream
$offsets = New-Object System.Collections.Generic.List[long]
function Write-Bytes([byte[]]$b) { $msOut.Write($b, 0, $b.Length) }
function Write-Str([string]$s) { Write-Bytes (To-Ascii $s) }

Write-Str "%PDF-1.4`n%\xE2\xE3\xCF\xD3`n"
for ($i = 0; $i -lt $objects.Count; $i++) {
  [void]$offsets.Add($msOut.Position)
  Write-Str "$($i+1) 0 obj`n"
  Write-Bytes $objects[$i]
  Write-Str "`nendobj`n"
}
$xrefPos = $msOut.Position
Write-Str "xref`n0 $($objects.Count + 1)`n"
Write-Str ("{0:0000000000} {1:00000} f `n" -f 0, 65535)
for ($i = 0; $i -lt $offsets.Count; $i++) {
  Write-Str ("{0:0000000000} {1:00000} n `n" -f $offsets[$i], 0)
}
Write-Str "trailer`n<< /Size $($objects.Count + 1) /Root 1 0 R >>`n"
Write-Str "startxref`n$xrefPos`n%%EOF`n"

[IO.File]::WriteAllBytes($outPdf, $msOut.ToArray())
$msOut.Dispose()
$info = Get-Item $outPdf
Write-Output "Wrote $($info.FullName) ($($info.Length) bytes, $pageCount pages)"
Write-Output "Logo: $logoPath"