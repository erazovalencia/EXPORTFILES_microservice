from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import io
from typing import Any, Dict, List
from datetime import datetime
from ...base import BaseExportService

class XLSXListExportService(BaseExportService):
    """Servicio para exportar una lista de reportes en un archivo XLSX"""

    def __init__(self):
        self.workbook = None
        self.colors = {
            "header_fill": "D9D9D9",
            "row_odd_fill": "FFFFFF",
            "row_even_fill": "F2F2F2",
        }
        self.border = Border(
            left=Side(style="thin", color="BFBFBF"),
            right=Side(style="thin", color="BFBFBF"),
            top=Side(style="thin", color="BFBFBF"),
            bottom=Side(style="thin", color="BFBFBF")
        )

    def generate_file(self, data: Any, options: Dict = None) -> io.BytesIO:
        if not self.validate_data(data):
            raise ValueError("Datos no válidos")

        if not isinstance(data, list):
            raise ValueError("Para listado se espera una lista de reportes")

        self.workbook = Workbook()
        sheet = self.workbook.active
        sheet.title = "Listado Reportes"

        # Encabezados conforme al modelo completo
        headers = [
            "id", "userId", "reportTitle",
            "conversation", "base", "createdAt", "updatedAt", "unity", "rig", "project", "field",
            "reportType", "hazardClassification", "hazardType", "detailedDescription", "findingCause",
            "reportEvidence", "reportStatus", "closureActions", "externalName", "externalOrganization",
            "loraReportCode"
        ]

        # Escribir encabezado
        for col_index, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=col_index, value=header)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color=self.colors["header_fill"], fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = self.border
        sheet.row_dimensions[1].height = 20

        # Escribir filas
        for row_index, report in enumerate(data, start=2):
            fill_color = self.colors["row_even_fill"] if row_index % 2 == 0 else self.colors["row_odd_fill"]
            for col_index, header in enumerate(headers, start=1):
                # permitir navegación en campos anidados (e.g., user.externalName)
                value = self._get_nested_value(report, header)
                cell = sheet.cell(row=row_index, column=col_index, value=value)
                cell.fill = PatternFill(start_color=fill_color, fill_type="solid")
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                cell.border = self.border
            sheet.row_dimensions[row_index].height = 30

        # Ajustar ancho de columnas
        for column_cells in sheet.columns:
            max_length = 0
            column = column_cells[0].column_letter
            for cell in column_cells:
                try:
                    length = len(str(cell.value or ""))
                    if length > max_length:
                        max_length = length
                except:
                    pass
            sheet.column_dimensions[column].width = min(max_length + 5, 50)

        # Crear buffer
        buffer = io.BytesIO()
        self.workbook.save(buffer)
        buffer.seek(0)
        return buffer

    def _get_nested_value(self, obj: Dict, key: str) -> Any:
        """
        Permite acceder a valores anidados usando punto como separador,
        por ejemplo: 'user.externalName'
        """
        parts = key.split('.')
        value = obj
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part, None)
            else:
                value = None
            if value is None:
                return ""
        return value

    def get_content_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def get_file_extension(self) -> str:
        return ".xlsx"
