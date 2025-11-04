import io
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from datetime import datetime
from ..models.ExportModel import FileFormat

from ..services.LORA.pdf.all_reports import ExportAllReports
from ..services.LORA.pdf.single_report_simple import ExportSinglePDFReportSimple
from ..services.LORA.pdf.single_report_with_styles import ExportSinglePDFReportWithStyle
from ..services.LORA.docs.single_report import DOCXExportService
from ..services.LORA.xlsx.single_report import XLSXExportService
from ..services.LORA.xlsx.all_reports import XLSXListExportService
from ..services.valera_client import get_report_by_id, get_reports

router = APIRouter()

# Mapeo de formatos a servicios (metadatos)
SERVICE_MAP = {
    FileFormat.PDF: ExportAllReports,
    FileFormat.DOCX: DOCXExportService,
    FileFormat.XLSX: XLSXExportService,
}

@router.get("/health")
async def health_check():
    return {
        "status": "Healthy",
        "timestamp": datetime.now().isoformat(),
        "supported_formats": [fmt.value for fmt in FileFormat],
    }

@router.get("/formats")
async def get_supported_formats():
    return {
        "supported_formats": [
            {
                "format": fmt.value,
                "content_type": SERVICE_MAP[fmt]().get_content_type(),
                "extension": SERVICE_MAP[fmt]().get_file_extension(),
            }
            for fmt in FileFormat
        ]
    }

@router.get("/lora/pdf_all_reports", summary="Exporta todos los reportes en un PDF")
async def export_pdf_all_reports():
    try:
        service = ExportAllReports()
        file_buffer = await service.generate_file()
        return Response(
            content=file_buffer.read(),
            media_type=service.get_content_type(),
            headers={"Content-Disposition": 'attachment; filename="todos_los_reportes.pdf"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al exportar reportes en PDF: {str(e)}")

@router.get("/lora/xlsx_all_reports", summary="Exporta todos los reportes en XLSX (listado)")
def export_xlsx_all_reports():
    data = get_reports()
    service = XLSXListExportService()
    file_buffer = service.generate_file(data, None)
    filename = f"todos_los_reportes{service.get_file_extension()}"
    return StreamingResponse(
        io.BytesIO(file_buffer.read()),
        media_type=service.get_content_type(),
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

@router.get("/lora/docx/{id}")
def export_single_report_docx(id: int):
    try:
        data = get_report_by_id(id)
        service = DOCXExportService()
        file_buffer = service.generate_file(data)
        filename = f"lora_report_{id}{service.get_file_extension()}"
        return StreamingResponse(
            io.BytesIO(file_buffer.read()),
            media_type=service.get_content_type(),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando DOCX: {str(e)}")

@router.get("/lora/xlsx/{id}")
def export_single_report_xlsx(id: int):
    try:
        data = get_report_by_id(id)
        service = XLSXExportService()
        file_buffer = service.generate_file(data)
        filename = f"lora_report_{id}{service.get_file_extension()}"
        return StreamingResponse(
            io.BytesIO(file_buffer.read()),
            media_type=service.get_content_type(),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando XLSX: {str(e)}")

def _normalize_report_for_single_pdf(data: dict) -> dict:
    # Adaptar evidencias a lista esperada por los servicios
    if 'evidence' not in data:
        evid = data.get('reportEvidence')
        if evid:
            data['evidence'] = [evid]
        else:
            data['evidence'] = []
    # Adaptar responsable dentro de acciones
    actions = data.get('actions') or []
    for act in actions:
        if 'responsible' not in act:
            assigned = act.get('assignedTo') or {}
            user_info = (assigned or {}).get('userInformation') or {}
            name = (user_info.get('name') or '').strip()
            last = (user_info.get('lastName') or '').strip()
            full = f"{name} {last}".strip()
            act['responsible'] = full or assigned.get('documentId') or ''
    return data

@router.get("/lora/pdf_simple/{id}")
def export_single_report_pdf_simple(id: int):
    try:
        data = get_report_by_id(id)
        data = _normalize_report_for_single_pdf(data)
        service = ExportSinglePDFReportSimple()
        file_buffer = service.generate_file(data)
        filename = f"lora_report_{id}.pdf"
        return StreamingResponse(
            io.BytesIO(file_buffer.read()),
            media_type=service.get_content_type(),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando PDF simple: {str(e)}")

@router.get("/lora/pdf_styled/{id}")
async def export_single_report_pdf_styled(id: int):
    try:
        data = get_report_by_id(id)
        data = _normalize_report_for_single_pdf(data)
        service = ExportSinglePDFReportWithStyle()
        file_buffer = await service.generate_file(data)
        filename = f"lora_report_{id}.pdf"
        return StreamingResponse(
            io.BytesIO(file_buffer.read()),
            media_type=service.get_content_type(),
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando PDF con estilo: {str(e)}")
