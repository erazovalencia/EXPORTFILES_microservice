@echo off
echo Export Files Microservice - Inicio Rápido
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo Verificando dependencias...
python check_deps.py

if errorlevel 1 (
    echo.
    echo ❌ Faltan dependencias. Ejecuta install-deps.bat primero.
    pause
    exit /b 1
)

echo.
echo Iniciando microservicio...
echo.
echo Servidor iniciándose en http://localhost:8000
echo.
echo Documentación disponible en:
echo - Swagger UI: http://localhost:8000/docs  
echo - ReDoc: http://localhost:8000/redoc
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
