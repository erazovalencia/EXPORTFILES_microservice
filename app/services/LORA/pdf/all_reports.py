from fpdf import FPDF
import io
from typing import Any, Dict, List
from datetime import datetime
from pathlib import Path
from ...base import BaseExportService
from ...valera_client import get_reports


class ExportAllReports(BaseExportService):
    """Genera un PDF con TODOS los reportes usando el mismo estilo que el PDF simple individual."""

    def __init__(self):
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=15)
        # Registrar fuentes Unicode (DejaVu) para soportar acentos y caracteres especiales
        BASE_DIR = Path(__file__).resolve().parents[3]
        FONT_DIR = BASE_DIR / "fonts"
        normal = FONT_DIR / "DejaVuSerif.ttf"
        bold = FONT_DIR / "DejaVuSerif-Bold.ttf"
        italic = normal  # fallback
        self.pdf.add_font("DejaVu", "", str(normal), uni=True)
        if bold.exists():
            self.pdf.add_font("DejaVu", "B", str(bold), uni=True)
        else:
            self.pdf.add_font("DejaVu", "B", str(normal), uni=True)
        # register italic as fallback
        self.pdf.add_font("DejaVu", "I", str(italic), uni=True)
        self.pdf.set_font("DejaVu", "", 11)

    async def generate_file(self, data: Any = None, options: Dict = None) -> io.BytesIO:
        reports = get_reports()
        if not isinstance(reports, list) or not reports:
            raise ValueError("No hay reportes disponibles para exportar")

        for report in reports:
            self._add_page_for_report(report)

        buffer = io.BytesIO()
        pdf_output = self.pdf.output(dest='S')
        if isinstance(pdf_output, (bytes, bytearray)):
            buffer.write(pdf_output)
        else:
            buffer.write(pdf_output.encode('latin-1'))
        buffer.seek(0)
        return buffer

    def _add_page_for_report(self, data: Dict):
        self.pdf.add_page()
        self.pdf.set_font("DejaVu", "", 11)
        self.pdf.set_text_color(0, 0, 0)

        self._render_header(data)
        self._render_section("Resumen", self._extract_summary(data))
        self._render_section("Descripcion", data.get("detailedDescription", "N/A"))
        self._render_section("Causa", data.get("findingCause", "N/A"))
        self._render_section("Conversacion", data.get("conversation", "N/A"))
        evidences = data.get("evidence")
        if evidences is None:
            rep_evid = data.get("reportEvidence")
            evidences = [rep_evid] if rep_evid else []
        self._render_section("Evidencias", "\n".join(evidences if isinstance(evidences, list) else [str(evidences)]))
        self._render_section("Acciones", self._format_actions(data.get("actions", [])))
        self._render_footer(data)

    def _render_header(self, data: Dict):
        self.pdf.set_font("DejaVu", "B", 14)
        self.pdf.cell(0, 8, f"Reporte LORA - {data.get('reportTitle', 'N/A')}", ln=True, align="C")
        self.pdf.set_font("DejaVu", "B", 10)
        self.pdf.cell(0, 8, f"ID de reporte: {data.get('id', 'N/A')}", ln=True, align="L")
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 6, f"Codigo: {data.get('loraReportCode', 'N/A')}", ln=True)
        self.pdf.cell(0, 6, f"Estado: {data.get('reportStatus', 'N/A').upper()}", ln=True)
        self.pdf.cell(0, 6, f"Fecha de creacion: {data.get('createdAt', 'N/A')}", ln=True)
        self._draw_separator()

    def _render_section(self, title: str, content: str):
        self.pdf.set_font("DejaVu", "B", 12)
        self.pdf.cell(0, 7, title.upper(), ln=True)
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.multi_cell(0, 6, str(content).strip() or "N/A")
        self._draw_separator()

    def _render_footer(self, data: Dict):
        self.pdf.set_y(-30)
        self._draw_separator()
        self.pdf.set_font("DejaVu", "I", 8)
        self.pdf.cell(0, 5, f"ID de reporte: {data.get('id', 'N/A')}", ln=True, align="R")
        self.pdf.cell(0, 5, f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")
        self.pdf.cell(0, 5, "Documento generado automaticamente por VALERA ECOSYSTEM", ln=True, align="C")

    def _draw_separator(self):
        self.pdf.ln(2)
        self.pdf.cell(0, 0, "-" * 120, ln=True)
        self.pdf.ln(3)

    def _extract_summary(self, data: Dict) -> str:
        fields = [
            ("Proyecto", "project"),
            ("Unidad", "unity"),
            ("Rig", "rig"),
            ("Base", "base"),
            ("Campo", "field"),
            ("Clasificacion", "hazardClassification"),
            ("Tipo de Reporte", "reportType"),
            ("Tipo", "hazardType"),
            ("Creado por", "createdBy"),
            ("Actualizado", "updatedAt"),
        ]
        return "\n".join([f"{label}: {data.get(key, 'N/A')}" for label, key in fields])

    def _format_actions(self, actions: List[Dict]) -> str:
        if not actions:
            return "Sin acciones registradas."
        result = []
        for i, act in enumerate(actions, 1):
            desc = act.get("description", "N/A")
            resp = act.get("responsible", "N/A")
            due = act.get("dueDate", "N/A")
            status = act.get("status", "N/A").upper()
            result.append(f"{i}. {desc}\n   Responsable: {resp}\n   Fecha limite: {due}\n   Estado: {status}\n")
        return "\n".join(result)

    def get_content_type(self) -> str:
        return "application/pdf"

    def get_file_extension(self) -> str:
        return ".pdf"
