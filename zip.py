import os
import pandas as pd

def read_excel_file(file_path):
    try:
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names
        dataframes = {}

        for sheet_name in sheet_names:
            df = xl.parse(sheet_name)

            # Handle datetime conversion for each sheet
            for column in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[column]):
                    df[column] = pd.to_datetime(df[column], errors='coerce')

            dataframes[sheet_name] = df

        return dataframes

    except pd.errors.ParserError as pe:
        print(f"Error parsing Excel file '{file_path}': {pe}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
        return None

# Example usage:
file_path = exported_file_path  # Replace with your actual file path
sheet_dataframes = read_excel_file(file_path)

if sheet_dataframes:
    for sheet_name, df in sheet_dataframes.items():
        print(f"Sheet Name: {sheet_name}")
        print(df)
        print()
