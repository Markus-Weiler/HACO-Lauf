import pandas as pd
import tabula
import numpy as np
import os
import re
from typing import Dict
from icecream import ic
import os
import openpyxl


def filenames_and_prefix_from_dir(directory: str) -> Dict[str, str]:
    """
    This function creates a dictionary of PDF filenames with their numeric prefixes from a given directory.

    Parameters:
    directory (str): The directory to search for PDF files

    Returns:
    pdf_dict (Dict[str, str]): A dictionary where the keys are the PDF filenames and the values are their numeric prefixes
    """
    # Initialize an empty dictionary to store the PDF filenames and their numeric prefixes
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


# Function to convert special names
def replace_special_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function replaces specific names in the first column of the DataFrame with corrected versions.

    Parameters:
    df (pd.DataFrame): The DataFrame with names to correct

    Returns:
    df (pd.DataFrame): The DataFrame with corrected names
    """
    # Get the first column of the DataFrame
    first_column = df.columns[0]

    df.loc[:, first_column] = df[first_column].str.replace("Aus der Fünten", "Aus-der-Fünten")
    df.loc[:, first_column] = df[first_column].str.replace("Weiker", "Weiler")
    df.loc[:, first_column] = df[first_column].str.replace("Wilhelm 194", "Wilhelm, unknown 194")
    df.loc[:, first_column] = df[first_column].str.replace("Schumacher, 198", "Schumacher, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Kornenberger, 197", "Kornenberger, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Nickels-Barth, 197", "Nickels-Barth, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Angelico, 197", "Angelico, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Maldener, 197", "Maldener, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Trampert, 198", "Trampert, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Grünewald, 196", "Grünewald, unknown 196")
    df.loc[:, first_column] = df[first_column].str.replace("Wilhelm, 194", "Wilhelm, unknown 194")
    df.loc[:, first_column] = df[first_column].str.replace("Schumacher, 194", "Schumacher, unknown 194")
    df.loc[:, first_column] = df[first_column].str.replace("Kallenberger, 197", "Kallenberger, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Haupenthal, 198", "Haupenthal, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Przywarra, 198", "Przywarra, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Freudenreich, 198", "Freudenreich, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Oberle 197", "Oberle, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Schneider, 198", "Schneider, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Mörsdorf, 197", "Mörsdorf, unknown 197")
    df.loc[:, first_column] = df[first_column].str.replace("Bernarding, 196", "Bernarding, unknown 196")
    df.loc[:, first_column] = df[first_column].str.replace("Kautenburger, 198", "Kautenburger, unknown 198")
    df.loc[:, first_column] = df[first_column].str.replace("Müller, Philip", "Müller, Philipp")

    # Return the dataframe with corrected names
    return df


def delete_first_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function deletes the first row of the dataframe if it contains '10km' or 'Stadtlauf'.
    """
    # Get the first row of the dataframe
    first_row = df.iloc[0]

    # Check if the first row contains '10km' or 'Stadtlauf'
    if "10km" in first_row.values or "Stadtlauf" in first_row.values:
        # If yes, remove the first row from the dataframe
        df = df.iloc[1:]

    # Return the modified dataframe
    return df


