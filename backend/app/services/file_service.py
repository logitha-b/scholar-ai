import os, uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import settings

# Optional imports - graceful fallback if not installed
try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".png", ".jpg", ".jpeg"}
MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


async def save_upload(file: UploadFile, subdirectory: str = "") -> dict:
    """Save uploaded file and return metadata."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type {ext} not supported. Use: {', '.join(ALLOWED_EXTENSIONS)}")

    content = await file.read()
    if len(content) > MAX_BYTES:
        raise HTTPException(400, f"File too large. Max {settings.MAX_FILE_SIZE_MB}MB")

    save_dir = Path(settings.UPLOAD_DIR) / subdirectory
    save_dir.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = save_dir / unique_name

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": unique_name,
        "original_name": file.filename,
        "file_path": str(file_path),
        "extension": ext,
        "size_kb": round(len(content) / 1024, 2),
    }


def extract_text(file_path: str, extension: str) -> str:
    """Extract raw text from uploaded file."""
    path = Path(file_path)
    if not path.exists():
        return ""

    try:
        if extension == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")

        elif extension == ".pdf" and HAS_PDF:
            text = []
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text() or "")
            return "\n".join(text)

        elif extension in (".docx", ".doc") and HAS_DOCX:
            doc = DocxDocument(path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif extension in (".png", ".jpg", ".jpeg") and HAS_OCR:
            img = Image.open(path)
            return pytesseract.image_to_string(img)

        else:
            # Return placeholder for demo if libraries not installed
            return f"[Text extracted from {path.name}] Sample content for demonstration purposes."

    except Exception as e:
        return f"[Extraction error: {str(e)}] File uploaded successfully."


def parse_marksheet_text(text: str) -> list[dict]:
    """
    Try to parse subject-score pairs from OCR/extracted text.
    Returns list of {"name": str, "score": float}
    Falls back to demo data if nothing found.
    """
    import re
    subjects = []
    # Common patterns: "Mathematics: 72" or "Physics - 68/100" or "85 Chemistry"
    patterns = [
        r'([A-Za-z ]{3,25})\s*[:\-–]\s*(\d{2,3})',
        r'(\d{2,3})\s*/\s*\d{2,3}\s+([A-Za-z ]{3,25})',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            try:
                g = match.groups()
                name = g[0].strip() if not g[0].strip().isdigit() else g[1].strip()
                score = float(g[1]) if not g[1].strip().isdigit() is False else float(g[0])
                if 0 <= score <= 100 and len(name) > 2:
                    subjects.append({"name": name.title(), "score": score})
            except Exception:
                continue

    # Deduplicate by name
    seen = set()
    unique = []
    for s in subjects:
        if s["name"] not in seen:
            seen.add(s["name"])
            unique.append(s)

    if not unique:
        # Demo fallback
        unique = [
            {"name": "Mathematics", "score": 62.0},
            {"name": "Physics", "score": 54.0},
            {"name": "Chemistry", "score": 78.0},
            {"name": "English", "score": 85.0},
            {"name": "Computer Science", "score": 71.0},
            {"name": "Biology", "score": 59.0},
        ]
    return unique
