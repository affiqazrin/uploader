import pandas as pd

def convert_columns_to_float(df, convert_lst):
    """
    Convert specified columns in the DataFrame to float data type.
    If not possible, retain the original data type. Convert None values to 0.

    Parameters:
    - df: DataFrame
    - convert_lst: List of substrings to identify columns for conversion

    Returns:
    - df: DataFrame after the column conversion
    """
    df = df.copy().reset_index(drop=True)

    for col in df.columns:
        for convert_item in convert_lst:
            if convert_item in col:
                try:
                    # Convert None values to 0
                    df.loc[df[col].isna(), col] = 0

                    # Check if the conversion to float is successful
                    converted_values = pd.to_numeric(df.loc[:, col], errors='coerce')

                    if not converted_values.isna().any():
                        df.loc[:, col] = converted_values.astype(float)
                    else:
                        print(f'Warning: Unable to convert column {col} to float. Retaining original data type.')
                except Exception as e:
                    print(f'Error converting column {col} to float: {e}. Retaining original data type.')

    return df
