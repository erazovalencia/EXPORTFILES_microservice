@echo off
echo ========================================
echo   EXPORT FILES MICROSERVICE - RUN
echo ========================================

echo.
echo Verificando Docker...

set DOCKER_CMD=docker
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
        set DOCKER_CMD="C:\Program Files\Docker\Docker\resources\bin\docker.exe"
    ) else (
        echo ERROR: Docker no encontrado
        echo Por favor ejecuta docker-build.bat primero
        pause
        exit /b 1
    )
)

echo.
echo Verificando si la imagen existe...
%DOCKER_CMD% images exportfiles_microservice-image -q >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Imagen exportfiles_microservice-image no encontrada
    echo.
    echo Ejecuta primero: docker-build.bat
    echo.
    pause
    exit /b 1
)

echo Imagen encontrada!
echo.

echo Parando contenedores existentes...
%DOCKER_CMD% stop exportfiles_microservice 2>nul
%DOCKER_CMD% rm exportfiles_microservice 2>nul

echo.
echo Ejecutando contenedor...
echo Puerto: 7000
echo Nombre: exportfiles_microservice
echo.

%DOCKER_CMD% run -d ^
  --name exportfiles_microservice ^
  -p 7000:7000 ^
  exportfiles_microservice-image

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================
    echo   CONTENEDOR EJECUTANDOSE
    echo ========================================
    echo.
    echo Servicios disponibles:
    echo - API: http://localhost:7000
    echo - Docs: http://localhost:7000/docs
    echo - Health: http://localhost:7000/api/v1/health
    echo.
    echo Para ver logs:
    echo %DOCKER_CMD% logs -f exportfiles_microservice
    echo.
    echo Para parar:
    echo %DOCKER_CMD% stop exportfiles_microservice
    echo.
) else (
    echo.
    echo ERROR: No se pudo ejecutar el contenedor
    echo.
)

pause
