import fitz  # PyMuPDF
import csv
import sys
from pathlib import Path


def classify_pdf(pdf_path):
    """
    Classify a PDF as text-based or image-based.

    Returns:
        'text': PDF has extractable text
        'image': PDF appears to be scanned/image-based
        'mixed': PDF has both significant text and images
    """
    try:
        doc = fitz.open(pdf_path)
        total_text_chars = 0
        total_images = 0
        num_pages = len(doc)

        for page in doc:
            # Extract text
            text = page.get_text().strip()
            total_text_chars += len(text)

            # Count images
            images = page.get_images()
            total_images += len(images)

        doc.close()

        # Classification logic
        has_text = total_text_chars > 50  # More than trivial text
        has_images = total_images > 0

        if has_text and not has_images:
            return 'text'
        elif has_images and not has_text:
            return 'image'
        elif has_text and has_images:
            # If text is substantial relative to pages, likely text-based with embedded images
            avg_chars_per_page = total_text_chars / max(num_pages, 1)
            if avg_chars_per_page > 100:
                return 'text'
            return 'image'
        else:
            return 'empty'

    except Exception as e:
        return f'error: {e}'


def scan_folder(folder_path):
    """Scan all PDFs in a folder and classify them."""
    folder = Path(folder_path)
    results = []

    for pdf_file in folder.glob('*.pdf'):
        classification = classify_pdf(pdf_file)
        results.append({
            'filename': pdf_file.name,
            'filepath': str(pdf_file.absolute()),
            'classification': classification
        })

    return results


def write_csv(results, output_path):
    """Write classification results to a CSV file."""
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'filepath', 'classification'])
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python classify_pdfs.py <input_folder> <output_csv>")
        print("Example: python classify_pdfs.py ./pdfs results.csv")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_csv = sys.argv[2]

    print(f"Scanning PDFs in: {input_folder}")
    results = scan_folder(input_folder)

    # Write to CSV
    write_csv(results, output_csv)
    print(f"Results saved to: {output_csv}")

    # Print summary
    text_count = sum(1 for r in results if r['classification'] == 'text')
    image_count = sum(1 for r in results if r['classification'] == 'image')
    error_count = sum(1 for r in results if r['classification'].startswith('error'))

    print(f"\nSummary: {len(results)} total, {text_count} text, {image_count} image-based, {error_count} errors")
