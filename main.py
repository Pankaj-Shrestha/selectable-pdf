import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import ocrmypdf

app = FastAPI()

# Mount static files (for favicon, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    """Render the upload form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=FileResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Accepts a PDF, processes it with OCR (German language), and returns the new PDF."""
    # Save the uploaded PDF to a temporary file.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_pdf:
        content = await file.read()
        input_pdf.write(content)
        input_pdf.flush()
        input_pdf_path = input_pdf.name

    # Define the output file path.
    output_pdf_path = input_pdf_path + "_ocr.pdf"

    try:
        # Run OCR on the PDF.
        # Added force_ocr=True to override the "Tagged PDF" check.
        ocrmypdf.ocr(
            input_pdf_path,
            output_pdf_path,
            language="deu",  # Use German language model
            deskew=True,     # Deskew pages before OCR
            force_ocr=True   # Force OCR even if the PDF is tagged
        )
    except Exception as e:
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")
    finally:
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)

    # Return the processed PDF as a file download.
    return FileResponse(
        output_pdf_path,
        media_type="application/pdf",
        filename="ocr.pdf"
    )
