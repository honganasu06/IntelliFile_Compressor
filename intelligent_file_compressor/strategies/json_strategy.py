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
                # Peek would be better, but with iter we just grab next
                # If next is "}", we are done.
                # If next is K<id>, it's a key.
                # We need to handle the case where the dict is empty "{}".
                # But our tokenizer always puts keys or } immediately.
                
                # However, since we can't peek easily with a simple iterator without buffering,
                # we have to be careful. 
                # Let's assume the token stream is valid.
                
                # We can't easily peek, so we might need to grab the next token and decide.
                # But if we grab it and it's a key, we need to process it.
                # If it's "}", we return.
                
                # To make this robust without peek, we can assume that after "{", 
                # we either have "}" or a Key.
                
                # Let's try to implement a peekable iterator wrapper or just handle it here.
                # Actually, we can just grab the next token.
                
                key_token = next(self.token_iter)
                
                if key_token == "}":
                    return obj
                
                # It must be a key
                if isinstance(key_token, str) and key_token.startswith("K"):
                    key_id = int(key_token[1:])
                    key = self.dict_encoder.get_value(key_id)
                    
                    # Value is next
                    value = self._consume()
                    obj[key] = value
                else:
                    raise ValueError(f"Expected Key or }} but got {key_token}")
            return obj

        elif token == "[":
            arr = []
            while True:
                # Similar logic for arrays.
                # We need to check if next is "]".
                # But we can't peek.
                # Wait, for arrays, we don't have keys.
                # So we can't distinguish between "End of Array" and "Start of Next Element" 
                # solely by type easily unless we check for "]".
                
                # We need a way to peek.
                # Let's buffer one token.
                
                # Actually, let's change the architecture slightly to use a list and index
                # or a peekable iterator.
                # Since we are already in this method, let's just hack a peek.
                pass 
                # This approach with raw iterator is flawed for "while True".
                # We need to change how we iterate.
                
            # RE-IMPLEMENTING WITH LIST INDEXING FOR SIMPLICITY
            pass

    def reconstruct(self, tokens: List[Any]) -> Any:
        self.tokens = tokens
        self.pos = 0
        return self._parse_value()

    def _peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _advance(self):
        if self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            self.pos += 1
            return t
        return None

    def _parse_value(self):
        token = self._advance()
        if token is None:
            return None

        if token == "{":
            return self._parse_object()
        elif token == "[":
            return self._parse_array()
        elif isinstance(token, str):
            if token.startswith("S:"):
                return token[2:]
            elif token.startswith("I:"):
                return int(token[2:])
            elif token.startswith("B:"):
                return token[2:] == "True"
            elif token == "NULL":
                return None
            elif token == "DELTA_INT_SEQ":
                # The next tokens are D<val> until ]
                # Actually, our tokenizer puts DELTA_INT_SEQ then D... then ]
                # But wait, the tokenizer puts [ then DELTA_INT_SEQ then D... then ]
                # Let's check tokenize method.
                # It puts [ then DELTA_INT_SEQ.
                # So if we hit [, we call _parse_array.
                # Inside _parse_array, we might see DELTA_INT_SEQ.
                pass
        
        return token # Should not happen if fully covered

    def _parse_object(self):
        obj = {}
        while True:
            t = self._peek()
            if t == "}":
                self._advance()
                return obj
            
            # Expect Key
            key_token = self._advance()
            if not isinstance(key_token, str) or not key_token.startswith("K"):
                 raise ValueError(f"Expected Key, got {key_token}")
            
            key_id = int(key_token[1:])
            key = self.dict_encoder.get_value(key_id)
            
            val = self._parse_value()
            obj[key] = val

    def _parse_array(self):
        arr = []
        
        # Check for special Delta Encoding
        if self._peek() == "DELTA_INT_SEQ":
            self._advance() # consume marker
            # Now we expect D<val> until ]
            deltas = []
            while True:
                t = self._peek()
                if t == "]":
                    self._advance()
                    break
                
                dt = self._advance()
                if isinstance(dt, str) and dt.startswith("D"):
                    deltas.append(int(dt[1:]))
                else:
                    raise ValueError(f"Expected Delta, got {dt}")
            
            return DeltaEncoder.decode(deltas)

        while True:
            t = self._peek()
            if t == "]":
                self._advance()
                return arr
            
            val = self._parse_value()
            arr.append(val)
