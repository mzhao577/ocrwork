# OCR Work Tools

PDF classification, OCR text extraction, and text filtering tools for document processing.

## Installation

```bash
pip install -r requirements.txt
```

Also requires system dependencies:
- **Tesseract OCR**: `brew install tesseract` (macOS) or `sudo apt-get install tesseract-ocr` (Ubuntu)
- **Poppler** (for PDF to image conversion): `brew install poppler` (macOS) or `sudo apt-get install poppler-utils` (Ubuntu)

## Scripts

### ocr_parsefiles.py

Extract text from PDF files. Supports both text-based PDFs (direct extraction) and image-based/scanned PDFs (OCR).

**Usage:**
```bash
python ocr_parsefiles.py <input_folder> <output_folder> [--type {text,image}]
```

**Arguments:**
- `input_folder` - Folder containing PDF files
- `output_folder` - Folder to save extracted text
- `--type` - PDF type: `text` (default) for text-based PDFs, `image` for scanned PDFs

**Examples:**
```bash
# For text-based PDFs (fast, direct extraction)
python ocr_parsefiles.py data/textinputs data/textoutputs --type text

# For scanned/image-based PDFs (uses Tesseract OCR)
python ocr_parsefiles.py data/scannedimages data/scannedoutputs --type image
```

**Output structure:**
```
output_folder/
├── pdf_name_1/
│   ├── page_001.txt
│   ├── page_001.png    (only for --type image)
│   ├── page_002.txt
│   └── full_text.txt   (combined text from all pages)
└── pdf_name_2/
    └── ...
```

### ocr_pdf.py

Basic PDF OCR script using Tesseract. Processes all PDFs in `data/textinputs` and outputs to `data/textoutputs`.

**Usage:**
```bash
python ocr_pdf.py
```

### ocr_image.py

Extract text from image files (PNG, JPG, etc.) using Tesseract OCR.

**Usage:**
```bash
python ocr_image.py <image_path> <output_path> [-l LANG]
```

**Example:**
```bash
python ocr_image.py scan.png output.txt -l eng
```

### classify_pdfs.py

Classifies PDF files as text-based or image-based (scanned).

**Usage:**
```bash
python classify_pdfs.py <input_folder> <output_csv>
```

**Example:**
```bash
python classify_pdfs.py ./documents results.csv
```

**Output CSV columns:**
- `filename` - PDF file name
- `filepath` - Full absolute path
- `classification` - `text`, `image`, `empty`, or error message

### filter_paragraphs.py

Filters paragraphs from a text file based on configurable criteria.

**Usage:**
```bash
python filter_paragraphs.py <input_file> <output_file>
```

**Example:**
```bash
python filter_paragraphs.py input.txt filtered_output.txt
```

**Configurable parameters** (edit at top of file):
```python
MIN_WORDS = 15       # Minimum word count per paragraph
MIN_CHARS = 60       # Minimum character count per paragraph
MIN_LINE_CHARS = 50  # At least one line must have this many characters
```

**Filtering rules:**
1. Removes paragraphs with fewer than `MIN_WORDS` words OR fewer than `MIN_CHARS` characters
2. Removes paragraphs where ALL lines have fewer than `MIN_LINE_CHARS` characters

Paragraphs are detected by blank lines (double newlines).
