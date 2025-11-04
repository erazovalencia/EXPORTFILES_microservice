import io
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import Dict, Any
from datetime import datetime
from ..utils.file_utils import generate_filename, validate_filename, get_file_size_mb

from ..models.ExportModel import ExportRequest, ExportResponse, FileFormat

from ..services.LORA.pdf.all_reports import ExportAllReports
from ..services.LORA.docs.single_report import DOCXExportService
from ..services.LORA.xlsx.single_report import XLSXExportService
from ..services.LORA.xlsx.all_reports import XLSXListExportService

router = APIRouter()

# Mapeo de formatos a servicios
SERVICE_MAP = {
    FileFormat.PDF: ExportAllReports,
    FileFormat.DOCX: DOCXExportService,
    FileFormat.XLSX: XLSXExportService,
}

@router.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    return {
        "status": "Healthy",
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

@router.post("/export/lora/pdf_single_report")
async def export_single_report_pdf(request_data: Dict[str, Any]):
    """
    Exporta un reporte LORA individual en formato PDF decorado.
    Espera un JSON como: { "id": 67 }
    """
    try:
        print(f"Solicitud recibida: {request_data}")
        
        service = ExportAllReports()
        file_buffer = await service.generate_file(data=request_data)

        filename = f"Reporte_LORA_{request_data['id']}.pdf"
        headers = {
            "Content-Disposition": f"attachment; filename={filename}"
        }

        return StreamingResponse(file_buffer, media_type="application/pdf", headers=headers)

    except Exception as e:
        import traceback
        print(f"Error en export_decorated_pdf: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error exportando PDF decorado: {str(e)}")
    
@router.post("/export/lora/docs_single_report")
async def export__single_report_docx(request_data: Dict[str, Any]):
    """Endpoint específico para exportar un unico rpeorte dado un id en formato DOCX"""
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
    return await export__single_report_docx(request)

@router.post("/export/lora/xlsx_single_report")
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

@router.get("/export/lora/pdf_all_reports", summary="Exporta todos los reportes como un único PDF")
async def export_pdf_all_reports():
    try:
        service = ExportAllReports()
        file_buffer = await service.generate_file()

        return Response(
            content=file_buffer.read(),
            media_type=service.get_content_type(),
            headers={
                "Content-Disposition": f'attachment; filename="todos_los_reportes.pdf"'
            }
        )
    except Exception as e:
        import traceback
        print(f"Error en export_all_reports: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error al exportar reportes en PDF")

@router.post("/export/xlsx_list")
async def export_xlsx_list(request: ExportRequest):
    if request.file_format != FileFormat.XLSX:
        raise HTTPException(400, "Formato no permitido para esta ruta")

    if isinstance(request.data, list):
        service = XLSXListExportService()
    else:
        service = XLSXExportService()

    file_buffer = service.generate_file(request.data, request.options)
    filename = (request.filename or "reporte") + service.get_file_extension()
    return StreamingResponse(
        io.BytesIO(file_buffer.read()),
        media_type=service.get_content_type(),
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

