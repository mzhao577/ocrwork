# OCR Work Tools

PDF classification and text filtering tools for document processing.

## Scripts

### classify_pdfs.py

Classifies PDF files as text-based or image-based (scanned).

**Usage:**
```bash
pip install pymupdf
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
