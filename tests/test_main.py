# In the above test cases, we are testing the following:
# 1. GET request to fetch data from the database
# 2. POST request to insert data into the database
# 3. GET request to test the moving average crossover strategy

import unittest
from fastapi.testclient import TestClient
from main import app
from models import TickerData

client = TestClient(app)

class TestFastAPI(unittest.TestCase):

    def test_get_data(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_insert_data_valid(self):
        data = {
            "datetime": "2025-03-01T00:00:00",
            "open": 100,
            "high": 110,
            "low": 90,
            "close": 105,
            "volume": 100000
        }
        response = client.post("/", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Data inserted successfully"})

    def test_insert_data_invalid(self):
        data = {
            "datetime": "2021-01-01T00:00:00",
            "open": 100,
            "high": 110,
            "low": 90,
            "close": 105,
            "volume": "ten thousand" 
        }
        response = client.post("/", json=data)
        self.assertNotEqual(response.status_code, 200)

    def test_get_strategy_performance(self):
        response = client.get("/strategy/performance?short_window=10&long_window=50")
        self.assertEqual(response.status_code, 200)
        self.assertIn("initial_capital", response.json())

if __name__ == "__main__":
    unittest.main()