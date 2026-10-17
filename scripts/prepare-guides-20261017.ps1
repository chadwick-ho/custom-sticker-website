$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $root 'custom-labels-stickers-website/assets/images'
$generated = 'C:\Users\Administrator\.codex\generated_images\019fd604-784a-7710-90dc-ce115cf4ddd4'
$images = [ordered]@{
    'peptide-vial-tray-scan-code-orientation' = 'exec-aab2d3dd-f40a-427e-a64c-143558784d43.png'
    'mixed-vial-research-kit-lot-matching' = 'exec-2bead33e-c773-4666-a504-c6466ecfd002.png'
    'supplement-blister-carton-vs-bottle-labels' = 'exec-21afd8c9-4dc0-485c-9995-aada151163f3.png'
    'supplement-30-vs-60-capsule-count-labels' = 'exec-f589f82d-99be-4cf6-a001-622a19f1be15.png'
    'hologram-seal-kraft-vs-coated-carton' = 'exec-afbe1171-1450-491f-99ca-6317abe7d584.png'
}
foreach ($name in $images.Keys) {
    $inputPath = Join-Path $generated $images[$name]
    if (-not (Test-Path -LiteralPath $inputPath)) { throw "Missing generated image: $inputPath" }
    $full = Join-Path $dest ($name + '.webp')
    $thumb = Join-Path $dest ($name + '-thumb.webp')
    if ((Test-Path -LiteralPath $full) -or (Test-Path -LiteralPath $thumb)) { throw "Will not overwrite image: $name" }
    & magick $inputPath -resize 1536x1024^ -gravity center -extent 1536x1024 -quality 82 $full
    if ($LASTEXITCODE -ne 0) { throw "ImageMagick full-size conversion failed: $name" }
    & magick $inputPath -resize 768x512^ -gravity center -extent 768x512 -quality 78 $thumb
    if ($LASTEXITCODE -ne 0) { throw "ImageMagick thumbnail conversion failed: $name" }
    Write-Output "$name`: $((Get-Item $full).Length) + $((Get-Item $thumb).Length) bytes"
}
