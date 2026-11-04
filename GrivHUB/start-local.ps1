<#
PowerShell helper to start backend and frontend for GrievHUB on Windows.
Creates .dev/pids.json with PIDs so stop-local.ps1 can stop them.
#>
param(
    [int]$BackendPort = 8005,
    [int]$FrontendPort = 3000
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $root
$env:USE_SQLITE = 'True'

# Check virtual environment in the wrapper root.
$venvPython = Join-Path $root "GrivHUB\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    $venvPython = Join-Path $root ".venv\Scripts\python.exe"
}
if (-not (Test-Path $venvPython)) {
    Write-Host "Virtualenv not found. Creating and installing requirements..."
    python -m venv .venv
    .venv\Scripts\python -m pip install --upgrade pip setuptools wheel
    if (Test-Path "GrivHUB\backend\requirements.txt") {
        .venv\Scripts\python -m pip install -r GrivHUB\backend\requirements.txt
    } elseif (Test-Path "requirements.txt") {
        .venv\Scripts\python -m pip install -r requirements.txt
    }
    $venvPython = Join-Path $root ".venv\Scripts\python.exe"
}

# Ensure .dev directory
$devDir = Join-Path $root ".dev"
if (-not (Test-Path $devDir)) { New-Item -ItemType Directory -Path $devDir | Out-Null }

# Avoid duplicate/stale services when the launcher is run again.
$pidsPath = Join-Path $devDir 'pids.json'
if (Test-Path $pidsPath) {
    & (Join-Path $root 'stop-local.ps1')
    Start-Sleep -Seconds 1
}

$pids = @{ }

# Start backend: Django runserver on port $BackendPort
$appDir = Join-Path $root "GrivHUB"
$backendProc = Start-Process -FilePath $venvPython -ArgumentList 'manage.py', 'runserver', "127.0.0.1:$BackendPort", '--noreload' -WorkingDirectory $appDir -PassThru -WindowStyle Hidden
$pids['backend'] = $backendProc.Id
Write-Host "Started backend (PID $($backendProc.Id)) on port $BackendPort"

# Start frontend: Vite dev server on port $FrontendPort
$nodeExe = "C:\Program Files\nodejs\node.exe"
$viteScript = Join-Path $appDir "node_modules\vite\bin\vite.js"
if (-not (Test-Path $nodeExe)) {
    throw "Node.js executable not found at $nodeExe. Install Node.js LTS first."
}
if (-not (Test-Path $viteScript)) {
    throw "Vite executable not found at $viteScript. Run npm install in $appDir."
}
$frontendArgs = @(
    "`"$viteScript`"",
    '--port',
    $FrontendPort.ToString(),
    '--host',
    '0.0.0.0'
)
$frontendProc = Start-Process -FilePath $nodeExe -ArgumentList $frontendArgs -WorkingDirectory $appDir -PassThru
$pids['frontend'] = $frontendProc.Id
Write-Host "Started frontend (PID $($frontendProc.Id)) on port $FrontendPort"

# Save pids
$pids | ConvertTo-Json | Out-File -FilePath $pidsPath -Encoding utf8
Write-Host "PIDs recorded in $pidsPath"

Write-Host "All services started. Open http://localhost:$FrontendPort for frontend and http://localhost:$BackendPort for backend (API)."
