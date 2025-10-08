"""
Generador de reportes en múltiples formatos.
Soporta Excel, Word, PDF con formato APA 7.
"""
import pandas as pd
from datetime import datetime
from pathlib import Path
from io import BytesIO
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    logger.warning("python-docx no disponible. Instale con: pip install python-docx")

try:
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl import Workbook
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    logger.warning("openpyxl no disponible. Instale con: pip install openpyxl")


def generate_excel_report(
    results_df: pd.DataFrame,
    scope_totals: Dict[int, float],
    category_totals: Dict[str, float],
    total_tonnes: float,
    metadata: Dict
) -> BytesIO:
    """
    Genera reporte Excel con múltiples hojas y formato profesional.
    
    Args:
        results_df: DataFrame con resultados detallados
        scope_totals: Totales por scope {1: 100.5, 2: 50.2, 3: 30.1}
        category_totals: Totales por categoría
        total_tonnes: Total general en tCO2e
        metadata: Metadatos (fecha, fuente, etc.)
    
    Returns:
        BytesIO con archivo Excel
    """
    if not OPENPYXL_AVAILABLE:
        raise ImportError("openpyxl no está instalado")
    
    # Crear workbook
    output = BytesIO()
    wb = Workbook()
    
    # === HOJA 1: RESUMEN EJECUTIVO ===
    ws_summary = wb.active
    ws_summary.title = "Resumen"
    
    # Header
    ws_summary['A1'] = "REPORTE DE HUELLA DE CARBONO"
    ws_summary['A1'].font = Font(size=16, bold=True, color="FFFFFF")
    ws_summary['A1'].fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    ws_summary.merge_cells('A1:D1')
    ws_summary['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws_summary.row_dimensions[1].height = 30
    
    # Metadata
    row = 3
    ws_summary[f'A{row}'] = "Fecha de Generación:"
    ws_summary[f'B{row}'] = metadata.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    row += 1
    ws_summary[f'A{row}'] = "Metodología:"
    ws_summary[f'B{row}'] = "GHG Protocol (Scopes 1, 2, 3)"
    row += 1
    ws_summary[f'A{row}'] = "Fuente de Factores:"
    ws_summary[f'B{row}'] = metadata.get('factor_source', 'N/A')
    row += 2
    
    # Totales
    ws_summary[f'A{row}'] = "EMISIONES TOTALES"
    ws_summary[f'A{row}'].font = Font(size=14, bold=True, color="FFFFFF")
    ws_summary[f'A{row}'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    ws_summary.merge_cells(f'A{row}:D{row}')
    row += 1
    
    ws_summary[f'A{row}'] = "Total Emisiones:"
    ws_summary[f'B{row}'] = total_tonnes
    ws_summary[f'C{row}'] = "tCO₂e"
    ws_summary[f'B{row}'].font = Font(size=14, bold=True)
    row += 2
    
    # Totales por Scope
    ws_summary[f'A{row}'] = "DISTRIBUCIÓN POR ALCANCE"
    ws_summary[f'A{row}'].font = Font(size=12, bold=True, color="FFFFFF")
    ws_summary[f'A{row}'].fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
    ws_summary.merge_cells(f'A{row}:D{row}')
    row += 1
    
    # Headers
    ws_summary[f'A{row}'] = "Alcance"
    ws_summary[f'B{row}'] = "Emisiones (tCO₂e)"
    ws_summary[f'C{row}'] = "Porcentaje"
    for col in ['A', 'B', 'C']:
        ws_summary[f'{col}{row}'].font = Font(bold=True)
        ws_summary[f'{col}{row}'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    row += 1
    
    for scope in [1, 2, 3]:
        value = scope_totals.get(scope, 0)
        percentage = (value / total_tonnes * 100) if total_tonnes > 0 else 0
        ws_summary[f'A{row}'] = f"Scope {scope}"
        ws_summary[f'B{row}'] = round(value, 3)
        ws_summary[f'C{row}'] = f"{percentage:.1f}%"
        row += 1
    
    # Ajustar anchos de columna
    ws_summary.column_dimensions['A'].width = 25
    ws_summary.column_dimensions['B'].width = 20
    ws_summary.column_dimensions['C'].width = 15
    ws_summary.column_dimensions['D'].width = 15
    
    # === HOJA 2: RESULTADOS DETALLADOS ===
    ws_details = wb.create_sheet("Resultados Detallados")
    
    # Agregar headers
    for r_idx, row in enumerate(dataframe_to_rows(results_df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws_details.cell(row=r_idx, column=c_idx, value=value)
            if r_idx == 1:  # Header
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
                cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Auto-ajustar columnas
    for column in ws_details.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws_details.column_dimensions[column_letter].width = adjusted_width
    
    # === HOJA 3: TOTALES POR CATEGORÍA ===
    ws_categories = wb.create_sheet("Por Categoría")
    
    ws_categories['A1'] = "Categoría"
    ws_categories['B1'] = "Emisiones (tCO₂e)"
    for col in ['A', 'B']:
        ws_categories[f'{col}1'].font = Font(bold=True, color="FFFFFF")
        ws_categories[f'{col}1'].fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    
    row = 2
    for category, value in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        ws_categories[f'A{row}'] = category
        ws_categories[f'B{row}'] = round(value, 3)
        row += 1
    
    ws_categories.column_dimensions['A'].width = 30
    ws_categories.column_dimensions['B'].width = 20
    
    # Guardar
    wb.save(output)
    output.seek(0)
    
    return output


def generate_word_report(
    results_df: pd.DataFrame,
    scope_totals: Dict[int, float],
    category_totals: Dict[str, float],
    total_tonnes: float,
    metadata: Dict
) -> BytesIO:
    """
    Genera reporte Word en formato APA 7.
    
    Args:
        results_df: DataFrame con resultados
        scope_totals: Totales por scope
        category_totals: Totales por categoría
        total_tonnes: Total general
        metadata: Metadatos
    
    Returns:
        BytesIO con archivo Word
    """
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx no está instalado")
    
    doc = Document()
    
    # === PORTADA ===
    title = doc.add_heading('Reporte de Huella de Carbono', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph('Cálculo de Emisiones de Gases de Efecto Invernadero')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.size = Pt(14)
    
    doc.add_paragraph()  # Espacio
    
    # Metadata
    meta_para = doc.add_paragraph()
    meta_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_para.add_run(f"Fecha: {metadata.get('fecha', datetime.now().strftime('%Y-%m-%d'))}\n")
    meta_para.add_run(f"Metodología: GHG Protocol (Corporate Standard)\n")
    meta_para.add_run(f"Fuente de Factores: {metadata.get('factor_source', 'UK Gov 2025')}\n")
    
    doc.add_page_break()
    
    # === RESUMEN EJECUTIVO ===
    doc.add_heading('Resumen Ejecutivo', 1)
    
    summary_para = doc.add_paragraph(
        f"Este reporte presenta el inventario de emisiones de gases de efecto invernadero (GEI) "
        f"calculado según la metodología del GHG Protocol Corporate Accounting and Reporting Standard. "
        f"Las emisiones totales calculadas ascienden a {total_tonnes:.2f} toneladas de CO₂ equivalente (tCO₂e), "
        f"distribuidas en los tres alcances definidos por el estándar."
    )
    summary_para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # === RESULTADOS ===
    doc.add_heading('Resultados Generales', 1)
    
    # Tabla de totales
    table = doc.add_table(rows=4, cols=3)
    table.style = 'Light Grid Accent 1'
    
    # Headers
    headers = table.rows[0].cells
    headers[0].text = 'Alcance'
    headers[1].text = 'Emisiones (tCO₂e)'
    headers[2].text = 'Porcentaje'
    
    for cell in headers:
        cell.paragraphs[0].runs[0].font.bold = True
    
    # Datos
    for idx, scope in enumerate([1, 2, 3], start=1):
        row = table.rows[idx].cells
        value = scope_totals.get(scope, 0)
        percentage = (value / total_tonnes * 100) if total_tonnes > 0 else 0
        row[0].text = f"Scope {scope}"
        row[1].text = f"{value:.2f}"
        row[2].text = f"{percentage:.1f}%"
    
    doc.add_paragraph()
    
    # Total
    total_para = doc.add_paragraph()
    total_para.add_run('Total General: ').bold = True
    total_para.add_run(f"{total_tonnes:.2f} tCO₂e")
    total_para.runs[1].font.size = Pt(14)
    
    # === METODOLOGÍA ===
    doc.add_heading('Metodología', 1)
    
    method_text = doc.add_paragraph(
        "El cálculo de emisiones se realizó utilizando la ecuación fundamental del GHG Protocol:"
    )
    method_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    formula = doc.add_paragraph()
    formula.alignment = WD_ALIGN_PARAGRAPH.CENTER
    formula.add_run('E = AD × EF × GWP').bold = True
    formula.runs[0].font.size = Pt(12)
    
    doc.add_paragraph(
        "Donde:\n"
        "• E = Emisiones de GEI (kg CO₂e)\n"
        "• AD = Dato de Actividad (cantidad de combustible, electricidad, etc.)\n"
        "• EF = Factor de Emisión (kg CO₂e por unidad de actividad)\n"
        "• GWP = Potencial de Calentamiento Global (según IPCC AR5, horizonte 100 años)"
    )
    
    # === REFERENCIAS ===
    doc.add_page_break()
    doc.add_heading('Referencias', 1)
    
    references = [
        "WBCSD/WRI. (2004). The Greenhouse Gas Protocol: A Corporate Accounting and Reporting Standard (Revised Edition). World Resources Institute and World Business Council for Sustainable Development.",
        
        "UK Government. (2025). Greenhouse Gas Reporting: Conversion Factors 2025. Department for Energy Security and Net Zero. https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting",
        
        "IPCC. (2014). Climate Change 2014: Synthesis Report. Contribution of Working Groups I, II and III to the Fifth Assessment Report of the Intergovernmental Panel on Climate Change. IPCC, Geneva, Switzerland.",
    ]
    
    for ref in references:
        ref_para = doc.add_paragraph(ref, style='List Bullet')
        ref_para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # Guardar
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    
    return output


def check_dependencies() -> Dict[str, bool]:
    """
    Verifica qué librerías están disponibles.
    
    Returns:
        Dict con disponibilidad de cada librería
    """
    return {
        'excel': OPENPYXL_AVAILABLE,
        'word': DOCX_AVAILABLE,
        'pdf': False  # TODO: Implementar con reportlab o fpdf2
    }
