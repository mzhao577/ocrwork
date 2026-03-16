import sys

# =============================================================================
# CONFIGURABLE PARAMETERS - Adjust these as needed
# =============================================================================

# Minimum word count for a paragraph
MIN_WORDS = 15

# Minimum character count for a paragraph
MIN_CHARS = 60

# Minimum character count that at least one line must have
MIN_LINE_CHARS = 50

# =============================================================================


def count_words(text):
    """Count the number of words in text."""
    return len(text.split())


def should_keep_paragraph(paragraph):
    """
    Determine if a paragraph should be kept based on the filtering rules.

    Returns False (remove) if:
    1. Paragraph has fewer than MIN_WORDS words OR fewer than MIN_CHARS characters
    2. ALL lines in the paragraph have fewer than MIN_LINE_CHARS characters
    """
    lines = paragraph.strip().split('\n')

    # Rule 1: Remove if fewer than MIN_WORDS words OR fewer than MIN_CHARS characters
    word_count = count_words(paragraph)
    char_count = len(paragraph.strip())

    if word_count < MIN_WORDS or char_count < MIN_CHARS:
        return False

    # Rule 2: Remove if ALL lines have fewer than MIN_LINE_CHARS characters
    has_long_line = any(len(line.strip()) >= MIN_LINE_CHARS for line in lines)
    if not has_long_line:
        return False

    return True


def filter_paragraphs(input_path, output_path):
    """Read input file, filter paragraphs, and write to output file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into paragraphs (separated by blank lines)
    paragraphs = content.split('\n\n')

    # Filter paragraphs
    kept = []
    removed = 0

    for para in paragraphs:
        if para.strip():  # Skip empty paragraphs
            if should_keep_paragraph(para):
                kept.append(para)
            else:
                removed += 1

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(kept))

    return len(kept), removed


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python filter_paragraphs.py <input_file> <output_file>")
        print("Example: python filter_paragraphs.py input.txt output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Filtering paragraphs from: {input_file}")
    print(f"Parameters: MIN_WORDS={MIN_WORDS}, MIN_CHARS={MIN_CHARS}, "
          f"MIN_LINE_CHARS={MIN_LINE_CHARS}")

    kept, removed = filter_paragraphs(input_file, output_file)

    print(f"\nResults:")
    print(f"  Kept: {kept} paragraphs")
    print(f"  Removed: {removed} paragraphs")
    print(f"  Output saved to: {output_file}")
