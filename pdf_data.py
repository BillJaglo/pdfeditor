from pathlib import Path
from pdfminer import high_level
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import re
import user_inputs


def get_usd_value(file):
    # location of files
    local_pdf_filename = f"{user_inputs.input_file_path}{file}"
    # this works for one page pdfs
    pages = [0]  # just the first page

    # this takes all the text on the pdf and stores it in a string variable
    extracted_text = high_level.extract_text(local_pdf_filename, "", pages)

    # this finds the first $ in the PDF and gives that index (int) position within the string
    dollar_sign_index = extracted_text.index('$')

    # there is a space after the $ sign on the invoice, this is for the for loop to start after that space
    usd_start = dollar_sign_index + 1
    # 20 is an arbitrary number, just want to include all possible digits if the number has many digits
    usd_end = dollar_sign_index + 20

    # this is used for the for loop and if statement to check to see if it is a valid character
    accepted_characters = [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        ',',
        '.'
    ]

    # created a variable to store the USD value
    usd_value = ''

    # runs through all of the numbers after the first $ is found. Adds the character to the usd_value variable if in the accepted character list
    for num_index in range(usd_start, usd_end):
        if extracted_text[num_index] in accepted_characters:
            usd_value = usd_value + extracted_text[num_index]
        else:
            pass
    return usd_value


def get_customer_name(file):
    # location of files
    local_pdf_filename = f"{user_inputs.input_file_path}{file}"
    # this works for one page pdfs
    pages = [0]  # just the first page

    # this takes all the text on the pdf and stores it in a string variable
    extracted_text = high_level.extract_text(local_pdf_filename, "", pages)

    # finds all text  that is enclosed by a (), then returns the second case and strips the () out, saves as variable
    customer_name = re.findall(r'\(.*?\)', extracted_text)[1].strip('()')
    return customer_name


def get_invoice_number(file):
    # location of files
    local_pdf_filename = f"{user_inputs.input_file_path}{file}"
    file_name = Path(local_pdf_filename).stem
    invoice_number = file_name.split(" ")[0]
    return invoice_number


def write_to_pdf(file_path, coding_text_1, *args):
    local_pdf_filename = f"{user_inputs.input_file_path}{file_path}"
    file_name = Path(local_pdf_filename).stem
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    try:
        can.drawString(10, 140, coding_text_1)
        can.drawString(10, 127, *args)
        can.save()
    except:
        can.drawString(10, 140, coding_text_1)
        can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(local_pdf_filename, "rb"))
    output = PdfFileWriter()
    # add the text (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(f"{user_inputs.output_file_path}{file_name}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
