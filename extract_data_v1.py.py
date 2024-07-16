import psycopg2
import pandas as pd
import sys
sys.path.append(r'/Users/DELL/Desktop/ETL')
from db_connection import get_db_connection
# Database connection parameters

def extract_data():
    try:
        # Establish the connection
        db_params = get_db_connection()
        conn = psycopg2.connect(**db_params)
        print("Connection to the database established successfully.")
        # List of table names
        tables = ['customers', 'orders', 'order_items', 'products', 'categories', 'reviews']
        # Example query
        for table in tables:
            #Get source data as per incremental logic on the basis of date if data is huge while doing staging
            query = f'SELECT * FROM {table}' 
            df = pd.read_sql(query, conn)
            #Perform  necessary data cleaning, handling missing values, duplicates
            df.fillna('', inplace=True) # Handling missing values (assuming no specific handling instructions)
            df.drop_duplicates(inplace=True) #drop duplicates from dataframe
            #Save the cleaned data for further use into any database or file
            file_path = f"/Users/DELL/Desktop/ETL/Data/{table}.csv"
            df.to_csv(file_path, index=False)
            print(f"Data from {table} extracted, cleaned, and saved to {table}.csv")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

data = extract_data()
