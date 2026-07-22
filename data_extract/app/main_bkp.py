from fastapi import FastAPI, UploadFile
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")

async def upload_invoice(file: UploadFile):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Invoice uploaded successfully",
        "filename": file.filename
    }
