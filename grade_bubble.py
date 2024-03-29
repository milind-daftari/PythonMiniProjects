import os
import fitz
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfArray

def add_text_field(input_file, output_file, page_number, x, y, width, height, default_value="1"):
    reader = PdfReader(input_file)
    page = reader.pages[page_number]

    if '/Annots' not in page:
        page.Annots = PdfArray()

    # Create a new text field
    text_field = PdfDict(
        FT="/Tx",
        Subtype="/Widget",
        T="CustomTextField",
        Rect=PdfArray([x, y, x + width, y + height]),
        DA="/Helv 0 Tf 0 g",
        Q=1,
        F=4,
        P=reader.Info,
    )

    # Add the text field to the specified page
    page.Annots.append(text_field)

    # Save the output PDF
    writer = PdfWriter()
    writer.trailer = reader
    writer.write(output_file)

    # Open the output PDF with PyMuPDF
    doc = fitz.open(output_file)
    page = doc[page_number]

    # Add the default text on top of the field
    text_color = (0, 0, 0)  # RGB color for the text
    fontname = "helv"
    page.insert_text((x + 2, y + 2), default_value, fontname=fontname, fontsize=12, color=text_color)

    # Save the output PDF with a temporary name
    temp_output_file = output_file[:-4] + "_temp.pdf"
    doc.save(temp_output_file)
    doc.close()

    # Replace the original output file with the temporary one
    os.remove(output_file)
    os.rename(temp_output_file, output_file)

def create_copies(input_file, output_folder, start, end, page_number, x, y, width, height):
    for i in range(start, end+1):
        output_file = os.path.join(output_folder, f'gradescope_bubble_out_{i}.pdf')
        add_text_field(input_file, output_file, page_number, x, y, width, height, str(i))

def merge_pdfs(pdfs, output_filename):
    merger = fitz.open()  # create a new empty PDF
    for pdf in pdfs:
        with fitz.open(pdf) as mfile:
            merger.insert_pdf(mfile)  # append the current PDF to the merger
    merger.save(output_filename)  # save the merged PDFs
    merger.close()

# Example usage
input_file = r'INPUT_DIRECTORY\gradescope_bubble.pdf'
output_folder = r'OUTPUT_DIRECTORY'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start = 1  # Starting number
end = 190  # Ending number
page_number = 0  # First page
x, y, width, height = 375, 108, 150, 25  # Position and size of the text field

create_copies(input_file, output_folder, start, end, page_number, x, y, width, height)

# Merge all generated PDFs
pdf_files = [os.path.join(output_folder, f'gradescope_bubble_out_{i}.pdf') for i in range(start, end+1)]
merged_output_file = os.path.join(output_folder, 'merged_gradescope_bubble.pdf')
merge_pdfs(pdf_files, merged_output_file)
