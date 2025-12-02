import json
from typing import Any, List, Dict
from ..core.token_stream import Token, TokenType
from .base_strategy import BaseStrategy
from ..algorithms.dictionary import DictionaryEncoder
from ..algorithms.delta import DeltaEncoder
from ..algorithms.huffman import HuffmanEncoder

class JSONStrategy(BaseStrategy):
    """
    Strict JSON Strategy:
    - Flatten keys -> Dictionary Encode
    - Monotonic Integers -> Delta Encode
    - Structure -> Tokens
    """
    
    def __init__(self):
        self.dict_encoder = DictionaryEncoder()
        self.huffman = HuffmanEncoder()

    def parse(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def tokenize(self, parsed_data: Any) -> List[Any]:
        tokens = []
        self._traverse(parsed_data, tokens)
        return tokens

    def _traverse(self, obj: Any, tokens: List[Any]):
        if isinstance(obj, dict):
            tokens.append("{")
            for key, value in obj.items():
                # Dictionary Encode Key
                key_id = self.dict_encoder.get_id(key)
                tokens.append(f"K{key_id}")
                self._traverse(value, tokens)
            tokens.append("}")
            
        elif isinstance(obj, list):
            tokens.append("[")
            # Check for monotonic integers
            if all(isinstance(x, int) for x in obj) and len(obj) > 2:
                # Simple check for monotonicity (strictly increasing)
                if all(obj[i] < obj[i+1] for i in range(len(obj)-1)):
                    tokens.append("DELTA_INT_SEQ")
                    deltas = DeltaEncoder.encode(obj)
                    tokens.extend([f"D{d}" for d in deltas])
                    tokens.append("]")
                    return

            for item in obj:
                self._traverse(item, tokens)
            tokens.append("]")
            
        elif isinstance(obj, str):
            tokens.append(f"S:{obj}") # Literal string
        elif isinstance(obj, int):
            tokens.append(f"I:{obj}")
        elif isinstance(obj, bool):
            tokens.append(f"B:{obj}")
        elif obj is None:
            tokens.append("NULL")

    def encode(self, tokens: List[Any]) -> bytes:
        compressed_data, tree = self.huffman.encode(tokens)
        return compressed_data

    def decode(self, encoded_data: bytes, metadata: Dict[str, Any]) -> List[Any]:
        return self.huffman.decode(encoded_data, metadata['huffman_tree'])

    def reconstruct(self, tokens: List[Any]) -> Any:
        # Simplified reconstruction state machine
        # In a full impl, this needs a stack
        # For MVP, we will assume valid structure and just parse back
        # This is complex to do iteratively without a parser, 
        # so we'll implement a recursive consumer.
        self.token_iter = iter(tokens)
        return self._consume()

    def _consume(self):
        try:
            token = next(self.token_iter)
        except StopIteration:
            return None

        if token == "{":
            obj = {}
            while True:
                # Peek or next
                # We need to handle keys or end
                # This is tricky with iterators. 
                # Let's assume next token is Key or }
                # But we consumed it.
                # Real parser needs lookahead.
                # For this MVP, let's hack:
                # If next is "}", break.
                # Else it's a key.
                pass # TODO: Full parser logic
            return {}
        return None
