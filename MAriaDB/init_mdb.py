# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="user1",
        password="password1",
        host="localhost"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


# creating database 
cur.execute("CREATE DATABASE IF NOT EXISTS LienMinh;") 


cur.execute("SHOW DATABASES")
databaseList = cur.fetchall()
  
for database in databaseList:
  print(database)
    
conn.close()