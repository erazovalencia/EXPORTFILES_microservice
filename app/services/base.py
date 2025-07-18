from abc import ABC, abstractmethod
from typing import Any, Dict
import io


class BaseExportService(ABC):
    """Clase base abstracta para todos los servicios de exportación"""
    
    @abstractmethod
    def generate_file(self, data: Any, options: Dict = None) -> io.BytesIO:
        """
        Genera un archivo en el formato específico
        
        Args:
            data: Los datos a exportar
            options: Opciones adicionales para la generación del archivo
            
        Returns:
            io.BytesIO: El archivo generado en memoria
        """
        pass
    
    @abstractmethod
    def get_content_type(self) -> str:
        """
        Retorna el tipo de contenido MIME del archivo
        
        Returns:
            str: El tipo de contenido MIME
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Retorna la extensión del archivo
        
        Returns:
            str: La extensión del archivo (incluyendo el punto)
        """
        pass
    
    def validate_data(self, data: Any) -> bool:
        """
        Valida los datos de entrada
        
        Args:
            data: Los datos a validar
            
        Returns:
            bool: True si los datos son válidos
        """
        return data is not None