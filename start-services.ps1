# Swift AI - Fraud Detection System Startup Script
# This script starts both the Banking Service and Fraud Detection Service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Swift AI - Fraud Detection System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to start a service in a new window
function Start-ServiceInWindow {
    param (
        [string]$ServiceName,
        [string]$Directory,
        [string]$Script,
        [int]$Port
    )
    
    Write-Host "Starting $ServiceName on port $Port..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Directory'; py $Script" -WindowStyle Normal
    Start-Sleep -Seconds 2
}

# Get the project root directory
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Banking Service (Port 5000)
$BankingDir = Join-Path $ProjectRoot "banking_service"
Start-ServiceInWindow -ServiceName "Banking Service" -Directory $BankingDir -Script "app.py" -Port 5000

# Start Fraud Detection Service (Port 5001)
$FraudDir = Join-Path $ProjectRoot "fraud_service"
Start-ServiceInWindow -ServiceName "Fraud Detection Service" -Directory $FraudDir -Script "app.py" -Port 5001

Write-Host ""
Write-Host "Services Starting..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Banking Service:    http://localhost:5000" -ForegroundColor White
Write-Host "Fraud Service:      http://localhost:5001" -ForegroundColor White
Write-Host "Fraud Dashboard:    http://localhost:5001/dashboard" -ForegroundColor White
Write-Host ""
Write-Host "Default Fraud Service Login:" -ForegroundColor Yellow
Write-Host "  Email:    admin@swiftai.com" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this window (services will continue running)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
