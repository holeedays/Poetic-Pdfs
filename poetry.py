import os
from fpdf2 import FPDF

filename = "my_data.txt"

# check if the file actually exists
if os.path.exists(filename):
    # if the file exists this is how we open it (read only)
    with open(filename, "r", encoding="utf-8") as file:
        raw_text = file.read() # the info is placed into raw text
else:
    # if there is no file, we use a default poem
    raw_text = """roses are red,\n
    violets are blue,\n
    there is no file,\n
    here is a poem for you"""

# function for making a pdf
def make_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    # this is your chance to choose a better font if you want!
    pdf.set_font("Courier", size=12)
    pdf.multi_cell(0, 10, txt=raw_text)
    pdf.output("poem.pdf")

print(raw_text)