param([Parameter(Mandatory = $true)][string]$Date)
$ErrorActionPreference = 'Stop'
if ($Date -notmatch '^\d{4}-\d{2}-\d{2}$') { throw 'Date must be YYYY-MM-DD' }
$root = Split-Path -Parent $PSScriptRoot
$manifest = Join-Path $root ("content/$Date/manifest.json")
if (-not (Test-Path -LiteralPath $manifest)) { throw "Missing manifest: $manifest" }
$items = Get-Content $manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$urls = @($items | ForEach-Object { 'https://rplabels.com/' + $_.slug })
$urls += @(
    'https://rplabels.com/blog',
    'https://rplabels.com/custom-peptide-vial-labels',
    'https://rplabels.com/custom-supplement-labels',
    'https://rplabels.com/custom-3d-holographic-labels',
    'https://rplabels.com/site-map'
)
& (Join-Path $PSScriptRoot 'Submit-IndexNow.ps1') -Urls $urls
