@echo off
echo Probando Export Files Microservice...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Instalar requests si no está instalado
echo Instalando requests para las pruebas...
pip install requests

echo.
echo Ejecutando pruebas...
echo Asegurate de que el microservicio esté ejecutándose en http://localhost:8000
echo.

python test_microservice.py

echo.
pause
