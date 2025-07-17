import os
import uuid
from typing import Optional
from datetime import datetime


def generate_filename(base_name: Optional[str] = None, extension: str = "") -> str:
    """
    Genera un nombre de archivo único
    
    Args:
        base_name: Nombre base del archivo
        extension: Extensión del archivo (con punto)
    
    Returns:
        str: Nombre de archivo único
    """
    if not base_name:
        base_name = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Limpiar caracteres no válidos del nombre base
    base_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    base_name = base_name.replace(' ', '_')
    
    # Añadir timestamp para mayor unicidad
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{base_name}_{timestamp}_{unique_id}{extension}"


def validate_filename(filename: str) -> bool:
    """
    Valida que el nombre de archivo sea seguro
    
    Args:
        filename: Nombre del archivo a validar
    
    Returns:
        bool: True si el nombre es válido
    """
    if not filename:
        return False
    
    # Caracteres no permitidos
    invalid_chars = '<>:"/\\|?*'
    
    for char in invalid_chars:
        if char in filename:
            return False
    
    # Nombres reservados en Windows
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                     'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                     'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    
    base_name = os.path.splitext(filename)[0].upper()
    if base_name in reserved_names:
        return False
    
    return True


def get_file_size_mb(file_buffer) -> float:
    """
    Obtiene el tamaño de un buffer de archivo en MB
    
    Args:
        file_buffer: Buffer del archivo
    
    Returns:
        float: Tamaño en MB
    """
    current_position = file_buffer.tell()
    file_buffer.seek(0, 2)  # Ir al final
    size_bytes = file_buffer.tell()
    file_buffer.seek(current_position)  # Volver a la posición original
    
    return size_bytes / (1024 * 1024)


def sanitize_data_for_export(data) -> str:
    """
    Sanitiza datos para exportación, manejando valores None y tipos especiales
    
    Args:
        data: Dato a sanitizar
    
    Returns:
        str: Dato sanitizado como string
    """
    if data is None:
        return ""
    
    if isinstance(data, (int, float)):
        return str(data)
    
    if isinstance(data, bool):
        return "Sí" if data else "No"
    
    if isinstance(data, (list, tuple)):
        return ", ".join(str(item) for item in data)
    
    return str(data).strip()