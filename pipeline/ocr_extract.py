import os, sys
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Point to Tesseract install
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    print("WARNING: Tesseract not found at default path, hoping it's in PATH")

pdf_dir = r"E:\downloads\uap_pdfs"
output_dir = r"E:\downloads\uap_pdfs"

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')])
print(f"Found {len(pdfs)} PDFs total")

# Find which ones are scanned (no text layer)
scanned = []
has_text = []
for f in pdfs:
    path = os.path.join(pdf_dir, f)
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if len(text.strip()) > 50:
            has_text.append(f)
        else:
            scanned.append(f)
    except:
        scanned.append(f)

print(f"{len(has_text)} already have text, {len(scanned)} need OCR")
print(f"Starting OCR on {len(scanned)} scanned PDFs...\n")

ocr_results = []
total_pages = 0

for i, filename in enumerate(scanned, 1):
    filepath = os.path.join(pdf_dir, filename)
    print(f"[{i}/{len(scanned)}] {filename}", end="", flush=True)
    
    file_text = ""
    try:
        doc = fitz.open(filepath)
        page_count = len(doc)
        print(f" ({page_count} pages)", end="", flush=True)
        
        for pi, page in enumerate(doc):
            # Rasterize at 200 DPI
            mat = fitz.Matrix(200/72, 200/72)
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            
            # OCR
            page_text = pytesseract.image_to_string(img)
            if page_text.strip():
                file_text += page_text + "\n"
            
            total_pages += 1
        
        doc.close()
        print(f" -> {len(file_text)} chars")
    except Exception as e:
        print(f" ERROR: {e}")
        file_text = f"*[OCR error: {e}]*"
    
    ocr_results.append((filename, file_text))

# Write OCR results
out_path = os.path.join(output_dir, "UAP_OCR_SCANNED.md")
with open(out_path, 'w', encoding='utf-8') as out:
    out.write("# PURSUE Release 01 - OCR Extracted (Scanned Documents)\n\n")
    out.write(f"OCR processed {len(scanned)} scanned PDFs, {total_pages} total pages\n\n---\n\n")
    
    for filename, text in ocr_results:
        out.write(f"## {filename}\n\n")
        if text.strip():
            out.write(text.strip() + "\n\n")
        else:
            out.write("*[OCR returned no readable text]*\n\n")
        out.write("---\n\n")

size_mb = os.path.getsize(out_path) / (1024*1024)
print(f"\nDone! {size_mb:.1f} MB written to {out_path}")
print(f"Total pages OCR'd: {total_pages}")
