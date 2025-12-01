import argparse
import csv
import re
import os
import sys

# --- CONFIGURATION ---
CSV_DELIMITER = ';'
ENCODING = 'utf-8-sig'
# ---------------------

def read_plain_text_lines(file_path):
    """Reads a plain text file into a list of strings."""
    if not os.path.exists(file_path):
        print(f"Error: Text file '{file_path}' not found.")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def resolve_output_path(input_path, output_arg, suffix_arg, extension):
    """Calculates final path with optional suffix."""
    folder, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    
    # Determine base name with suffix
    final_name = name
    if suffix_arg:
        final_name += suffix_arg
    final_name += extension

    # Determine folder
    if output_arg:
        if os.path.isdir(output_arg):
            return os.path.join(output_arg, final_name)
        return output_arg # output_arg is a full path
    
    return os.path.join(folder, final_name)

def check_overwrite(path, force_mode):
    """Checks if file exists and asks user if not forced."""
    if not os.path.exists(path):
        return True
    
    if force_mode:
        return True
    
    print(f"WARNING: File '{path}' already exists.")
    choice = input("Overwrite? (y/n): ").lower()
    if choice == 'y':
        return True
    print("Operation aborted.")
    return False

def apply_formatting(text, enclose_mode):
    """Handles parentheses logic based on -e argument."""
    text = text.strip()
    if not text: return ""

    if enclose_mode == 0: # Remove ()
        if text.startswith('(') and text.endswith(')'):
            return text[1:-1].strip()
    elif enclose_mode == 1: # Add ()
        if not (text.startswith('(') and text.endswith(')')):
            return f"({text})"
    return text

def show_preview(lines, verbosity=0, interactive=False, is_csv=False):
    """Shows a preview of the output and asks for confirmation if interactive."""
    if not lines:
        print("Preview: (No output generated)")
        return True # Nothing to write

    print("\n--- Preview ---")
    
    # Determine how many lines to show
    max_lines = 10
    if verbosity > 0:
        max_lines = len(lines)
    
    preview_lines = lines[:max_lines]
        
    # Display the lines
    for line in preview_lines:
        # For CSV, format with | for better readability
        if is_csv:
            print(" | ".join(map(str, line)))
        else:
            print(line)
        
    if len(lines) > len(preview_lines):
        print(f"... ({len(lines) - len(preview_lines)} more lines)")
    
    print("--- End Preview ---\n")

    if interactive:
        choice = input("Do you want to write this to the file? (y/n): ").lower()
        if choice == 'y':
            return True
        print("Operation aborted by user.")
        return False
        
    return True # Non-interactive, always proceed

def normalize_text(text):
    """Normalizes text for comparison by lowercasing and removing parentheses."""
    text = text.lower().strip()
    if text.startswith('(') and text.endswith(')'):
        return text[1:-1].strip()
    return text

def parse_lrc_lines(file_path, translated_mode=False, enclose_mode=None):
    """
    Parses LRC. 
    If translated_mode (-t) is True, non-timestamped lines are treated as 
    translations of the previous timestamp.
    """
    time_pattern = re.compile(r'^(\[\d{2}:\d{2}\.\d{2,3}\])(.*)')
    tag_pattern = re.compile(r'^(\[[a-zA-Z]+:.*\])$')
    
    parsed_data = [] # List of dicts: {'type': 'tag'|'lyric', 'time': str, 'lines': []}
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        current_lyric = None

        for line in f:
            line = line.strip()
            
            # 1. Metadata Tags
            tag_match = tag_pattern.match(line)
            if tag_match:
                if current_lyric:
                    parsed_data.append(current_lyric)
                    current_lyric = None
                parsed_data.append({'type': 'tag', 'content': tag_match.group(1)})
                continue

            # 2. Timestamp Lines
            time_match = time_pattern.match(line)
            if time_match:
                if current_lyric:
                    parsed_data.append(current_lyric)
                
                timestamp = time_match.group(1)
                text = time_match.group(2).strip()
                current_lyric = {'type': 'lyric', 'time': timestamp, 'lines': []}
                if text:
                    current_lyric['lines'].append(text)
                continue

            # 3. Translation Lines (The non-timestamped lines)
            if translated_mode and current_lyric and line:
                formatted_line = apply_formatting(line, enclose_mode)
                current_lyric['lines'].append(formatted_line)

        if current_lyric:
            parsed_data.append(current_lyric)

    return parsed_data

# --- ACTIONS ---

