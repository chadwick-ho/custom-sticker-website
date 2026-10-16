param([switch]$CheckOnly)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$site = Join-Path $root 'custom-labels-stickers-website'
$source = Join-Path $root 'content/2026-10-16'
$items = Get-Content (Join-Path $source 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$date = '2026-10-16'
$displayDate = 'October 16, 2026'
$base = 'https://rplabels.com'
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Read-Text([string]$path) { return [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8) }
function Write-Text([string]$path, [string]$value) {
    if ($CheckOnly) { return }
    [System.IO.File]::WriteAllText($path, $value, $utf8)
}
function Html([string]$value) { return [System.Net.WebUtility]::HtmlEncode($value) }
function Json-Ld($value) {
    $json = ConvertTo-Json -InputObject $value -Depth 15 -Compress
    return '<script type="application/ld+json">' + $json.Replace('</', '<\/') + '</script>'
}
function Link([string]$slug, [string]$title) {
    return '<a href="/' + (Html $slug) + '">' + (Html $title) + '</a>'
}
function Insert-Once([string]$text, [string]$anchor, [string]$addition) {
    if ($text.Contains($addition)) { return $text }
    if (($text.Split(@($anchor), [StringSplitOptions]::None).Count - 1) -ne 1) {
        throw "Expected one anchor: $anchor"
    }
    return $text.Replace($anchor, $addition + $anchor)
}

$template = Read-Text (Join-Path $site 'contact.html')
$header = [regex]::Match($template, '(?s)<header\b.*?</header>').Value
$footer = [regex]::Match($template, '(?s)<footer\b.*?</footer>').Value
if (-not $header -or -not $footer -or $items.Count -ne 5) { throw "Missing layout or five-item manifest: header=$($header.Length), footer=$($footer.Length), items=$($items.Count)" }
$css = '<link rel="stylesheet" href="/assets/css/editorial-guides.css?v=20260927">'

foreach ($item in $items) {
    $url = "$base/$($item.slug)"
    $img = "/assets/images/$($item.image).webp"
    $body = Read-Text (Join-Path $source ($item.slug + '.html'))
    $headings = [System.Collections.Generic.List[object]]::new()
    $body = [regex]::Replace($body, '<h2>(.*?)</h2>', {
        param($m)
        $id = 'section-' + ($headings.Count + 1)
        $headings.Add(@{ id = $id; title = $m.Groups[1].Value })
        return '<h2 id="' + $id + '">' + $m.Groups[1].Value + '</h2>'
    })
    $figure = '<figure class="editorial-photo"><img src="' + $img + '" srcset="' + $img.Replace('.webp','-thumb.webp') + ' 768w, ' + $img + ' 1536w" sizes="(max-width: 900px) calc(100vw - 40px), 850px" alt="' + (Html $item.alt) + '" width="1536" height="1024" loading="eager" fetchpriority="high" decoding="async"><figcaption>' + (Html $item.caption) + '</figcaption></figure>'
    $paras = [regex]::Matches($body, '</p>')
    if ($paras.Count -lt 2) { throw "Too few introduction paragraphs: $($item.slug)" }
    $position = $paras[1].Index + 4
    $body = $body.Insert($position, $figure)
    $article = [ordered]@{
        '@context'='https://schema.org'; '@type'='Article'; headline=$item.title
        description=$item.description; datePublished=$date; dateModified=$date
        inLanguage='en'; mainEntityOfPage=$url
        image=[ordered]@{'@type'='ImageObject';url="$base$img";width=1536;height=1024;caption=$item.caption}
        author=[ordered]@{'@type'='Organization';name='RP Labels';url="$base/about"}
        publisher=[ordered]@{'@type'='Organization';name='RP';url="$base/"}
    }
    $crumbs = [ordered]@{
        '@context'='https://schema.org';'@type'='BreadcrumbList';itemListElement=@(
            [ordered]@{'@type'='ListItem';position=1;name='Home';item="$base/"},
            [ordered]@{'@type'='ListItem';position=2;name='Blog';item="$base/blog"},
            [ordered]@{'@type'='ListItem';position=3;name=$item.title;item=$url}
        )
    }
    $toc = ($headings | ForEach-Object { '<a href="#' + $_.id + '">' + $_.title + '</a>' }) -join ''
    $tags = (@($item.tags) | ForEach-Object { '<span>' + (Html $_) + '</span>' }) -join ''
    $sources = (@($item.sources) | ForEach-Object { '<li><a href="' + (Html $_[1]) + '">' + (Html $_[0]) + '</a></li>' }) -join ''
    $sources = '<section class="editorial-sources"><h2>Sources and scope</h2><p>Reviewed October 16, 2026. The primary references below support the cited technical or regulatory points. The illustrated buying scenarios are editorial guidance, not RP production records, certifications, legal approvals or universal acceptance standards.</p><ul>' + $sources + '</ul></section>'
    $related = (Link $item.categoryUrl $item.category) + ((@($item.related) | ForEach-Object { Link $_[0] $_[1] }) -join '') + (Link 'contact' 'Prepare a custom label inquiry')
    $related = '<div class="article-related"><h2>Related guides and custom options</h2>' + $related + '</div>'
    $safeTitle = Html $item.title
    $safeDesc = Html $item.description
    $safeIntro = Html $item.intro
    $safeCategory = Html $item.category
    $page = @"
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>$(Html $item.seoTitle)</title><meta name="description" content="$safeDesc">
<link rel="canonical" href="$url">
<meta property="og:type" content="article"><meta property="og:title" content="$safeTitle"><meta property="og:description" content="$safeDesc"><meta property="og:url" content="$url"><meta property="og:image" content="$base$img"><meta property="og:image:alt" content="$(Html $item.alt)"><meta property="article:published_time" content="$date">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="$safeTitle"><meta name="twitter:description" content="$safeDesc"><meta name="twitter:image" content="$base$img">
<link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/style.css?v=20260926-planner">$css
$(Json-Ld $article)
$(Json-Ld $crumbs)
</head><body class="article-page editorial-guide">
$header
<main><article><section class="article-hero"><div class="container"><div class="breadcrumbs"><a href="/">Home</a> / <a href="/blog">Blog</a> / $safeCategory</div><span class="eyebrow">$safeCategory</span><h1>$safeTitle</h1><p>$safeIntro</p><p class="article-meta">Published <time datetime="$date">$displayDate</time> - By <a href="/about">RP Labels</a></p><div class="article-tags">$tags</div></div></section>
<section class="section"><div class="container article-layout"><aside class="article-sidebar"><h2>In this guide</h2>$toc</aside><div class="article-content">
$body
$sources
$related
</div></div></section></article></main>
<section class="section section-dark final-cta"><div class="container"><h2>Plan Your Custom Label Order</h2><p>Send your container reference, finished size, quantity per artwork and application method. Ask for a quote and a production-representative sample plan.</p><a class="btn btn-primary" data-whatsapp href="https://wa.me/8613285455519?text=Hi%20RP%20Labels%2C%20I%20saw%20your%20custom%20labels%20on%20rplabels.com.%20I%27d%20like%20a%20quote%20and%20free%20design%20help%20for%20my%20project.%20Can%20we%20chat%3F">Discuss My Label Project</a></div></section>
$footer<script src="/assets/js/main.js?v=20261008-chat"></script></body></html>
"@
    Write-Text (Join-Path $site ($item.slug + '.html')) $page
}

$blogPath = Join-Path $site 'blog.html'
$blog = Read-Text $blogPath
$blog = Insert-Once $blog '</head>' ($css + "`n")
$batchMarker = '<!-- Guides published 2026-10-16 -->'
if (-not $blog.Contains($batchMarker)) {
    $cards = @()
    for ($i=0; $i -lt $items.Count; $i++) {
        $a = $items[$i]
        $load = if ($i -eq 0) { 'loading="eager" fetchpriority="high"' } else { 'loading="lazy"' }
        $cards += '<article class="blog-card blog-photo-card"><a class="blog-card-image" href="/' + $a.slug + '"><img src="assets/images/' + $a.image + '-thumb.webp" alt="' + (Html $a.alt) + '" width="768" height="512" decoding="async" ' + $load + '></a><div class="blog-card-body"><span class="eyebrow">' + (Html $a.category) + '</span><h2>' + (Link $a.slug $a.title) + '</h2><p class="blog-date">Published October 16, 2026</p><p>' + (Html $a.description) + '</p><a class="btn btn-primary" href="/' + $a.slug + '">Read Guide</a></div></article>'
    }
    $anchor = '<div class="container blog-list">'
    if (-not $blog.Contains($anchor)) { throw 'Blog list anchor missing' }
    $blog = $blog.Replace($anchor, $anchor + "`n" + $batchMarker + "`n" + ($cards -join "`n"))
    $list = [ordered]@{'@context'='https://schema.org';'@type'='ItemList';name='RP label guides published October 16, 2026';itemListElement=@()}
    for ($i=0; $i -lt $items.Count; $i++) { $list.itemListElement += [ordered]@{'@type'='ListItem';position=($i+1);name=$items[$i].title;url="$base/$($items[$i].slug)"} }
    $blog = Insert-Once $blog '</head>' ((Json-Ld $list) + "`n")
}
Write-Text $blogPath $blog

$categories = @($items | ForEach-Object categoryUrl | Sort-Object -Unique)
foreach ($cat in $categories) {
    $path = Join-Path $site ($cat + '.html')
    $text = Read-Text $path
    $text = Insert-Once $text '</head>' ($css + "`n")
    $links = (@($items | Where-Object categoryUrl -eq $cat) | ForEach-Object { Link $_.slug $_.title }) -join ''
    $section = '<section class="recent-guide-links"><div class="container"><h2>Production and Purchasing Guides</h2>' + $links + '</div></section>' + "`n"
    $text = Insert-Once $text '</main>' $section
    Write-Text $path $text
}

$path = Join-Path $site 'site-map.html'
$text = Read-Text $path
$links = ($items | ForEach-Object { Link $_.slug $_.title }) -join ''
$addition = '<article class="sitemap-card"><h2>New Guides: October 16, 2026</h2>' + $links + '</article>'
if (-not $text.Contains($addition)) {
    $anchor = '<div class="container sitemap-grid">'
    if (-not $text.Contains($anchor)) { throw 'HTML sitemap anchor missing' }
    $text = $text.Replace($anchor, $anchor + "`n" + $addition)
}
Write-Text $path $text

$path = Join-Path $site 'llms.txt'
$text = Read-Text $path
$addition = "`nGuides published October 16, 2026:`n" + (($items | ForEach-Object { '- ' + $_.title + ': ' + "$base/$($_.slug)" }) -join "`n") + "`n"
if (-not $text.Contains($addition)) { $text += $addition }
Write-Text $path $text

$path = Join-Path $site 'sitemap.xml'
[xml]$xml = Read-Text $path
$ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
$existing = @{}
foreach ($u in $xml.DocumentElement.ChildNodes) { $existing[$u.loc] = $u }
foreach ($slug in (@('blog','site-map') + $categories)) {
    $url = "$base/$slug"
    if (-not $existing.ContainsKey($url)) { throw "Sitemap hub missing: $url" }
    $existing[$url].lastmod = $date
}
foreach ($a in $items) {
    $url = "$base/$($a.slug)"
    if (-not $existing.ContainsKey($url)) {
        $node = $xml.CreateElement('url', $ns)
        foreach ($field in @('loc','lastmod','changefreq','priority')) {
            $child = $xml.CreateElement($field, $ns)
            $child.InnerText = switch ($field) { 'loc' {$url} 'lastmod' {$date} 'changefreq' {'monthly'} 'priority' {'0.8'} }
            [void]$node.AppendChild($child)
        }
        [void]$xml.DocumentElement.AppendChild($node)
    }
}
$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('<?xml version="1.0" encoding="UTF-8"?>')
$lines.Add('<urlset xmlns="' + $ns + '">')
foreach ($u in $xml.DocumentElement.ChildNodes) {
    $line = '  <url>'
    foreach ($field in $u.ChildNodes) { $line += '<' + $field.LocalName + '>' + (Html $field.InnerText) + '</' + $field.LocalName + '>' }
    $lines.Add($line + '</url>')
}
$lines.Add('</urlset>')
Write-Text $path (($lines -join "`n") + "`n")
Write-Output 'Built five article pages and updated blog, three category hubs, XML/HTML sitemap and llms.txt.'
