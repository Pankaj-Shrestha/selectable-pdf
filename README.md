# Selectable PDF: OCR-Powered Text Layer for Scanned PDFs

> 🧠 A simple yet powerful Flask-based web app to convert scanned or image-based PDFs into fully selectable and searchable documents using Tesseract OCR.

---

## 📌 Description

Scanned PDF documents — like the ones professors upload as handwritten lecture slides — often lack a selectable text layer, making it difficult to search or copy important content. This project was built during my free time as a **Bachelor’s student** to **practice what I was learning** and also to solve a real need: making lecture PDFs actually usable.

It’s a fun and useful side project that reflects how I apply what I learn, take initiative, and build solutions for my own academic workflow — while sharpening my Python and web dev skills.

### 🔧 What it does

- Accepts scanned/image PDFs via upload.
- Uses **Tesseract OCR** to extract text.
- Overlays invisible text on the original pages.
- Outputs a downloadable, **searchable PDF**.

### 🔧 Technologies Used

- **Python 3.8+**
- **Flask** for the web app
- **Tesseract OCR** for optical character recognition
- **PDF2Image**, **PyMuPDF (fitz)** for PDF/image handling
- **Docker** for easy deployment

---

## ⚙️ Installation

Make sure you have **Python 3.7+**, **Tesseract OCR**, and **Poppler** installed.

```bash
# 1. Clone the repo
git clone https://github.com/Pankaj-Shrestha/selectable-pdf.git
cd selectable-pdf

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install system tools (if not already installed)
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt install tesseract-ocr poppler-utils
```

---

## 🚀 Usage

```bash
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

Then open your browser at [http://localhost:5000](http://localhost:5000).

### Example Flow:

1. Upload a scanned/handwritten PDF.
2. The app processes each page with OCR.
3. A new PDF is created with selectable/searchable text.
4. You download the result.

---

## 📊 Data Sources

No external dataset is used. All input PDFs are uploaded by users. OCR is performed using:

- **Tesseract OCR**: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

---

## 📬 Contact

- GitHub: [@Pankaj-Shrestha](https://github.com/Pankaj-Shrestha)
- Email: pankaj.shrestha@smail.th-koeln.de

---

## 🙏 Acknowledgments

- Tesseract and the open-source community
- Professors who upload handwritten slides 😅
- My curiosity and the need to make study life easier

---

> *Built with Flask, focus, and the frustration of unsearchable PDFs.*
