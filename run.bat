@echo off
echo Iniciando Export Files Microservice...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias con diferentes estrategias
echo Instalando dependencias...
echo Intentando instalación estándar...

pip install fastapi==0.104.1 uvicorn==0.24.0 fpdf2==2.7.6 python-docx==1.1.0 openpyxl==3.1.2 pydantic==2.5.0 requests==2.31.0

if errorlevel 1 (
    echo.
    echo Error en instalación estándar. Intentando con wheel precompilados...
    pip install --only-binary=all fastapi uvicorn fpdf2 python-docx openpyxl pydantic requests
    
    if errorlevel 1 (
        echo.
        echo Error en instalación con wheels. Intentando sin dependencias problemáticas...
        pip install fastapi uvicorn fpdf2 python-docx openpyxl pydantic requests --no-deps --force-reinstall
        pip install typing-extensions
    )
)

REM Ejecutar el microservicio
echo.
echo Iniciando servidor en http://localhost:8000
echo Presiona Ctrl+C para detener el servidor
echo.
echo Documentacion disponible en:
echo - Swagger UI: http://localhost:8000/docs
echo - ReDoc: http://localhost:8000/redoc
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
