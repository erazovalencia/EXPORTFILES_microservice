from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import io
from datetime import datetime

from ..models.ExportModel import ExportRequest, ExportResponse, FileFormat
from ..services.pdf_service import PDFExportService
from ..services.doc_service import DOCXExportService
from ..services.xls_service import XLSXExportService
from ..utils.file_utils import generate_filename, validate_filename, get_file_size_mb

router = APIRouter()

# Mapeo de formatos a servicios
SERVICE_MAP = {
    FileFormat.PDF: PDFExportService,
    FileFormat.DOCX: DOCXExportService,
    FileFormat.XLSX: XLSXExportService,
}

@router.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "supported_formats": [format.value for format in FileFormat]
    }


@router.get("/formats")
async def get_supported_formats():
    """Endpoint para obtener los formatos soportados"""
    return {
        "supported_formats": [
            {
                "format": format.value,
                "content_type": SERVICE_MAP[format]().get_content_type(),
                "extension": SERVICE_MAP[format]().get_file_extension()
            }
            for format in FileFormat
        ]
    }


@router.get("/examples")
async def get_examples():
    """Endpoint para obtener ejemplos de datos de prueba"""
    return {
        "simple_table": {
            "title": "Ejemplo de Tabla Simple",
            "headers": ["Producto", "Cantidad", "Precio"],
            "rows": [
                ["Laptop", 10, 1200.00],
                ["Mouse", 50, 25.00],
                ["Teclado", 30, 45.00]
            ]
        },
        "document_with_content": {
            "title": "Documento de Ejemplo",
            "content": [
                "Este es el primer párrafo del documento.",
                "Aquí va información adicional en el segundo párrafo."
            ],
            "tables": [
                {
                    "title": "Datos de Muestra",
                    "headers": ["Columna 1", "Columna 2"],
                    "rows": [["Dato 1", "Dato 2"], ["Dato 3", "Dato 4"]]
                }
            ]
        },
        "multiple_tables": {
            "tables": [
                {
                    "title": "Ventas Q1",
                    "headers": ["Mes", "Ventas"],
                    "rows": [["Enero", 1000], ["Febrero", 1200], ["Marzo", 1100]]
                },
                {
                    "title": "Ventas Q2",
                    "headers": ["Mes", "Ventas"],
                    "rows": [["Abril", 1300], ["Mayo", 1400], ["Junio", 1250]]
                }
            ]
        }
    }


@router.post("/export")
async def export_file(request: ExportRequest):
    """
    Endpoint principal para exportar archivos
    
    Args:
        request: Solicitud de exportación con datos y formato
    
    Returns:
        StreamingResponse: Archivo generado para descarga
    """
    try:
        print(f" Debug: Procesando solicitud para formato {request.file_format}")
        print(f" Debug: Datos recibidos: {type(request.data)}")
        
        # Validar formato
        if request.file_format not in SERVICE_MAP:
            raise HTTPException(
                status_code=400, 
                detail=f"Formato no soportado: {request.file_format}"
            )
        
        # Obtener servicio correspondiente
        service_class = SERVICE_MAP[request.file_format]
        service = service_class()
        print(f"🔍 Debug: Servicio creado: {service.__class__.__name__}")
        
        # Generar archivo
        file_buffer = service.generate_file(request.data, request.options)
        print(f"🔍 Debug: Buffer generado: {type(file_buffer)}")
        
        # Validar que el archivo se generó correctamente
        if not file_buffer:
            raise HTTPException(
                status_code=500,
                detail="Error al generar el archivo: buffer vacío"
            )
        
        # Verificar que hay contenido en el buffer
        current_pos = file_buffer.tell()
        file_buffer.seek(0, 2)  # Ir al final
        file_size = file_buffer.tell()
        file_buffer.seek(current_pos)  # Volver a la posición original
        
        print(f"🔍 Debug: Tamaño del archivo: {file_size} bytes")
        
        if file_size == 0:
            raise HTTPException(
                status_code=500,
                detail="Error al generar el archivo: archivo vacío"
            )
        
        # Generar nombre de archivo
        base_filename = request.filename or f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not validate_filename(base_filename):
            base_filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filename = base_filename + service.get_file_extension()
        
        # Obtener información del archivo
        file_size_mb = get_file_size_mb(file_buffer)
        
        # Resetear buffer para lectura
        file_buffer.seek(0)
        
        # Retornar archivo como respuesta de streaming
        return StreamingResponse(
            io.BytesIO(file_buffer.read()),
            media_type=service.get_content_type(),
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(file_buffer.getbuffer().nbytes),
                "X-File-Size-MB": str(round(file_size_mb, 2))
            }
        )
        
    except ValueError as e:
        print(f"ValueError en export_file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error de validación: {str(e)}")
    except KeyError as e:
        print(f"KeyError en export_file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Campo requerido faltante: {str(e)}")
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        # Log del error para debugging
        import traceback
        error_detail = f"Error interno: {str(e)}"
        print(f"Error en export_file: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/export/pdf")
