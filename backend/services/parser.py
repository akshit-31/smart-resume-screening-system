import fitz  # PyMuPDF

def extract_text_from_pdf(filepath: str) -> str:
    """Extract raw text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to parse PDF '{filepath}': {str(e)}")
