param([Parameter(Mandatory = $true)][string[]]$Urls)
$ErrorActionPreference = 'Stop'
$site = 'https://rplabels.com'
$key = '625f7aa89eff4015b2e47a282080fe8f'
$keyLocation = "$site/$key.txt"
$liveKey = Invoke-WebRequest -Uri $keyLocation -UseBasicParsing -TimeoutSec 30
if ($liveKey.StatusCode -ne 200 -or $liveKey.Content.Trim() -ne $key) {
    throw 'The IndexNow ownership file is not live yet. Deploy before submitting.'
}
$liveMap = Invoke-WebRequest -Uri "$site/sitemap.xml" -UseBasicParsing -TimeoutSec 30
[xml]$sitemap = $liveMap.Content
$canonicalUrls = @($sitemap.urlset.url | ForEach-Object { [string]$_.loc })
$urlList = @($Urls | Select-Object -Unique)
foreach ($entry in $urlList) {
    $parsed = [uri]$entry
    if ($parsed.Scheme -ne 'https' -or $parsed.Host -ne 'rplabels.com' -or $parsed.Query -or $parsed.Fragment -or $entry -notin $canonicalUrls) {
        throw "Only canonical URLs in the live sitemap can be submitted: $entry"
    }
    $page = Invoke-WebRequest -Uri $entry -UseBasicParsing -TimeoutSec 30
    if ($page.StatusCode -ne 200) { throw "URL is not live: $entry" }
}
$payload = @{ host = 'rplabels.com'; key = $key; keyLocation = $keyLocation; urlList = $urlList } | ConvertTo-Json -Depth 3
$result = Invoke-WebRequest -Uri 'https://api.indexnow.org/indexnow' -Method Post -ContentType 'application/json; charset=utf-8' -Body $payload -UseBasicParsing -TimeoutSec 30
[pscustomobject]@{ Status = $result.StatusCode; UrlCount = $urlList.Count; Meaning = 'URLs received; crawling and indexing are determined by the search engines.' }
