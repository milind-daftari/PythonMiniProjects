"""
The JSON file which will be given as input has to have a specific format.
Example:
[
    {
        "course": "Course_Number_1",
        "section": "Section",
        "instructor": "Instructor_Name",
        "formula_sheet": "Formula_Sheet_Name",
        "count": "Number_of_Copies",
        "name": "PDF_Name"
    },
    {
        "course": "Course_Number_2",
        "section": "Section",
        "instructor": "Instructor_Name",
        "formula_sheet": "Formula_Sheet_Name",
        "count": "Number_of_Copies",
        "name": "PDF_Name"
    }
]

You can add as many courses as you want.
"""
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PyPDF2 import PdfReader, PdfWriter
import tempfile

# Constants
JSON_FILE_PATH = ""
QUIZ_NUMBER = ""
DATE = ""
PDF_LOCATION_FOLDER = ""
OUTPUT_PATH = ""
temp_file = os.path.join(tempfile.gettempdir(), "title_page.pdf")


def validate_json_entry(entry):
    """
    Validates a single entry from the JSON input.

    Parameters:
        entry (dict): A dictionary representing a course entry.

    Raises:
        ValueError: If the entry is missing required keys or has values of incorrect types.
    """
    required_keys = {
        "instructor": str,
        "course": str,
        "section": str,
        "name": str,
        "formula_sheet": str
    }

    for key, expected_type in required_keys.items():
        if key not in entry:
            raise KeyError(f"Missing key '{key}' in JSON entry.")
        if not isinstance(entry[key], expected_type):
            raise TypeError(f"Key '{key}' should be of type '{expected_type}' but is '{type(entry[key])}'.")

    if "count" not in entry:
        raise KeyError("Missing key 'count' in JSON entry.")

    if not (isinstance(entry["count"], int) or (isinstance(entry["count"], str) and entry["count"].isdigit())):
        raise ValueError(f"Key 'count' should be of type 'int' or a string representing an int but is '{type(entry['count'])}'.")


def generate_title_page(entry, temp_file_path, quiz_number, date):
    """
    Generates a title page PDF for the given course entry.

    Parameters:
        entry (dict): A dictionary representing a course entry.
        temp_file_path (str): Path to save the generated title page.
        quiz_number (str): The quiz number.
        date (str): The quiz date.
    """
    doc = SimpleDocTemplate(temp_file_path, pagesize=letter)
    story = []
    title_style = getSampleStyleSheet()['Heading1']
    title_style.fontName = 'Times-Roman'
    title_style.fontSize = 26
    title_style.leading = 40
    title_style.alignment = 1  # Center aligned
    title_style.textColor = colors.black
    title_style.underline = True
    title = Paragraph("COVER SHEET FOR QUIZZES", title_style)
    table_data = [
        ["Instructor Name", ":", entry["instructor"]],
        ["Course #", ":", entry["course"]],
        ["Section (letter + #)", ":", entry["section"]],
        ["Quiz #", ":", quiz_number],
        ["Date", ":", date]
    ]
    table_style = TableStyle([
        ('FONT', (0, 0), (0, -1), 'Times-Roman', 26),
        ('FONT', (1, 0), (1, -1), 'Times-Roman', 26),
        ('FONT', (2, 0), (2, -1), 'Times-Bold', 26),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12)
    ])
    table = Table(table_data, colWidths=[270, 20, 260])
    table.setStyle(table_style)
    story.append(title)
    story.append(Spacer(1, 1 * inch))
    story.append(table)
    doc.build(story)


def add_pdf_to_output_with_check(pdf_path, output):
    """
    Adds a PDF page to the output writer after checking its existence and content.

    Parameters:
        pdf_path (str): Path of the source PDF.
        output (PdfWriter): PDF writer object to which the page should be added.

    Raises:
        FileNotFoundError: If the source PDF doesn't exist.
        ValueError: If the source PDF has no pages.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Missing PDF file: {pdf_path}")
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        if len(reader.pages) == 0:
            raise ValueError(f"PDF file {pdf_path} has no pages.")
        output.add_page(reader.pages[0])


def adjusted_merge_pdfs_with_check(json_file, quiz_number, date, pdf_location_folder, output_path):
    """
    Merges multiple PDFs based on the given JSON input.

    Parameters:
        json_file (str): Path to the JSON input file.
        quiz_number (str): The quiz number.
        date (str): The quiz date.
        pdf_location_folder (str): Folder where the source PDFs are located.
        output_path (str): Path to save the merged output PDF.

    Returns:
        str: Path to the merged output PDF.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)

    output = PdfWriter()

    for idx, entry in enumerate(data):
        try:
            print(f"Processing entry {idx + 1}: {entry}")
            validate_json_entry(entry)
            generate_title_page(entry, temp_file, quiz_number, date)
            add_pdf_to_output_with_check(temp_file, output)
            print(f"Added title page for entry {idx + 1}")
            output.add_blank_page()
            print(f"Added blank page after title for entry {idx + 1}")
            pdf_path = os.path.join(pdf_location_folder, entry["name"])
            formula_sheet_path = os.path.join(pdf_location_folder, f"{entry['formula_sheet']}.pdf")
            for _ in range(int(entry["count"])):
                add_pdf_to_output_with_check(pdf_path, output)
                print(f"Added quiz sheet for entry {idx + 1}")
                add_pdf_to_output_with_check(formula_sheet_path, output)
                print(f"Added formula sheet for entry {idx + 1}")
        except (KeyError, TypeError, ValueError, FileNotFoundError) as e:
            print(f"Error processing entry {idx + 1}: {e}")
            continue

    with open(output_path, "wb") as f:
        output.write(f)

    if os.path.exists(temp_file):
        os.remove(temp_file)

    return output_path

output_file = adjusted_merge_pdfs_with_check(JSON_FILE_PATH, QUIZ_NUMBER, DATE, PDF_LOCATION_FOLDER, OUTPUT_PATH)
print(f"Merged PDF saved at: {output_file}")
