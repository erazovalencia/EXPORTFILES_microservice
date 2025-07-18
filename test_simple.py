"""
Prueba rápida del endpoint de PDF - Usar después de iniciar el microservicio
"""
import requests
import json

# URL del microservicio
BASE_URL = "http://localhost:8000/api/v1"

def test_simple_pdf():
    """Prueba simple del endpoint de PDF"""
    
    # Datos de prueba simples
    data = {
        "title": "Test Simple",
        "headers": ["ID", "Nombre", "Valor"],
        "rows": [
            [1, "Producto A", 100],
            [2, "Producto B", 200],
            [3, "Producto C", 300]
        ]
    }
    
    try:
        print("🧪 Probando endpoint PDF...")
        response = requests.post(f"{BASE_URL}/export/pdf", json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Guardar el archivo
            with open("test_simple.pdf", "wb") as f:
                f.write(response.content)
            print("✅ PDF generado exitosamente: test_simple.pdf")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al microservicio.")
        print("Asegúrate de que esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_endpoint_test():
    """Prueba el endpoint /test/pdf"""
    try:
        print("\n🧪 Probando endpoint de prueba...")
        response = requests.post(f"{BASE_URL}/test/pdf")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            with open("test_auto.pdf", "wb") as f:
                f.write(response.content)
            print("✅ PDF de prueba generado: test_auto.pdf")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas rápidas...")
    test_simple_pdf()
    test_endpoint_test()
    print("\n✅ Pruebas completadas!")
    print("Revisa los archivos generados: test_simple.pdf, test_auto.pdf")
