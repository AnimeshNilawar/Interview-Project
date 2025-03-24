# In the test case, we will test the moving_average_crossover_strategy function in strategy.py. 
# We will check if the function returns the expected keys in the output dictionary and if the trade signals are generated correctly.

import unittest
from strategy import moving_average_crossover_strategy

class TestStrategy(unittest.TestCase):
    
    def test_moving_average_crossover_strategy(self):
        result = moving_average_crossover_strategy(short_window=10, long_window=50)
        self.assertIn("initial_capital", result)
        self.assertIn("final_value", result)
        self.assertIn("return_percentage", result)

        def test_trade_signals(self):
            result = moving_average_crossover_strategy()
            trade_log = result["trades"]
            self.assertTrue(any(trade["action"] in ["BUY", "SELL"] for trade in trade_log))
            
if __name__ == "__main__":
    unittest.main()
