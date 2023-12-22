import pandas as pd
import tabula
import numpy as np
import os
import re
from typing import Dict
from icecream import ic

ic.disable()


# Function to create a dictionary of PDF files with a numeric prefix
def filenames_and_prefix_from_dir(directory: str) -> Dict[str, str]:
    pdf_dict: Dict[str, str] = {}

    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        # Use regex to match the first four digits in the filename
        match = re.match(r"^(\d{4})", filename)

        # If the file is a PDF and the regex match is successful, add it to the dictionary
        if filename.endswith(".pdf") and match:
            pdf_dict[filename] = match.group(1)

    # Return the dictionary
    return pdf_dict


# Function to convert special names (e.g. Aus der Fünten)
# Replace in column 1 the string "Aus der Fünten" with "Aus-der-Fünten"
# from pandas import DataFrame


def replace_special_names(df: pd.DataFrame) -> pd.DataFrame:
    first_column = df.columns[0]
    df.loc[:, first_column] = df[first_column].str.replace(
        "Aus der Fünten", "Aus-der-Fünten"
    )
    df.loc[:, first_column] = df[first_column].str.replace("Weiter", "Weiler")
    return df


# Function: delete erroneous rows from the dataframe
# Delete 1st row of the dataframe if a value in the first row is '10km' or contains 'Stadtlauf'
def delete_first_row(df):
    first_row = df.iloc[0]
    ic(first_row.values)
    if "10km" in first_row.values or "Stadtlauf" in first_row.values:
        ic(first_row.values)
        df = df[1:]
    return df


# Function that takes the first column of a dataframe and splits the words by spaces and writes the words into new columns
def split_first_column(df: pd.DataFrame) -> pd.DataFrame:
    first_column = df.columns[0]
    # Remove the "," from the first column
    df.loc[:, first_column] = df[first_column].str.replace(",", "")

    # Check if the last 4 characters either start with '19' or '20'
    # and if yes, then create a separate column for the last 4 characters
    # and remove them from the first column
    if df[first_column].str[-4:].str.contains("19|20").all():
        df.insert(1, "Jahrg", df[first_column].str[-4:])
        df.loc[:, first_column] = df[first_column].str[:-5]
    split_data = df[first_column].str.split(" ", expand=True)
    for i, col in enumerate(split_data.columns):
        df.insert(i, f"new_col_{i+1}", split_data[col])
    df.pop(first_column)
    return df


# Function, checks in the first row of the dataframe whether the first 4 characters of the cell either start with '19' or '20' and do not contain ":"
# and if yes, then create then add an empty column before it
def check_first_row(df: pd.DataFrame) -> pd.DataFrame:
    first_row = df.iloc[0]
    for i, value in enumerate(first_row):
        if i < len(first_row) - 1:
            str_value = str(value)
            if (
                ("19" in str(value)[:2] or "20" in str(value)[:2])
                and str_value[2:4].isdigit()
                and i > 4
            ):
                df.insert(i, "empty column", np.nan)
    return df


# Function that names the column names from 1 to n
def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [f"Column{i+1}" for i in range(df.shape[1])]
    return df


# Function that replaces certain strings e.g. to avoid blanks
def replace_word_1(df: pd.DataFrame) -> pd.DataFrame:
    first_column = df.columns[0]
    df.loc[:, first_column] = df[first_column].str.replace(" U", "_U")
    return df


def main() -> pd.DataFrame:
    # Create a dictionary of PDF files with a numeric prefix

    # Get the path to the currently executing file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Get the path to the parent directory (one level up)
    parent_directory = os.path.dirname(current_directory)

    pdf_dir: str = parent_directory + "/data/raw"
    filenames_prefix = filenames_and_prefix_from_dir(pdf_dir)

    result_table = []
    all_dfs = []
    for key, value in filenames_prefix.items():
        print(f"{key}: {value}")
        test_table = []
        test_table = tabula.read_pdf(pdf_dir + "/" + key, pages="all")
        for df_testtable in test_table:
            df_testtable.insert(len(df_testtable.columns), "Jahr", value)
        result_table.append(test_table)

    # tables1 = tabula.read_pdf(
    #     "pdf_files/2013_HACO_ErgebnislistenZieleinlaufliste.pdf", pages="all"
    # )
    # tables2 = tabula.read_pdf(
    #     "pdf_files/2014_HACO_ErgebnislistenZieleinlaufliste.pdf", pages="all"
    # )
    # tables = tables1 + tables2

    # tables = result_table
    dataframes = {}
    for table in result_table:
        for i, df in enumerate(table):
            df = delete_first_row(df)
            df = replace_special_names(df)
            df.columns = df.iloc[0]
            df = df[2:] if i == 0 else df[1:]
            split_df = replace_word_1(df)
            split_df = split_first_column(df)
            # all columns should be formatted as string
            split_df = split_df.astype(str)
            split_df = check_first_row(df)
            split_df = rename_columns(df)
            dataframes[f"split_df{i+1}"] = split_df
            all_dfs.append(split_df)
    return dataframes


if __name__ == "__main__":
    df_list = main()
    pass
