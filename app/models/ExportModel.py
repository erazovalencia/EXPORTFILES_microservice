from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum


class FileFormat(str, Enum):
    """Formatos de archivo soportados"""
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"


class ExportRequest(BaseModel):
    """Modelo para la solicitud de exportación"""
    file_format: FileFormat = Field(..., description="Formato del archivo a generar")
    data: Dict[str, Any] = Field(..., description="Datos a exportar")
    filename: Optional[str] = Field(None, description="Nombre del archivo (sin extensión)")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Opciones adicionales")
    
    class Config:
        # Configuración para Pydantic v1 y v2 compatibilidad
        use_enum_values = True


class TableData(BaseModel):
    """Modelo para datos de tabla"""
    headers: List[str] = Field(..., description="Encabezados de la tabla")
    rows: List[List[Any]] = Field(..., description="Filas de datos")
    title: Optional[str] = Field(None, description="Título de la tabla")


class DocumentData(BaseModel):
    """Modelo para datos de documento"""
    title: Optional[str] = Field(None, description="Título del documento")
    content: List[str] = Field(..., description="Contenido del documento (párrafos)")
    tables: Optional[List[TableData]] = Field(None, description="Tablas incluidas en el documento")


class ExportResponse(BaseModel):
    """Modelo para la respuesta de exportación"""
    success: bool = Field(..., description="Indica si la exportación fue exitosa")
    message: str = Field(..., description="Mensaje de estado")
    filename: Optional[str] = Field(None, description="Nombre del archivo generado")
    content_type: Optional[str] = Field(None, description="Tipo de contenido del archivo")