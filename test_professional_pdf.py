#!/usr/bin/env python3
"""
Script de prueba para el PDF profesional mejorado
"""

import sys
import os
import traceback

# Añadir el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.pdf_service import PDFExportService
    print("✓ Importación exitosa del PDFExportService")
    
    # Datos de prueba completos
    test_data = {
        "title": "Reporte Profesional de Ventas Q4 2024",
        "subtitle": "Análisis Detallado de Rendimiento",
        "headers": ["Producto", "Unidades Vendidas", "Revenue", "Margen"],
        "rows": [
            ["Producto Alpha", "1,250", "$125,000", "25%"],
            ["Producto Beta", "890", "$89,000", "22%"],
            ["Producto Gamma", "2,100", "$210,000", "28%"],
            ["Producto Delta", "750", "$75,000", "20%"]
        ],
        "metrics": {
            "Ventas Totales": "4,990",
            "Revenue Total": "$499,000",
            "Crecimiento": "+15.5%",
            "Margen Promedio": "23.75%"
        },
        "summary": "Este reporte muestra un crecimiento sostenido en todas las líneas de productos durante el Q4 2024."
    }
    
    print("✓ Datos de prueba preparados")
    
    # Crear instancia del servicio
    pdf_service = PDFExportService()
    print("✓ Servicio PDF creado")
    
    # Generar PDF
    result = pdf_service.export_data(test_data, "reporte_profesional_q4")
    print(f"✓ PDF generado exitosamente: {result['filename']}")
    print(f"  Tamaño del archivo: {result['file_size']} bytes")
    
    # Verificar que el archivo existe
    if os.path.exists(result['filename']):
        print(f"✓ Archivo verificado en: {result['filename']}")
        file_size = os.path.getsize(result['filename'])
        print(f"  Tamaño real del archivo: {file_size} bytes")
    else:
        print("✗ Error: El archivo no se encontró")
        
except ImportError as e:
    print(f"✗ Error de importación: {e}")
    print("Verificando dependencias...")
    try:
        import fpdf
        print("✓ fpdf disponible")
    except ImportError:
        print("✗ fpdf no está instalado")
    
except Exception as e:
    print(f"✗ Error durante la ejecución: {e}")
    print("\nTraceback completo:")
    traceback.print_exc()

print("\n" + "="*50)
print("Prueba completada")
