import requests
import io
import re
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from fpdf import FPDF
from textwrap import wrap

API_KEY = "b5d10d3891de0bbb191c841099881256"

# 🔍 Chargement des données SCImago depuis le CSV
def load_scimago_data(csv_path):
    scimago_info = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            title = row["Title"].strip().lower()
            scimago_info[title] = {
                "issn": row["Issn"],
                "sjr": row["SJR"],
                "quartile": row["SJR Best Quartile"],
                "h_index": row["H index"]
            }
    return scimago_info

# 📄 Classe PDF personnalisée
class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=10)
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', size=8)

    def render_table(self, data, headers, col_widths, line_height):
        self.set_fill_color(200, 220, 255)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align='C', fill=True)
        self.ln()

        for row in data:
            num_lines = [len(wrap(str(row[i]), width=int(col_widths[i] / 2.5))) for i in range(len(row))]
            row_height = max(num_lines) * line_height

            if self.get_y() + row_height > self.page_break_trigger:
                self.add_page()

            y_start = self.get_y()
            x_start = self.get_x()

            for i, item in enumerate(row):
                max_chars = int(col_widths[i] * 0.55)
                lines = wrap(str(item), width=max_chars)
                cell_x = self.get_x()
                cell_y = self.get_y()
                self.rect(cell_x, cell_y, col_widths[i], row_height)
                for j, line in enumerate(lines):
                    self.set_xy(cell_x, cell_y + j * line_height)
                    self.cell(col_widths[i], line_height, line, ln=0)
                self.set_xy(x_start + sum(col_widths[:i+1]), y_start)
            self.ln(row_height)

# 🔁 Fonction principale
def run_search(method, first_name=None, last_name=None, scopus_id=None, year=None, export_type="pdf", csv_path="scimagojr 2024.csv"):
    scimago_data = load_scimago_data(csv_path)
    headers = {
        "X-ELS-APIKey": API_KEY,
        "Accept": "application/json"
    }

    if method == "name":
        full_name = f"{last_name} {first_name}".strip()
        query = f'AUTH("{full_name}")'
        if year:
            query += f' AND PUBYEAR IS {year}'
    elif method == "id":
        full_name = f"(Scopus ID: {scopus_id})"
        query = f"AU-ID({scopus_id})"
        if year:
            query += f" AND PUBYEAR IS {year}"
        author_info_url = f"https://api.elsevier.com/content/author/author_id/{scopus_id}"
        author_response = requests.get(author_info_url, headers=headers)
        if author_response.status_code == 200:
            author_data = author_response.json()
            author_name = author_data.get("author-retrieval-response", [{}])[0].get("preferred-name", {})
            full_name = f"{author_name.get('surname', '')} {author_name.get('given-name', '')}"
    else:
        raise ValueError("Invalid search method")

    url = f"https://api.elsevier.com/content/search/scopus?query={query}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError("Scopus API request failed")

    data = response.json()
    entries = data.get("search-results", {}).get("entry", [])

    results = []
    for i, pub in enumerate(entries, start=1):
        title = pub.get("dc:title", "No title")
        journal = pub.get("prism:publicationName", "No journal")
        date = pub.get("prism:coverDate", "No date")

        journal_key = journal.strip().lower()
        journal_info = scimago_data.get(journal_key, {})

        sjr = journal_info.get("sjr", "N/A")
        h_index = journal_info.get("h_index", "N/A")
        quartile = journal_info.get("quartile", "N/A")
        issn = journal_info.get("issn", "N/A")

        results.append([i, title, journal, date, sjr, h_index, quartile, issn])

    safe_name = re.sub(r'[^\w\-_.]', '_', full_name)

    if export_type == "excel" or export_type == "both":
        wb = Workbook()
        ws = wb.active
        ws.title = "Publications"
        headers_excel = ["N°", "Titre", "Journal", "Date", "SJR", "H-index", "Quartile", "ISSN"]
        ws.append(headers_excel)
        for row in results:
            ws.append(row)
        for cell in ws["1:1"]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")
        excel_filename = f"publications_{safe_name}.xlsx"
        wb.save(excel_filename)

    if export_type == "pdf" or export_type == "both":
        pdf = PDF()
        pdf.add_page()
        pdf.render_table(results, ["N°", "Titre", "Journal", "Date", "SJR", "H-index", "Quartile", "ISSN"],
                         [10, 75, 60, 25, 15, 20, 20, 35], 5)
        pdf_filename = f"publications_{safe_name}.pdf"
        pdf.output(pdf_filename)

    return {
        "name": full_name,
        "total": len(results),
        "excel_file": excel_filename if export_type in ["excel", "both"] else None,
        "pdf_file": pdf_filename if export_type in ["pdf", "both"] else None
    }
