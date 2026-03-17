#!/bin/bash

# postprocess.sh
# Applies postprocessing.py to all full_text.txt files in the input folder structure
# Also removes special characters, keeping only letters, numbers, and common punctuation
# Usage: ./postprocess.sh <input_folder> <output_folder>

# Function to clean special characters from a file
# Keeps: letters (a-z, A-Z), numbers (0-9), whitespace, and punctuation: . , ! ? ; : ' " - ( ) /
clean_special_chars() {
    local file="$1"
    local temp_file="${file}.tmp"

    # Remove all characters except: letters, numbers, spaces, newlines, tabs, and . , ! ? ; : ' " - ( ) /
    # Note: hyphen must be at end of character class for BSD sed (macOS)
    sed 's/[^a-zA-Z0-9[:space:].,!?;:'"'"'"()/-]//g' "$file" > "$temp_file"
    mv "$temp_file" "$file"

    # Ensure file ends with a newline (removes zsh % indicator)
    [ -n "$(tail -c 1 "$file")" ] && echo "" >> "$file"
}

# Check arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_folder> <output_folder>"
    echo "Example: $0 ./rawdata ./cleandata"
    exit 1
fi

INPUT_FOLDER="$1"
OUTPUT_FOLDER="$2"

# Check if input folder exists
if [ ! -d "$INPUT_FOLDER" ]; then
    echo "Error: Input folder '$INPUT_FOLDER' does not exist."
    exit 1
fi

# Get the directory where this script is located (for finding postprocessing.py)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
POSTPROCESS_PY="$SCRIPT_DIR/postprocessing.py"

# Check if postprocessing.py exists
if [ ! -f "$POSTPROCESS_PY" ]; then
    echo "Error: postprocessing.py not found at '$POSTPROCESS_PY'"
    exit 1
fi

# Create output folder if it doesn't exist
mkdir -p "$OUTPUT_FOLDER"

# Counters
processed=0
skipped=0

# Find all full_text.txt files in policyid/noteid structure
find "$INPUT_FOLDER" -type f -name "full_text.txt" | while read -r input_file; do
    # Get the relative path from input folder
    relative_path="${input_file#$INPUT_FOLDER/}"

    # Get the directory structure (policyid/noteid)
    relative_dir="$(dirname "$relative_path")"

    # Create output directory structure
    output_dir="$OUTPUT_FOLDER/$relative_dir"
    mkdir -p "$output_dir"

    # Define output file path
    output_file="$output_dir/full_text_processed.txt"

    echo "Processing: $input_file"
    echo "  -> Output: $output_file"

    # Run postprocessing.py
    python3 "$POSTPROCESS_PY" "$input_file" "$output_file"

    if [ $? -eq 0 ]; then
        # Clean special characters from the output file
        clean_special_chars "$output_file"
        echo "  Cleaned special characters"
        ((processed++))
    else
        echo "  Warning: Failed to process $input_file"
        ((skipped++))
    fi

    echo ""
done

echo "=========================================="
echo "Postprocessing complete!"
echo "Input folder:  $INPUT_FOLDER"
echo "Output folder: $OUTPUT_FOLDER"
echo "=========================================="
