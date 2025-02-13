import argparse
import re
import logging
import pandas as pd

from utils import file_exists, is_empty, check_columns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_knit_products(input_file: str, output_file: str) -> None:
    if not file_exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} does not exist.")

    if is_empty(input_file):
        raise ValueError(f"Input file {input_file} is empty.")


    df = pd.read_csv(input_file)
    check_columns(df, ['product_name'])
    pattern = re.compile(r'\bKnit\b(?!.*Jumper)', re.IGNORECASE)
    df_filtered = df[df['product_name'].str.contains(pattern, na=False)]
    df_filtered.to_csv(output_file, index=False)
    logging.info(f"Filtered knit products (excluding jumpers) from {input_file} to {output_file}.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, help='Input file path')
    parser.add_argument('--out', required=True, help='Output file path')

    args = parser.parse_args()
    filter_knit_products(args.infile, args.out)

if __name__ == "__main__":
    main()
