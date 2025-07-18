#!/usr/bin/env python3
"""
Prueba local directa del servicio PDF corregido
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pdf_locally():
    """Prueba el servicio PDF directamente sin usar el servidor web"""
    
    try:
        print("📦 Importando el servicio PDF...")
        from app.services.pdf_service import PDFExportService
        print("✅ Servicio PDF importado correctamente")
        
        # Datos de prueba
        test_data = {
            "title": "Reporte de Prueba Local",
            "subtitle": "Verificación Directa del PDF",
            "headers": ["Item", "Cantidad", "Valor"],
            "rows": [
                ["Item A", "10", "$100"],
                ["Item B", "20", "$200"],
                ["Item C", "15", "$150"]
            ],
            "metrics": {
                "Total Items": "45",
                "Valor Total": "$450",
                "Promedio": "$15"
            },
            "summary": "Este es un reporte generado localmente para verificar el funcionamiento."
        }
        
        print("🔧 Creando instancia del servicio...")
        service = PDFExportService()
        
        print("🎨 Generando PDF...")
        result = service.export_data(test_data, "test_local_corregido")
        
        print(f"✅ PDF generado exitosamente!")
        print(f"📁 Archivo: {result.get('filename', 'N/A')}")
        print(f"📊 Tamaño: {result.get('file_size', 'N/A')} bytes")
        
        # Verificar que el archivo existe
        filename = result.get('filename')
        if filename and os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"✅ Archivo verificado en el sistema")
            print(f"📏 Tamaño real: {file_size:,} bytes")
            print(f"📍 Ubicación: {os.path.abspath(filename)}")
            return True
        else:
            print("❌ El archivo no se encontró en el sistema")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        print("\n🔍 Detalles del error:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("         PRUEBA LOCAL DEL PDF CORREGIDO")
    print("="*60)
    
    success = test_pdf_locally()
    
    if success:
        print("\n🎉 ¡Prueba local completada exitosamente!")
        print("💡 El PDF se generó correctamente con las correcciones aplicadas")
    else:
        print("\n💥 La prueba local falló")
    
    print("="*60)
