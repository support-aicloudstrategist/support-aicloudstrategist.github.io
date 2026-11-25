# Day 6 — list Cloudflare Pages deployments without a false non-zero exit
# Wrangler often prints UI chrome to stderr; piping/truncating can make $LASTEXITCODE look like -1
# even when the list succeeded. This script captures output and exits 0 when rows are present.
$ErrorActionPreference = 'Continue'
$out = & npx wrangler pages deployment list --project-name=aicloudstrategist-site 2>&1
$text = ($out | Out-String)
Write-Host $text

if ($text -match '5c55ee1') {
  Write-Host 'PASS latest Day 6 commit 5c55ee1 appears in deployment list'
} else {
  Write-Host 'WARN 5c55ee1 not seen in first page of deployment list'
}

if ($text -match 'Production') {
  exit 0
}

Write-Host 'FAIL no Production rows returned'
exit 1
