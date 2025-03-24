from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_table_if_not_exists, load_data_from_csv, get_db_connection
from models import TickerData
from strategy import moving_average_crossover_strategy
from typing import List


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table_if_not_exists()
    load_data_from_csv()
    yield  

app = FastAPI(lifespan=lifespan)

@app.get("/", response_model=List[TickerData])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT datetime, open, high, low, close, volume FROM ticker_data")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"datetime": row[0].isoformat(), "open": row[1], "high": row[2], "low": row[3], "close": row[4], "volume": row[5]}
        for row in rows
    ]

@app.post("/")
def insert_data(data: TickerData):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ticker_data (datetime, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (datetime) DO NOTHING
""", (data.datetime, data.open, data.high, data.low, data.close, data.volume))

    conn.commit()
    conn.close()
    return {"message": "Data inserted successfully"}

@app.get("/strategy/performance")
def get_strategy_performance(short_window: int = 10, long_window: int = 50):
    return moving_average_crossover_strategy(short_window, long_window)
