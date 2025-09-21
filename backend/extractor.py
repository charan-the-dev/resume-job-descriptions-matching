import io
import re
import pdfplumber
import docx2txt

def clean_text(text: str) -> str:
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    # Remove common headers/footers if present heuristically
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    return text.strip()

def extract_pdf(file_path_or_bytes) -> str:
    # file_path_or_bytes can be path or bytes
    text = []
    if isinstance(file_path_or_bytes, (bytes, bytearray)):
        with pdfplumber.open(io.BytesIO(file_path_or_bytes)) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
    else:
        with pdfplumber.open(file_path_or_bytes) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
    raw = "\n".join(text)
    return clean_text(raw)

def extract_docx(file_path_or_bytes) -> str:
    if isinstance(file_path_or_bytes, (bytes, bytearray)):
        # docx2txt requires a file path; write to temp
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_path_or_bytes)
            tmp.flush()
            raw = docx2txt.process(tmp.name) or ""
    else:
        raw = docx2txt.process(file_path_or_bytes) or ""
    return clean_text(raw)

def extract_text_from_upload(uploaded_file) -> str:
    # uploaded_file is starlette UploadFile or filepath
    name = getattr(uploaded_file, "filename", str(uploaded_file))
    if name.lower().endswith(".pdf"):
        content = uploaded_file.read() if hasattr(uploaded_file, "read") else open(uploaded_file, "rb").read()
        return extract_pdf(content)
    if name.lower().endswith(".docx"):
        content = uploaded_file.read() if hasattr(uploaded_file, "read") else open(uploaded_file, "rb").read()
        return extract_docx(content)
    else:
        # fallback: treat as text
        content = uploaded_file.read() if hasattr(uploaded_file, "read") else open(uploaded_file).read()
        return clean_text(content.decode() if isinstance(content, (bytes,bytearray)) else content)
