# app/utils/pdf_generator.py
from fpdf import FPDF
from datetime import datetime
import os

def generar_pdf_test(test_data, resultados, output_path="output/test.pdf"):
    """
    Función unificada para generar PDFs de pruebas (compatible con continuidad y megado)
    
    :param test_data: Dict con {equipo_id, usuario_id, observaciones, fecha}
    :param resultados: Lista de dicts con {punto_prueba, referencia_valor, resultado_valor, aprobado}
    :param output_path: Ruta de salida del PDF
    :return: Ruta del archivo generado
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Reporte de Pruebas Eléctricas", ln=1, align='C')
    pdf.ln(10)
    
    # Datos del test
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Equipo ID: {test_data['equipo_id']}", ln=1)
    pdf.cell(0, 10, f"Fecha: {test_data.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", ln=1)
    
    if test_data.get('observaciones'):
        pdf.multi_cell(0, 10, f"Observaciones: {test_data['observaciones']}")
    
    # Tabla de resultados
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Resultados:", ln=1)
    pdf.set_font("Arial", size=10)
    
    # Cabecera de tabla
    col_widths = [60, 40, 40, 30]
    pdf.cell(col_widths[0], 10, "Punto Prueba", border=1)
    pdf.cell(col_widths[1], 10, "Valor Ref.", border=1)
    pdf.cell(col_widths[2], 10, "Valor Medido", border=1)
    pdf.cell(col_widths[3], 10, "Estado", border=1)
    pdf.ln()
    
    # Filas de datos
    for res in resultados:
        estado = "APROBADO" if res["aprobado"] else "RECHAZADO"
        pdf.cell(col_widths[0], 10, res["punto_prueba"], border=1)
        pdf.cell(col_widths[1], 10, str(res["referencia_valor"]), border=1)
        pdf.cell(col_widths[2], 10, str(res["resultado_valor"]), border=1)
        pdf.cell(col_widths[3], 10, estado, border=1)
        pdf.ln()
    
    # Guardar PDF
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    
    return output_path

def generar_informe_test(test_type, test_data, resultados, output_dir="app/media"):
    """Función alternativa más moderna (compatible con ambas versiones)"""
    return generar_pdf_test(test_data, resultados, os.path.join(output_dir, f"{test_type.lower()}/reporte_{test_data['equipo_id']}.pdf"))