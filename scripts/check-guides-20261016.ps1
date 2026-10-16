$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$site = Join-Path $root 'custom-labels-stickers-website'
$items = Get-Content (Join-Path $root 'content/2026-10-16/manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
[xml]$sitemap = Get-Content (Join-Path $site 'sitemap.xml') -Raw -Encoding UTF8
$urls = @($sitemap.DocumentElement.ChildNodes | ForEach-Object { $_.loc })
if ($urls.Count -ne (@($urls | Select-Object -Unique)).Count) { throw 'Duplicate sitemap URLs' }

foreach ($item in $items) {
    $path = Join-Path $site ($item.slug + '.html')
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing article: $path" }
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $url = 'https://rplabels.com/' + $item.slug
    if (([regex]::Matches($text, '<h1\b')).Count -ne 1) { throw "H1 count: $path" }
    if (-not $text.Contains('<link rel="canonical" href="' + $url + '">')) { throw "Canonical: $path" }
    if (-not $text.Contains('name="description"')) { throw "Meta description: $path" }
    if ($urls -notcontains $url) { throw "Sitemap: $url" }
    $schemas = @([regex]::Matches($text, '(?s)<script type="application/ld\+json">(.*?)</script>') | ForEach-Object { $_.Groups[1].Value | ConvertFrom-Json })
    if (@($schemas | Where-Object { $_.'@type' -eq 'Article' -and $_.datePublished -eq '2026-10-16' }).Count -ne 1) { throw "Article schema: $path" }
    if (@($schemas | Where-Object { $_.'@type' -eq 'BreadcrumbList' }).Count -ne 1) { throw "Breadcrumb schema: $path" }
    $ids = @([regex]::Matches($text, 'id="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    if ($ids.Count -ne @($ids | Select-Object -Unique).Count) { throw "Duplicate IDs: $path" }
    if ($text -match '<style\b|\sstyle=|\son\w+=') { throw "Inline CSS/handler: $path" }
    foreach ($m in [regex]::Matches($text, '(?:href|src)="([^"]+)"')) {
        $value = [System.Net.WebUtility]::HtmlDecode($m.Groups[1].Value)
        if ($value -match '^(https?:|mailto:|tel:|data:)') { continue }
        if ($value.StartsWith('#')) {
            if ($ids -notcontains $value.Substring(1)) { throw "Broken fragment $value on $path" }
            continue
        }
        $relative = ($value -split '[?#]')[0].TrimStart('/')
        $target = if ($relative) { Join-Path $site $relative } else { Join-Path $site 'index.html' }
        if (-not [IO.Path]::GetExtension($target)) { $target += '.html' }
        if (-not (Test-Path -LiteralPath $target)) { throw "Broken local link $value on $path" }
    }
    foreach ($hub in @('blog.html','site-map.html',($item.categoryUrl + '.html'))) {
        if (-not ([IO.File]::ReadAllText((Join-Path $site $hub))).Contains('/' + $item.slug)) { throw "Missing hub link $hub -> $($item.slug)" }
    }
    $plain = [regex]::Replace($text, '(?s)<script\b.*?</script>', ' ')
    $plain = [regex]::Replace($plain, '<[^>]+>', ' ')
    $words = @($plain -split '\s+' | Where-Object { $_ }).Count
    if ($words -lt 850) { throw "Short page $path ($words words)" }
    foreach ($size in @(@('',1536,1024),@('-thumb',768,512))) {
        $imagePath = Join-Path $site ('assets/images/' + $item.image + $size[0] + '.webp')
        if (-not (Test-Path -LiteralPath $imagePath)) { throw "Missing image $imagePath" }
        $dimensions = & magick identify -format '%w %h' $imagePath
        if ($LASTEXITCODE -ne 0 -or $dimensions -ne ($size[1].ToString() + ' ' + $size[2].ToString())) { throw "Bad image dimensions: $imagePath ($dimensions)" }
    }
    Write-Output "$($item.slug): OK, $words words"
}
Write-Output "PASS: five article pages, schemas, links, images and $($urls.Count) unique sitemap URLs"
