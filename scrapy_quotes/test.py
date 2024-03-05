


import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5034",
    database="quotes"
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to retrieve the data
cursor.execute("SELECT * FROM quotes")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Print the retrieved data
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()