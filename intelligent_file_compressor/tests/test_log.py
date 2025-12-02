import unittest
from intelligent_file_compressor.strategies.log_strategy import LogStrategy

class TestLogStrategy(unittest.TestCase):
    def test_log_parsing(self):
        strat = LogStrategy()
        lines = [
            "2023-01-01 10:00:00 INFO Starting",
            "2023-01-01 10:00:01 ERROR Failed"
        ]
        tokens = strat.tokenize(lines)
        
        # Should have deltas for timestamps
        # 10:00:00 -> TS1
        # 10:00:01 -> TS2 (Delta 1)
        # We look for "D..." tokens
        self.assertTrue(any(t.startswith("D") for t in tokens if isinstance(t, str)))
        
        # Severity mapping
        self.assertIn("SEV:1", tokens) # INFO
        self.assertIn("SEV:3", tokens) # ERROR

if __name__ == '__main__':
    unittest.main()
