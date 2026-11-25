# Day 6 — verify diagnostic page is published (indexable, no draft banner)
# Usage: powershell -File ops/day6-2026-11-25/08-verify-diagnostic-live.ps1
$ErrorActionPreference = 'Stop'
$url = 'https://aicloudstrategist.com/resources/ai-cost-governance-diagnostic/'
$r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
$fail = @()

if ($r.StatusCode -ne 200) { $fail += "HTTP $($r.StatusCode) (expected 200)" }

if ($r.Content -match 'name="robots"\s+content="([^"]+)"') {
  $robots = $Matches[1]
  if ($robots -ne 'index,follow') { $fail += "robots='$robots' (expected index,follow)" }
  else { Write-Host "PASS robots=index,follow" }
} else {
  $fail += 'robots meta missing'
}

if ($r.Content -match '(?i)Draft page|not production-indexed|noindex') {
  $fail += 'draft/noindex text still present on live HTML'
} else {
  Write-Host 'PASS draft banner absent (no Draft page / noindex text)'
}

if ($r.Content -match 'Updated 25 Nov 2026') {
  Write-Host 'PASS publish eyebrow present'
} else {
  Write-Host 'WARN publish eyebrow "Updated 25 Nov 2026" not found (non-blocking)'
}

if ($fail.Count) {
  Write-Host 'FAIL'
  $fail | ForEach-Object { Write-Host " - $_" }
  exit 1
}

Write-Host 'PASS diagnostic page is live and indexable'
exit 0
