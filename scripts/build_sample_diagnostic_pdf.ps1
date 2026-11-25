# Build dense branded SynthoSaaS sample diagnostic PDF with embedded Syne + Figtree.
# Entry point: downloads fonts if needed, then runs Node/pdfkit builder.
$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$fontsDir = Join-Path $root "assets\fonts"
$pdfTools = Join-Path $PSScriptRoot "pdf-tools"
$builder = Join-Path $PSScriptRoot "build_sample_diagnostic_pdf.mjs"

New-Item -ItemType Directory -Force -Path $fontsDir | Out-Null

$fontUrls = @{
  "Figtree-Regular.ttf" = "https://cdn.jsdelivr.net/fontsource/fonts/figtree@5.2.5/latin-400-normal.ttf"
  "Figtree-Bold.ttf"    = "https://cdn.jsdelivr.net/fontsource/fonts/figtree@5.2.5/latin-700-normal.ttf"
  "Syne-Bold.ttf"       = "https://cdn.jsdelivr.net/fontsource/fonts/syne@5.2.5/latin-700-normal.ttf"
  "Syne-Regular.ttf"    = "https://cdn.jsdelivr.net/fontsource/fonts/syne@5.2.5/latin-400-normal.ttf"
}

foreach ($name in $fontUrls.Keys) {
  $dest = Join-Path $fontsDir $name
  if (-not (Test-Path $dest) -or (Get-Item $dest).Length -lt 1000) {
    Write-Host "Downloading $name ..."
    & curl.exe -fsSL --retry 3 -o $dest $fontUrls[$name]
  }
}

if (-not (Test-Path (Join-Path $pdfTools "node_modules\pdfkit"))) {
  New-Item -ItemType Directory -Force -Path $pdfTools | Out-Null
  Push-Location $pdfTools
  if (-not (Test-Path "package.json")) { npm init -y | Out-Null }
  npm install pdfkit@0.15.2 --no-fund --no-audit
  Pop-Location
}

# Ensure Node can resolve pdfkit from pdf-tools
$env:NODE_PATH = Join-Path $pdfTools "node_modules"
Write-Host "Building dense PDF with embedded Syne + Figtree ..."
& node $builder
if ($LASTEXITCODE -ne 0) { throw "PDF build failed with exit $LASTEXITCODE" }

$outs = @(
  (Join-Path $root "downloads\sample-cloud-ai-cost-governance-diagnostic.pdf"),
  (Join-Path $root "resources\sample-diagnostic-deliverable\sample-cloud-ai-cost-governance-diagnostic.pdf")
)
foreach ($p in $outs) {
  if (-not (Test-Path $p)) { throw "Missing output: $p" }
  $bytes = [IO.File]::ReadAllBytes($p)
  $ascii = [Text.Encoding]::ASCII.GetString($bytes)
  $pages = ([regex]::Matches($ascii, '/Type\s*/Page[^s]')).Count
  $fig = $ascii -match 'Figtree'
  $syne = $ascii -match 'Syne'
  $ff = $ascii -match '/FontFile2'
  Write-Host ("OK {0} size={1} pages={2} Figtree={3} Syne={4} FontFile2={5}" -f $p, $bytes.Length, $pages, $fig, $syne, $ff)
}
