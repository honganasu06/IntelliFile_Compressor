import re
from typing import Any, List, Dict
from .base_strategy import BaseStrategy
from ..algorithms.huffman import HuffmanEncoder

class TextStrategy(BaseStrategy):
    """
    Strict Text Strategy:
    - Tokenize: words, punct, spaces
    - Huffman Encode
    """
    def __init__(self):
        self.huffman = HuffmanEncoder()

    def parse(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

    def tokenize(self, parsed_data: str) -> List[Any]:
        # Regex to split by words, spaces, punctuation
        pattern = r'(\w+|[^\w\s]|\s+)'
        parts = re.findall(pattern, parsed_data)
        return parts

    def encode(self, tokens: List[Any]) -> bytes:
        return self.huffman.encode(tokens)[0]

    def decode(self, encoded_data: bytes, metadata: Dict[str, Any]) -> List[Any]:
        return self.huffman.decode(encoded_data, metadata['huffman_tree'])

    def reconstruct(self, tokens: List[Any]) -> Any:
        return "".join(tokens)
