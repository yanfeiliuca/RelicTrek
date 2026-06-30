# git-push-edit.ps1 — RelicTrek safe manual publish helper
#
# Default behavior is DRY-RUN ONLY. It never commits or pushes unless the caller
# explicitly passes -Commit and/or -Push.
#
# Examples:
#   pwsh git-push-edit.ps1 -Message "Fix page copy" -Files en/page.html zh/page.html
#   pwsh git-push-edit.ps1 -Commit -Message "Fix page copy" -Files en/page.html zh/page.html
#   pwsh git-push-edit.ps1 -Commit -Push -Message "Fix page copy" -Files en/page.html zh/page.html

param(
    [string]$Message = "",
    [string[]]$Files = @(),
    [switch]$Commit,
    [switch]$Push,
    [switch]$AllowSitemap
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Fail($Text) {
    Write-Host "ERROR: $Text" -ForegroundColor Red
    exit 1
}

function RunGit($ArgsList) {
    & git @ArgsList
    if ($LASTEXITCODE -ne 0) {
        Fail "git $($ArgsList -join ' ') failed"
    }
}

Write-Host ""
Write-Host "== RelicTrek safe publish helper ==" -ForegroundColor Cyan

if (-not $Commit -and -not $Push -and $Files.Count -eq 0 -and [string]::IsNullOrWhiteSpace($Message)) {
    Write-Host "No arguments provided. Treating this as a launchd/no-op invocation." -ForegroundColor Yellow
    Write-Host "No git fetch, add, commit, or push was executed." -ForegroundColor Green
    exit 0
}

$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne "main") {
    Fail "expected branch main, got '$branch'"
}

RunGit @("fetch", "origin")

$divergence = (& git rev-list --left-right --count main...origin/main).Trim()
if ($LASTEXITCODE -ne 0) {
    Fail "could not check main...origin/main divergence"
}
if ($divergence -ne "0`t0") {
    Fail "main and origin/main diverged or are not aligned: $divergence"
}

if ($Files.Count -eq 0) {
    Fail "no files were provided. Pass -Files path1 path2 ..."
}

if ([string]::IsNullOrWhiteSpace($Message)) {
    Fail "commit message is empty. Pass -Message '...'"
}

$blockedPrefixes = @(
    "workdocs/",
    "daily_plans/",
    ".codex/",
    ".agents/"
)

$blockedExact = @(
    "CLAUDE.md",
    ".gitignore",
    "PROGRESS.md",
    "git-push-edit.ps1"
)

$allowedPatterns = @(
    "^en/.+\.html$",
    "^zh/.+\.html$",
    "^en/blog/index\.json$",
    "^zh/blog/index\.json$",
    "^\.autoblog-tracker\.json$"
)

if ($AllowSitemap) {
    $allowedPatterns += "^sitemap\.xml$"
}

$normalizedFiles = @()
foreach ($file in $Files) {
    $path = $file.Replace("\", "/").Trim()
    if ([string]::IsNullOrWhiteSpace($path)) {
        Fail "empty file path in -Files"
    }
    if ($path.StartsWith("/") -or $path.Contains("..")) {
        Fail "only repo-relative paths without '..' are allowed: $path"
    }
    foreach ($prefix in $blockedPrefixes) {
        if ($path.StartsWith($prefix)) {
            Fail "blocked private/handoff path: $path"
        }
    }
    if ($blockedExact -contains $path) {
        Fail "blocked file: $path"
    }
    if ($path -eq "sitemap.xml" -and -not $AllowSitemap) {
        Fail "sitemap.xml requires explicit -AllowSitemap"
    }
    $allowed = $false
    foreach ($pattern in $allowedPatterns) {
        if ($path -match $pattern) {
            $allowed = $true
            break
        }
    }
    if (-not $allowed) {
        Fail "file is outside the allowed publish set: $path"
    }
    if (-not (Test-Path -LiteralPath $path)) {
        Fail "file does not exist: $path"
    }
    $normalizedFiles += $path
}

$status = & git status --short
Write-Host "Branch: $branch"
Write-Host "Divergence main...origin/main: $divergence"
Write-Host "Commit message: $Message" -ForegroundColor Yellow
Write-Host "Files ($($normalizedFiles.Count)):" -ForegroundColor Cyan
foreach ($file in $normalizedFiles) {
    Write-Host "  $file"
}
Write-Host ""
Write-Host "Current git status:" -ForegroundColor Cyan
if ($status) {
    $status | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host "  clean"
}

Write-Host ""
Write-Host "Diff summary for requested files:" -ForegroundColor Cyan
& git diff --stat -- @normalizedFiles
if ($LASTEXITCODE -ne 0) {
    Fail "could not show diff stat"
}

if (-not $Commit -and -not $Push) {
    Write-Host ""
    Write-Host "DRY RUN ONLY. No git add, commit, or push was executed." -ForegroundColor Green
    Write-Host "To commit: add -Commit. To commit and push: add -Commit -Push." -ForegroundColor Green
    exit 0
}

if ($Push -and -not $Commit) {
    Fail "-Push requires -Commit in this helper"
}

# ── Anti-Hallucination Gate ───────────────────────────────────────────────────
# Validate every blog HTML file before it can be committed or pushed.
# The validator only acts on en/blog/ and zh/blog/ paths; others are skipped.
$blogFiles = $normalizedFiles | Where-Object { $_ -match "^(en|zh)/blog/.*\.html$" }
if ($blogFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "Anti-hallucination source check..." -ForegroundColor Cyan
    $validatorArgs = @("validate-blog-sources.py") + $blogFiles
    & python3 @validatorArgs
    if ($LASTEXITCODE -ne 0) {
        Fail (
            "Anti-hallucination gate BLOCKED the commit.`n" +
            "Blog file(s) are missing a valid <section class=`"sources-section`"> " +
            "with >= 2 verified external source URLs.`n" +
            "Correct the issues shown above, then re-run this script."
        )
    }
}
# ─────────────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "Staging requested files only..." -ForegroundColor Cyan
RunGit (@("add", "--") + $normalizedFiles)

$staged = & git diff --cached --name-only
if ($LASTEXITCODE -ne 0) {
    Fail "could not inspect staged files"
}

$expected = $normalizedFiles | Sort-Object
$actual = $staged | Sort-Object
if (($expected -join "`n") -ne ($actual -join "`n")) {
    Write-Host "Expected staged files:" -ForegroundColor Yellow
    $expected | ForEach-Object { Write-Host "  $_" }
    Write-Host "Actual staged files:" -ForegroundColor Yellow
    $actual | ForEach-Object { Write-Host "  $_" }
    Fail "staged files do not exactly match requested files"
}

RunGit @("diff", "--cached", "--check")
RunGit @("commit", "-m", $Message)

if ($Push) {
    RunGit @("push", "origin", "main")
    RunGit @("fetch", "origin")
    $after = (& git rev-list --left-right --count main...origin/main).Trim()
    if ($after -ne "0`t0") {
        Fail "post-push divergence is not clean: $after"
    }
    Write-Host "Pushed and verified origin/main." -ForegroundColor Green
} else {
    Write-Host "Committed locally. Push was not requested." -ForegroundColor Green
}
