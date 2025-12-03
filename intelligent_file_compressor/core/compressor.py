import os
from .file_detector import FileDetector
from ..strategies.json_strategy import JSONStrategy
from ..strategies.text_strategy import TextStrategy
from ..strategies.csv_strategy import CSVStrategy
from ..strategies.log_strategy import LogStrategy
from ..storage.writer import IFCWriter
from ..utils.bit_stream import BitWriter

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
        
        # Check if strategy supports streaming (has 'train' method)
        if hasattr(strategy, 'train'):
            # --- Streaming Flow ---
            
            # Pass 1: Train
            parsed_1 = strategy.parse(input_path)
            tokens_1 = strategy.tokenize(parsed_1)
            strategy.train(tokens_1)
            
            # Collect Metadata
            metadata = {
                "huffman_tree": strategy.huffman.reverse_mapping,
                "token_count": strategy.huffman.total_tokens
            }
            if hasattr(strategy, 'dict_encoder'):
                metadata['dict_main'] = strategy.dict_encoder.to_dict()
            if hasattr(strategy, 'dict_encoders'):
                metadata['dict_cols'] = {str(k): v.to_dict() for k, v in strategy.dict_encoders.items()}
            
            # Pass 2: Write & Encode
            with open(output_path, 'wb') as f:
                IFCWriter.write_header(f, strat_id, metadata)
                
                parsed_2 = strategy.parse(input_path)
                tokens_2 = strategy.tokenize(parsed_2)
                
                bit_writer = BitWriter(f)
                strategy.encode(tokens_2, bit_writer)
                bit_writer.close()
                
        else:
            # --- Legacy Flow ---
            
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
            with open(output_path, 'wb') as f:
                IFCWriter.write_header(f, strat_id, metadata)
                f.write(compressed_data)

        print(f"Written to {output_path}")
