from fpdf import FPDF
import io
from typing import Any, Dict, List
from datetime import datetime
from ...base import BaseExportService


class ExportSinglePDFReportWithStyle(BaseExportService):
    """Genera PDF de un reporte LORA con estilo visual."""

    def __init__(self):
        self.pdf = None
        self.colors = {
            'background': (247, 243, 233),
            'border': (224, 207, 163),
            'text_dark': (45, 36, 24),
            'text_brown': (122, 92, 27),
            'open_stamp_bg': (224, 112, 112),
            'close_stamp_bg': (127, 186, 0),
            'open_stamp_border': (224, 26, 26),
            'close_stamp_border': (170, 240, 18),
            'block_bg': (255, 251, 231),
            'summary_bg': (244, 236, 217),
            'action_open': (224, 112, 112),
            'action_close': (198, 223, 144),
        }

    async def generate_file(self, data: Any, options: Dict = None) -> io.BytesIO:
        if not isinstance(data, dict):
            raise ValueError("Se requiere un diccionario con los datos del reporte")

        report_data = data
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_fill_color(*self.colors['background'])
        self.pdf.rect(0, 0, 210, 297, 'F')
        self.pdf.set_font("Courier", "", 11)
        self.pdf.set_text_color(*self.colors['text_dark'])

        self._draw_stamp(report_data)
        self._draw_header(report_data)
        self._draw_summary(report_data)
        self._draw_description(report_data)
        self._draw_conversation(report_data)
        self._draw_evidences(report_data)
        self._draw_actions(report_data)
        self._draw_footer(report_data)

        buffer = io.BytesIO()
        pdf_output = self.pdf.output(dest='S')
        buffer.write(pdf_output if isinstance(pdf_output, (bytes, bytearray)) else pdf_output.encode('latin-1'))
        buffer.seek(0)
        return buffer

    # Visual components
    def _draw_stamp(self, data: Dict):
        status = str(data.get("reportStatus", "open")).lower()
        stamp_text = "ABIERTO" if status == "open" else "CERRADO"
        if status == "open":
            bg = self.colors['open_stamp_bg']
            border = self.colors['open_stamp_border']
        else:
            bg = self.colors['close_stamp_bg']
            border = self.colors['close_stamp_border']
        self.pdf.set_xy(150, 15)
        self.pdf.set_fill_color(*bg)
        self.pdf.set_draw_color(*border)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Courier", "B", 14)
        self.pdf.cell(45, 10, stamp_text, border=1, align='C', fill=True)

    def _draw_header(self, data: Dict):
        code = data.get("loraReportCode", "Sin codigo")
        title = data.get("reportTitle", "Sin titulo")
        created = data.get("createdAt", datetime.now().strftime("%Y-%m-%d"))
        self.pdf.ln(20)
        self.pdf.set_font("Courier", "B", 11)
        self.pdf.set_text_color(*self.colors['text_brown'])
        self.pdf.cell(0, 8, f"CODIGO: {code}", ln=True)
        self.pdf.set_font("Courier", "B", 18)
        self.pdf.set_text_color(*self.colors['text_dark'])
        self.pdf.cell(0, 10, title.upper(), ln=True)
        self.pdf.set_font("Courier", "", 9)
        self.pdf.set_text_color(*self.colors['text_brown'])
        self.pdf.cell(0, 8, f"Creado: {created}", ln=True)
        self._draw_line()

    def _draw_summary(self, data: Dict):
        summary_fields = [
            ("Proyecto", data.get("project", "N/A")),
            ("Unidad", data.get("unity", "N/A")),
            ("Rig", data.get("rig", "N/A")),
            ("Base", data.get("base", "N/A")),
            ("Campo", data.get("field", "N/A")),
            ("Clasificacion", data.get("hazardClassification", "N/A")),
            ("Tipo de Reporte", data.get("reportType", "N/A")),
            ("Tipo", data.get("hazardType", "N/A")),
            ("Creado por", data.get("createdBy", "N/A")),
            ("Actualizado", data.get("updatedAt", "N/A")),
        ]
        self._draw_block("Resumen", self._render_summary_grid, summary_fields)

    def _draw_description(self, data: Dict):
        if data.get("detailedDescription"):
            self._draw_block("Descripcion", self._render_paragraph, data["detailedDescription"])
        if data.get("findingCause"):
            self._draw_block("Causa", self._render_paragraph, data["findingCause"])

    def _draw_conversation(self, data: Dict):
        if data.get("conversation"):
            self._draw_block("Conversacion", self._render_paragraph, data["conversation"])

    def _draw_evidences(self, data: Dict):
        evidences = data.get("evidence", [])
        if evidences:
            self._draw_block("Evidencias", self._render_evidences, evidences)
        else:
            self._draw_block("Evidencias", self._render_paragraph, "Sin evidencias adjuntas")

    def _draw_actions(self, data: Dict):
        actions = data.get("actions", [])
        if not actions:
            return
        self._draw_block("Acciones", self._render_actions, actions)

    def _draw_footer(self, data: Dict):
        self.pdf.ln(10)
        self._draw_line()
        self.pdf.set_font("Courier", "I", 8)
        self.pdf.set_text_color(*self.colors['text_brown'])
        self.pdf.cell(0, 6, f"ID: {data.get('id', 'N/A')}", ln=True, align="R")
        self.pdf.cell(0, 5, "Documento generado automaticamente por VALERA ECOSYSTEM", ln=True, align="C")

    # Blocks / sections helpers
    def _draw_block(self, title: str, render_fn, content):
        y = self.pdf.get_y() + 4
        self.pdf.set_fill_color(*self.colors['block_bg'])
        self.pdf.set_draw_color(*self.colors['border'])
        self.pdf.rect(10, y, 190, 10, 'F')
        self.pdf.set_y(y + 2)
        self.pdf.set_x(15)
        self.pdf.set_font("Courier", "B", 12)
        self.pdf.set_text_color(*self.colors['text_brown'])
        self.pdf.cell(0, 8, title.upper(), ln=True)
        self._draw_line()
        render_fn(content)
        self.pdf.ln(3)

    def _render_summary_grid(self, items: List):
        self.pdf.set_font("Courier", "", 10)
        self.pdf.set_fill_color(*self.colors['summary_bg'])
        self.pdf.set_text_color(*self.colors['text_dark'])
        col_width = 95
        for i, (k, v) in enumerate(items):
            if i % 2 == 0:
                self.pdf.set_x(15)
            else:
                self.pdf.set_x(110)
            self.pdf.cell(col_width - 5, 7, f"{k}: {v}", ln=(i % 2 != 0), fill=True)
        self.pdf.ln(2)

    def _render_paragraph(self, text: str):
        clean = str(text).replace("\n", " ").strip()
        self.pdf.set_font("Courier", "", 10)
        self.pdf.multi_cell(0, 6, clean)
        self.pdf.ln(2)

    def _render_evidences(self, evidences: List):
        for e in evidences:
            self.pdf.set_font("Courier", "", 10)
            self.pdf.cell(0, 6, f"- {e}", ln=True)
        self.pdf.ln(2)

    def _render_actions(self, actions: List[Dict]):
        for act in actions:
            status = str(act.get("status", "open")).lower()
            bg = self.colors['action_close'] if status == "close" else self.colors['action_open']
            self.pdf.set_fill_color(*bg)
            self.pdf.set_x(15)
            self.pdf.set_font("Courier", "B", 10)
            self.pdf.cell(0, 8, f"Accion: {act.get('description', 'N/A')}", ln=True, fill=True)
            self.pdf.set_font("Courier", "", 9)
            resp = act.get("responsible", "No asignado")
            due = act.get("dueDate", "N/A")
            self.pdf.cell(0, 6, f"Responsable: {resp}", ln=True)
            self.pdf.cell(0, 6, f"Fecha limite: {due}", ln=True)
            self.pdf.ln(3)

    # Utils
    def _draw_line(self):
        self.pdf.set_draw_color(*self.colors['border'])
        y = self.pdf.get_y()
        self.pdf.line(10, y, 200, y)
        self.pdf.ln(4)

    def get_content_type(self) -> str:
        return "application/pdf"

    def get_file_extension(self) -> str:
        return ".pdf"

