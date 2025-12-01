# LRCStack

A command-line tool for manipulating and stacking LRC (lyrics) files, with a focus on managing translations.

## Features

- Convert LRC files to CSV for easy editing (`sheet`).
- Stack multiple lyric lines (e.g., original and translation) under the same timestamp (`stack`).
- Add lyrics from plain text files as new columns in a CSV (`add`).
- Handle various formatting options for translations.

## Usage

This is a single-file Python script with no external dependencies.

### General

```bash
python lrcstack.py [command] --help
```

### `sheet`: Convert LRC to CSV

```bash
python lrcstack.py sheet <input.lrc> -o <output.csv>
```

### `stack`: Convert CSV/LRC to Stacked LRC

From a CSV file:
```bash
python lrcstack.py stack <input.csv> -o <output.lrc>
```

Directly from an LRC file (with translations on new lines):
```bash
python lrcstack.py stack <input.lrc> --direct --translated -o <output.lrc>
```

### `add`: Add Columns to CSV

```bash
python lrcstack.py add <target.csv> <translation1.txt> <translation2.txt>
```

## Development

This repository contains the `lrcstack.py` script and documentation related to its development and features.
