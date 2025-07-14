# app/utils/pdf_generator.py

from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logos (cliente y subcontrata)
        if hasattr(self, 'logo_cliente') and self.logo_cliente:
            self.image(self.logo_cliente, 10, 8, 33)
        if hasattr(self, 'logo_subcontrata') and self.logo_subcontrata:
            self.image(self.logo_subcontrata, 165, 8, 33)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Informe Técnico de Prueba', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

def generar_pdf_test(test_data, resultados_pdf, output_path):
    pdf = PDF()
    pdf.logo_cliente = f"static/img/logos/{test_data['logo_cliente']}"
    pdf.logo_subcontrata = f"static/img/logos/{test_data['logo_subcontrata']}"
    pdf.add_page()

    # Título
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"{test_data['detalles_equipo']['Tipo de Equipo']} - {test_data['tipo_prueba'].capitalize()}", ln=True, align='C')
    pdf.ln(10)

    # Datos del equipo en tabla
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Datos del Equipo:', ln=True)
    pdf.set_font('Arial', '', 11)
    for clave, valor in test_data['detalles_equipo'].items():
        pdf.cell(60, 8, f"{clave}", border=1)
        pdf.cell(0, 8, f"{valor}", border=1, ln=True)

    # Línea separadora
    pdf.ln(10)

    # Resultados de la prueba
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Resultados:', ln=True)

    pdf.set_font('Arial', 'B', 10)
    headers = ['Cable Set', 'Punto', 'Referencia', 'Resultado', 'Unidad', 'Aprobado', 'Observaciones']
    col_widths = [20, 25, 25, 25, 20, 20, 50]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1)
    pdf.ln()

    pdf.set_font('Arial', '', 10)
    for r in resultados_pdf:
        fila = [
            str(r.get('cable_set', '')),
            r.get('punto_prueba', ''),
            r.get('referencia_valor', ''),
            str(r.get('resultado_valor', '')),
            r.get('unidad', ''),
            r.get('aprobado', ''),
            r.get('observaciones', '')
        ]
        for i, valor in enumerate(fila):
            pdf.cell(col_widths[i], 8, valor, border=1)
        pdf.ln()
        for r in resultados_pdf:
        fila = [
            str(r.get('cable_set', '')),
            r.get('punto_prueba', ''),
            r.get('referencia_valor', ''),
            str(r.get('resultado_valor', '')),
            r.get('unidad', ''),
            r.get('aprobado', ''),
            r.get('observaciones', '')
        ]
        for i, valor in enumerate(fila):
            pdf.cell(col_widths[i], 8, valor, border=1)
        pdf.ln()

        # Mostrar imagen si existe para este punto
        imagenes = test_data.get("imagenes", [])
        for imagen in imagenes:
            if (imagen["cable_set"] == r.get("cable_set") and
                imagen["punto_prueba"] == r.get("punto_prueba")):
                if os.path.exists(imagen["path"]):
                    try:
                        pdf.image(imagen["path"], x=pdf.get_x(), y=pdf.get_y(), w=50)
                        pdf.ln(30)
                    except Exception as e:
                        pdf.set_font('Arial', 'I', 8)
                        pdf.cell(0, 10, f"[Error al mostrar imagen: {e}]", ln=True)


    # Observaciones y usuario
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Realizado por: {test_data.get('nombre_usuario', 'Desconocido')}", ln=True)
    pdf.cell(0, 10, f"Fecha: {test_data.get('fecha', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))}", ln=True)

    # Guardar
    pdf.output(output_path)
