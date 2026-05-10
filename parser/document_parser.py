import pdfplumber

from PIL import Image

from ocr.ocr_reader import (
    extract_text_from_scanned_pdf,
    extract_text_from_image
)

# ================= TEXT EXTRACTION =================

def extract_text(file):

    filename = file.name.lower()

    # ================= PDF =================
    if filename.endswith(".pdf"):

        text = ""

        try:

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    content = page.extract_text()

                    if content:
                        text += content + "\n"

        except:
            pass

        # ================= OCR FALLBACK =================
        if len(text.strip()) < 20:

            file.seek(0)

            text = extract_text_from_scanned_pdf(
                file
            )

        return text

    # ================= IMAGE OCR =================
    elif (
        filename.endswith(".png")
        or filename.endswith(".jpg")
        or filename.endswith(".jpeg")
    ):

        image = Image.open(file)

        text = extract_text_from_image(image)

        return text

    # ================= TXT =================
    else:

        return file.read().decode("utf-8")