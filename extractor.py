cat > extractor.py << 'EOF'
import pdfplumber
import pypdf

def extract_pdf(file_path: str) -> dict:
    meta = {}
    try:
        reader = pypdf.PdfReader(file_path)
        m = reader.metadata
        meta = {
            "title": m.title or "",
            "author": m.author or "",
        }
    except:
        pass

    pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pages.append({
                "text": page.extract_text() or "",
                "tables": page.extract_tables() or []
            })

    full_text = "\n".join(p["text"] for p in pages)
    return {"meta": meta, "pages": pages, "full_text": full_text}
EOF