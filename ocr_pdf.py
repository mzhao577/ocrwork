#!/usr/bin/env python3
"""
OCR script to extract text from PDF files using pytesseract.

Requirements:
    pip install pytesseract pillow pdf2image

    Also requires:
    - Tesseract OCR: brew install tesseract (macOS)
    - Poppler (for pdf2image): brew install poppler (macOS)
"""

import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
except ImportError as e:
    print(f"Error: Missing required package. {e}")
    print("Install with: pip install pytesseract pillow pdf2image")
    sys.exit(1)


def extract_text_from_pdf(pdf_path: Path, output_dir: Path, lang: str = "eng") -> None:
    """
    Extract text from a PDF file using Tesseract OCR.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save output files
        lang: Language code for OCR (default: 'eng')
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF to images: {pdf_path.name}")
    pages = convert_from_path(pdf_path)

    all_text = []

    for i, page in enumerate(pages, start=1):
        print(f"  Processing page {i}/{len(pages)}...")

        # Save the page image
        image_path = output_dir / f"page_{i:03d}.png"
        page.save(image_path, "PNG")

        # Extract text from the page
        text = pytesseract.image_to_string(page, lang=lang)

        # Save individual page text
        text_path = output_dir / f"page_{i:03d}.txt"
        text_path.write_text(text, encoding="utf-8")

        all_text.append(f"=== Page {i} ===\n{text}")

    # Save combined text
    combined_path = output_dir / "full_text.txt"
    combined_path.write_text("\n\n".join(all_text), encoding="utf-8")
    print(f"  Saved combined text to: {combined_path}")


def main():
    input_dir = Path("data/textinputs")
    output_dir = Path("data/textoutputs")

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s)")

    for pdf_path in pdf_files:
        # Create output subfolder for each PDF
        pdf_output_dir = output_dir / pdf_path.stem

        try:
            extract_text_from_pdf(pdf_path, pdf_output_dir)
            print(f"Completed: {pdf_path.name} -> {pdf_output_dir}\n")
        except pytesseract.TesseractNotFoundError:
            print("Error: Tesseract is not installed or not in PATH.")
            print("Install: brew install tesseract")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")
            continue

    print("Done!")


if __name__ == "__main__":
    main()
