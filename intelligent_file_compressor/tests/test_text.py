import unittest
from intelligent_file_compressor.strategies.text_strategy import TextStrategy

class TestTextStrategy(unittest.TestCase):
    def test_tokenization(self):
        strat = TextStrategy()
        text = "Hello, world!"
        tokens = strat.tokenize(text)
        # ["Hello", ",", " ", "world", "!"]
        self.assertIn("Hello", tokens)
        self.assertIn(",", tokens)
        self.assertIn("world", tokens)

if __name__ == '__main__':
    unittest.main()
