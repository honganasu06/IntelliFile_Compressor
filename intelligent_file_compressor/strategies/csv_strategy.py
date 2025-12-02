import csv
from typing import Any, List, Dict
from .base_strategy import BaseStrategy
from ..algorithms.dictionary import DictionaryEncoder
from ..algorithms.delta import DeltaEncoder
from ..algorithms.huffman import HuffmanEncoder

class CSVStrategy(BaseStrategy):
    """
    Strict CSV Strategy:
    - Columnar analysis
    - Numeric -> Delta
    - String -> Dictionary
    """
    def __init__(self):
        self.huffman = HuffmanEncoder()
        self.col_types = [] # 'int', 'str'
        self.dict_encoders = {} # col_idx -> encoder

    def parse(self, file_path: str) -> Any:
        rows = []
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
        return rows

    def tokenize(self, parsed_data: List[List[str]]) -> List[Any]:
        if not parsed_data:
            return []
            
        headers = parsed_data[0]
        data_rows = parsed_data[1:]
        
        # 1. Analyze Columns
        num_cols = len(headers)
        columns = [[] for _ in range(num_cols)]
        
        for row in data_rows:
            for i, val in enumerate(row):
                if i < num_cols:
                    columns[i].append(val)
                    
        tokens = ["HEADERS"] + headers + ["DATA"]
        
        for i, col in enumerate(columns):
            # Heuristic: Try to convert to int
            try:
                int_col = [int(x) for x in col]
                # Success -> Delta Encode
                tokens.append(f"COL_INT_{i}")
                deltas = DeltaEncoder.encode(int_col)
                tokens.extend([f"D{d}" for d in deltas])
                self.col_types.append('int')
            except ValueError:
                # String -> Dict Encode
                tokens.append(f"COL_STR_{i}")
                if i not in self.dict_encoders:
                    self.dict_encoders[i] = DictionaryEncoder()
                
                for val in col:
                    vid = self.dict_encoders[i].get_id(val)
                    tokens.append(f"K{vid}")
                self.col_types.append('str')
                
        return tokens

    def encode(self, tokens: List[Any]) -> bytes:
        return self.huffman.encode(tokens)[0]

    def decode(self, encoded_data: bytes, metadata: Dict[str, Any]) -> List[Any]:
        return self.huffman.decode(encoded_data, metadata['huffman_tree'])

    def reconstruct(self, tokens: List[Any]) -> Any:
        # Placeholder for columnar reconstruction
        return []
