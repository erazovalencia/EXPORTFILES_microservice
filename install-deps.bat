@echo off
echo Instalación de dependencias para Export Files Microservice
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Actualizar pip y herramientas
echo 1. Actualizando pip y herramientas...
python -m pip install --upgrade pip setuptools wheel

REM Instalar dependencias básicas primero (versiones compatibles)
echo.
echo 2. Instalando FastAPI con versión compatible...
pip install "fastapi>=0.100.0,<0.105.0"

echo.
echo 3. Instalando Uvicorn...
pip install "uvicorn>=0.20.0,<0.25.0"

echo.
echo 4. Instalando Pydantic (versión compatible sin Rust)...
pip install "pydantic>=1.10.0,<2.0.0"

echo.
echo 5. Instalando fpdf2 para PDFs...
pip install fpdf2

echo.
echo 6. Instalando python-docx para Word...
pip install python-docx

echo.
echo 7. Instalando openpyxl para Excel...
pip install openpyxl

echo.
echo 8. Instalando requests para pruebas...
pip install requests

echo.
echo Instalación completada!
echo.

REM Verificar instalación
echo Verificando instalación...
python -c "import fastapi, uvicorn, fpdf, docx, openpyxl, pydantic, requests; print('✅ Todas las dependencias instaladas correctamente')" 2>nul

if errorlevel 1 (
    echo.
    echo ❌ Hubo problemas con algunas dependencias
    echo Intenta ejecutar el microservicio y verifica qué librerías faltan
    echo.
    echo 🔧 Si persisten los problemas, prueba:
    echo    1. Usar wheels precompilados: pip install --only-binary=all fastapi uvicorn pydantic
    echo    2. Usar versiones específicas sin Rust: pip install "pydantic==1.10.12"
) else (
    echo.
    echo ✅ ¡Listo! Puedes ejecutar el microservicio con start.bat
)

pause
