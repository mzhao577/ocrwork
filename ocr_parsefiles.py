#!/usr/bin/env python3
"""
Script to extract text from PDF files.

For image-based PDFs: Uses Tesseract OCR
For text-based PDFs: Uses PyPDF2 for direct text extraction

Requirements:
    pip install pytesseract pillow pdf2image pypdf2

    Also requires (for image-based PDFs):
    - Tesseract OCR: brew install tesseract (macOS)
    - Poppler (for pdf2image): brew install poppler (macOS)
"""

import argparse
import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
    from PyPDF2 import PdfReader
except ImportError as e:
    print(f"Error: Missing required package. {e}")
    print("Install with: pip install pytesseract pillow pdf2image pypdf2")
    sys.exit(1)


def extract_text_from_image_pdf(pdf_path: Path, output_dir: Path, lang: str = "eng") -> None:
    """
    Extract text from an image-based PDF file using Tesseract OCR.

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


def extract_text_from_text_pdf(pdf_path: Path, output_dir: Path) -> None:
    """
    Extract text from a text-based PDF file using PyPDF2.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save output files
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting text from PDF: {pdf_path.name}")
    reader = PdfReader(pdf_path)

    all_text = []

    for i, page in enumerate(reader.pages, start=1):
        print(f"  Processing page {i}/{len(reader.pages)}...")

        text = page.extract_text() or ""

        # Save individual page text
        text_path = output_dir / f"page_{i:03d}.txt"
        text_path.write_text(text, encoding="utf-8")

        all_text.append(f"=== Page {i} ===\n{text}")

    # Save combined text
    combined_path = output_dir / "full_text.txt"
    combined_path.write_text("\n\n".join(all_text), encoding="utf-8")
    print(f"  Saved combined text to: {combined_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files"
    )
    parser.add_argument(
        "input_folder",
        help="Path to the input folder containing PDF files"
    )
    parser.add_argument(
        "output_folder",
        help="Path to the output folder for extracted text"
    )
    parser.add_argument(
        "--type",
        choices=["text", "image"],
        default="text",
        help="PDF type: 'text' for text-based PDFs (default), 'image' for scanned/image-based PDFs"
    )

    args = parser.parse_args()

    input_dir = Path(args.input_folder)
    output_dir = Path(args.output_folder)

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s)")
    print(f"Processing as {args.type}-based PDFs\n")

    for pdf_path in pdf_files:
        # Create output subfolder for each PDF
        pdf_output_dir = output_dir / pdf_path.stem

        try:
            if args.type == "image":
                extract_text_from_image_pdf(pdf_path, pdf_output_dir)
            else:
                extract_text_from_text_pdf(pdf_path, pdf_output_dir)
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
