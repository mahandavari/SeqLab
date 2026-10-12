param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Python environment is missing. See README.md for setup.' }
if (-not (Test-Path -LiteralPath (Join-Path $root 'frontend\dist\index.html'))) { throw 'The frontend must be built first. See README.md.' }
$url = 'http://127.0.0.1:8765'
$running = $false
try {
    $health = Invoke-RestMethod -Uri "$url/api/health" -TimeoutSec 2
    if ($health.application -ne 'seq-lab') { throw 'Port 8765 is occupied by another application.' }
    $running = $true
} catch {
    if (Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue) { throw 'Port 8765 is occupied. Stop the conflicting application before launching Seq Lab.' }
}
if (-not $running) {
    $logDir = Join-Path $root 'artifacts'
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    $env:SEQ_LAB_DATA = Join-Path $root 'data'
    $process = Start-Process -FilePath $python -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8765','--no-access-log' -WorkingDirectory (Join-Path $root 'backend') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDir 'server.stdout.log') -RedirectStandardError (Join-Path $logDir 'server.stderr.log') -PassThru
    $process.Id | Set-Content -LiteralPath (Join-Path $logDir 'server.pid')
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Milliseconds 300
        if ($process.HasExited) { throw 'Server exited. See artifacts/server.stderr.log.' }
        try { $health = Invoke-RestMethod -Uri "$url/api/health" -TimeoutSec 1; if ($health.application -eq 'seq-lab') { $ready = $true; break } } catch {}
    }
    if (-not $ready) { throw 'The server did not become ready. See artifacts/server.stderr.log.' }
}
Write-Output "Seq Lab is ready at $url"
if (-not $NoBrowser) { Start-Process $url }
