import os
import csv
import time
import numpy as np
import pandas as pd
from DataProcessor import DataProcessor
from dotenv.main import load_dotenv
from pgr_snowflake.connect import connect_user_via_oauth_noninteractive
from snowflake_queries.call_one_query import query, query2
from call_functions.subline_conversion_function import subline_conversion_function
from call_functions.class_code_conversion_function import class_code_conversion_function

load_dotenv()

data_processor = DataProcessor()
  
start = time.time()

data_processor.setup_snowflake_connection(os.environ.get('USER'),os.environ.get('USER_UPN'),os.environ.get('USER_PWD'))
data_processor.setup_database(warehouse='free_the_data_xs',db='premiums',schema='user_managed', query=query)
data_processor.add_columns(['CLASS_CODE','SUBLINE_CODE'])
data_processor.process_and_write_data()

end = time.time()

rows = data_processor.get_row_count()
print(f"{rows} rows in {round(((end - start) / 60), 2)} mins.")