# PAV Sheet Merger

A platform to intelligently merge Physical Asset Verification (PAV) sheets from multiple engineers into a single consolidated Excel file.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Merge your PAV sheets
python pav_merger.py "Anshu K.xlsx" "Rohil Kohli.xlsx"
```

See [QUICKSTART.md](QUICKSTART.md) for a complete quick start guide.

## Overview

This tool helps combine PAV sheets where multiple engineers have updated different assets during verification. It intelligently merges the data by:

- Preserving all non-empty values
- Prioritizing the latest updates when conflicts occur
- Tracking and reporting conflicts
- Maintaining data integrity

## Features

- ✅ Merges multiple Excel files with PAV sheets
- ✅ Intelligent field-level merging
- ✅ Conflict detection and resolution
- ✅ Detailed merge report
- ✅ Preserves data integrity
- ✅ Easy-to-use command-line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rohilkohli/PAV-sheet-merger.git
cd PAV-sheet-merger
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Merge two or more PAV sheets:

```bash
python pav_merger.py "Anshu K.xlsx" "Rohil Kohli.xlsx"
```

This will create a file named `merged_pav_sheet.xlsx` with all the combined data.

### Advanced Usage

**Custom output filename:**
```bash
python pav_merger.py file1.xlsx file2.xlsx -o final_output.xlsx
```

**Merge multiple files:**
```bash
python pav_merger.py engineer1.xlsx engineer2.xlsx engineer3.xlsx
```

**Custom key column:**
```bash
python pav_merger.py file1.xlsx file2.xlsx --key "Serial Number"
```

### Command-Line Options

- `files`: Excel files to merge (required, one or more)
- `-o, --output`: Output file name (default: `merged_pav_sheet.xlsx`)
- `-k, --key`: Column to use as unique identifier (default: `Asset Code`)
- `-h, --help`: Show help message

## How It Works

The merger uses an intelligent field-level merge strategy:

```
For each asset (identified by Asset Code):
  For each field:
    ┌─────────────────────────────────────┐
    │ Is current value empty?             │
    │ AND new value NOT empty?            │
    └──────────┬──────────────────────────┘
               │ YES
               ▼
    ┌──────────────────────────┐
    │ Use new value            │
    └──────────────────────────┘
               
               │ NO
               ▼
    ┌─────────────────────────────────────┐
    │ Are both values non-empty           │
    │ AND different?                      │
    └──────────┬──────────────────────────┘
               │ YES
               ▼
    ┌──────────────────────────┐
    │ Use latest value         │
    │ (report as conflict)     │
    └──────────────────────────┘
```

**Example:**
```
Asset: 15C-SCN-X-28974
  Anshu K.xlsx:      PAV Status = [empty]
  Rohil Kohli.xlsx:  PAV Status = "Not Available"
  Merged:            PAV Status = "Not Available" ✓
```

The merger follows this logic:

1. **Load Files**: Reads all specified Excel files and their PAV sheets
2. **Identify Assets**: Uses Asset Code (or custom key) to match rows across files
3. **Merge Data**: For each field:
   - If current value is empty and new value is not empty → use new value
   - If both values are non-empty but different → use latest value (from last file)
   - Track conflicts for reporting
4. **Generate Output**: Creates merged Excel file with all combined data
5. **Report**: Displays statistics and any conflicts encountered

## Example Output

```
PAV Sheet Merger
============================================================
Loading 2 file(s)...
  ✓ Loaded Anshu K.xlsx: 709 rows
  ✓ Loaded Rohil Kohli.xlsx: 709 rows

Merging sheets...

  Processing: Rohil Kohli.xlsx
    ↻ Updated 6 field(s) for: 15C-SCN-X-28974
    ↻ Updated 6 field(s) for: 19L-DTP-X-68011
    ...

Saving merged sheet to: merged_pav_sheet.xlsx
  ✓ Saved successfully!

============================================================
MERGE REPORT
============================================================
Files processed: 2
Total assets: 709
Fields updated: 156
Conflicts resolved: 0
============================================================

✓ Merge completed successfully!
```

## File Structure

```
PAV-sheet-merger/
├── pav_merger.py           # Main merger script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── Anshu K.xlsx           # Sample input file 1
├── Rohil Kohli.xlsx       # Sample input file 2
└── merged_pav_sheet.xlsx  # Generated output (after running)
```

## Requirements

- Python 3.7 or higher
- pandas >= 2.0.0
- openpyxl >= 3.0.0

## Input File Format

The input Excel files should have:
- A sheet named "PAV Sheet"
- A column for unique asset identification (default: "Asset Code")
- Standard PAV columns like:
  - Asset Code, Serial Number, Make, Model
  - PAV Status, Asset status
  - Engineer Name, PAV Date of visit
  - Asset Availability Remarks
  - And other verification fields

## Troubleshooting

**Error: File not found**
- Ensure file paths are correct
- Use quotes around filenames with spaces

**Error: Sheet not found**
- Verify your Excel file has a sheet named "PAV Sheet"
- Or check if sheet name is different in your files

**Wrong merge results**
- Files should have matching Asset Codes for proper merging
- Ensure column names are consistent across files

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is provided as-is for asset verification sheet management.

## Author

Created for efficient PAV sheet management and consolidation.
