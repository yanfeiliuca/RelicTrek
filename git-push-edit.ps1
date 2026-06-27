# git-push-edit.ps1 — RelicTrek 页面编辑提交助手
# Claude 在每次编辑完成后会重写 FILES 和 MESSAGE 两个变量。
# 使用方法：在 Terminal 运行  pwsh git-push-edit.ps1

Set-Location $PSScriptRoot

# ── 本次提交配置（由 Claude 在每次编辑完毕后更新）─────────────────────
$MESSAGE = "待更新"
$FILES   = @(
    "待更新"
)
# ──────────────────────────────────────────────────────────────────────

# 清除残留锁文件
Remove-Item -Force ".git/index.lock" -ErrorAction SilentlyContinue
Remove-Item -Force ".git/HEAD.lock"  -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "== RelicTrek git-push-edit ==" -ForegroundColor Cyan
Write-Host "Commit: $MESSAGE" -ForegroundColor Yellow
Write-Host "Files ($($FILES.Count)):" -ForegroundColor Cyan
foreach ($f in $FILES) { Write-Host "  $f" }
Write-Host ""

# 仅 stage 指定文件
foreach ($f in $FILES) {
    git add $f
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: git add 失败 — $f" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
}

# Commit
git commit -m $MESSAGE
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: git commit 失败" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}

# Push
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: git push 失败" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}

Write-Host ""
Write-Host "完成。$($FILES.Count) 个文件已推送。" -ForegroundColor Green
Write-Host "Commit: $MESSAGE" -ForegroundColor Green
Read-Host "按 Enter 关闭"
