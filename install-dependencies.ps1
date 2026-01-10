# Swift AI - Install Python Dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing Python Dependencies" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Upgrading pip..." -ForegroundColor Yellow
py -m pip install --upgrade pip

Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
py -m pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Core packages installed:" -ForegroundColor White
Write-Host "  - flask" -ForegroundColor Gray
Write-Host "  - flask-cors" -ForegroundColor Gray
Write-Host "  - pymongo" -ForegroundColor Gray
Write-Host "  - requests" -ForegroundColor Gray
Write-Host ""
Write-Host "Optional ML packages installed:" -ForegroundColor White
Write-Host "  - lightgbm" -ForegroundColor Gray
Write-Host "  - scikit-learn" -ForegroundColor Gray
Write-Host "  - numpy" -ForegroundColor Gray
Write-Host "  - pandas" -ForegroundColor Gray
Write-Host ""
