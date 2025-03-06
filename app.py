import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import ocrmypdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    # Render the HTML form for file upload.
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=FileResponse)
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded PDF temporarily.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_pdf:
        content = await file.read()
        input_pdf.write(content)
        input_pdf.flush()
        input_pdf_path = input_pdf.name

    # Define the output file path.
    output_pdf_path = input_pdf_path + "_ocr.pdf"
    
    try:
        # Process the PDF with OCR; this will add a hidden text layer.
        ocrmypdf.ocr(input_pdf_path, output_pdf_path, deskew=True)
    except Exception as e:
        # In a real app, you might want to return an error page or JSON.
        return {"error": str(e)}
    finally:
        # Clean up the input temporary file.
        os.remove(input_pdf_path)

    # Return the new PDF to the client.
    return FileResponse(
        output_pdf_path, 
        media_type="application/pdf", 
        filename="ocr.pdf"
    )
