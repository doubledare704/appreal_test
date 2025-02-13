import os

import pandas as pd


def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def is_empty(file_path: str) -> bool:
    return os.path.getsize(file_path) == 0


def is_tsv(file_path: str) -> bool:
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return '\t' in first_line


def check_columns(df: pd.DataFrame, required_columns: list):
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
