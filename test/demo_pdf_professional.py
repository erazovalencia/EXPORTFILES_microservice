#!/usr/bin/env python3
"""
Script de demostración del PDF profesional mejorado
Muestra todas las nuevas características implementadas
"""

import os
import sys
import json
from datetime import datetime

# Añadir el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "="*60)
    print("         DEMOSTRACIÓN PDF PROFESIONAL MEJORADO")
    print("="*60)
    
    try:
        from app.services.LORA.pdf.all_reports import PDFExportService
        print("✓ Servicio PDF cargado correctamente")
        
        # Datos de demostración completos
        demo_data = {
            "title": "Informe Ejecutivo de Ventas Q4 2024",
            "subtitle": "Análisis Integral de Rendimiento Comercial",
            "company": "TechCorp Solutions",
            "author": "Departamento de Análisis",
            "date": datetime.now().strftime("%d/%m/%Y"),
            
            # Tabla principal de productos
            "headers": ["Producto", "Unidades", "Revenue", "Margen %", "Crecimiento"],
            "rows": [
                ["Smart Widget Pro", "2,450", "$245,000", "28.5%", "+12.3%"],
                ["Digital Assistant", "1,890", "$189,000", "32.1%", "+18.7%"],
                ["Cloud Platform", "3,200", "$480,000", "45.2%", "+25.4%"],
                ["Mobile Suite", "1,650", "$165,000", "22.8%", "+8.9%"],
                ["Enterprise Tools", "980", "$147,000", "38.7%", "+15.2%"]
            ],
            
            # Métricas clave (KPIs)
            "metrics": {
                "Ventas Totales": "10,170 unidades",
                "Revenue Total": "$1,226,000",
                "Crecimiento Anual": "+16.1%",
                "Margen Promedio": "33.5%",
                "Clientes Nuevos": "142",
                "Retención": "94.2%"
            },
            
            # Datos adicionales
            "summary": [
                "El Q4 2024 ha mostrado un crecimiento excepcional del 16.1% respecto al año anterior.",
                "Cloud Platform lidera el crecimiento con un incremento del 25.4% en ventas.",
                "La retención de clientes se mantiene en niveles excelentes (94.2%).",
                "Se han incorporado 142 nuevos clientes durante este período."
            ],
            
            # Información adicional estructurada
            "details": {
                "Regiones": {
                    "América del Norte": "$610,000",
                    "Europa": "$385,000", 
                    "Asia-Pacífico": "$231,000"
                },
                "Canales de Venta": {
                    "Venta Directa": "45%",
                    "Partners": "35%",
                    "Online": "20%"
                }
            }
        }
        
        print("✓ Datos de demostración preparados")
        print(f"  - Productos: {len(demo_data['rows'])}")
        print(f"  - Métricas: {len(demo_data['metrics'])}")
        print(f"  - Regiones: {len(demo_data['details']['Regiones'])}")
        
        # Generar PDF profesional
        service = PDFExportService()
        print("\n🎨 Generando PDF con diseño profesional...")
        
        result = service.export_data(demo_data, "informe_ejecutivo_q4_2024")
        
        print(f"\n✅ PDF GENERADO EXITOSAMENTE")
        print(f"📁 Archivo: {result['filename']}")
        print(f"📊 Tamaño: {result['file_size']:,} bytes")
        
        # Verificar archivo
        if os.path.exists(result['filename']):
            file_size = os.path.getsize(result['filename'])
            print(f"✓ Archivo verificado (tamaño real: {file_size:,} bytes)")
            
            # Mostrar características implementadas
            print(f"\n🎯 CARACTERÍSTICAS PROFESIONALES IMPLEMENTADAS:")
            print("   ➤ Encabezados y pies de página con branding")
            print("   ➤ Esquema de colores corporativo elegante")
            print("   ➤ Tablas con diseño moderno y colores alternados")
            print("   ➤ Sección de métricas/KPIs con cajas visuales")
            print("   ➤ Tipografía profesional y jerarquía visual")
            print("   ➤ Espaciado y márgenes optimizados")
            print("   ➤ Alineación inteligente de datos numéricos")
            print("   ➤ Procesamiento automático de estructuras complejas")
            
            print(f"\n📍 El archivo se encuentra en:")
            print(f"   {os.path.abspath(result['filename'])}")
            
        else:
            print("❌ Error: No se pudo verificar el archivo generado")
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Verifica que estén instaladas las dependencias: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        import traceback
        print("\n🔍 Detalles del error:")
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("             DEMOSTRACIÓN COMPLETADA")
    print("="*60)

if __name__ == "__main__":
    main()
