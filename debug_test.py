"""
Debug específico para el error actual
"""
import requests
import json

# Test del endpoint debug
def test_debug_endpoint():
    """Test del endpoint de debug"""
    try:
        print("🔍 Testing debug endpoint...")
        response = requests.get("http://localhost:8000/api/v1/debug/pdf")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Debug response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Debug failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Test simple del endpoint de PDF
def test_simple_pdf():
    """Test simple con datos mínimos"""
    simple_data = {
        "title": "Test Simple"
    }
    
    try:
        print("\n🔍 Testing simple PDF...")
        response = requests.post(
            "http://localhost:8000/api/v1/export/pdf", 
            json=simple_data
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ PDF generado exitosamente")
            with open("debug_simple.pdf", "wb") as f:
                f.write(response.content)
            print("📄 Guardado como debug_simple.pdf")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Test del endpoint de prueba
def test_test_endpoint():
    """Test del endpoint /test/pdf"""
    try:
        print("\n🔍 Testing /test/pdf endpoint...")
        response = requests.post("http://localhost:8000/api/v1/test/pdf")
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Test PDF generado exitosamente")
            with open("debug_test.pdf", "wb") as f:
                f.write(response.content)
            print("📄 Guardado como debug_test.pdf")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando debug del microservicio...")
    test_debug_endpoint()
    test_simple_pdf()
    test_test_endpoint()
    print("\n✅ Debug completado!")
