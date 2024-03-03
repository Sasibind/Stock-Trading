import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

# deleting old data and creating a new database
sql = '''DROP database IF EXISTS stock_data;'''
cursor.execute(sql)
sql = '''CREATE database stock_data;'''
cursor.execute(sql)
# print("new database created")

#Closing the connection
conn.close()