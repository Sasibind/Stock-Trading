import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine

db_params = {
   'host': '127.0.0.1',
   'port' : '5432',
   'database': 'stock_data',
   'user': 'postgres',
   'password': 'password'
}

# establishing the connection
conn = psycopg2.connect(
   database=db_params['database'],
   user=db_params['user'],
   password=db_params['password'],
   host=db_params['host'],
   port=db_params['port']
)
conn.autocommit = True

# creating a cursor object using the cursor() method
cursor = conn.cursor()

# deleting old data and creating a new database
sql = '''DROP database IF EXISTS stock_data;'''
cursor.execute(sql)
sql = '''CREATE database stock_data;'''
cursor.execute(sql)
# print("new database created")

# connecting to the newly database
db_params['database'] = 'stock_data'
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

# defining the file paths for the data files
dirpath = os.path.join(os.getcwd(), 'data')
file_list = os.listdir(dirpath)

file_loc = {}

# mapping table names to filepaths
for file in file_list:
   filepath = os.path.join(dirpath, file)
   name = file[:-4].lower()
   name = ''.join(e for e in name if e.isalnum())
   file_loc[name] = filepath

# # printing some data from the tables to verify
# for filename, filepath in file_loc.items():
#    print(f"Contents of '{filename}' CSV file:")
#    df = pd.read_csv(filepath)
#    print(df.head(2))
#    print("\n")

# adding the data to the database
for filename, filepath in file_loc.items():
   df = pd.read_csv(filepath)
   df.columns = map(str.lower, df.columns)
   df.to_sql(filename, engine, if_exists='replace', index=False)

# closing the connection
conn.close()