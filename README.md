# NDS File Renamer

A Python script to recursively process Nintendo DS (`.nds`) files in a directory, automatically renaming them (and their associated `.sav` files) based on the game’s internal serial code and an external XML database of game names.

------------------------------------------------------------

## Table of Contents

- Features
- Requirements
- Installation
- Usage
- Arguments
- Example
- How It Works
- Warnings & Notes

------------------------------------------------------------

## Features

- Recursively scans a directory and all subdirectories for `.nds` files.
- Extracts the internal game code from each `.nds` file.
- Matches the game code with a game name from a No-Intro XML database.
- Optionally cleans the game name to remove region or other extra information.
- Optionally appends the serial number to the file name.
- Renames corresponding `.sav` files to match the new `.nds` name.
- Provides console output detailing each step.

------------------------------------------------------------

## Requirements

- Python 3.7 or higher
- Standard Python libraries: `os`, `argparse`, `xml.etree.ElementTree`, `pathlib`

------------------------------------------------------------

## Installation

1. Clone or download this repository.
2. Ensure Python 3 is installed and accessible from your terminal.
3. Download the No-Intro Nintendo DS XML database from [No-Intro DAT Files](https://datomatic.no-intro.org/index.php?page=download&op=dat&s=28).
4. Place the XML file somewhere accessible for the script.

------------------------------------------------------------

## Usage

Run the script from the command line:

```bash
python nds_renamer.py --directory <path_to_nds_files> --xml_file <path_to_xml_file> [--clean_name] [--add_serial]
```

------------------------------------------------------------

## Arguments

| Argument       | Type   | Description |
|----------------|--------|-------------|
| `--directory`  | `str`  | **Required.** Path to the directory containing `.nds` files. |
| `--xml_file`   | `str`  | **Required.** Path to the No-Intro XML database file. |
| `--clean_name` | `flag` | Optional. Remove extra information (e.g., region codes) from the game name. |
| `--add_serial` | `flag` | Optional. Append the internal ROM serial code to the filename. |

------------------------------------------------------------

## Example

```bash
python nds_renamer.py --directory "C:\Games\NDS" --xml_file "C:\No-Intro\nds.xml" --clean_name --add_serial
```

This will:

1. Scan `C:\Games\NDS` and all subfolders for `.nds` files.
2. Extract the internal game serial code from each `.nds`.
3. Look up the game name in `nds.xml`.
4. Remove extra region info from the name.
5. Append the serial number to the filename.
6. Rename the `.nds` file and its `.sav` file (if present) to the new name.

Console output will show the serial code, new name, and any warnings if a `.sav` file is missing.

------------------------------------------------------------

## How It Works

1. **Reading the NDS file code**
   - The script opens each `.nds` file and reads 4 bytes at offset `0x0C`.
   - This gives the internal game code (serial).

2. **Mapping serial to game name**
   - The script loads the XML database using `xml.etree.ElementTree`.
   - It finds the game entry where the `rom` tag has a matching `serial`.
   - Retrieves the `name` attribute of that game.

3. **Renaming files**
   - The `.nds` file is renamed to the game name (optionally cleaned and/or appended with serial).
   - If a corresponding `.sav` file exists, it is also renamed.

4. **Recursion**
   - The script recursively processes all subdirectories.

------------------------------------------------------------

## Warnings & Notes

- The script will **overwrite files with the same name**, so ensure backups exist.
- If a `.sav` file does not exist for a `.nds` file, a warning is printed.
- Make sure the XML database is up-to-date for accurate game name mapping.
- Only `.nds` and `.sav` files are renamed; other files are ignored.

------------------------------------------------------------

**Enjoy organized NDS collections!**
