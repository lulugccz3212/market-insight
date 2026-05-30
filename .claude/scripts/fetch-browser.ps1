<#
.SYNOPSIS
    使用 Chrome 浏览器 Headers 抓取网页内容，绕过基础 WAF/反爬检测。
    用于替代 WebFetch 访问巴西政府网站 (gov.br, anatel.gov.br 等)。

.PARAMETER Url
    要抓取的网页 URL

.PARAMETER OutFile
    输出文本文件路径 (可选，默认输出到临时文件)

.EXAMPLE
    .\.claude\scripts\fetch-browser.ps1 -Url "https://apps.anatel.gov.br/ParticipaAnatel/"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Url,

    [Parameter(Mandatory=$false)]
    [string]$OutFile
)

$ErrorActionPreference = "Stop"

# Chrome 131 on Windows 的完整浏览器 Headers
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    "Accept-Language" = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    "Cache-Control" = "no-cache"
    "Pragma" = "no-cache"
    "Sec-Ch-Ua" = '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
    "Sec-Ch-Ua-Mobile" = "?0"
    "Sec-Ch-Ua-Platform" = '"Windows"'
    "Sec-Fetch-Dest" = "document"
    "Sec-Fetch-Mode" = "navigate"
    "Sec-Fetch-Site" = "none"
    "Sec-Fetch-User" = "?1"
    "Upgrade-Insecure-Requests" = "1"
}

try {
    $response = Invoke-WebRequest -Uri $Url -Headers $headers -UseBasicParsing -TimeoutSec 30
    $content = $response.Content

    if (-not $content -or $content.Length -lt 100) {
        Write-Error "Fetched content is too short ($($content.Length) bytes) - possible block"
        exit 1
    }

    # Remove scripts and styles, extract text
    $text = $content -replace '<script[^>]*>.*?</script>', ' ' `
                     -replace '<style[^>]*>.*?</style>', ' ' `
                     -replace '<[^>]+>', ' ' `
                     -replace '&nbsp;', ' ' `
                     -replace '&amp;', '&' `
                     -replace '&lt;', '<' `
                     -replace '&gt;', '>' `
                     -replace '&quot;', '"' `
                     -replace '\s+', ' '

    $text = $text.Trim()

    if (-not $OutFile) {
        $OutFile = [System.IO.Path]::GetTempFileName() + ".txt"
    }

    # Ensure output directory exists
    $outDir = Split-Path $OutFile -Parent
    if (-not (Test-Path $outDir)) {
        New-Item -ItemType Directory -Force -Path $outDir | Out-Null
    }

    $text | Out-File -FilePath $OutFile -Encoding utf8

    Write-Output "OK:$($OutFile):$($text.Length)"

} catch {
    Write-Error "Fetch failed: $($_.Exception.Message)"
    exit 1
}
