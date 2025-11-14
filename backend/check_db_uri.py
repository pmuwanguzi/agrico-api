import psycopg2

# Replace the credentials below with your actual PostgreSQL setup
DB_HOST = "localhost"
DB_NAME = "agrico_db"
DB_USER = "postgres"
DB_PASS = "1704"  # <-- replace this with your actual PostgreSQL password

try:
    connection = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    print(" Connection successful!")
    connection.close()
except Exception as e:
    print(" Error connecting to database:")
    print(e)
