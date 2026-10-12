$ErrorActionPreference = 'Stop'
$pidPath = Join-Path $PSScriptRoot 'artifacts\server.pid'
if (-not (Test-Path -LiteralPath $pidPath)) { Write-Output 'No recorded Seq Lab server.'; exit }
$serverPid = [int](Get-Content -LiteralPath $pidPath)
$process = Get-CimInstance Win32_Process -Filter "ProcessId = $serverPid"
$expected = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if ($process -and $process.ExecutablePath -eq $expected -and $process.CommandLine -match 'uvicorn.*app.main:app.*8765') {
    Get-CimInstance Win32_Process -Filter "ParentProcessId = $serverPid" | Where-Object { $_.CommandLine -match 'uvicorn.*app.main:app.*8765' } | ForEach-Object { Stop-Process -Id $_.ProcessId }
    Stop-Process -Id $serverPid -ErrorAction SilentlyContinue
    Write-Output 'Seq Lab server stopped. Saved projects are retained.'
} elseif ($process) { throw 'Process identity does not match Seq Lab; no process was stopped.' }
Remove-Item -LiteralPath $pidPath
