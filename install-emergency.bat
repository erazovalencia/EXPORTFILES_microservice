@echo off
echo 🚨 Instalación de EMERGENCIA - Dependencias Básicas
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado
    pause
    exit /b 1
)

echo Instalando dependencias básicas sin versiones específicas...
echo.

echo 1/6 Instalando FastAPI...
pip install fastapi --no-deps
pip install starlette
pip install typing-extensions

echo 2/6 Instalando Uvicorn...
pip install uvicorn --no-deps
pip install click h11 

echo 3/6 Instalando Pydantic v1 (sin Rust)...
pip install "pydantic<2.0"

echo 4/6 Instalando fpdf2...
pip install fpdf2

echo 5/6 Instalando python-docx...
pip install python-docx

echo 6/6 Instalando openpyxl...
pip install openpyxl

echo.
echo 🧪 Probando instalación...
python -c "import fastapi; print('✅ FastAPI OK')"
python -c "import uvicorn; print('✅ Uvicorn OK')" 
python -c "import pydantic; print('✅ Pydantic OK')"
python -c "import fpdf; print('✅ FPDF OK')"
python -c "import docx; print('✅ DOCX OK')"
python -c "import openpyxl; print('✅ OpenPyXL OK')"

echo.
echo 🎉 Instalación básica completada!
echo Ahora puedes probar con: start.bat
echo.
pause
