import re
from typing import Any, List, Dict, Iterator
from .base_strategy import BaseStrategy
from ..algorithms.huffman import HuffmanEncoder
from ..utils.bit_stream import BitWriter, BitReader

class TextStrategy(BaseStrategy):
    """
    Strict Text Strategy:
    - Tokenize: words, punct, spaces
    - Huffman Encode
    """
    def __init__(self):
        self.huffman = HuffmanEncoder()

    def parse(self, file_path: str) -> Iterator[str]:
        # Generator that yields lines to avoid loading full file
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                yield line

    def tokenize(self, parsed_data: Iterator[str]) -> Iterator[Any]:
        # Regex to split by words, spaces, punctuation
        pattern = re.compile(r'(\w+|[^\w\s]|\s+)')
        for line in parsed_data:
            for match in pattern.finditer(line):
                yield match.group(0)

    def train(self, tokens: Iterator[Any]):
        self.huffman.train(tokens)

    def encode(self, tokens: Iterator[Any], writer: BitWriter):
        self.huffman.encode(tokens, writer)

    def decode(self, reader: BitReader, metadata: Dict[str, Any]) -> List[Any]:
        limit = metadata.get('token_count')
        return self.huffman.decode(reader, metadata['huffman_tree'], limit=limit)

    def reconstruct(self, tokens: List[Any]) -> Any:
        return "".join(tokens)
