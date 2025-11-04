"""
Test directo del servicio PDF para debugging
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.services.pdf_service import PDFExportService
    
    def test_pdf_service():
        """Test directo del servicio PDF"""
        print("🧪 Probando servicio PDF directamente...")
        
        # Crear instancia del servicio
        pdf_service = PDFExportService()
        
        # Datos de prueba simples
        test_data = {
            "title": "Test PDF",
            "headers": ["ID", "Nombre", "Precio"],
            "rows": [
                [1, "Producto A", 100.50],
                [2, "Producto B", 200.75],
                [3, "Producto C", 300.25]
            ]
        }
        
        try:
            # Generar PDF
            buffer = pdf_service.generate_file(test_data)
            
            # Verificar que se generó contenido
            if buffer and buffer.getvalue():
                print(f"✅ PDF generado exitosamente: {len(buffer.getvalue())} bytes")
                
                # Guardar archivo de prueba
                with open("test_direct.pdf", "wb") as f:
                    f.write(buffer.getvalue())
                print("📄 Archivo guardado como: test_direct.pdf")
                
                return True
            else:
                print("❌ Error: PDF vacío")
                return False
                
        except Exception as e:
            print(f"❌ Error al generar PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    if __name__ == "__main__":
        if test_pdf_service():
            print("🎉 Test exitoso!")
        else:
            print("💥 Test falló")
            
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de estar en el directorio correcto y tener las dependencias instaladas")
