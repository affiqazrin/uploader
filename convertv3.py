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
                    df[col] = df[col].apply(lambda x: 0 if x is None else x).astype(float)
                except ValueError as e:
                    print(f'Error converting column {col} to float: {e}. Retaining original data type.')

    return df
