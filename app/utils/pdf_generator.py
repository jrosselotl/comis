from fpdf import FPDF
import os
from datetime import datetime

# ✅ Ruta absoluta segura
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "..", "static", "fonts")
IMG_DIR = os.path.join(BASE_DIR, "..", "static", "img", "logos")

# ✅ Color corporativo azul
CORPORATE_BLUE = (0, 51, 102)  # Azul oscuro

class PDF(FPDF):
    def header(self):
        # ✅ Franja azul completa
        self.set_fill_color(*CORPORATE_BLUE)
        self.rect(0, 0, 210, 20, "F")

        # ✅ Logos
        if hasattr(self, 'client_logo') and self.client_logo and os.path.exists(self.client_logo):
            self.image(self.client_logo, 10, 4, 25)
        if hasattr(self, 'subcontractor_logo') and self.subcontractor_logo and os.path.exists(self.subcontractor_logo):
            self.image(self.subcontractor_logo, 175, 4, 25)

        # ✅ Título blanco
        self.set_font("DejaVu", "B", 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Technical Test Report", align="C", ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def generate_test_pdf(test_data, pdf_results, output_path):
    pdf = PDF()

    # ✅ Fuente con soporte UTF-8
    pdf.add_font("DejaVu", "", os.path.join(FONTS_DIR, "DejaVuSans.ttf"), uni=True)
    pdf.add_font("DejaVu", "B", os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf"), uni=True)
    pdf.add_font("DejaVu", "I", os.path.join(FONTS_DIR, "DejaVuSans-Oblique.ttf"), uni=True)
    pdf.set_font("DejaVu", "B", 14)

    # ✅ Logos absolutos
    client_logo_name = test_data.get("client_logo", "")
    subcontractor_logo_name = test_data.get("subcontractor_logo", "")
    pdf.client_logo = os.path.join(IMG_DIR, client_logo_name) if client_logo_name else None
    pdf.subcontractor_logo = os.path.join(IMG_DIR, subcontractor_logo_name) if subcontractor_logo_name else None

    pdf.add_page()

    # ✅ Título completo
    project_name = test_data["equipment_details"].get("Project", "")
    equipment_code = test_data.get("equipment_id", "")
    test_type = test_data.get("test_type", "").capitalize()
    title = f"{project_name} – {equipment_code} – {test_type}"
    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, title, align="C")
    pdf.ln(5)

    # ✅ Equipment details con estilo
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Equipment Details:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    for key, value in test_data['equipment_details'].items():
        pdf.set_fill_color(*CORPORATE_BLUE)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(60, 8, str(key), border=1, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, str(value), border=1, ln=True)
    pdf.ln(5)

    # ✅ Test results con cabecera azul
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Results:", ln=True)
    pdf.set_font("DejaVu", "B", 10)

    headers = ["Cable Set", "Test Point", "Result", "Unit", "Observations"]
    col_widths = [25, 40, 30, 25, 70]

    pdf.set_fill_color(*CORPORATE_BLUE)
    pdf.set_text_color(255, 255, 255)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(0, 0, 0)
    for r in pdf_results:
        row = [
            str(r.get("cable_set", "")),
            r.get("test_point", ""),
            str(r.get("result_value", "")),
            r.get("unit", ""),
            r.get("observation", "")
        ]
        for i, value in enumerate(row):
            pdf.cell(col_widths[i], 8, str(value)[:40], border=1)
        pdf.ln()

    # ✅ Anexos con imágenes al final
    images = test_data.get("images", [])
    if images:
        pdf.add_page()
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "ANNEXES", ln=True, align="C")
        pdf.ln(5)

        for img in images:
            if os.path.exists(img["path"]):
                pdf.set_font("DejaVu", "B", 11)
                pdf.cell(0, 8, f"Cable Set {img['cable_set']} – Test Point {img['test_point']}", ln=True)
                try:
                    pdf.image(img["path"], w=100)
                    pdf.ln(10)
                except Exception as e:
                    pdf.set_font("DejaVu", "I", 8)
                    pdf.cell(0, 10, f"[Error displaying image: {e}]", ln=True)

    # ✅ Footer info
    pdf.ln(5)
    pdf.set_font("DejaVu", "I", 10)
    pdf.cell(0, 10, f"Performed by: {test_data.get('user_name', 'Unknown')}", ln=True)
    pdf.cell(0, 10, f"Date: {test_data.get('date', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))}", ln=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
