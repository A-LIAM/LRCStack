# Project Overview

This project is a Python script named `lrcstack.py` that provides a command-line interface for manipulating LRC (lyrics) files. It is designed to help manage and format lyrics, with a particular focus on handling translations.

The script has three main commands:
- `sheet`: Converts an LRC file into a CSV file.
- `stack`: Converts a CSV file (or another LRC file) into a final, "stacked" LRC file. This is useful for combining original lyrics with their translations.
- `add`: Adds new columns (from plain text files) to an existing CSV file.

## Conversation with Gemini.md - Development Log and Detailed Usage

The file `Conversation with Gemini.md` serves as a comprehensive development log and detailed usage guide for the `lrcstack.py` script. It chronicles the iterative process of developing this tool, including:
- Initial problem statements and requirements from the user.
- Discussions on various LRC formatting standards and their compatibility with music players (e.g., AIMP).
- Step-by-step evolution of the Python script, including early versions and their refinements.
- Detailed explanations and examples for using the `lrcstack.py` commands (`sheet`, `stack`, `add`) with various arguments (`-t`, `-p`, `-f`, `-s`, `-a`, `-d`).
- Specific advice on workflow for different platforms (e.g., Android with Pydroid 3, PC terminal).

This file is an invaluable resource for understanding the rationale behind the script's features, troubleshooting, and exploring advanced usage patterns beyond what is covered in the basic help messages.

## Building and Running

This is a single-file Python script with no external dependencies listed in a `requirements.txt` file. It uses standard libraries like `argparse`, `csv`, `re`, `os`, and `sys`.

### Running the script

To use the script, you need to have Python installed. You can run it from the command line.

**General Usage:**

```bash
python lrcstack.py [command] [arguments]
```

**Commands:**

*   **`sheet`**: Convert LRC to CSV.
    ```bash
    python lrcstack.py sheet <input.lrc> -o <output.csv>
    ```

*   **`stack`**: Convert CSV (or LRC) to a stacked LRC file.
    ```bash
    # From CSV
    python lrcstack.py stack <input.csv> -o <output.lrc>

    # Directly from LRC
    python lrcstack.py stack <input.lrc> -d -o <output.lrc>
    ```

*   **`add`**: Add text files as columns to a CSV.
    ```bash
    python lrcstack.py add <target.csv> <file1.txt> <file2.txt>
    ```

For more detailed options and arguments, you can use the `-h` or `--help` flag:

```bash
python lrcstack.py -h
python lrcstack.py sheet -h
python lrcstack.py stack -h
python lrcstack.py add -h
```

## Development Conventions

*   **Formatting**: The code uses standard Python formatting.
*   **Error Handling**: The script includes checks for file existence and provides error messages to the user. It also has an overwrite confirmation prompt to prevent accidental data loss, which can be bypassed with the `-f` or `--force` flag.
*   **Modularity**: The code is organized into functions, with clear separation between parsing logic, actions for each command, and argument parsing.