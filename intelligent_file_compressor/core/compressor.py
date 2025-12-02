import os
from .file_detector import FileDetector
from ..strategies.json_strategy import JSONStrategy
from ..strategies.text_strategy import TextStrategy
from ..strategies.csv_strategy import CSVStrategy
from ..strategies.log_strategy import LogStrategy
from ..storage.writer import IFCWriter

class Compressor:
    def __init__(self):
        self.strategies = {
            FileDetector.JSON: (1, JSONStrategy),
            FileDetector.CSV: (2, CSVStrategy),
            FileDetector.LOG: (3, LogStrategy),
            FileDetector.TEXT: (4, TextStrategy)
        }

    def compress(self, input_path: str, output_path: str):
        print(f"Compressing {input_path}...")
        
        # 1. Detect
        file_type = FileDetector.detect(input_path)
        strat_id, strat_cls = self.strategies[file_type]
        strategy = strat_cls()
        
        # 2. Parse
        parsed = strategy.parse(input_path)
        
        # 3. Tokenize
        tokens = strategy.tokenize(parsed)
        
        # 4. Encode
        compressed_data = strategy.encode(tokens)
        
        # 5. Collect Metadata
        metadata = {
            "huffman_tree": strategy.huffman.reverse_mapping
        }
        # Add dictionary tables if present
        if hasattr(strategy, 'dict_encoder'):
            metadata['dict_main'] = strategy.dict_encoder.to_dict()
        if hasattr(strategy, 'dict_encoders'):
            metadata['dict_cols'] = {str(k): v.to_dict() for k, v in strategy.dict_encoders.items()}
            
        # 6. Write
        IFCWriter.write(output_path, strat_id, metadata, compressed_data)
        print(f"Written to {output_path}")
