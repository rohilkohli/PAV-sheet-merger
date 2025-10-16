# Quick Start Guide - PAV Sheet Merger

## Setup (30 seconds)

```bash
# 1. Clone the repository
git clone https://github.com/rohilkohli/PAV-sheet-merger.git
cd PAV-sheet-merger

# 2. Install dependencies
pip install -r requirements.txt
```

## Usage (10 seconds)

```bash
# Merge your PAV sheets
python pav_merger.py "Engineer1.xlsx" "Engineer2.xlsx"
```

That's it! Your merged file will be `merged_pav_sheet.xlsx`

## What it does

```
┌─────────────────┐     ┌─────────────────┐
│  Anshu K.xlsx   │     │ Rohil Kohli.xlsx│
│  (709 assets)   │     │  (709 assets)   │
│                 │     │                 │
│  Some assets    │     │  Some assets    │
│  have updates   │     │  have updates   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         │    Smart Merge        │
         └───────────┬───────────┘
                     │
          ┌──────────▼──────────┐
          │ merged_pav_sheet.xlsx│
          │    (709 assets)     │
          │                     │
          │   ALL updates       │
          │   combined!         │
          └─────────────────────┘
```

## Example Output

```
PAV Sheet Merger
============================================================
Loading 2 file(s)...
  ✓ Loaded Anshu K.xlsx: 709 rows
  ✓ Loaded Rohil Kohli.xlsx: 709 rows

Merging sheets...
  ↻ Updated 6 field(s) for: 15C-SCN-X-28974
  ↻ Updated 6 field(s) for: 19L-DTP-X-68011
  ...

============================================================
MERGE REPORT
============================================================
Files processed: 2
Total assets: 709
Fields updated: 261
Conflicts resolved: 0
============================================================

✓ Merge completed successfully!
```

## Need Help?

```bash
python pav_merger.py --help
```

## Advanced Options

```bash
# Custom output name
python pav_merger.py file1.xlsx file2.xlsx -o my_merged_file.xlsx

# Merge 3+ files
python pav_merger.py eng1.xlsx eng2.xlsx eng3.xlsx
```
