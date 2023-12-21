from sqlalchemy import create_engine, select, MetaData, Table

def get_distinct_values_as_string(column_name, table_name):
    # Replace these values with your MySQL database credentials
    db_url = 'mysql+mysqlconnector://your_user:your_password@your_host/your_database'

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Create a metadata object
    metadata = MetaData()

    # Reflect the table
    table = Table(table_name, metadata, autoload_with=engine)

    # Create a select statement to get distinct values from the specified column
    distinct_query = select([table.columns[column_name].distinct()])

    # Execute the query and fetch distinct values
    with engine.connect() as connection:
        distinct_values = connection.execute(distinct_query).fetchall()

    # Concatenate distinct values into a comma-separated string
    distinct_values_string = ', '.join(str(value[0]) for value in distinct_values)

    return distinct_values_string

# Example usage
column_name = 'your_column'
table_name = 'your_table'
distinct_values_string = get_distinct_values_as_string(column_name, table_name)

print(f"Distinct values for {column_name}: {distinct_values_string}")
