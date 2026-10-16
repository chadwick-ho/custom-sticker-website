$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $root 'custom-labels-stickers-website/assets/images'
$generated = 'C:\Users\Administrator\.codex\generated_images\019fd604-784a-7710-90dc-ce115cf4ddd4'
$images = [ordered]@{
    'refrigerated-vs-frozen-peptide-vial-labels' = 'exec-e9f0053b-c6ec-4895-9a3a-a321422b5f20.png'
    'mixed-flavor-supplement-sample-kit-labels' = 'exec-2e84177b-4aaf-431f-9d3a-d4efbf306155.png'
    'amber-dropper-bottle-label-oil-residue-proof' = 'exec-fd116008-44aa-4718-a2cf-c018a2fa4116.png'
    'holographic-label-sheets-vs-rolls' = 'exec-6a30d52a-adcc-4473-96a9-89f614c196ed.png'
    'hologram-carton-seal-return-inspection-guide' = 'exec-44d030ee-8c02-4869-9028-0e23b19d7d4a.png'
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
