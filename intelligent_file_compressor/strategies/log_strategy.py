from typing import Any, List, Dict
import re
from datetime import datetime
from .base_strategy import BaseStrategy
from ..algorithms.delta import DeltaEncoder
from ..algorithms.huffman import HuffmanEncoder

class LogStrategy(BaseStrategy):
    """
    Strict Log Strategy:
    - Timestamp -> UNIX -> Delta
    - Severity -> Int Map
    - Message -> Template Dict (Simplified to Huffman for now)
    """
    SEVERITY_MAP = {"INFO": 1, "WARN": 2, "WARNING": 2, "ERROR": 3, "DEBUG": 0}

    def __init__(self):
        self.huffman = HuffmanEncoder()

    def parse(self, file_path: str) -> List[str]:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.readlines()

    def tokenize(self, parsed_data: List[str]) -> List[Any]:
        tokens = []
        timestamps = []
        
        # Regex for ISO timestamp (simple approximation)
        ts_pattern = r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
        
        for line in parsed_data:
            match = re.match(ts_pattern, line)
            if match:
                ts_str = match.group(0)
                # Parse to unix
                try:
                    dt = datetime.fromisoformat(ts_str.replace(' ', 'T'))
                    timestamps.append(int(dt.timestamp()))
                    
                    # Remainder of line
                    remainder = line[len(ts_str):].strip()
                    tokens.append("TS_PLACEHOLDER") # Will inject deltas later
                    
                    # Check severity
                    found_sev = False
                    for sev, code in self.SEVERITY_MAP.items():
                        if sev in remainder:
                            tokens.append(f"SEV:{code}")
                            remainder = remainder.replace(sev, "", 1)
                            found_sev = True
                            break
                    if not found_sev:
                        tokens.append("SEV:UNKNOWN")
                        
                    tokens.append(f"MSG:{remainder}")
                    
                except ValueError:
                    tokens.append(f"RAW:{line.strip()}")
            else:
                tokens.append(f"RAW:{line.strip()}")
                
        # Inject Deltas
        if timestamps:
            deltas = DeltaEncoder.encode(timestamps)
            # This is tricky to interleave without a complex structure.
            # For strict spec, we might store deltas as a block.
            tokens.insert(0, "TS_BLOCK_START")
            tokens.insert(1, deltas) # Store as list, flatten later?
            # Actually, let's just append deltas to tokens for now or rely on Huffman
            # The spec says "Delta encode timestamp".
            # Let's flatten:
            flat_tokens = []
            ts_idx = 0
            for t in tokens:
                if t == "TS_PLACEHOLDER":
                    if ts_idx < len(deltas):
                        flat_tokens.append(f"D{deltas[ts_idx]}")
                        ts_idx += 1
                elif isinstance(t, list):
                    pass # Skip the block insert attempt
                else:
                    flat_tokens.append(t)
            return flat_tokens
            
        return tokens

    def encode(self, tokens: List[Any]) -> bytes:
        return self.huffman.encode(tokens)[0]

    def decode(self, encoded_data: bytes, metadata: Dict[str, Any]) -> List[Any]:
        return self.huffman.decode(encoded_data, metadata['huffman_tree'])

    def reconstruct(self, tokens: List[Any]) -> Any:
        lines = []
        current_ts = 0
        
        # Reverse severity map
        sev_map_rev = {v: k for k, v in self.SEVERITY_MAP.items()}
        
        iterator = iter(tokens)
        
        while True:
            try:
                t = next(iterator)
            except StopIteration:
                break
                
            if isinstance(t, str) and t.startswith("D"):
                # Delta Timestamp
                delta = int(t[1:])
                current_ts += delta
                dt = datetime.fromtimestamp(current_ts)
                ts_str = dt.isoformat(sep=' ')
                
                # Next should be SEV
                sev_token = next(iterator)
                sev_str = "UNKNOWN"
                if isinstance(sev_token, str) and sev_token.startswith("SEV:"):
                    code_str = sev_token.split(":")[1]
                    if code_str == "UNKNOWN":
                        sev_str = ""
                    else:
                        code = int(code_str)
                        sev_str = sev_map_rev.get(code, "UNKNOWN")
                
                # Next should be MSG
                msg_token = next(iterator)
                msg_str = ""
                if isinstance(msg_token, str) and msg_token.startswith("MSG:"):
                    msg_str = msg_token[4:]
                    
                line = f"{ts_str} {sev_str} {msg_str}".strip()
                # Fix double spaces if sev is empty
                line = re.sub(r'\s+', ' ', line)
                lines.append(line)
                
            elif isinstance(t, str) and t.startswith("RAW:"):
                lines.append(t[4:])
                
        return "\n".join(lines)
