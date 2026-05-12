import os
from pypdf import PdfReader
import fitz

pdf_dir = r"E:\downloads\uap_pdfs"
output = r"E:\downloads\uap_pdfs\ALL_UAP_FILES.md"

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')])
print(f"Found {len(pdfs)} PDFs")

with open(output, 'w', encoding='utf-8') as out:
    out.write("# PURSUE Release 01 - Full Text Archive\n\n")
    out.write(f"Extracted from {len(pdfs)} PDFs\n\n---\n\n")
    
    for i, filename in enumerate(pdfs, 1):
        filepath = os.path.join(pdf_dir, filename)
        print(f"[{i}/{len(pdfs)}] {filename}")
        
        out.write(f"## {filename}\n\n")
        
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            
            if len(text.strip()) > 50:
                out.write(text.strip() + "\n\n")
            else:
                doc = fitz.open(filepath)
                mutext = ""
                for page in doc:
                    t = page.get_text()
                    if t:
                        mutext += t + "\n"
                doc.close()
                
                if len(mutext.strip()) > 50:
                    out.write(mutext.strip() + "\n\n")
                else:
                    out.write("*[Scanned document - no extractable text layer]*\n\n")
        except Exception as e:
            out.write(f"*[Error reading file: {e}]*\n\n")
        
        out.write("---\n\n")

size_mb = os.path.getsize(output) / (1024*1024)
print(f"\nDone! {size_mb:.1f} MB written to {output}")
