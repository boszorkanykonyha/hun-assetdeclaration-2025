import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import re
import os

def to_camel_case(name):
    return ''.join(word.capitalize() for word in name.split())

def find_split_points_and_names(pdf_path, keyword):
    split_points = [0]
    names = ["Start"]
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and keyword in text:
                split_points.append(i)
                match = re.search(f"{keyword}: (.+)", text)
                if match:
                    name = to_camel_case(match.group(1))
                else:
                    name = "UnknownName"
                names.append(name)
    return split_points, names

def split_pdf_by_keyword(input_pdf, keyword):
    reader = PdfReader(input_pdf)
    split_points, names = find_split_points_and_names(input_pdf, keyword)
    split_points.append(len(reader.pages))

    for i in range(len(split_points) - 1):
        writer = PdfWriter()
        for j in range(split_points[i], split_points[i + 1]):
            writer.add_page(reader.pages[j])
        
        name = names[i]
        output_filename = f"{name}.pdf"
        counter = 1
        while os.path.exists(output_filename):
            output_filename = f"{name}_{counter}.pdf"
            counter += 1
        
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)
        print(f"Saved: {output_filename}")

split_pdf_by_keyword("\Step1\source.pdf", "A nyilatkozatot adó neve")