# Auto-generated: clears stale git locks and pushes today's blog post
Set-Location $PSScriptRoot

Remove-Item -Force ".git\index.lock" -ErrorAction SilentlyContinue
Remove-Item -Force ".git\HEAD.lock" -ErrorAction SilentlyContinue

git add .
git commit -m "auto-blog: 2026-06-02 [bmw] triple-tipped-spear"
git push

Write-Host "`nDone. Press Enter to close." -ForegroundColor Green
Read-Host
