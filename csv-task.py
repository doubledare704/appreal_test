import argparse

import pandas as pd

def is_tsv(file_path: str) -> bool:
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return '\t' in first_line

def convert_tsv_to_csv(input_file: str, output_file: str):
    if not is_tsv(input_file):
        raise ValueError(f"Input file {input_file} does not appear to be a TSV (tab-separated values) file.")

    df = pd.read_csv(input_file, sep='\t')
    # df['price_edited'] = df['price'].astype(float)
    df.to_csv(output_file, index=False)
    print(f"Converted {input_file} to {output_file} with new column 'price_edited'.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, help='Input file path')
    parser.add_argument('--out', required=True, help='Output file path')

    args = parser.parse_args()
    convert_tsv_to_csv(args.infile, args.out)


if __name__ == "__main__":
    main()
