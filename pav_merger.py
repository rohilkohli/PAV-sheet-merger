#!/usr/bin/env python3
"""
PAV Sheet Merger
================
A tool to intelligently merge Physical Asset Verification (PAV) sheets from multiple engineers.

This script merges Excel files containing PAV data, prioritizing non-empty values
and preserving all updates from different engineers.
"""

import pandas as pd
import openpyxl
from pathlib import Path
from datetime import datetime
import argparse
import sys


class PAVMerger:
    """Handles merging of PAV sheets from multiple Excel files."""
    
    def __init__(self, files, output_file='merged_pav_sheet.xlsx', key_column='Asset Code'):
        """
        Initialize the PAV merger.
        
        Args:
            files: List of Excel file paths to merge
            output_file: Output file path for merged sheet
            key_column: Column to use as unique identifier for merging
        """
        self.files = files
        self.output_file = output_file
        self.key_column = key_column
        self.dataframes = []
        self.merge_report = {
            'total_assets': 0,
            'files_processed': 0,
            'updates_merged': 0,
            'conflicts': []
        }
    
    def load_files(self):
        """Load all Excel files into dataframes."""
        print(f"Loading {len(self.files)} file(s)...")
        
        for file_path in self.files:
            try:
                # Read the PAV Sheet
                df = pd.read_excel(file_path, sheet_name='PAV Sheet')
                self.dataframes.append({
                    'file': file_path,
                    'data': df
                })
                print(f"  ✓ Loaded {file_path}: {len(df)} rows")
                self.merge_report['files_processed'] += 1
            except Exception as e:
                print(f"  ✗ Error loading {file_path}: {e}")
                sys.exit(1)
    
    def merge_sheets(self):
        """
        Merge all loaded dataframes intelligently.
        
        Priority logic:
        1. For each asset (identified by key_column), collect all versions
        2. For each field, prioritize non-empty values
        3. If multiple non-empty values exist, use the most recent (last file)
        4. Track conflicts where different non-empty values exist
        """
        if not self.dataframes:
            print("No dataframes to merge!")
            sys.exit(1)
        
        print("\nMerging sheets...")
        
        # Start with first dataframe as base
        merged_df = self.dataframes[0]['data'].copy()
        
        # Convert all columns to object dtype to avoid type conflicts
        for col in merged_df.columns:
            if col != self.key_column:
                merged_df[col] = merged_df[col].astype('object')
        
        self.merge_report['total_assets'] = len(merged_df)
        
        # Columns to track for updates (exclude system columns)
        update_columns = [col for col in merged_df.columns 
                         if col not in [self.key_column, '__EMPTY', '__EMPTY_1']]
        
        # Merge each subsequent dataframe
        for i in range(1, len(self.dataframes)):
            df_to_merge = self.dataframes[i]['data']
            file_name = self.dataframes[i]['file']
            
            print(f"\n  Processing: {file_name}")
            
            # Iterate through each asset
            for idx, row in df_to_merge.iterrows():
                asset_code = row[self.key_column]
                
                # Find matching row in merged dataframe
                merged_idx = merged_df[merged_df[self.key_column] == asset_code].index
                
                if len(merged_idx) == 0:
                    # New asset not in merged sheet - add it
                    merged_df = pd.concat([merged_df, row.to_frame().T], ignore_index=True)
                    self.merge_report['updates_merged'] += 1
                    print(f"    + Added new asset: {asset_code}")
                else:
                    # Asset exists - merge fields
                    merged_idx = merged_idx[0]
                    updates_count = 0
                    
                    for col in update_columns:
                        new_value = row[col]
                        current_value = merged_df.at[merged_idx, col]
                        
                        # Check if new value should replace current
                        if self._should_update(current_value, new_value, col):
                            # Check for conflicts
                            if self._is_conflict(current_value, new_value):
                                self.merge_report['conflicts'].append({
                                    'asset': asset_code,
                                    'column': col,
                                    'value1': current_value,
                                    'value2': new_value,
                                    'resolution': 'Using latest'
                                })
                            
                            # Use loc to avoid dtype warning
                            merged_df.loc[merged_idx, col] = new_value
                            updates_count += 1
                    
                    if updates_count > 0:
                        print(f"    ↻ Updated {updates_count} field(s) for: {asset_code}")
                        self.merge_report['updates_merged'] += updates_count
        
        return merged_df
    
    def _should_update(self, current_value, new_value, column):
        """
        Determine if new value should replace current value.
        
        Args:
            current_value: Current value in merged sheet
            new_value: New value from file being merged
            column: Column name
            
        Returns:
            True if new value should replace current value
        """
        # If current is empty/NaN and new is not, update
        if pd.isna(current_value) and not pd.isna(new_value):
            return True
        
        # If new is empty/NaN, don't update
        if pd.isna(new_value):
            return False
        
        # If both have values and they're different, use new (latest wins)
        if current_value != new_value:
            return True
        
        return False
    
    def _is_conflict(self, value1, value2):
        """Check if two values represent a conflict (both non-empty and different)."""
        return (not pd.isna(value1) and not pd.isna(value2) and value1 != value2)
    
    def save_output(self, merged_df):
        """Save merged dataframe to Excel file."""
        print(f"\nSaving merged sheet to: {self.output_file}")
        
        # Create Excel writer
        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            merged_df.to_excel(writer, sheet_name='PAV Sheet', index=False)
        
        print(f"  ✓ Saved successfully!")
    
    def print_report(self):
        """Print merge report."""
        print("\n" + "=" * 60)
        print("MERGE REPORT")
        print("=" * 60)
        print(f"Files processed: {self.merge_report['files_processed']}")
        print(f"Total assets: {self.merge_report['total_assets']}")
        print(f"Fields updated: {self.merge_report['updates_merged']}")
        print(f"Conflicts resolved: {len(self.merge_report['conflicts'])}")
        
        if self.merge_report['conflicts']:
            print("\nConflicts (showing first 5):")
            for conflict in self.merge_report['conflicts'][:5]:
                print(f"  - Asset: {conflict['asset']}")
                print(f"    Column: {conflict['column']}")
                print(f"    Value 1: {conflict['value1']}")
                print(f"    Value 2: {conflict['value2']}")
                print(f"    Resolution: {conflict['resolution']}")
        
        print("=" * 60)
    
    def run(self):
        """Execute the complete merge process."""
        print("PAV Sheet Merger")
        print("=" * 60)
        
        self.load_files()
        merged_df = self.merge_sheets()
        self.save_output(merged_df)
        self.print_report()
        
        print("\n✓ Merge completed successfully!")
        return merged_df


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Merge PAV (Physical Asset Verification) sheets from multiple Excel files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge two files
  python pav_merger.py "Anshu K.xlsx" "Rohil Kohli.xlsx"
  
  # Merge with custom output name
  python pav_merger.py file1.xlsx file2.xlsx -o final_pav.xlsx
  
  # Merge multiple files
  python pav_merger.py file1.xlsx file2.xlsx file3.xlsx
        """
    )
    
    parser.add_argument('files', nargs='+', help='Excel files to merge')
    parser.add_argument('-o', '--output', default='merged_pav_sheet.xlsx',
                       help='Output file name (default: merged_pav_sheet.xlsx)')
    parser.add_argument('-k', '--key', default='Asset Code',
                       help='Column to use as unique identifier (default: Asset Code)')
    
    args = parser.parse_args()
    
    # Validate input files exist
    for file in args.files:
        if not Path(file).exists():
            print(f"Error: File not found: {file}")
            sys.exit(1)
    
    # Run merger
    merger = PAVMerger(args.files, args.output, args.key)
    merger.run()


if __name__ == '__main__':
    main()
