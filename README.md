# CSV and Regex Processing Scripts

This project includes two Python scripts for processing CSV files:
1. **`csv-task.py`**: Converts a TSV (Tab-Separated Values) file to a CSV, with an additional column based on a price transformation.
2. **`regex-task.py`**: Filters products with "Knit" in their name (excluding "Knit Jumper") from a CSV file.

## Requirements

The following Python packages are required:

- `pandas` (or the version you're using)
- Python 3.8+

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Scripts

1. **`csv-task.py`**: Convert TSV to CSV with Price Transformation.
- This script converts a TSV file to a CSV file, while also adding a new column, price_edited, which is derived from the rrp_price column.
```bash 
  python csv-task.py --infile <input_tsv_file> --out <output_csv_file>
  ```
2. **`regex-task.py`**: Filter Knit Products (Excluding Jumpers)
- This script filters products that contain the word "Knit" in their name, but excludes those with the word "Jumper". The filtered results are saved to a new CSV file.
```bash 
python regex-task.py --infile <input_csv_file> --out <output_csv_file>
```