def split_first_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function that takes the first column of a dataframe and splits the words by spaces and writes the words into new columns
    """

    # Get the name of the first column
    first_column = df.columns[0]

    # Remove the "," from the first column
    df.loc[:, first_column] = df[first_column].str.replace(",", "")

    # Check if the last 4 characters of the first column start with '19' or '20'
    if df[first_column].str[-4:].str.contains("19|20").all():
        # If yes, create a separate column for the last 4 characters
        df.insert(1, "Jahrg", df[first_column].str[-4:])
        # And remove them from the first column
        df.loc[:, first_column] = df[first_column].str[:-5]

    # Split the first column by space and expand the result into separate columns
    split_data = df[first_column].str.split(" ", expand=True)

    # Insert the new columns into the dataframe and remove the original first column
    for i, col in enumerate(split_data.columns):
        df.insert(i, f"new_col_{i+1}", split_data[col])
    df.pop(first_column)

    # Fill any NaN values with an empty string
    df = df.fillna("")

    return df


def check_first_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function checks in the first row of the dataframe whether the first 4 characters of the cell either start with '19' or '20'
    and do not contain ":". If yes, then it adds an empty column before it.
    """
    # Convert empty cells to NaN
    df = convert_empty_to_nan(df)

    # Get the first row of the dataframe
    first_row = df.iloc[0]

    # Iterate over each cell in the first row
    for i, value in enumerate(first_row):
        # Convert the cell value to a string
        str_value = str(value)

        # Check if the first 4 characters of the cell start with '19' or '20' and are digits
        # and the cell index is greater than 4
        if (
            i < len(first_row) - 1
            and ("19" in str_value[:2] or "20" in str_value[:2])
            and str_value[2:4].isdigit()
            and i > 4
        ):
            # If yes, insert an empty column at the current index
            df.insert(i, "empty column", "")

    # Convert empty cells to NaN again
    df = convert_empty_to_nan(df)

    # Return the modified dataframe
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function renames the column names of a DataFrame from 'C1', 'C2', ..., 'Cn'
    where n is the number of columns in the DataFrame.
    """
    # Use a list comprehension to generate the new column names
    # The new names are 'C1', 'C2', ..., 'Cn' where n is the number of columns
    df.columns = [f"C{i+1}" for i in range(df.shape[1])]

    # Return the DataFrame with the renamed columns
    return df


def convert_empty_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function converts all empty or 'NaN' fields to nan in a DataFrame.
    """
    # Convert the entire DataFrame to string
    df = df.astype(str)

    # Rename the columns
    df = rename_columns(df)

    # Get the list of column names
    column_names = df.columns

    # Loop through all columns
    for column_name in column_names:
        # Replace all empty strings with NaN
        df[column_name] = df[column_name].replace(r"^\s*$", np.nan, regex=True)
        # Replace all occurrences of 'NaN', 'None' and np.nan with NaN
        df[column_name] = df[column_name].replace(["NaN", "None", np.nan], np.nan)
        # If a column only contains empty strings, replace them with NaN
        if count_characters_in_column(df, column_name) == 0:
            df[column_name] = np.nan

    # Return the modified DataFrame
    return df


def replace_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function replaces certain strings in a DataFrame to avoid blanks.
    It also replaces strings that start with '00:'.
    """
    # Get the name of the first column
    first_column = df.columns[0]

    # Replace " U1" and " U2" with "_U1" and "_U2" in the first column
    df.loc[:, first_column] = df[first_column].str.replace(" U1", "_U1")
    df.loc[:, first_column] = df[first_column].str.replace(" U2", "_U2")

    # Define a function to replace strings that start with '00:'
    def replace_if_starts_with_00(val):
        if isinstance(val, str) and val.startswith("00:"):
            return val.replace("00:", "")
        return val

    # Apply the function to every value in the DataFrame
    df = df.apply(lambda series: series.map(replace_if_starts_with_00))

    # Return the modified DataFrame
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function cleans columns 7 and 8 of the DataFrame based on certain conditions.
    If all values in column 8 start with "19" or "20" and the value in column 7 is 'NaN' or 'nan',
    it writes the first 4 characters from column 8 into column 7 and removes those characters from column 8.
    It also removes column 7 and/or 10 if they are empty.
    """
    # Convert empty cells to NaN
    df = convert_empty_to_nan(df)

    # Replace all NaN with None
    df = df.replace(np.nan, None)

    # Check if all values in column 8 start with "19" or "20"
    if df.iloc[:, 7].astype(str).str[:4].str.contains("19|20").all():
        # If the value in column 7 is 'NaN' or 'nan', then write the value from column 8 into column 7
        if df.iloc[:, 6].isnull().all() or df.iloc[:, 6].astype(str).str.lower().eq("nan").all():
            df.iloc[:, 6] = df.iloc[:, 7].str[:4]
            # Remove the first 4 characters from column 8
            df.iloc[:, 7] = df.iloc[:, 7].str[4:]

    # Remove column 7 and/or 10 if they are empty
    if df.iloc[:, 9].eq("").all():
        df = df.drop(columns=[df.columns[9]])
    if df.iloc[:, 6].eq("").all():
        df = df.drop(columns=[df.columns[6]])

    # Convert empty cells to NaN again
    df = convert_empty_to_nan(df)

    # Return the modified DataFrame
    return df


def count_characters_in_column(df: pd.DataFrame, column_name: str) -> int:
    """
    This function counts the total number of characters in a specified column of a DataFrame.
    """
    # Convert the specified column to string
    df[column_name] = df[column_name].astype(str)

    # Count the total number of characters in the specified column
    character_counts = df[column_name].str.len().sum()

    # Return the total number of characters
    return character_counts


