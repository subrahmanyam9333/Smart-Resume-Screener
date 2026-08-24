from fastapi import FastAPI, UploadFile, File
import tempfile
import os

from backend.parser import extract_text_from_pdf


app = FastAPI(
    title="Smart Resume Screener",
    description="AI-powered resume screening and job matching system",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Smart Resume Screener API is running"
    }


@app.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported currently."
        }

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        text = extract_text_from_pdf(temp_path)

        return {
            "filename": file.filename,
            "text": text
        }

    finally:

        os.remove(temp_path)