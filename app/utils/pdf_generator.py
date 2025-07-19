from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'client_logo') and self.client_logo and os.path.exists(self.client_logo):
            self.image(self.client_logo, 10, 8, 33)
        if hasattr(self, 'subcontractor_logo') and self.subcontractor_logo and os.path.exists(self.subcontractor_logo):
            self.image(self.subcontractor_logo, 165, 8, 33)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Technical Test Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_test_pdf(test_data, pdf_results, output_path):
    pdf = PDF()
    pdf.client_logo = f"static/img/logos/{test_data.get('client_logo', '')}"
    pdf.subcontractor_logo = f"static/img/logos/{test_data.get('subcontractor_logo', '')}"
    pdf.add_page()

    # ✅ Title
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(
        0,
        10,
        f"{test_data['equipment_details'].get('Equipment Type', '')} - {test_data.get('test_type', '').capitalize()}",
        ln=True,
        align='C'
    )
    pdf.ln(10)

    # ✅ Equipment details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Equipment Details:', ln=True)
    pdf.set_font('Arial', '', 11)
    for key, value in test_data['equipment_details'].items():
        pdf.cell(60, 8, f"{key}", border=1)
        pdf.cell(0, 8, f"{value}", border=1, ln=True)
    pdf.ln(10)

    # ✅ Test results
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Results:', ln=True)
    pdf.set_font('Arial', 'B', 10)

    headers = ['Cable Set', 'Test Point', 'Result', 'Unit', 'Observations']
    col_widths = [25, 40, 30, 25, 70]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align='C')
    pdf.ln()

    pdf.set_font('Arial', '', 10)
    for r in pdf_results:
        row = [
            str(r.get('cable_set', '')),
            r.get('test_point', ''),
            str(r.get('result_value', '')),
            r.get('unit', ''),
            r.get('observation', '')
        ]
        for i, value in enumerate(row):
            pdf.cell(col_widths[i], 8, value, border=1)
        pdf.ln()

        # ✅ Associated images
        images = test_data.get("images", [])
        for img in images:
            if (
                img.get("cable_set") == r.get("cable_set")
                and img.get("test_point") == r.get("test_point")
            ):
                if os.path.exists(img["path"]):
                    try:
                        pdf.image(img["path"], x=pdf.get_x(), y=pdf.get_y(), w=50)
                        pdf.ln(30)
                    except Exception as e:
                        pdf.set_font('Arial', 'I', 8)
                        pdf.cell(0, 10, f"[Error displaying image: {e}]", ln=True)

    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Performed by: {test_data.get('user_name', 'Unknown')}", ln=True)
    pdf.cell(0, 10, f"Date: {test_data.get('date', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))}", ln=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
