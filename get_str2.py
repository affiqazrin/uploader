import pandas as pd

def get_distinct_values_as_string(data_frame, column_name):
    """
    Get distinct values from a specified column in a DataFrame and return them as a string.

    Parameters:
    - data_frame (pd.DataFrame): The DataFrame containing the data.
    - column_name (str): The name of the column for which distinct values are required.

    Returns:
    - str: A string containing distinct values separated by commas.
    """
    # Get distinct values from the specified column
    distinct_values = data_frame[column_name].unique()

    # Convert the distinct values to a comma-separated string
    distinct_values_string = ', '.join(map(str, distinct_values))

    return distinct_values_string

# Example DataFrame creation
data = {'your_column': [1, 2, 3, 1, 2, 4, 5, 3, 6]}
df = pd.DataFrame(data)

# Call the method
result = get_distinct_values_as_string(df, 'your_column')

# Print or use the result as needed
print(result)
