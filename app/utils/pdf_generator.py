from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logos
        if getattr(self, 'logo_cliente', None) and os.path.exists(self.logo_cliente):
            self.image(self.logo_cliente, 10, 8, 30)
        if getattr(self, 'logo_subcontrata', None) and os.path.exists(self.logo_subcontrata):
            self.image(self.logo_subcontrata, 170, 8, 30)

        # Título principal
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Informe Técnico de Prueba', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')


def generar_pdf_test(test_data, resultados_pdf, output_path):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.logo_cliente = f"static/img/logos/{test_data.get('logo_cliente', '')}"
    pdf.logo_subcontrata = f"static/img/logos/{test_data.get('logo_subcontrata', '')}"
    pdf.add_page()

    # Título del test
    pdf.set_font('Arial', 'B', 12)
    titulo = f"{test_data['equipo_id']} - {test_data.get('tipo_prueba', '').capitalize()}"
    pdf.cell(0, 10, titulo, ln=True, align='C')
    pdf.ln(5)

    # Datos del equipo
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Datos del Equipo:', ln=True)
    pdf.set_font('Arial', '', 10)
    for clave, valor in test_data['detalles_equipo'].items():
        pdf.cell(60, 8, f"{clave}:", border=1)
        pdf.cell(0, 8, f"{valor}", border=1, ln=True)
    pdf.ln(5)

    # Resultados
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Resultados:', ln=True)
    pdf.set_font('Arial', 'B', 9)

    headers = ['Cable Set', 'Punto', 'Referencia', 'Resultado', 'Unidad', 'Aprobado', 'Obs.']
    col_widths = [18, 25, 25, 25, 20, 20, 45]

    # Encabezados
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 7, header, border=1, align='C')
    pdf.ln()

    pdf.set_font('Arial', '', 9)

    for r in resultados_pdf:
        fila = [
            str(r.get('cable_set', '-')),
            r.get('punto_prueba', ''),
            str(r.get('referencia_valor', '-')),
            str(r.get('resultado_valor', '-')),
            r.get('unidad', ''),
            "✔" if r.get('aprobado') in (True, "SI", "✔") else "✘",
            r.get('observaciones', '')
        ]
        for i, valor in enumerate(fila):
            pdf.cell(col_widths[i], 7, valor, border=1)
        pdf.ln()

        # Imágenes (si existen)
        for imagen in test_data.get("imagenes", []):
            if (
                imagen.get("cable_set") == r.get("cable_set")
                and imagen.get("punto_prueba") == r.get("punto_prueba")
                and os.path.exists(imagen["path"])
            ):
                try:
                    # Ajustar la imagen proporcionalmente
                    pdf.ln(1)
                    pdf.image(imagen["path"], x=pdf.get_x(), y=pdf.get_y(), w=50)
                    pdf.ln(30)
                except Exception as e:
                    pdf.set_font('Arial', 'I', 7)
                    pdf.cell(0, 6, f"[No se pudo mostrar la imagen: {e}]", ln=True)

    # Firma y fecha
    pdf.ln(8)
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 6, f"Realizado por: {test_data.get('nombre_usuario', 'Desconocido')}", ln=True)
    pdf.cell(0, 6, f"Fecha: {test_data.get('fecha', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))}", ln=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
