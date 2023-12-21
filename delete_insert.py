import pandas as pd
from sqlalchemy import create_engine

def delete_and_append_records(df, target_month, table_name, engine):
    try:
        # Delete records for the specified month
        delete_query = f"DELETE FROM {table_name} WHERE Month = '{target_month}'"
        pd.read_sql_query(delete_query, engine)
        print(f"Records for Month: {target_month} deleted successfully")
    except Exception as delete_error:
        print("Error deleting records:", delete_error)
        return

    try:
        # Append new records to the table
        df.to_sql(con=engine, name=table_name, if_exists='append', index=False)
        print("Records appended successfully")
    except Exception as append_error:
        print("Error appending records:", append_error)

# Example usage:
# Replace 'your_database_url' with your actual MySQL database URL
database_url = 'mysql://username:password@localhost/your_database_name'
engine = create_engine(database_url)

# Assuming you have a DataFrame df, a target_month, and a table_name
delete_and_append_records(df, '2023-01', 'your_table_name', engine)