def update_jahrgang_aus_2012(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function updates the 'Jahrgang' column in the input DataFrame based on the values in an Excel file.
    The Excel file contains 'Startnummer' and 'Jahrgang' columns.
    If the 'Startnummer' in the DataFrame matches with the 'Startnummer' in the Excel file and the 'Jahr' in the DataFrame is '2012',
    the 'Jahrgang' in the DataFrame is updated with the 'Jahrgang' from the Excel file.
    """
    # Define the path to the Excel file
    table_jahrgang_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw", "2012_Name_Jahrgang.xlsx"
    )

    # Read the Excel file into a DataFrame
    table_jahrgang_df = pd.read_excel(table_jahrgang_path, engine="openpyxl")

    # Create a dictionary from the Excel DataFrame for quick access to the 'Jahrgang' values based on 'Startnummer'
    dic_jahrgang = {str(row["Startnummer"]): row["Jahrgang"] for _, row in table_jahrgang_df.iterrows()}

    # Update 'Jahrgang' in the input DataFrame if 'Startnummer' matches in dic_jahrgang and 'Jahr' is '2012'
    for index, row in df.iterrows():
        key = row["Startnummer"]
        if key in dic_jahrgang and df.at[index, "Jahr"] == "2012":
            df.at[index, "Jahrgang"] = dic_jahrgang[key]

    # Return the updated DataFrame
    return df


def update_column8_gender(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function updates the 8th column (index 7) of the DataFrame with gender information.
    If the 3rd column (index 2) contains 'M' or 'm', it writes 'm' into the 8th column.
    If the 3rd column (index 2) contains 'W' or 'w', it writes 'w' into the 8th column.
    """
    # Reset the DataFrame index
    df = df.reset_index(drop=True)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Convert the value in the 3rd column to lowercase and check if it contains 'm' or 'w'
        if "m" in str(row.iloc[1]).lower():
            # If it contains 'm', write 'm' into the 8th column
            df.iloc[index, 7] = "m"
        elif "w" in str(row.iloc[1]).lower():
            # If it contains 'w', write 'w' into the 8th column
            df.iloc[index, 7] = "w"

    # Return the updated DataFrame
    return df


def get_first_x_characters(df: pd.DataFrame, x: int, column_name: str, column_index: int) -> pd.DataFrame:
    """
    This function takes the first 'x' characters from a specified column in a DataFrame.
    The column can be specified either by its name or its index.

    Parameters:
    df (pd.DataFrame): The input DataFrame
    x (int): The number of characters to take from the start of the column
    column_name (str): The name of the column
    column_index (int): The index of the column

    Returns:
    df (pd.DataFrame): The DataFrame with the modified column
    """
    # Check if a valid column name is provided
    if column_name and column_name.strip():
        # Convert the specified column to string
        df[column_name] = df[column_name].astype(str)
        # Take the first 'x' characters from the specified column
        df[column_name] = df[column_name].str[:x]
    else:
        # If no valid column name is provided, use the column index
        df.iloc[:, column_index] = df.iloc[:, column_index].astype(str)
        df.iloc[:, column_index] = df.iloc[:, column_index].str[:x]

    # Return the modified DataFrame
    return df


def get_one_dataframe(dic: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    This function combines multiple dataframes into one and returns the combined dataframe.

    Parameters:
    dic (Dict[str, pd.DataFrame]): A dictionary of dataframes

    Returns:
    pd.DataFrame: The combined dataframe
    """

    def validiere_und_transformiere_zeit(time_string: str) -> str:
        """
        This function validates and transforms a time string.

        Parameters:
        time_string (str): The time string

        Returns:
        str: The validated and transformed time string
        """
        regex_mm_ss = r"^\d{2}:\d{2}$"
        regex_hh_mm_ss = r"^\d{1,2}:\d{2}:\d{2}$"

        if re.match(regex_mm_ss, time_string):
            return "00:" + time_string
        elif re.match(regex_hh_mm_ss, time_string):
            return time_string
        else:
            return "00:00:00"

    # Initialize an empty dictionary to store the dataframes
    dataframes = {}

    # Initialize an empty dataframe
    one_df = pd.DataFrame()

    # Define the column names
    column_name = [
        "Gesamt Platz",
        "Platz AK",
        "Startnummer",
        "Name",
        "Vorname1",
        "Vorname2",
        "Jahrgang",
        "Geschlecht",
        "Zeit",
        "Jahr",
    ]
    number_of_columns = len(column_name)

    j = 0
    # Iterate over the dataframes in the dictionary
    for key, df in dic.items():
        # If the number of columns is less than the required number, add empty columns
        if number_of_columns > len(df.columns):
            for i in range(number_of_columns - len(df.columns)):
                df.insert(len(df.columns), f"Spalte {i+1}", "")

        # Select the first 7 columns and the last column
        df = pd.concat([df.iloc[:, : number_of_columns - 1], df.iloc[:, -1:]], axis=1)

        # Rename the columns
        df.columns = column_name

        # Add the dataframe to the combined dataframe
        one_df = pd.concat([one_df, df], ignore_index=True)
        dataframes[f"df{j+1}"] = df
        j += 1

    one_df = update_jahrgang_aus_2012(one_df)

    # Define data types of the columns in dataframe.

    # Remove the period from the 'Gesamt Platz' column and convert it to integer
    one_df["Gesamt Platz"] = one_df["Gesamt Platz"].str.replace(".", "")
    one_df["Gesamt Platz"] = one_df["Gesamt Platz"].astype(int)

    one_df["Platz AK"] = one_df["Platz AK"].astype(str)
    one_df["Startnummer"] = one_df["Startnummer"].astype(int)
    one_df["Name"] = one_df["Name"].astype(str)
    one_df["Vorname1"] = one_df["Vorname1"].astype(str)
    one_df["Vorname2"] = one_df["Vorname2"].astype(str)
    one_df["Jahrgang"] = one_df["Jahrgang"].astype(int)
    one_df["Geschlecht"] = one_df["Geschlecht"].astype(str)

    one_df["Zeit"] = one_df["Zeit"].astype(str)
    one_df["Zeit"] = one_df["Zeit"].str.replace("[", "").str.replace("]", "").str.replace("'", "")
    one_df["Zeit"] = one_df["Zeit"].apply(validiere_und_transformiere_zeit)
    one_df["Zeit"] = pd.to_datetime(one_df["Zeit"], format="%H:%M:%S").dt.time

    one_df["Jahr"] = one_df["Jahr"].astype(int)

    # Save the combined dataframe to an Excel file
    one_df.to_excel("one_def_1.xlsx")

    return one_df


def check_time_format(time_string) -> bool:
    """
    This function checks if a given time string is in a valid format.
    Valid formats are 'HH:MM:SS' or 'MM:SS', where HH is 00-23, MM is 00-59, and SS is 00-59.

    Parameters:
    time_string (str): The time string to check

    Returns:
    bool: True if the time string is in a valid format, False otherwise
    """
    # Define the regular expression pattern for the time format
    pattern = r"^(?:\d|1\d|2[0-3]):[0-5]\d:[0-5]\d$|^[0-5]\d:[0-5]\d$"

    # Use the re.match function to check if the time string matches the pattern
    return bool(re.match(pattern, time_string))


def find_time_formats_in_string(input_string) -> list[str]:
    """
    This function finds all time formats in a given string.
    The time formats can be 'HH:MM:SS' or 'MM:SS', where HH is 00-23, MM is 00-59, and SS is 00-59.

    Parameters:
    input_string (str): The string to search for time formats

    Returns:
    matches (List[str]): A list of all time formats found in the string
    """
    # Define the regular expression pattern for the time format
    pattern = r"(\d{1,2}:\d{2}(?::\d{2})?)"

    # Use the re.findall function to find all occurrences of the pattern in the string
    matches = re.findall(pattern, input_string)

    # Return the list of all time formats found in the string
    return matches


def get_time_format_in_column(df: pd.DataFrame, column_index: int) -> pd.DataFrame:
    """
    This function checks a column of a DataFrame for values in a time format.
    The time formats can be 'HH:MM:SS' or 'MM:SS', where HH is 00-23, MM is 00-59, and SS is 00-59.

    Parameters:
    df (pd.DataFrame): The DataFrame to check
    column_index (int): The index of the column to check

    Returns:
    df (pd.DataFrame): The DataFrame with the checked column
    """
    # Convert the column to string
    df.iloc[:, column_index] = df.iloc[:, column_index].astype(str)

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Check if the value in the column contains a time format
        row.iloc[column_index] = find_time_formats_in_string(row.iloc[column_index])

    # Return the DataFrame with the checked column
    return df


def define_time_and_year_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function checks a DataFrame for columns containing time and year values.
    If found, it moves these values to specific columns and removes all other columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to check

    Returns:
    df (pd.DataFrame): The DataFrame with the checked columns
    """

    # Function to check if a value contains a time format
    def contains_time(val):
        if isinstance(val, list):
            # Überprüfen Sie, ob die Liste mindestens ein Element enthält
            if len(val) > 0:
                # Wenn 'my_list' eine Liste ist, konvertieren Sie das erste Element in einen String
                val = str(val[0])
        if isinstance(val, str):
            return re.search(r"(\d{1,2}:\d{2}:\d{2})|(\d{2}:\d{2})", val) is not None
        return False

    # Function to check if a value contains a year
    def contains_year(val):
        if isinstance(val, str):
            return re.search(r"\d{4}", val) is not None
        return False

    # Check each column from index 8 for a time formatt
    for col in df.columns[8:]:
        b_time = False
        if df[col].apply(contains_time).any():
            df.iloc[:, 8] = df[col]
            b_time = True
            # Spalte index 8 den Namen Zeit geben
            df = df.rename(columns={df.columns[8]: "Zeit"})

    # Check each column from index 8 for a year
    for col in df.columns[8:]:
        b_year = False
        if df[col].apply(contains_year).any():
            df.iloc[:, 9] = df[col]
            b_year = True
            # Spalte index 9 den Namen Jahr geben
            df = df.rename(columns={df.columns[9]: "Jahr"})

    # Remove all columns from index 10
    df = df.iloc[:, :10]

    # Return the DataFrame with the checked columns
    return df


def get_dataframes() -> Dict[str, pd.DataFrame]:
    """
    This function reads PDF files from a directory, extracts tables from them, processes the tables,
    and stores them in a dictionary.

    Returns:
    dataframes (Dict[str, pd.DataFrame]): A dictionary of processed dataframes
    """
    # Get the path to the currently executing file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the directory where the raw PDF data is stored
    parent_directory = os.path.dirname(current_directory)
    pdf_dir: str = parent_directory + "/data/raw"

    # Create a dictionary of PDF files with a numeric prefix
    filenames_prefix = filenames_and_prefix_from_dir(pdf_dir)

    # Initialize a list to store the tables read from the PDFs
    result_table = []
    all_dfs = []

    # Loop over each PDF file
    for key, value in filenames_prefix.items():
        # Read the tables from the current PDF file
        test_table = tabula.read_pdf(pdf_dir + "/" + key, pages="all")
        # Insert the year of competition into each table
        for df_testtable in test_table:
            df_testtable.insert(len(df_testtable.columns), "Jahr", value)
        # Add the tables to the result list
        result_table.append(test_table)

    # Initialize a dictionary to store the processed dataframes
    dic_dataframes = {}
    j = 0

    # Loop over each table in the result list
    for table in result_table:
        for i, df in enumerate(table):
            # Preprocess the dataframe
            df = delete_first_row(df)
            df = replace_special_names(df)
            df.columns = df.iloc[0]
            df = df[2:] if i == 0 else df[1:]
            split_df = convert_empty_to_nan(df)
            split_df = replace_strings(df)
            split_df = split_first_column(split_df)
            split_df = split_df.astype(str)
            split_df = check_first_row(split_df)
            split_df = rename_columns(split_df)
            split_df = clean_columns(split_df)
            split_df = get_first_x_characters(split_df, 4, "", 6)
            split_df = update_column8_gender(split_df)

            # Loop over each column beginn in 9.column in the dataframe
            for k in range(8, split_df.shape[1] - 1):
                # Extract the time format from the column
                split_df = get_time_format_in_column(split_df, k)

            # Define the time and year columns
            split_df = define_time_and_year_columns(split_df)

            # Add the processed dataframe to the dictionary
            dic_dataframes[f"split_df{j+1}"] = split_df
            j += 1
            if j == 3:
                pass

            # Add the processed dataframe to the list
            all_dfs.append(split_df)

    # Return the dictionary of processed dataframes
    return dic_dataframes


def main() -> pd.DataFrame:
    """
    This function retrieves multiple dataframes, combines them into one, and returns the combined dataframe.

    Returns:
    pd.DataFrame: The combined dataframe
    """
    # Retrieve the dataframes
    dic_df = get_dataframes()

    # Combine the dataframes into one
    onedf_all = get_one_dataframe(dic_df)

    return onedf_all


if __name__ == "__main__":
    main()
