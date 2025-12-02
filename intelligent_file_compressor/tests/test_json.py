import unittest
import os
from intelligent_file_compressor.strategies.json_strategy import JSONStrategy
from intelligent_file_compressor.algorithms.delta import DeltaEncoder

class TestJSONStrategy(unittest.TestCase):
    def test_monotonic_delta(self):
        strat = JSONStrategy()
        data = [100, 101, 102, 103]
        tokens = strat.tokenize(data)
        # Expected: [, DELTA_INT_SEQ, D100, D1, D1, D1, ]
        self.assertIn("DELTA_INT_SEQ", tokens)
        self.assertIn("D100", tokens)
        self.assertIn("D1", tokens)

    def test_dict_encoding(self):
        strat = JSONStrategy()
        data = {"name": "Alice", "role": "admin"}
        tokens = strat.tokenize(data)
        # Keys should be K1, K2 etc.
        self.assertTrue(any(t.startswith("K") for t in tokens if isinstance(t, str)))

if __name__ == '__main__':
    unittest.main()
