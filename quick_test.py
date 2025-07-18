import os
import sys

# Añadir el directorio actual al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=== PRUEBA PDF PROFESIONAL ===")

try:
    # Importar el servicio
    from app.services.pdf_service import PDFExportService
    print("✓ Servicio PDF importado correctamente")
    
    # Crear datos de prueba
    data = {
        "title": "Reporte de Ventas",
        "headers": ["Producto", "Cantidad", "Precio"],
        "rows": [
            ["Producto A", "100", "$10.00"],
            ["Producto B", "150", "$15.00"]
        ],
        "metrics": {
            "Total Items": "250",
            "Revenue": "$2,500"
        }
    }
    
    # Crear servicio y generar PDF
    service = PDFExportService()
    result = service.export_data(data, "test_professional")
    
    print(f"✓ PDF generado: {result.get('filename', 'N/A')}")
    print(f"✓ Tamaño: {result.get('file_size', 'N/A')} bytes")
    print("✓ Prueba completada exitosamente")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona Enter para continuar...")
