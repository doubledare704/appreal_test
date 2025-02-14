import argparse
import logging

import pandas as pd

from utils import file_exists, is_empty, is_tsv, check_columns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_tsv_to_csv(input_file: str, output_file: str):
    if not file_exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} does not exist.")
    if is_empty(input_file):
        raise ValueError(f"Input file {input_file} is empty.")

    if not is_tsv(input_file):
        raise ValueError(f"Input file {input_file} does not appear to be a TSV (tab-separated values) file.")
    try:
        df = pd.read_csv(input_file, sep='\t')
    except Exception as e:
        raise ValueError(f"Failed to read the TSV file {input_file}: {e}")

    original_field = "search_price"
    check_columns(df, [original_field])
    df[original_field] = pd.to_numeric(df[original_field], errors='coerce')
    df['price_edited'] = df[original_field].astype(float)

    try:
        df.to_csv(output_file, index=False)
        logging.info(f"Converted {input_file} to {output_file} with new column 'price_edited'.")
    except Exception as e:
        raise ValueError(f"Failed to write the CSV file {output_file}: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, help='Input file path')
    parser.add_argument('--out', required=True, help='Output file path')

    args = parser.parse_args()
    try:
        convert_tsv_to_csv(args.infile, args.out)
    except ValueError as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    main()