async def export_pdf(request_data: Dict[str, Any]):
    """Endpoint específico para exportar PDF"""
    try:
        print(f"🔍 PDF Debug: Datos recibidos: {request_data}")
        
        # Manejar tanto el formato completo como el formato simplificado
        if 'data' in request_data and 'file_format' not in request_data:
            # Formato simplificado: {data: {...}, filename: "..."}
            data = request_data.get('data', request_data)
            filename = request_data.get('filename', None)
        else:
            # Formato completo o datos directos
            data = request_data
            filename = request_data.get('filename', None)
        
        print(f"🔍 PDF Debug: Data procesada: {data}")
        print(f"🔍 PDF Debug: Filename: {filename}")
        
        request = ExportRequest(
            file_format=FileFormat.PDF,
            data=data,
            filename=filename
        )
        
        print(f"🔍 PDF Debug: Request creado: {request}")
        
        return await export_file(request)
        
    except Exception as e:
        import traceback
        print(f"❌ Error en export_pdf: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error en PDF endpoint: {str(e)}")


@router.post("/export/docx")
async def export_docx(request_data: Dict[str, Any]):
    """Endpoint específico para exportar DOCX"""
    # Manejar tanto el formato completo como el formato simplificado
    if 'data' in request_data and 'file_format' not in request_data:
        # Formato simplificado: {data: {...}, filename: "..."}
        data = request_data.get('data', request_data)
        filename = request_data.get('filename', None)
    else:
        # Formato completo o datos directos
        data = request_data
        filename = request_data.get('filename', None)
    
    request = ExportRequest(
        file_format=FileFormat.DOCX,
        data=data,
        filename=filename
    )
    return await export_file(request)


@router.post("/export/xlsx")
async def export_xlsx(request_data: Dict[str, Any]):
    """Endpoint específico para exportar XLSX"""
    # Manejar tanto el formato completo como el formato simplificado
    if 'data' in request_data and 'file_format' not in request_data:
        # Formato simplificado: {data: {...}, filename: "..."}
        data = request_data.get('data', request_data)
        filename = request_data.get('filename', None)
    else:
        # Formato completo o datos directos
        data = request_data
        filename = request_data.get('filename', None)
    
    request = ExportRequest(
        file_format=FileFormat.XLSX,
        data=data,
        filename=filename
    )
    return await export_file(request)


@router.post("/test/{format}")
async def test_export(format: str):
    """Endpoint de prueba rápida para generar archivos de ejemplo"""
    if format not in ["pdf", "docx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Formato no válido. Use: pdf, docx, xlsx")
    
    # Datos de prueba
    test_data = {
        "title": f"Documento de Prueba - {format.upper()}",
        "content": [
            "Este es un documento de prueba generado automáticamente.",
            "Contiene datos de muestra para verificar la funcionalidad."
        ],
        "tables": [
            {
                "title": "Datos de Prueba",
                "headers": ["ID", "Producto", "Cantidad", "Precio"],
                "rows": [
                    [1, "Laptop", 5, 1200.00],
                    [2, "Mouse", 10, 25.00],
                    [3, "Teclado", 8, 45.00],
                    [4, "Monitor", 3, 300.00]
                ]
            }
        ]
    }
    
    request = ExportRequest(
        file_format=FileFormat(format),
        data=test_data,
        filename=f"test_{format}"
    )
    
    return await export_file(request)


@router.get("/debug/pdf")
async def debug_pdf():
    """Endpoint de debug para PDF con datos mínimos"""
    minimal_data = {
        "title": "Test Debug",
        "content": ["Prueba simple"]
    }
    
    try:
        from ..services.pdf_service import PDFExportService
        service = PDFExportService()
        buffer = service.generate_file(minimal_data)
        
        return {
            "success": True,
            "buffer_type": str(type(buffer)),
            "buffer_size": len(buffer.getvalue()) if buffer else 0,
            "buffer_tell": buffer.tell() if buffer else "N/A"
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
