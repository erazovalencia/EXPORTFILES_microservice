from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
from typing import Any, Dict, List
from datetime import datetime
from ...base import BaseExportService


class DOCXExportService(BaseExportService):
    """Servicio para generar reportes DOCX con formato institucional y sobrio"""

    def __init__(self):
        self.document = None

    def generate_file(self, data: Any, options: Dict = None) -> io.BytesIO:
        if not self.validate_data(data):
            raise ValueError("Datos no válidos")

        self.document = Document()
        self._apply_base_styles()

        # Secciones principales del documento
        self._render_header(data)
        self._render_summary(data)
        self._render_section("Descripción", data.get("detailedDescription"))
        self._render_section("Causa", data.get("findingCause"))
        self._render_section("Conversación", data.get("conversation"))
        self._render_evidences(data.get("evidence", []))
        self._render_actions(data.get("actions", []))
        self._render_footer(data)

        # Guardar documento en buffer
        buffer = io.BytesIO()
        self.document.save(buffer)
        buffer.seek(0)

        # Log de control
        print("DOCX buffer size:", buffer.getbuffer().nbytes)

        return buffer

    # ---------------------------
    # RENDERIZADORES PRINCIPALES
    # ---------------------------

    def _render_header(self, data: Dict):
        """Encabezado institucional"""
        title = data.get("reportTitle", "Reporte de Hallazgo").upper()
        code = data.get("loraReportCode", "N/A")
        status = data.get("reportStatus", "N/A").upper()
        created = data.get("createdAt", "N/A")

        # Título principal
        heading = self.document.add_heading(title, level=0)
        heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Subtítulo con código y estado
        p = self.document.add_paragraph(f"Código: {code}    Estado: {status}")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Fecha de creación
        p2 = self.document.add_paragraph(f"Fecha de creación: {created}")
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER

        self._add_separator()

    def _render_summary(self, data: Dict):
        """Bloque resumen (proyecto, unidad, base, etc.)"""
        self.document.add_heading("Resumen", level=1)

        summary_fields = [
            ("Proyecto", data.get("project", "N/A")),
            ("Unidad", data.get("unity", "N/A")),
            ("Rig", data.get("rig", "N/A")),
            ("Base", data.get("base", "N/A")),
            ("Campo", data.get("field", "N/A")),
            ("Clasificación", data.get("hazardClassification", "N/A")),
            ("Tipo de Reporte", data.get("reportType", "N/A")),
            ("Tipo", data.get("hazardType", "N/A")),
            ("Creado por", data.get("createdBy", "N/A")),
            ("Actualizado", data.get("updatedAt", "N/A")),
        ]

        table = self.document.add_table(rows=1, cols=2)
        table.style = "Table Grid"
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Campo"
        hdr_cells[1].text = "Valor"

        for label, value in summary_fields:
            row = table.add_row().cells
            row[0].text = str(label)
            row[1].text = str(value)

        self._add_separator()

    def _render_section(self, title: str, content: str):
        """Sección textual genérica"""
        if not content:
            return
        self.document.add_heading(title, level=1)
        p = self.document.add_paragraph(content)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self._add_separator()

    def _render_evidences(self, evidences: List):
        """Sección de evidencias"""
        self.document.add_heading("Evidencias", level=1)
        if evidences:
            for e in evidences:
                self.document.add_paragraph(f"- {e}", style="List Bullet")
        else:
            self.document.add_paragraph("Sin evidencias adjuntas.")
        self._add_separator()

    def _render_actions(self, actions: List[Dict]):
        """Sección de acciones"""
        self.document.add_heading("Acciones", level=1)
        if not actions:
            self.document.add_paragraph("Sin acciones registradas.")
            return

        for i, act in enumerate(actions, 1):
            desc = act.get("description", "N/A")
            resp = act.get("responsible", "No asignado")
            due = act.get("dueDate", "N/A")
            status = act.get("status", "N/A").upper()

            self.document.add_paragraph(f"{i}. {desc}", style="List Number")
            self.document.add_paragraph(f"   Responsable: {resp}")
            self.document.add_paragraph(f"   Fecha límite: {due}")
            self.document.add_paragraph(f"   Estado: {status}")
            self.document.add_paragraph()

        self._add_separator()

    def _render_footer(self, data: Dict):
        """Pie de documento con identificación"""
        section = self.document.sections[-1]
        footer = section.footer.paragraphs[0] if section.footer.paragraphs else section.footer.add_paragraph()
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.text = (
            f"ID: {data.get('id', 'N/A')}  |  "
            f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  "
            "VALERA ECOSYSTEM"
        )

    # ---------------------------
    # UTILITARIOS / ESTILO
    # ---------------------------

    def _apply_base_styles(self):
        """Estilos base para texto institucional"""
        style = self.document.styles["Normal"]
        font = style.font
        font.name = "Courier New"
        font.size = Pt(10)

    def _add_separator(self):
        """Agrega un pequeño espacio como separador visual"""
        self.document.add_paragraph("\n")

    def get_content_type(self) -> str:
        """Retorna el tipo MIME del DOCX"""
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    def get_file_extension(self) -> str:
        """Retorna la extensión de archivo DOCX"""
        return ".docx"
