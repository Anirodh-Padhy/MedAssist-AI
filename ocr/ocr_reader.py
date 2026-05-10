import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

# ================= TESSERACT PATH =================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

# ================= IMAGE OCR =================

def extract_text_from_image(image):

    text = pytesseract.image_to_string(image)

    return text

# ================= PDF OCR =================

def extract_text_from_scanned_pdf(pdf_file):

    images = convert_from_bytes(
        pdf_file.read()
    )

    full_text = ""

    for image in images:

        text = pytesseract.image_to_string(
            image
        )

        full_text += text + "\n"

    return full_text