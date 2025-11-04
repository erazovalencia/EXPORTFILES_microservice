from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import io
from typing import Any, Dict, List
from datetime import datetime
from ...base import BaseExportService


class XLSXExportService(BaseExportService):
    """Servicio para generar reportes XLSX con formato empresarial estructurado"""

    def __init__(self):
        self.workbook = None
        # Colores y estilos
        self.colors = {
            "header_fill": "DCE6F1",
            "summary_fill": "F2F2F2",
            "open_fill": "F8CECC",   # rojo claro
            "close_fill": "D5E8D4",  # verde claro
        }
        self.border = Border(
            left=Side(style="thin", color="BFBFBF"),
            right=Side(style="thin", color="BFBFBF"),
            top=Side(style="thin", color="BFBFBF"),
            bottom=Side(style="thin", color="BFBFBF")
        )

    def generate_file(self, data: Any, options: Dict = None) -> io.BytesIO:
        """Genera un archivo XLSX con diseño estructurado"""
        if not self.validate_data(data):
            raise ValueError("Los datos proporcionados no son válidos")

        self.workbook = Workbook()
        default_sheet = self.workbook.active
        self.workbook.remove(default_sheet)

        if isinstance(data, dict):
            self._create_summary_sheet(data)
            self._create_details_sheet(data)
            self._create_actions_sheet(data)
        else:
            self._create_simple_sheet(data)

        buffer = io.BytesIO()
        self.workbook.save(buffer)
        buffer.seek(0)
        return buffer

    # ---------------------------
    # HOJA 1: RESUMEN
    # ---------------------------
    def _create_summary_sheet(self, data: Dict):
        ws = self.workbook.create_sheet("Resumen")
        ws.sheet_properties.tabColor = "1F497D"

        ws.merge_cells("A1:B1")
        title = ws["A1"]
        title.value = data.get("reportTitle", "Reporte de Hallazgo").upper()
        title.font = Font(bold=True, size=14, color="1F497D")
        title.alignment = Alignment(horizontal="center")
        ws.row_dimensions[1].height = 25

        # Campos clave
        summary_fields = [
            ("Identificador", data.get("id", "N/A")),
            ("Código", data.get("loraReportCode", "N/A")),
            ("Estado", data.get("reportStatus", "N/A").upper()),
            ("Proyecto", data.get("project", "N/A")),
            ("Unidad", data.get("unity", "N/A")),
            ("Rig", data.get("rig", "N/A")),
            ("Base", data.get("base", "N/A")),
            ("Campo", data.get("field", "N/A")),
            ("Clasificación", data.get("hazardClassification", "N/A")),
            ("Tipo de Reporte", data.get("reportType", "N/A")),
            ("Tipo", data.get("hazardType", "N/A")),
            ("Creado por", data.get("createdBy", "N/A")),
            ("Creado en", data.get("createdAt", "N/A")),
            ("Actualizado", data.get("updatedAt", "N/A")),
        ]

        start_row = 3
        ws.append(["Campo", "Valor"])
        ws["A3"].font = ws["B3"].font = Font(bold=True)
        ws["A3"].fill = ws["B3"].fill = PatternFill(start_color=self.colors["header_fill"], fill_type="solid")
        ws["A3"].alignment = ws["B3"].alignment = Alignment(horizontal="center")

        for i, (label, value) in enumerate(summary_fields, start=start_row + 1):
            ws[f"A{i}"] = label
            ws[f"B{i}"] = str(value)
            ws[f"A{i}"].fill = PatternFill(start_color=self.colors["summary_fill"], fill_type="solid")
            ws[f"A{i}"].font = Font(bold=True)
            ws[f"A{i}"].border = ws[f"B{i}"].border = self.border

        ws.column_dimensions["A"].width = 25
        ws.column_dimensions["B"].width = 60

    # ---------------------------
    # HOJA 2: DETALLES
    # ---------------------------
    def _create_details_sheet(self, data: Dict):
        ws = self.workbook.create_sheet("Detalles")
        ws.sheet_properties.tabColor = "76933C"

        sections = [
            ("Descripción", data.get("detailedDescription")),
            ("Causa", data.get("findingCause")),
            ("Conversación", data.get("conversation")),
            ("Evidencias", "\n".join(data.get("evidence", [])) if data.get("evidence") else "Sin evidencias adjuntas"),
        ]

        row = 1
        for title, content in sections:
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
            cell = ws.cell(row=row, column=1, value=title.upper())
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4BACC6", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            ws.row_dimensions[row].height = 22

            row += 1
            ws.merge_cells(start_row=row, start_column=1, end_row=row + 3, end_column=3)
            text_cell = ws.cell(row=row, column=1, value=content or "N/A")
            text_cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="justify")
            text_cell.border = self.border
            ws.row_dimensions[row].height = 80
            row += 5

        ws.column_dimensions["A"].width = 25
        ws.column_dimensions["B"].width = 45
        ws.column_dimensions["C"].width = 45

    # ---------------------------
    # HOJA 3: ACCIONES
    # ---------------------------
    def _create_actions_sheet(self, data: Dict):
        ws = self.workbook.create_sheet("Acciones")
        ws.sheet_properties.tabColor = "C0504D"

        headers = ["Descripción", "Responsable", "Fecha Límite", "Estado"]
        ws.append(headers)

        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="404040", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
            cell.border = self.border

        actions = data.get("actions", [])
        if not actions:
            ws.append(["Sin acciones registradas"])
        else:
            for i, act in enumerate(actions, start=2):
                status = act.get("status", "open").lower()
                fill_color = self.colors["close_fill"] if status == "close" else self.colors["open_fill"]

                ws.cell(row=i, column=1, value=act.get("description", "N/A"))
                ws.cell(row=i, column=2, value=act.get("responsible", "No asignado"))
                ws.cell(row=i, column=3, value=act.get("dueDate", "N/A"))
                ws.cell(row=i, column=4, value=status.upper())

                for col in range(1, 5):
                    c = ws.cell(row=i, column=col)
                    c.alignment = Alignment(vertical="center", wrap_text=True)
                    c.border = self.border
                    c.fill = PatternFill(start_color=fill_color, fill_type="solid")

        ws.column_dimensions["A"].width = 50
        ws.column_dimensions["B"].width = 30
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 15

    # ---------------------------
    # HOJA SIMPLE (fallback)
    # ---------------------------
    def _create_simple_sheet(self, data: Any):
        ws = self.workbook.create_sheet("Datos")
        ws["A1"] = str(data)
        ws["A1"].font = Font(bold=True)
        ws.column_dimensions["A"].width = 50

    # ---------------------------
    # METADATOS
    # ---------------------------
    def get_content_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def get_file_extension(self) -> str:
        return ".xlsx"
