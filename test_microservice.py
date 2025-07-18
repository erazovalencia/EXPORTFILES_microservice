"""
Script de ejemplo para probar el microservicio de exportación de archivos
"""

import requests
import json

# URL base del microservicio
BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Probar el endpoint de salud"""
    response = requests.get(f"{BASE_URL}/health")
    print("=== Test Health ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_pdf_export():
    """Probar exportación a PDF"""
    data = {
        "file_format": "pdf",
        "filename": "reporte_ventas",
        "data": {
            "title": "Reporte de Ventas Mensual",
            "content": [
                "Este reporte muestra las ventas del mes actual.",
                "Se incluyen datos de productos y cantidades vendidas."
            ],
            "tables": [
                {
                    "title": "Ventas por Producto",
                    "headers": ["Producto", "Cantidad", "Precio Unitario", "Total"],
                    "rows": [
                        ["Laptop", 10, 1200.00, 12000.00],
                        ["Mouse", 50, 25.00, 1250.00],
                        ["Teclado", 30, 45.00, 1350.00],
                        ["Monitor", 15, 300.00, 4500.00]
                    ]
                }
            ]
        }
    }
    
    response = requests.post(f"{BASE_URL}/export", json=data)
    print("=== Test PDF Export ===")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        with open("test_output.pdf", "wb") as f:
            f.write(response.content)
        print("PDF guardado como test_output.pdf")
    else:
        print(f"Error: {response.text}")
    print()

def test_docx_export():
    """Probar exportación a DOCX"""
    data = {
        "title": "Informe Ejecutivo",
        "content": [
            "Resumen ejecutivo del trimestre.",
            "Los resultados han sido positivos en todas las áreas.",
            "Se recomienda continuar con la estrategia actual."
        ],
        "tables": [
            {
                "title": "Métricas Clave",
                "headers": ["Métrica", "Q1", "Q2", "Q3"],
                "rows": [
                    ["Ventas", 100000, 120000, 135000],
                    ["Clientes", 500, 600, 720],
                    ["Satisfacción", "85%", "88%", "92%"]
                ]
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/export/docx", json=data)
    print("=== Test DOCX Export ===")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        with open("test_output.docx", "wb") as f:
            f.write(response.content)
        print("DOCX guardado como test_output.docx")
    else:
        print(f"Error: {response.text}")
    print()

def test_xlsx_export():
    """Probar exportación a XLSX"""
    data = {
        "tables": [
            {
                "title": "Ventas_Q1",
                "headers": ["Mes", "Producto", "Ventas", "Meta"],
                "rows": [
                    ["Enero", "Laptop", 15000, 12000],
                    ["Febrero", "Laptop", 18000, 15000],
                    ["Marzo", "Laptop", 22000, 18000],
                    ["Enero", "Mouse", 2500, 2000],
                    ["Febrero", "Mouse", 3000, 2500],
                    ["Marzo", "Mouse", 3200, 3000]
                ]
            },
            {
                "title": "Resumen_Trimestral",
                "headers": ["Categoría", "Total Ventas", "% Crecimiento"],
                "rows": [
                    ["Laptops", 55000, "25%"],
                    ["Accesorios", 8700, "15%"],
                    ["Monitores", 12000, "8%"]
                ]
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/export/xlsx", json=data)
    print("=== Test XLSX Export ===")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        with open("test_output.xlsx", "wb") as f:
            f.write(response.content)
        print("XLSX guardado como test_output.xlsx")
    else:
        print(f"Error: {response.text}")
    print()

def test_formats():
    """Probar endpoint de formatos soportados"""
    response = requests.get(f"{BASE_URL}/formats")
    print("=== Test Supported Formats ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    try:
        print("Iniciando pruebas del microservicio de exportación...")
        print("Asegúrate de que el servicio esté ejecutándose en http://localhost:8000")
        print()
        
        test_health()
        test_formats()
        test_pdf_export()
        test_docx_export()
        test_xlsx_export()
        
        print("✅ Todas las pruebas completadas!")
        print("Revisa los archivos generados: test_output.pdf, test_output.docx, test_output.xlsx")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al microservicio.")
        print("Asegúrate de que esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
