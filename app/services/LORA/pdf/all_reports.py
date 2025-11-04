from fpdf import FPDF
import io
import requests
from typing import Any, Dict, List
from datetime import datetime
from pathlib import Path
from ...base import BaseExportService

""" Obtiene todos los reportes desde VALERA, mapea y convierte el JSON en un documento PDF """
class ExportAllPdfReports(BaseExportService):
    
    API_URL = "http://localhost:3000/api/lora-report"

    def __init__(self):
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=15)

        BASE_DIR = Path(__file__).resolve().parents[1]
        FONT_DIR = BASE_DIR / "fonts"

        normal = FONT_DIR / "DejaVuSerif.ttf"
        bold = FONT_DIR / "DejaVuSerif.ttf"
        italic = FONT_DIR / "DejaVuSerif.ttf"

        if not normal.exists():
            raise FileNotFoundError(f"Falta la fuente principal: {normal}")

        # Registrar todas las variantes necesarias
        self.pdf.add_font("DejaVu", "", str(normal), uni=True)
        if bold.exists():
            self.pdf.add_font("DejaVu", "B", str(bold), uni=True)
        if italic.exists():
            self.pdf.add_font("DejaVu", "I", str(italic), uni=True)

        # Fuente por defecto
        self.pdf.set_font("DejaVu", "", 11)


    async def generate_file(self, data: Any = None, options: Dict = None) -> io.BytesIO:
        """Obtiene los reportes desde la API y genera un PDF con todos"""
        response = requests.get(self.API_URL)
        if response.status_code != 200:
            raise ValueError("No se pudo obtener la información de la API externa")

        reports = response.json()
        if not isinstance(reports, list) or not reports:
            raise ValueError("No hay reportes disponibles para exportar")

        for report in reports:
            self._add_page_for_report(report)

        buffer = io.BytesIO()
        pdf_output = self.pdf.output(dest='S')
        buffer.write(pdf_output if isinstance(pdf_output, (bytes, bytearray)) else pdf_output.encode('latin-1'))
        buffer.seek(0)
        return buffer

    def _add_page_for_report(self, data: Dict):
        self.pdf.add_page()
        self._render_header(data)
        self._render_section("Resumen", self._extract_summary(data))
        self._render_section("Descripción", data.get("detailedDescription", "N/A"))
        self._render_section("Causa", data.get("findingCause", "N/A"))
        self._render_section("Conversación", data.get("conversation", "N/A"))
        self._render_section("Evidencias", data.get("reportEvidence", "N/A"))
        self._render_section("Acciones", self._format_actions(data.get("actions", [])))
        self._render_footer(data)

    def _render_header(self, data: Dict):
        self.pdf.set_font("DejaVu", "B", 14)
        self.pdf.cell(0, 8, "REPORTES LORA", ln=True, align="C")
        self.pdf.set_font("DejaVu", "", 10)
        self.pdf.cell(0, 6, f"Código: {data.get('loraReportCode', 'N/A')}", ln=True)
        self.pdf.cell(0, 6, f"Título: {data.get('reportTitle', 'N/A')}", ln=True)
        self.pdf.cell(0, 6, f"Estado: {data.get('reportStatus', 'N/A').upper()}", ln=True)
        self.pdf.cell(0, 6, f"Fecha de creación: {data.get('createdAt', 'N/A')}", ln=True)
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
        self.pdf.cell(0, 5, f"ID: {data.get('id', 'N/A')}", ln=True, align="R")
        self.pdf.cell(0, 5, f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")
        self.pdf.cell(0, 5, "VALERA ECOSYSTEM", ln=True, align="C")

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
            ("Clasificación", "hazardClassification"),
            ("Tipo de Reporte", "reportType"),
            ("Tipo", "hazardType"),
            ("Creado por", "user"),
            ("Actualizado", "updatedAt"),
        ]
        summary_lines = []
        for label, key in fields:
            value = data.get(key, "N/A")
            if isinstance(value, dict):
                value = value.get("documentId", "N/A")
            summary_lines.append(f"{label}: {value}")
        return "\n".join(summary_lines)

    def _format_actions(self, actions: List[Dict]) -> str:
        if not actions:
            return "Sin acciones registradas."

        result = []
        for i, act in enumerate(actions, 1):
            desc = act.get("description", "N/A")
            due = act.get("dueDate", "N/A")
            status = act.get("status", "N/A").upper()

            assigned_to = act.get("assignedTo")
            if assigned_to and isinstance(assigned_to, dict):
                user_info = assigned_to.get("userInformation", {})
                name = user_info.get("name", "")
                last = user_info.get("lastName", "")
                resp = f"{name} {last}".strip() or "N/A"
            else:
                resp = "N/A"

            result.append(f"{i}. {desc}\n   Responsable: {resp}\n   Fecha límite: {due}\n   Estado: {status}\n")

        return "\n".join(result)

    def get_content_type(self) -> str:
        return "application/pdf"

    def get_file_extension(self) -> str:
        return ".pdf"
