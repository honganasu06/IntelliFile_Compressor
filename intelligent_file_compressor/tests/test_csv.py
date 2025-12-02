import unittest
from intelligent_file_compressor.strategies.csv_strategy import CSVStrategy

class TestCSVStrategy(unittest.TestCase):
    def test_columnar_delta(self):
        strat = CSVStrategy()
        # Mock parsed data: Header + 2 rows
        data = [["ID", "Val"], ["10", "A"], ["11", "B"]]
        tokens = strat.tokenize(data)
        
        # Should detect int column and delta encode
        self.assertIn("COL_INT_0", tokens)
        self.assertIn("D10", tokens) # First value
        self.assertIn("D1", tokens)  # Delta
        
        # Should detect str column and dict encode
        self.assertIn("COL_STR_1", tokens)
        self.assertTrue(any(t.startswith("K") for t in tokens))

if __name__ == '__main__':
    unittest.main()