def action_sheet(args):
    """LRC -> CSV"""
    output_path = resolve_output_path(args.input, args.output, args.suffix, ".csv")

    if not check_overwrite(output_path, args.force):
        return

    data = parse_lrc_lines(args.input, args.translated, args.enclose)

    # Prepare base rows
    rows = []
    lyric_row_indices = []

    for i, item in enumerate(data):
        if item['type'] == 'tag':
            rows.append([item['content']])
        elif item['type'] == 'lyric':
            if args.remove_identical:
                unique_lines = []
                seen = set()
                for line in item['lines']:
                    normalized = normalize_text(line)
                    if normalized not in seen:
                        unique_lines.append(line)
                        seen.add(normalized)
                item['lines'] = unique_lines

            row = [item['time']] + item['lines']
            rows.append(row)
            lyric_row_indices.append(len(rows) - 1)

    # Handle --add
    if args.add_files:
        for txt_file in args.add_files:
            extra_lines = read_plain_text_lines(txt_file)
            for idx, lyric_row_idx in enumerate(lyric_row_indices):
                if idx < len(extra_lines):
                    rows[lyric_row_idx].append(extra_lines[idx])
                else:
                    rows[lyric_row_idx].append("") # Pad if text file is shorter

    # Handle preview and writing
    if args.preview:
        # Interactive preview before writing
        if not show_preview(rows, args.verbosity, interactive=True, is_csv=True):
            return # Abort if user says no
    
    try:
        with open(output_path, 'w', newline='', encoding=ENCODING) as f:
            writer = csv.writer(f, delimiter=CSV_DELIMITER)
            writer.writerows(rows)
        print(f"Sheet created: {output_path}")

        if not args.preview:
            # Non-interactive snippet after writing
            show_preview(rows, args.verbosity, interactive=False, is_csv=True)

    except Exception as e:
        print(f"Error writing CSV: {e}")

def action_stack(args):
    """CSV/LRC -> Final LRC"""
    output_path = resolve_output_path(args.input, args.output, args.suffix, ".lrc")

    if not check_overwrite(output_path, args.force):
        return

    final_lines = []

    # --- Line Generation ---
    # MODE A: Direct (LRC -> LRC)
    if args.direct:
        data = parse_lrc_lines(args.input, args.translated, args.enclose)
        
        if args.add_files:
            lyric_items = [item for item in data if item['type'] == 'lyric']
            for txt_file in args.add_files:
                extra_lines = read_plain_text_lines(txt_file)
                for idx, item in enumerate(lyric_items):
                    if idx < len(extra_lines):
                        item['lines'].append(extra_lines[idx])

        for item in data:
            if item['type'] == 'tag':
                final_lines.append(item['content'])
            elif item['type'] == 'lyric':
                if not item['lines']:
                    final_lines.append(item['time']) # Instrumental break
                else:
                    lines_to_process = item['lines']
                    if args.remove_identical:
                        unique_lines = []
                        seen = set()
                        for line in lines_to_process:
                            normalized = normalize_text(line)
                            if normalized not in seen:
                                unique_lines.append(line)
                                seen.add(normalized)
                        lines_to_process = unique_lines
                    
                    for line in lines_to_process:
                        final_lines.append(f"{item['time']}{line}")

    # MODE B: Standard (CSV -> LRC)
    else:
        if not os.path.exists(args.input):
            print(f"Error: File '{args.input}' not found.")
            sys.exit(1)
        
        rows = []
        try:
            with open(args.input, 'r', encoding=ENCODING) as f:
                reader = csv.reader(f, delimiter=CSV_DELIMITER)
                rows = list(reader)
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return

        if args.add_files:
            lyric_rows = [row for row in rows if row and re.match(r'^\[\d{2}:\d{2}', row[0])]
            for txt_file in args.add_files:
                extra_lines = read_plain_text_lines(txt_file)
                for idx, row in enumerate(lyric_rows):
                    row.append(extra_lines[idx] if idx < len(extra_lines) else "")

        for row in rows:
            if not row: continue
            col_a = row[0].strip()

            if col_a.startswith('[') and ':' in col_a and not re.match(r'^\[\d{2}:', col_a):
                final_lines.append(col_a)
                continue

            if re.match(r'^\[\d{2}:\d{2}', col_a):
                content_cols = [c.strip() for c in row[1:] if c.strip()]
                
                if args.remove_identical:
                    unique_cols = []
                    seen = set()
                    for text in content_cols:
                        normalized = normalize_text(text)
                        if normalized not in seen:
                            unique_cols.append(text)
                            seen.add(normalized)
                    content_cols = unique_cols

                if not content_cols:
                    final_lines.append(col_a) # Break
                else:
                    for text in content_cols:
                        final_lines.append(f"{col_a}{text}")

    # --- Preview and Writing ---
    if args.preview:
        if not show_preview(final_lines, args.verbosity, interactive=True):
            return

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_lines))
        print(f"Stacked to: {output_path}")

        if not args.preview:
            show_preview(final_lines, args.verbosity, interactive=False)

    except Exception as e:
        print(f"Error writing file: {e}")

