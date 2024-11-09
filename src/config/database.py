import mysql.connector
from mysql.connector import Error

# Database credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "admin@123"
DB_NAME = "airline_management"

def establish_connection():
    """Establish a database connection."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
    return None

def execute_query(query, params=()):
    """Execute a query on the database."""
    conn = establish_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    return None