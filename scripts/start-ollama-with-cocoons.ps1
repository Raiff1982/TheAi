# Ollama + Cocoon Monitor Startup Script
# Starts Ollama server and cocoon monitor service in parallel
# Usage: .\start-ollama-with-cocoons.ps1

param(
    [string]$Model = "Raiff1982/codette-ultimate-rc-xi-cpu:latest",
    [string]$Port = "11434"
)

Write-Host "[*] Ollama + Cocoon Monitor Startup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check if Ollama is installed
Write-Host ""
Write-Host "[*] Checking Ollama installation..." -ForegroundColor Yellow
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue

if (-not $ollamaPath) {
    Write-Host "[!] Ollama not found! Install from https://ollama.ai" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Ollama found at: $($ollamaPath.Source)" -ForegroundColor Green

# Check if model is available
Write-Host ""
Write-Host "[*] Checking model availability..." -ForegroundColor Yellow

$modelList = ollama list 2>$null

if ($modelList | Select-String -Pattern $Model) {
    Write-Host "[OK] Model '$Model' is available" -ForegroundColor Green
} else {
    Write-Host "[*] Model '$Model' not found locally, pulling..." -ForegroundColor Yellow
    ollama pull $Model
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Failed to pull model" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Model pulled successfully" -ForegroundColor Green
}

# Start Ollama server
Write-Host ""
Write-Host "[*] Starting Ollama server..." -ForegroundColor Yellow

$ollamaProcess = Start-Process -FilePath "ollama" `
    -ArgumentList "serve" `
    -WindowStyle Hidden `
    -PassThru

if ($ollamaProcess) {
    Write-Host "[OK] Ollama server started (PID: $($ollamaProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "[!] Failed to start Ollama server" -ForegroundColor Red
    exit 1
}

# Wait for server to be ready
Write-Host "[*] Waiting for Ollama server to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start monitor service
Write-Host ""
Write-Host "[*] Starting cocoon monitor service..." -ForegroundColor Yellow

$monitorProcess = Start-Process -FilePath "python" `
    -ArgumentList "ollama_monitor_service.py" `
    -WindowStyle Normal `
    -PassThru

if ($monitorProcess) {
    Write-Host "[OK] Monitor service started (PID: $($monitorProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "[!] Failed to start monitor service" -ForegroundColor Red
    exit 1
}

# Display status
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "[OK] System Ready!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Ollama API:     http://localhost:$Port" -ForegroundColor White
Write-Host "  Model:          $Model" -ForegroundColor White
Write-Host "  Cocoon Dir:     cocoons/codette-ultimate/" -ForegroundColor White
Write-Host ""
Write-Host "Usage Example:" -ForegroundColor Cyan
Write-Host "  ollama run $Model" -ForegroundColor White
Write-Host ""
Write-Host "Monitor Status:" -ForegroundColor Cyan
Write-Host "  Ollama PID:     $($ollamaProcess.Id)" -ForegroundColor White
Write-Host "  Monitor PID:    $($monitorProcess.Id)" -ForegroundColor White
Write-Host ""
