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
    """Accepts a PDF file, processes it with OCR (German language), and returns the new PDF."""
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
        # Note: The "clean" option is omitted to avoid dependency on unpaper.
        ocrmypdf.ocr(
            input_pdf_path,
            output_pdf_path,
            language="deu",  # Use German language to correctly recognize umlauts.
            deskew=True      # Deskew pages before OCR.
        )
    except Exception as e:
        # If an error occurs, remove the temporary file and return an HTTP error.
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")
    finally:
        # Ensure the temporary input file is removed.
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)

    # Return the processed PDF to the client.
    return FileResponse(
        output_pdf_path,
        media_type="application/pdf",
        filename="ocr.pdf"
    )
