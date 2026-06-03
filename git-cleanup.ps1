# One-time cleanup: abort stale rebase, sync local to remote, verify push works
Set-Location $PSScriptRoot

Write-Host "Cleaning up stale git state..." -ForegroundColor Yellow

# Remove all lock files
Get-ChildItem .git\*.lock -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem .git\*.lock.old -ErrorAction SilentlyContinue | Remove-Item -Force

# Abort any in-progress rebase/merge
git rebase --abort 2>$null
git merge --abort 2>$null

# Pull latest from remote and reset local to match
git fetch origin
git reset --hard origin/main

# Verify auth and push (should say "Everything up-to-date")
git push origin main

Write-Host "`nDone. Git state is clean." -ForegroundColor Green
Write-Host "Future auto-blog runs will push automatically." -ForegroundColor Cyan
Read-Host "Press Enter to close"