def action_add(args):
    """Add columns to an existing CSV"""
    if not os.path.exists(args.csv_input):
        print(f"Error: CSV '{args.csv_input}' not found.")
        sys.exit(1)

    rows = []
    with open(args.csv_input, 'r', encoding=ENCODING) as f:
        reader = csv.reader(f, delimiter=CSV_DELIMITER)
        rows = list(reader)

    lyric_row_indices = [i for i, row in enumerate(rows) if row and re.match(r'^\[\d{2}:\d{2}', row[0])]

    for txt_file in args.text_files:
        extra_lines = read_plain_text_lines(txt_file)
        for idx, lyric_row_idx in enumerate(lyric_row_indices):
            if idx < len(extra_lines):
                rows[lyric_row_idx].append(extra_lines[idx])
            else:
                rows[lyric_row_idx].append("")

    try:
        with open(args.csv_input, 'w', newline='', encoding=ENCODING) as f:
            writer = csv.writer(f, delimiter=CSV_DELIMITER)
            writer.writerows(rows)
        print(f"Updated CSV: {args.csv_input}")
    except Exception as e:
        print(f"Error updating CSV: {e}")


def main():
    parser = argparse.ArgumentParser(description="lrcstack: Advanced LRC & Translation Tool")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # --- SHARED ARGUMENTS ---
    parent_shared = argparse.ArgumentParser(add_help=False)
    parent_shared.add_argument('-e', '--enclose', type=int, choices=[0, 1], 
                            help='0=Remove (), 1=Add () to translations')
    parent_shared.add_argument('-s', '--suffix', nargs='?', const='_stacked', 
                            help='Append suffix to output filename. Defaults to "_stacked" if flag is present without value.')
    parent_shared.add_argument('-f', '--force', action='store_true', 
                            help='Force overwrite existing files without asking')
    parent_shared.add_argument('-a', '--add', dest='add_files', nargs='+', 
                         help='Add plain text files as extra lines/columns')
    parent_shared.add_argument('-p', '--preview', action='store_true',
                            help='Show a preview of the output before writing to file')
    parent_shared.add_argument('-v', '--verbosity', action='count', default=0,
                            help='Increase output verbosity. Shows more lines in preview.')
    parent_shared.add_argument('-i', '--remove-identical', action='store_true',
                            help='Remove identical translation lines (case-insensitive).')

    # --- SHEET ---
    p_sheet = subparsers.add_parser('sheet', parents=[parent_shared], help='Convert LRC to CSV Sheet')
    p_sheet.add_argument('input', help='Input LRC file')
    p_sheet.add_argument('-o', '--output', help='Output path')
    p_sheet.add_argument('-t', '--translated', action='store_true', 
                         help='Treat new lines as translations of the previous timestamp')

    # --- STACK ---
    p_stack = subparsers.add_parser('stack', parents=[parent_shared], help='Convert Sheet (or LRC) to Final Stacked LRC')
    p_stack.add_argument('input', help='Input file (CSV or LRC)')
    p_stack.add_argument('-o', '--output', help='Output path')
    p_stack.add_argument('-d', '--direct', action='store_true', 
                         help='Direct conversion (Input is LRC, not CSV). Skips sheet creation.')
    p_stack.add_argument('-t', '--translated', action='store_true', 
                         help='(For --direct only) Treat new lines as translations')

    # --- ADD (Standalone) ---
    p_add = subparsers.add_parser('add', help='Add text files as columns to an existing CSV')
    p_add.add_argument('csv_input', help='Target CSV file')
    p_add.add_argument('text_files', nargs='+', help='Plain text files to append')

    args = parser.parse_args()

    if args.command == 'sheet':
        action_sheet(args)
    elif args.command == 'stack':
        action_stack(args)
    elif args.command == 'add':
        action_add(args)

if __name__ == "__main__":
    main()