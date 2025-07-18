from fpdf import FPDF
import io
from typing import Any, Dict, List
from datetime import datetime
from ..services.base import BaseExportService
from ..models.ExportModel import TableData, DocumentData


class PDFExportService(BaseExportService):
    """Servicio para generar archivos PDF con diseño profesional"""
    
    def __init__(self):
        self.pdf = None
        # Colores del tema profesional
        self.colors = {
            'primary': (41, 128, 185),      # Azul profesional
            'secondary': (52, 73, 94),      # Gris oscuro
            'accent': (231, 76, 60),        # Rojo acento
            'light_gray': (236, 240, 241),  # Gris claro
            'dark_gray': (127, 140, 141),   # Gris medio
            'white': (255, 255, 255),       # Blanco
            'success': (39, 174, 96),       # Verde
        }
        
    def generate_file(self, data: Any, options: Dict = None) -> io.BytesIO:
        """Genera un archivo PDF con diseño profesional"""
        if not self.validate_data(data):
            raise ValueError("Los datos proporcionados no son válidos")
        
        try:
            # Configurar PDF con márgenes profesionales
            self.pdf = FPDF(orientation='P', unit='mm', format='A4')
            self.pdf.set_auto_page_break(auto=True, margin=20)
            self.pdf.add_page()
            
            # Agregar encabezado del documento
            self._add_header()
            
            # Si los datos son un diccionario con estructura de documento
            if isinstance(data, dict):
                self._process_document_data(data, options or {})
            else:
                # Datos simples como texto
                self._add_simple_text(str(data))
            
            # Agregar pie de página
            self._add_footer()
            
            # Guardar en buffer
            buffer = io.BytesIO()
            pdf_output = self.pdf.output(dest='S')
            
            # fpdf2 puede devolver bytes o bytearray dependiendo de la versión
            if isinstance(pdf_output, str):
                buffer.write(pdf_output.encode('latin-1'))
            else:
                # Ya es bytes o bytearray
                buffer.write(pdf_output)
            
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            raise ValueError(f"Error al generar PDF: {str(e)}")
    
    def _add_header(self):
        """Añade un encabezado profesional al documento"""
        # Línea superior decorativa
        self.pdf.set_fill_color(*self.colors['primary'])
        self.pdf.rect(10, 10, 190, 3, 'F')
        
        # Espacio después de la línea
        self.pdf.ln(8)
        
        # Logo/Título de la empresa (simulado)
        self.pdf.set_font('Arial', 'B', 20)
        self.pdf.set_text_color(*self.colors['primary'])
        self.pdf.cell(0, 12, 'REPORTE', ln=True, align='C')
        
        # Fecha y hora de generación
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_text_color(*self.colors['dark_gray'])
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.pdf.cell(0, 6, f'Generado el: {fecha_actual}', ln=True, align='R')
        
        # Línea separadora
        self.pdf.set_draw_color(*self.colors['light_gray'])
        self.pdf.line(10, self.pdf.get_y() + 2, 200, self.pdf.get_y() + 2)
        
        self.pdf.ln(8)
    
    def _add_footer(self):
        """Añade un pie de página profesional"""
        # Posicionar en la parte inferior
        self.pdf.set_y(-20)
        
        # Línea separadora
        self.pdf.set_draw_color(*self.colors['light_gray'])
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        
        self.pdf.ln(2)
        
        # Información del pie
        self.pdf.set_font('Arial', 'I', 8)
        self.pdf.set_text_color(*self.colors['dark_gray'])
        self.pdf.cell(0, 4, 'Documento generado automáticamente por VALERA exp fille service', ln=True, align='C')
        self.pdf.cell(0, 4, f'Página {self.pdf.page_no()}', ln=True, align='C')
    
    def _process_document_data(self, data: Dict, options: Dict):
        """Procesa datos estructurados de documento con diseño profesional"""
        # Título principal del documento con estilo
        if 'title' in data and data['title']:
            self._add_main_title(data['title'])
        
        # Resumen ejecutivo o introducción
        if 'summary' in data and data['summary']:
            self._add_section('RESUMEN EJECUTIVO', data['summary'])
        
        # Contenido de párrafos organizados por secciones
        if 'content' in data and isinstance(data['content'], list):
            self._add_section('CONTENIDO', data['content'])
        
        # Tablas con diseño profesional
        if 'tables' in data and isinstance(data['tables'], list):
            self._add_section_title('DATOS Y ANÁLISIS')
            for i, table in enumerate(data['tables'], 1):
                self._add_professional_table(table, f"Tabla {i}")
        
        # Si es una tabla simple, mostrarla como tabla principal
        if 'headers' in data and 'rows' in data:
            self._add_section_title('INFORMACIÓN PRINCIPAL')
            self._add_professional_table(data, "Datos Principales")
        
        # Métricas o KPIs si están presentes
        if 'metrics' in data and isinstance(data['metrics'], dict):
            self._add_metrics_section(data['metrics'])
        
        # Procesar datos restantes si no se han procesado ya
        self._process_additional_data(data)
    
    def _process_additional_data(self, data):
        """Procesa datos adicionales que no fueron procesados en las secciones principales"""
        processed_keys = {'title', 'subtitle', 'summary', 'content', 'headers', 'rows', 'metrics'}
        
        if isinstance(data, dict):
            remaining_data = {k: v for k, v in data.items() if k not in processed_keys}
            
            if remaining_data:
                self._add_section_title('INFORMACIÓN ADICIONAL')
                for key, value in remaining_data.items():
                    if isinstance(value, (dict, list)) and value:
                        # Si el valor es complejo, procesarlo recursivamente
                        self._add_section_title(str(key).upper().replace('_', ' '))
                        self._process_dynamic_data(value)
                    elif value:
                        # Valor simple
                        self.pdf.set_font('Arial', 'B', 10)
                        self.pdf.set_text_color(*self.colors['secondary'])
                        clean_key = str(key).replace('_', ' ').title().encode('latin-1', 'ignore').decode('latin-1')
                        self.pdf.cell(50, 6, f"{clean_key}:", ln=False)
                        
                        self.pdf.set_font('Arial', '', 10)
                        self.pdf.set_text_color(*self.colors['dark_gray'])
                        clean_value = str(value).encode('latin-1', 'ignore').decode('latin-1')
                        self.pdf.cell(0, 6, clean_value, ln=True)
                        self.pdf.ln(2)
    
    def _process_dynamic_data(self, data):
        """Procesa cualquier tipo de dato de manera profesional"""
        if isinstance(data, str):
            self._add_simple_text(data)
        elif isinstance(data, list):
            # Procesar lista con formato profesional
            self._add_section_title('LISTADO')
            for i, item in enumerate(data, 1):
                if isinstance(item, dict) and 'headers' in item:
                    self._add_professional_table(item, f"Tabla {i}")
                else:
                    self.pdf.set_font('Arial', '', 10)
                    self.pdf.set_text_color(*self.colors['secondary'])
                    clean_item = str(item).encode('latin-1', 'ignore').decode('latin-1')
                    self.pdf.cell(10, 6, f"{i}.", ln=False)
                    self.pdf.cell(0, 6, clean_item, ln=True)
                    self.pdf.ln(2)
        elif isinstance(data, dict) and 'headers' in data:
            self._add_professional_table(data)
        elif isinstance(data, dict) and any(key.lower() in ['metric', 'kpi', 'total', 'sum', 'count'] for key in data.keys()):
            self._add_metrics_section(data)
        elif isinstance(data, dict):
            # Procesar diccionario con formato profesional
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    # Si el valor es complejo, procesarlo recursivamente
                    self._add_section_title(str(key).upper())
                    self._process_dynamic_data(value)
                else:
                    # Valor simple
                    self.pdf.set_font('Arial', 'B', 10)
                    self.pdf.set_text_color(*self.colors['secondary'])
                    clean_key = str(key).encode('latin-1', 'ignore').decode('latin-1')
                    self.pdf.cell(50, 6, f"{clean_key}:", ln=False)
                    
                    self.pdf.set_font('Arial', '', 10)
                    self.pdf.set_text_color(*self.colors['dark_gray'])
                    clean_value = str(value).encode('latin-1', 'ignore').decode('latin-1')
                    self.pdf.cell(0, 6, clean_value, ln=True)
                    self.pdf.ln(2)
    
    def _add_main_title(self, title: str):
        """Añade el título principal con diseño elegante"""
        # Fondo decorativo para el título
        self.pdf.set_fill_color(*self.colors['primary'])
        self.pdf.rect(10, self.pdf.get_y(), 190, 15, 'F')
        
        # Título en blanco sobre fondo azul
        self.pdf.set_font('Arial', 'B', 18)
        self.pdf.set_text_color(*self.colors['white'])
        clean_title = str(title).encode('latin-1', 'ignore').decode('latin-1')
        
        # Centrar el título verticalmente en el rectángulo
        current_y = self.pdf.get_y()
        self.pdf.set_y(current_y + 4)
        self.pdf.cell(190, 7, clean_title, ln=True, align='C')
        
        # Resetear color de texto
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(8)
    
    def _add_section_title(self, title: str):
        """Añade un título de sección con estilo"""
        self.pdf.ln(5)
        
        # Línea decorativa antes del título
        self.pdf.set_draw_color(*self.colors['primary'])
        self.pdf.set_line_width(0.8)
        self.pdf.line(10, self.pdf.get_y(), 50, self.pdf.get_y())
        
        self.pdf.ln(2)
        
        # Título de sección
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.colors['secondary'])
        clean_title = str(title).encode('latin-1', 'ignore').decode('latin-1')
        self.pdf.cell(0, 8, clean_title, ln=True)
        
        # Línea decorativa después del título
        self.pdf.set_line_width(0.3)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(5)
    
    def _add_section(self, title: str, content):
        """Añade una sección completa con título y contenido"""
        self._add_section_title(title)
        
        if isinstance(content, list):
            for paragraph in content:
                self._add_paragraph(str(paragraph))
        else:
            self._add_paragraph(str(content))
    
    def _add_paragraph(self, text: str):
        """Añade un párrafo con formato profesional"""
        self.pdf.set_font('Arial', '', 11)
        self.pdf.set_text_color(*self.colors['secondary'])
        
        # Limpiar texto
        clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
        
        # Añadir el párrafo con sangría
        self.pdf.set_x(15)  # Sangría de 5mm
        self.pdf.multi_cell(180, 6, clean_text)
        self.pdf.ln(3)
        
        self.pdf.set_text_color(0, 0, 0)
    
    def _add_professional_table(self, table_data: Dict, table_label: str = ""):
        """Añade una tabla con diseño profesional y moderno"""
        headers = table_data.get('headers', [])
        rows = table_data.get('rows', [])
        title = table_data.get('title', table_label)
        
        if not headers or not rows:
            return
        
        # Título de la tabla
        if title:
            self.pdf.ln(3)
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.set_text_color(*self.colors['secondary'])
            clean_title = str(title).encode('latin-1', 'ignore').decode('latin-1')
            self.pdf.cell(0, 8, clean_title, ln=True)
            self.pdf.ln(2)
        
        # Calcular ancho de columnas dinámicamente
        table_width = 180  # Ancho total de la tabla
        col_width = table_width / len(headers)
        
        # Encabezados con estilo profesional
        self.pdf.set_font('Arial', 'B', 10)
        self.pdf.set_fill_color(*self.colors['primary'])
        self.pdf.set_text_color(*self.colors['white'])
        self.pdf.set_draw_color(*self.colors['secondary'])
        self.pdf.set_line_width(0.3)
        
        # Centrar la tabla
        start_x = (210 - table_width) / 2
        self.pdf.set_x(start_x)
        
        for header in headers:
            clean_header = str(header).encode('latin-1', 'ignore').decode('latin-1')
            self.pdf.cell(col_width, 10, clean_header, border=1, align='C', fill=True)
        self.pdf.ln()
        
        # Filas de datos con colores alternados
        self.pdf.set_font('Arial', '', 9)
        self.pdf.set_text_color(*self.colors['secondary'])
        
        for i, row in enumerate(rows):
            # Color de fondo alternado
            if i % 2 == 0:
                self.pdf.set_fill_color(*self.colors['light_gray'])
                fill = True
            else:
                self.pdf.set_fill_color(*self.colors['white'])
                fill = False
            
            self.pdf.set_x(start_x)
            
            for j, item in enumerate(row):
                clean_item = str(item).encode('latin-1', 'ignore').decode('latin-1')
                
                # Alineación inteligente: números a la derecha, texto a la izquierda
                align = 'R' if self._is_number(item) else 'L'
                
                self.pdf.cell(col_width, 8, clean_item, border=1, align=align, fill=fill)
            self.pdf.ln()
        
        # Línea de cierre de la tabla
        self.pdf.set_draw_color(*self.colors['primary'])
        self.pdf.set_line_width(0.8)
        self.pdf.line(start_x, self.pdf.get_y(), start_x + table_width, self.pdf.get_y())
        
        # Resetear colores
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.ln(8)
    
    def _add_metrics_section(self, metrics: Dict):
        """Añade una sección de métricas/KPIs con diseño atractivo"""
        self._add_section_title('MÉTRICAS CLAVE')
        
        # Crear cajas de métricas
        metrics_per_row = 3
        box_width = 180 / metrics_per_row
        current_x = 15
        
        for i, (key, value) in enumerate(metrics.items()):
            if i > 0 and i % metrics_per_row == 0:
                self.pdf.ln(25)
                current_x = 15
            
            # Caja de métrica
            self.pdf.set_fill_color(*self.colors['light_gray'])
            self.pdf.rect(current_x, self.pdf.get_y(), box_width - 5, 20, 'F')
            
            # Valor de la métrica
            self.pdf.set_font('Arial', 'B', 16)
            self.pdf.set_text_color(*self.colors['primary'])
            self.pdf.set_xy(current_x + 5, self.pdf.get_y() + 3)
            clean_value = str(value).encode('latin-1', 'ignore').decode('latin-1')
            self.pdf.cell(box_width - 10, 8, clean_value, align='C')
            
            # Etiqueta de la métrica
            self.pdf.set_font('Arial', '', 9)
            self.pdf.set_text_color(*self.colors['dark_gray'])
            self.pdf.set_xy(current_x + 5, self.pdf.get_y() + 8)
            clean_key = str(key).encode('latin-1', 'ignore').decode('latin-1')
            self.pdf.cell(box_width - 10, 6, clean_key, align='C')
            
            current_x += box_width
        
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.ln(15)
    
    def _is_number(self, value):
        """Verifica si un valor es numérico"""
        try:
            float(str(value).replace(',', '').replace('$', '').replace('%', ''))
            return True
        except (ValueError, TypeError):
            return False
    
    def _add_simple_text(self, text: str):
        """Añade texto simple con formato mejorado"""
        self._add_section_title('INFORMACIÓN')
        self._add_paragraph(text)
    
    def get_content_type(self) -> str:
        """Retorna el tipo de contenido MIME para PDF"""
        return "application/pdf"
    
    def get_file_extension(self) -> str:
        """Retorna la extensión del archivo PDF"""
        return ".pdf"