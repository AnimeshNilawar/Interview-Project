import psycopg2
import pandas as pd
import os

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "root"
DB_PORT = "5432"
CSV_FILE = "dataset/HINDALCO.csv"

if os.path.exists("/.dockerenv"):
    DB_HOST = "host.docker.internal"
else:
    DB_HOST = "localhost"

def get_db_connection():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticker_data (
        datetime TIMESTAMP PRIMARY KEY,
        open DOUBLE PRECISION,
        high DOUBLE PRECISION,
        low DOUBLE PRECISION,
        close DOUBLE PRECISION,
        volume BIGINT
    );
    """)
    
    conn.commit()
    conn.close()

# Load CSV data into the database
def load_data_from_csv():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ticker_data;")
    count = cursor.fetchone()[0]

    if count == 0:  
        df = pd.read_csv(CSV_FILE)
        df["datetime"] = pd.to_datetime(df["datetime"])  

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO ticker_data (datetime, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (row["datetime"], row["open"], row["high"], row["low"], row["close"], row["volume"]))

        conn.commit()

    conn.close()
