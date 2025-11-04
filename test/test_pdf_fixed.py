#!/usr/bin/env python3
"""
Script de prueba rápida para verificar el PDF corregido
"""

import requests
import json

def test_pdf_service():
    """Prueba el servicio PDF con datos de ejemplo"""
    
    # URL del servicio
    url = "http://localhost:7000/api/v1/export"
    
    # Datos de prueba
    test_data = {
        "file_format": "pdf",
        "filename": "test_reporte_corregido",
        "data": {
            "title": "Reporte de Prueba Corregido",
            "subtitle": "Verificación del PDF Profesional",
            "headers": ["Producto", "Ventas", "Revenue"],
            "rows": [
                ["Producto A", "150", "$15,000"],
                ["Producto B", "200", "$25,000"],
                ["Producto C", "100", "$12,500"]
            ],
            "metrics": {
                "Total Ventas": "450",
                "Revenue Total": "$52,500",
                "Promedio": "$17,500"
            },
            "summary": [
                "Este es un reporte de prueba para verificar el PDF corregido.",
                "Las mejoras incluyen diseño profesional y manejo de errores."
            ]
        }
    }
    
    try:
        print("🚀 Enviando solicitud al servicio PDF...")
        response = requests.post(url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ PDF generado exitosamente!")
            print(f"📁 Archivo: {result.get('filename', 'N/A')}")
            print(f"📊 Tamaño: {result.get('file_size', 'N/A')} bytes")
            print(f"🎯 Formato: {result.get('format', 'N/A')}")
            
            # Descargar el archivo
            if 'download_url' in result:
                print(f"🔗 URL de descarga: {result['download_url']}")
            
            return True
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servicio")
        print("💡 Asegúrate de que el servidor esté ejecutándose en http://localhost:7000")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("         PRUEBA DE PDF CORREGIDO")
    print("="*60)
    
    success = test_pdf_service()
    
    if success:
        print("\n🎉 ¡Prueba completada exitosamente!")
    else:
        print("\n💥 La prueba falló. Revisa los errores arriba.")
    
    print("="*60)
