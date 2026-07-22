from fastapi import FastAPI, UploadFile
import shutil
import os

from ocr import extract_text
from parser import parse_invoice

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload(file: UploadFile):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # OCR
    text = extract_text(file_path)

    with open("output/ocr_output.txt", "w") as f:
         f.write(text)

    # Parse invoice
    invoice = parse_invoice(text)

    return invoice
