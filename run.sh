#!/bin/bash

echo "Iniciando Export Files Microservice..."
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado"
    exit 1
fi

# Instalar dependencias si no existen
echo "Instalando dependencias..."
pip3 install -r requeriments.txt

# Ejecutar el microservicio
echo
echo "Iniciando servidor en http://localhost:8000"
echo "Presiona Ctrl+C para detener el servidor"
echo
echo "Documentación disponible en:"
echo "- Swagger UI: http://localhost:8000/docs"
echo "- ReDoc: http://localhost:8000/redoc"
echo

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
