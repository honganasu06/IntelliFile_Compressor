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
            
            tokens.append("END_COL")
                
        return tokens

    def encode(self, tokens: List[Any]) -> bytes:
        return self.huffman.encode(tokens)[0]

    def decode(self, encoded_data: bytes, metadata: Dict[str, Any]) -> List[Any]:
        return self.huffman.decode(encoded_data, metadata['huffman_tree'])

    def reconstruct(self, tokens: List[Any]) -> Any:
        # 1. Parse Headers
        if not tokens:
            return []
            
        iterator = iter(tokens)
        
        if next(iterator) != "HEADERS":
            raise ValueError("Invalid CSV Stream: Missing HEADERS")
            
        headers = []
        while True:
            t = next(iterator)
            if t == "DATA":
                break
            headers.append(t)
            
        num_cols = len(headers)
        columns = [[] for _ in range(num_cols)]
        
        # 2. Parse Columns
        current_col_idx = 0
        
        while True:
            try:
                t = next(iterator)
            except StopIteration:
                break
                
            if isinstance(t, str) and t.startswith("COL_INT_"):
                # Delta Encoded Column
                col_idx = int(t.split("_")[-1])
                deltas = []
                while True:
                    dt = next(iterator)
                    if dt == "END_COL":
                        break
                    if isinstance(dt, str) and dt.startswith("D"):
                        deltas.append(int(dt[1:]))
                    else:
                        raise ValueError(f"Expected Delta, got {dt}")
                
                columns[col_idx] = DeltaEncoder.decode(deltas)
                
            elif isinstance(t, str) and t.startswith("COL_STR_"):
                # Dictionary Encoded Column
                col_idx = int(t.split("_")[-1])
                col_vals = []
                while True:
                    kt = next(iterator)
                    if kt == "END_COL":
                        break
                    if isinstance(kt, str) and kt.startswith("K"):
                        kid = int(kt[1:])
                        val = self.dict_encoders[col_idx].get_value(kid)
                        col_vals.append(val)
                    else:
                        raise ValueError(f"Expected Key, got {kt}")
                columns[col_idx] = col_vals
                
            else:
                # Should be end of stream or unexpected
                pass

        # 3. Transpose back to rows
        # Check all cols have same length
        if not columns:
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            return output.getvalue()
            
        num_rows = len(columns[0])
        rows = [headers]
        
        for r in range(num_rows):
            row = []
            for c in range(num_cols):
                if r < len(columns[c]):
                    row.append(str(columns[c][r]))
                else:
                    row.append("") # Should not happen if valid
            rows.append(row)
            
        import io
        output = io.StringIO()
        writer = csv.writer(output, lineterminator='\n') # Use \n for consistency
        writer.writerows(rows)
        return output.getvalue()
