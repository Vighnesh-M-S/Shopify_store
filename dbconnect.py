from fastapi import FastAPI
import pymysql
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

# Retrieve MySQL credentials from environment variables
mysql_user = os.getenv("MYSQLUSER")
mysql_password = os.getenv("MYSQLPASSWORD")
mysql_host = os.getenv("MYSQLHOST")
mysql_database = os.getenv("MYSQLDATABASE")
mysql_port = os.getenv("MYSQLPORT")

# Create a MySQL connection
mysql_connection = pymysql.connect(
    user=mysql_user,
    password=mysql_password,
    host=mysql_host,
    database=mysql_database,
    port=int(mysql_port)  # Ensure the port is an integer
)

@app.get("/")
async def list_data():
    cursor = mysql_connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM majesticcoding")  # Replace 'majesticcoding' with your table name
    data = cursor.fetchall()
    cursor.close()

    return {"data": data}

if __name__ == "__mysql__":
    uvicorn.run(app, host="0.0.0.0", port=8884)