@echo off
echo ========================================
echo Installing Python Dependencies
echo ========================================
echo.

echo Installing required packages...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Core packages installed:
echo   - flask
echo   - flask-cors
echo   - pymongo
echo   - requests
echo.
echo Optional ML packages installed:
echo   - lightgbm
echo   - scikit-learn
echo   - numpy
echo   - pandas
echo.
pause
