# app/utils/pdf_generator.py
from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Informe de Pruebas Eléctricas", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def generar_pdf_test(test_data, resultados, output_path="output/test.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    # Datos generales
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Datos del Equipo", ln=1)
    pdf.set_font("Arial", size=11)

    pdf.cell(0, 8, f"Equipo: {test_data['equipo_id']}", ln=1)
    pdf.cell(0, 8, f"Fecha de prueba: {test_data.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", ln=1)
    pdf.ln(3)

    # Detalles del equipo
    detalles = test_data.get("detalles_equipo", {})
    for etiqueta, valor in detalles.items():
        pdf.cell(0, 8, f"{etiqueta}: {valor}", ln=1)

    if test_data.get("observaciones"):
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Observaciones Generales", ln=1)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, test_data["observaciones"])

    pdf.ln(8)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Resultados del Test", ln=1)
    pdf.set_font("Arial", size=10)

    # Encabezado tabla
    col_widths = [35, 35, 35, 25, 60]
    pdf.set_fill_color(220, 220, 220)
    headers = ["Punto", "Referencia", "Resultado", "Estado", "Observaciones"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border=1, fill=True)
    pdf.ln()

    for res in resultados:
        estado = "APROBADO" if res["aprobado"] else "RECHAZADO"
        valores = [
            res["punto_prueba"],
            str(res["referencia_valor"]),
            str(res["resultado_valor"]),
            estado,
            res.get("observaciones", "")
        ]
        for i, val in enumerate(valores):
            pdf.cell(col_widths[i], 10, val, border=1)
        pdf.ln()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    return output_path

def generar_informe_test(test_type, test_data, resultados, output_dir="app/media"):
    nombre_equipo = test_data["equipo_id"]
    return generar_pdf_test(test_data, resultados, os.path.join(output_dir, f"{test_type.lower()}/reporte_{nombre_equipo}.pdf"))
