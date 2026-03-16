#!/bin/bash

# Script to filter and copy PDF files from input folder to output folder
# Usage: ./filter_pdfs.sh <input_folder> <output_folder>
# Criteria:
#   1) Exclude PDF files with "Professional" in the filename
#   2) Include only PDF files whose filename has exactly 41 characters
#   3) Include only files ending with ".pdf"

# Check if both arguments are provided
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <input_folder> <output_folder>"
    echo "Example: $0 ./rawdata ./cleandata"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# Check if input directory exists
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Find all subfolders in rawdata
for subfolder in "$INPUT_DIR"/*/; do
    # Get subfolder name
    subfolder_name=$(basename "$subfolder")

    # Create corresponding subfolder in cleandata
    mkdir -p "$OUTPUT_DIR/$subfolder_name"

    # Process each file in the subfolder
    for file in "$subfolder"*; do
        # Skip if not a file
        [ -f "$file" ] || continue

        filename=$(basename "$file")

        # Check if file ends with .pdf (case sensitive)
        if [[ "$filename" != *.pdf ]]; then
            echo "SKIP (not .pdf): $filename"
            continue
        fi

        # Check if filename contains "Professional"
        if [[ "$filename" == *Professional* ]]; then
            echo "SKIP (contains Professional): $filename"
            continue
        fi

        # Check if filename has exactly 41 characters
        len=${#filename}
        if [[ $len -ne 41 ]]; then
            echo "SKIP (length $len, not 41): $filename"
            continue
        fi

        # File passes all criteria - copy it
        echo "COPY: $filename -> $OUTPUT_DIR/$subfolder_name/"
        cp "$file" "$OUTPUT_DIR/$subfolder_name/"
    done
done

echo ""
echo "Done! Filtered PDFs copied to $OUTPUT_DIR"
