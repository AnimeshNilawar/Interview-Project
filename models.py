from pydantic import BaseModel
from typing import List

class TickerData(BaseModel):
    datetime: str
    open: float
    high: float
    low: float
    close: float
    volume: int
