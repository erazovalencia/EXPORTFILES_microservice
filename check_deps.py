"""
Verificador de dependencias para Export Files Microservice
"""

import sys

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    missing_deps = []
    
    # Lista de dependencias requeridas
    dependencies = {
        'fastapi': 'FastAPI framework',
        'uvicorn': 'ASGI server',
        'pydantic': 'Data validation',
        'fpdf': 'PDF generation (fpdf2)',
        'docx': 'DOCX generation (python-docx)',
        'openpyxl': 'Excel XLSX generation'
    }
    
    print("🔍 Verificando dependencias...")
    print()
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} - NO INSTALADO")
            missing_deps.append(module)
    
    print()
    
    if missing_deps:
        print("⚠️  Dependencias faltantes encontradas:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("💡 Para instalar las dependencias faltantes:")
        print("   Windows: ejecuta install-deps.bat")
        print("   Manual: pip install <nombre_del_paquete>")
        print()
        
        # Mapeo de nombres de módulos a nombres de paquetes pip
        pip_names = {
            'fpdf': 'fpdf2',
            'docx': 'python-docx'
        }
        
        pip_commands = []
        for dep in missing_deps:
            pip_name = pip_names.get(dep, dep)
            pip_commands.append(pip_name)
        
        if pip_commands:
            print(f"   Comando completo: pip install {' '.join(pip_commands)}")
        
        return False
    else:
        print("🎉 ¡Todas las dependencias están instaladas correctamente!")
        return True

if __name__ == "__main__":
    if check_dependencies():
        print()
        print("🚀 Listo para ejecutar el microservicio!")
        print("   Ejecuta: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        sys.exit(1)
