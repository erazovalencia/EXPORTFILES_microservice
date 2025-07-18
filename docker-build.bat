@echo off
echo ========================================
echo   EXPORT FILES MICROSERVICE - DOCKER
echo ========================================

echo.
echo Verificando Docker...

REM Intentar diferentes rutas de Docker
set DOCKER_CMD=docker
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker no encontrado en PATH, buscando instalaciones...
    
    REM Ruta típica de Docker Desktop
    if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
        set DOCKER_CMD="C:\Program Files\Docker\Docker\resources\bin\docker.exe"
        echo Docker encontrado en Docker Desktop
    ) else if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
        echo Docker Desktop instalado pero no en PATH
        echo Por favor, asegurate de que Docker Desktop este ejecutandose
        echo y que este agregado al PATH del sistema
        pause
        exit /b 1
    ) else (
        echo ERROR: Docker no encontrado
        echo.
        echo Por favor instala Docker Desktop desde:
        echo https://www.docker.com/products/docker-desktop
        echo.
        pause
        exit /b 1
    )
)

echo Docker disponible: %DOCKER_CMD%
echo.

echo Verificando archivos necesarios...
if not exist "requirements.txt" (
    echo ERROR: requirements.txt no encontrado
    pause
    exit /b 1
)

if not exist "Dockerfile" (
    echo ERROR: Dockerfile no encontrado
    pause
    exit /b 1
)

if not exist "app\main.py" (
    echo ERROR: app\main.py no encontrado
    pause
    exit /b 1
)

echo Archivos verificados correctamente
echo.

echo Construyendo imagen Docker...
echo Comando: %DOCKER_CMD% build -t exportfiles_microservice-image .
echo.

%DOCKER_CMD% build -t exportfiles_microservice-image .

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================
    echo   IMAGEN CONSTRUIDA EXITOSAMENTE
    echo ========================================
    echo.
    echo Para ejecutar el contenedor:
    echo %DOCKER_CMD% run -p 7000:7000 exportfiles_microservice-image
    echo.
    echo Para acceder a la documentacion:
    echo http://localhost:7000/docs
    echo.
) else (
    echo.
    echo ========================================
    echo   ERROR EN LA CONSTRUCCION
    echo ========================================
    echo.
    echo Revisa los errores arriba y corrige los problemas
)

echo.
pause
