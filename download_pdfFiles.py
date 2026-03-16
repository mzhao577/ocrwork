#!/usr/bin/env python3
"""
Script to download sample PDF files for testing.
Downloads both scanned image-based PDFs and text-based PDFs,
including medical notes samples.
"""

import os
import requests
from pathlib import Path


def download_file(url: str, filename: str, output_dir: Path) -> bool:
    """
    Download a file from URL and save it to the output directory.

    Args:
        url: The URL to download from
        filename: The name to save the file as
        output_dir: The directory to save the file in

    Returns:
        True if successful, False otherwise
    """
    filepath = output_dir / filename
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=60, allow_redirects=True, headers=headers)
        response.raise_for_status()

        # Verify it's actually a PDF
        if not response.content[:4] == b'%PDF':
            print(f"  Warning: {filename} may not be a valid PDF")

        with open(filepath, 'wb') as f:
            f.write(response.content)

        size_kb = len(response.content) / 1024
        print(f"  Saved: {filepath} ({size_kb:.1f} KB)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"  Error downloading {filename}: {e}")
        return False


def main():
    # Create output directory (data subfolder)
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define PDF files to download
    pdf_files = {
        # Scanned/Image-based PDFs
        "scanned_sample1.pdf": "http://solutions.weblite.ca/pdfocrx/scansmpl.pdf",
        "scanned_sample2.pdf": "https://www.csun.edu/sites/default/files/pdf_scanned_ocr.pdf",

        # Text-based PDFs
        "text_sample1.pdf": "https://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf",
        "text_sample2.pdf": "https://pdfobject.com/pdf/sample.pdf",

        # Medical Notes PDFs
        "medical_soap_template.pdf": "https://hsc.unm.edu/medicine/departments/family-community/_media/docs/patemplateclinsoapnote.pdf",
        "medical_record_chapter.pdf": "https://samples.jbpub.com/9781449652722/9781449645106_ch02_037_064.pdf",
        "medical_progress_notes_samples.pdf": "https://www.schulich.uwo.ca/cquins/docs/Sample-Progress-Notes-and-DC-Note-Brochure-1.pdf",
        "medical_progress_note_example.pdf": "https://www.optumsandiego.com/content/dam/san-diego/documents/ffsproviders/templates/outpatient-services-examples/Progress%20Note%20Example.pdf",
        "medical_cms_progress_note.pdf": "https://www.cms.gov/files/document/home-health-progress-note-template-cms-10564-finalpdf",
    }

    print(f"Downloading {len(pdf_files)} PDF files to: {output_dir}\n")

    # Download each file
    success_count = 0
    for filename, url in pdf_files.items():
        if download_file(url, filename, output_dir):
            success_count += 1

    print(f"\nCompleted: {success_count}/{len(pdf_files)} files downloaded successfully")


if __name__ == "__main__":
    main()
