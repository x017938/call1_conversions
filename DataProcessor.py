import os
import csv
import pandas as pd
from pgr_snowflake.connect import connect_user_via_oauth_noninteractive
from call_functions.subline_conversion_function import subline_conversion_function
from call_functions.class_code_conversion_function import class_code_conversion_function

class DataProcessor:
  def __init__(self):
    self.col_names = []
    self.rowAmount = 0
    self.cur = None
  
  def setup_snowflake_connection(self, user, user_upn, password):
    """ This method serves the purpose of bringing in the data from snowflake. It takes a query as a parameter that is ran by the Snowflake cursor object. """
    # Oauth connection using userid, user_upn, and user_pwd
    conn = connect_user_via_oauth_noninteractive(sf_user=user, user_upn=user_upn, user_pwd=password)
    # Create cursor object and set up warehouse/db/schema
    self.cur = conn.cursor()

  def setup_database(self, query, warehouse, db, schema):
    self.cur.execute(f"USE WAREHOUSE {warehouse}")
    self.cur.execute(f"USE DATABASE {db}")
    self.cur.execute(f"USE SCHEMA {schema}")

    # Query that brings in the necessary data for Call1
    self.cur.execute(query)
  
  def add_columns(self, arr):
    """ This method adds necessary column names to our col_names array. It also determines the rowAmount for the batching process."""
    # Adding the column names from the data brought in from snowflake
    self.col_names = [name[0] for name in self.cur.description]
    self.col_names.extend(arr)
    self.rowAmount = min((self.cur.rowcount / 2), 1_000_000)

  def process_and_write_data(self):
    """ This method writes our transformed data into a csv for export """
    with open('Final_Test_Data.csv', mode='w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(self.col_names)

      total_rows_processed = 0

      while total_rows_processed != self.cur.rowcount:
        rows = self.cur.fetchmany(self.rowAmount)
        df = pd.DataFrame(rows, columns=self.col_names[:-2])
        df = class_code_conversion_function(df)
        df = subline_conversion_function(df)
        
        processed_rows = df.values.tolist()

        writer.writerows(processed_rows)

        total_rows_processed += len(rows)
  
  def get_row_count(self):
    """ This method returns the amount of rows within the cursor object """
    return self.cur.rowcount

