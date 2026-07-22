import os
import cv2
import pytesseract
import pdfplumber

from pdf2image import convert_from_path
from PIL import Image


def preprocess_image(image_path):
    """
    Read image and improve it for OCR.
    """

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.medianBlur(gray, 3)

    # Threshold
    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return gray


def extract_text_from_image(image_path):
    """
    OCR for JPG / PNG
    """

    processed_image = preprocess_image(image_path)

    text = pytesseract.image_to_string(
        processed_image,
        lang="eng"
    )

    return text


def extract_text_from_pdf(pdf_path):
    """
    OCR for PDF
    """

    text = ""

    # Try extracting text directly
    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        if len(text.strip()) > 20:
            return text

    except Exception:
        pass

    # OCR scanned PDF
    pages = convert_from_path(pdf_path)

    for page in pages:

        image = page.convert("RGB")

        text += pytesseract.image_to_string(image)

    return text


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".jpg", ".jpeg", ".png"]:

        return extract_text_from_image(file_path)

    elif extension == ".pdf":

        return extract_text_from_pdf(file_path)

    else:

        raise ValueError("Unsupported file format")
