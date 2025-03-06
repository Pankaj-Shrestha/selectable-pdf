import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import ocrmypdf

app = FastAPI()

# Mount the static directory for assets like favicon
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the index.html form for uploading PDFs."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Receives a PDF, processes it with OCRmyPDF using Tesseract configured for German,
    and returns the OCR'd PDF file.
    """
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        content = await file.read()
        temp_input.write(content)
        temp_input.flush()
        input_pdf_path = temp_input.name

    # Define output file path (same temporary path with a suffix)
    output_pdf_path = input_pdf_path + "_ocr.pdf"

    try:
        # Run OCRmyPDF with desired options:
        # - 'language="deu"' loads the German language model (for umlauts, etc.)
        # - 'deskew=True' straightens skewed pages
        # - 'clean=True' cleans the input image to remove extraneous marks
        ocrmypdf.ocr(
            input_pdf_path,
            output_pdf_path,
            language="deu",
            deskew=True,
            clean=True
        )
    except Exception as e:
        # Ensure cleanup of the temporary input file before raising an error
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")
    finally:
        # Remove the temporary input file if it exists
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)

    # Return the OCR'd PDF as a file download
    return FileResponse(
        output_pdf_path,
        media_type="application/pdf",
        filename="ocr.pdf"
    )
