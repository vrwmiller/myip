#! /usr/bin/env python3
"""
CSV Transform Tool

This script transforms CSV files by rearranging columns and handling debit/credit 
indicators. It reads a CSV file with combined debit/credit amounts and separates 
them into distinct debit and credit columns based on an indicator field.

Author: [Your Name]
Date: October 18, 2025
"""

import sys
import csv
import argparse
import pprint

def transform_csv(input_file, output_file):
    """
    Transform a CSV file by rearranging columns and separating debit/credit amounts.
    
    This function reads a CSV file where debit and credit amounts are stored in a 
    single 'Amount' column with a separate 'Credit Debit Indicator' column. It 
    transforms this data by creating separate 'Debit' and 'Credit' columns.
    
    Args:
        input_file (str): Path to the input CSV file to be transformed
        output_file (str): Path where the transformed CSV file will be saved
        
    Expected input CSV format:
        - Booking Date: Date of the transaction
        - Check Serial Number: Serial number of the check (if applicable)
        - Description: Description of the transaction
        - Amount: The monetary amount (positive value)
        - Credit Debit Indicator: 'Credit' or 'Debit' to indicate transaction type
        - Category: Transaction category
        
    Output CSV format:
        - Booking Date: Date of the transaction
        - Check Serial Number: Serial number of the check (if applicable)
        - Description: Description of the transaction
        - Debit: Amount if it's a debit transaction, None otherwise
        - Credit: Amount if it's a credit transaction, None otherwise
        - Category: Transaction category
    """
    # Open the input CSV file with UTF-8-sig encoding to handle BOM (Byte Order Mark)
    with open(input_file, mode='r', newline='', encoding='utf-8-sig') as input_f:
        # Create a CSV reader that treats the first row as column headers
        csv_reader = csv.DictReader(input_f)

        # Define the order of the columns for the output file
        # This ensures consistent column ordering in the transformed CSV
        fieldnames = [
                       'Booking Date',          # Transaction date
                       'Check Serial Number',   # Check number (if applicable)
                       'Description',           # Transaction description
                       'Debit',                # Debit amount (negative transactions)
                       'Credit',               # Credit amount (positive transactions)
                       'Category'              # Transaction category
                     ]

        # Open the output CSV file for writing
        with open(output_file, mode='w', newline='') as output_f:
            # Create a CSV writer with the defined field order
            csv_writer = csv.DictWriter(output_f, fieldnames=fieldnames)

            # Write the header row to the output file
            csv_writer.writeheader()

            # Process each row from the input file
            for row in csv_reader:
                # Determine whether this is a debit or credit transaction
                # and assign the amount to the appropriate column
                if row['Credit Debit Indicator'] == 'Debit':
                    # For debit transactions, amount goes in debit column
                    credit = None
                    debit  = row['Amount']
                elif row['Credit Debit Indicator'] == 'Credit':
                    # For credit transactions, amount goes in credit column
                    credit = row['Amount']
                    debit  = None

                # Create a new row dictionary with the transformed structure
                # This maps the input columns to the desired output format
                transformed_row = {
                    'Booking Date':        row['Booking Date'],        # Copy date as-is
                    'Check Serial Number': row['Check Serial Number'], # Copy check number as-is
                    'Description':         row['Description'],         # Copy description as-is
                    'Debit':               debit,                      # Debit amount or None
                    'Credit':              credit,                     # Credit amount or None
                    'Category':            row['Category']             # Copy category as-is
                }
                # Write the transformed row to the output file
                csv_writer.writerow(transformed_row)

    # Inform the user that the transformation is complete
    print(f"Transformed data has been written to {output_file}")

def main():
    """
    Main function that handles command-line argument parsing and executes the transformation.
    
    This function sets up the argument parser to accept input and output file paths,
    validates the arguments, and calls the transform_csv function to perform the
    actual data transformation.
    
    Command-line usage:
        python csvtransform.py -i input.csv -o output.csv
        python csvtransform.py --input input.csv --output output.csv
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description='Transform CSV data by rearranging columns and separating debit/credit amounts.',
        epilog='Example: python csvtransform.py -i bank_data.csv -o transformed_data.csv'
    )
    
    # Define required arguments for input and output file paths
    parser.add_argument('-i', '--input', 
                       required=True, 
                       help='Path to the input CSV file to be transformed')
    parser.add_argument('-o', '--output', 
                       required=True, 
                       help='Path where the transformed CSV file will be saved')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Execute the CSV transformation
    transform_csv(args.input, args.output)

if __name__ == "__main__":
    # This ensures that main() only runs when the script is executed directly,
    # not when it's imported as a module
    main()
