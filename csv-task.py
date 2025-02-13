import argparse
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_tsv(file_path: str) -> bool:
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return '\t' in first_line

def convert_tsv_to_csv(input_file: str, output_file: str):
    if not is_tsv(input_file):
        raise ValueError(f"Input file {input_file} does not appear to be a TSV (tab-separated values) file.")
    try:
        df = pd.read_csv(input_file, sep='\t')
    except Exception as e:
        raise ValueError(f"Failed to read the TSV file {input_file}: {e}")

    if 'rrp_price' not in df.columns:
        raise ValueError(f"Column 'rrp_price' not found in {input_file}")
    # i've picked this field because 'price' is not present in tsv file in test assignment
    df['rrp_price'] = pd.to_numeric(df['rrp_price'], errors='coerce')
    df['price_edited'] = df['rrp_price'].astype(float)

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
