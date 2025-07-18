@echo off
echo ===================================
echo PRUEBA DEL PDF CORREGIDO VIA API
echo ===================================

echo.
echo Probando endpoint de test PDF...
curl -X POST "http://localhost:7000/api/v1/test/pdf" -H "Content-Type: application/json"

echo.
echo.
echo Probando endpoint de exportacion completa...
curl -X POST "http://localhost:7000/api/v1/export" ^
  -H "Content-Type: application/json" ^
  -d "{\"file_format\": \"pdf\", \"filename\": \"reporte_corregido\", \"data\": {\"title\": \"Reporte de Ventas Corregido\", \"headers\": [\"Producto\", \"Ventas\"], \"rows\": [[\"Producto A\", \"100\"], [\"Producto B\", \"150\"]], \"metrics\": {\"Total\": \"250\"}}}"

echo.
echo ===================================
echo PRUEBA COMPLETADA
echo ===================================
pause
