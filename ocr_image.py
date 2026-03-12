#!/usr/bin/env python3
"""
OCR script to extract text from PNG images using pytesseract.

Requirements:
    pip install pytesseract pillow

    Also requires Tesseract OCR to be installed:
    - macOS: brew install tesseract
    - Ubuntu: sudo apt-get install tesseract-ocr
    - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
"""

import argparse
import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing required package. {e}")
    print("Install with: pip install pytesseract pillow")
    sys.exit(1)


def extract_text_from_image(image_path: str, lang: str = "eng") -> str:
    """
    Extract text from an image file using Tesseract OCR.

    Args:
        image_path: Path to the image file (PNG, JPG, etc.)
        lang: Language code for OCR (default: 'eng')
              Use 'eng+chi_sim' for English + Simplified Chinese, etc.

    Returns:
        Extracted text as a string.
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PNG/image files using Tesseract OCR"
    )
    parser.add_argument(
        "image_path",
        help="Path to the input image file (PNG, JPG, etc.)"
    )
    parser.add_argument(
        "output_path",
        help="Path to the output text file"
    )
    parser.add_argument(
        "-l", "--lang",
        default="eng",
        help="Language code for OCR (default: eng). Examples: 'eng', 'chi_sim', 'jpn', 'eng+chi_sim'"
    )

    args = parser.parse_args()

    image_path = Path(args.image_path)
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    try:
        text = extract_text_from_image(str(image_path), lang=args.lang)

        Path(args.output_path).write_text(text, encoding="utf-8")
        print(f"Text saved to: {args.output_path}")

    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in PATH.")
        print("Install Tesseract OCR:")
        print("  macOS: brew install tesseract")
        print("  Ubuntu: sudo apt-get install tesseract-ocr")
        sys.exit(1)


if __name__ == "__main__":
    main()
