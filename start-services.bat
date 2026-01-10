@echo off
echo ========================================
echo Swift AI - Fraud Detection System
echo ========================================
echo.

REM Start Banking Service in new window
echo Starting Banking Service on port 5000...
start "Banking Service (Port 5000)" cmd /k "cd banking_service && py app.py"

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Fraud Detection Service in new window
echo Starting Fraud Detection Service on port 5001...
start "Fraud Detection Service (Port 5001)" cmd /k "cd fraud_service && py app.py"

echo.
echo Services Starting...
echo.
echo Banking Service:    http://localhost:5000
echo Fraud Service:      http://localhost:5001
echo Fraud Dashboard:    http://localhost:5001/dashboard
echo.
echo Default Fraud Service Login:
echo   Email:    admin@swiftai.com
echo   Password: admin123
echo.
echo Press any key to exit this window (services will continue running)...
pause >nul
