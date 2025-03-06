import io
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pdfplumber

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Render the form with no extracted text initially
    return templates.TemplateResponse("index.html", {"request": request, "extracted_text": None})

@app.post("/", response_class=HTMLResponse)
async def extract_text(request: Request, file: UploadFile = File(...)):
    file_contents = await file.read()
    extracted_text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_contents)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
    except Exception as e:
        extracted_text = f"An error occurred: {str(e)}"
    
    # Render the same page with the extracted text
    return templates.TemplateResponse("index.html", {"request": request, "extracted_text": extracted_text})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
