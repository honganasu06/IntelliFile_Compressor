import json
from ..storage.reader import IFCReader
from ..strategies.json_strategy import JSONStrategy
from ..strategies.text_strategy import TextStrategy
from ..strategies.csv_strategy import CSVStrategy
from ..strategies.log_strategy import LogStrategy

class Decompressor:
    def __init__(self):
        self.strategy_map = {
            1: JSONStrategy,
            2: CSVStrategy,
            3: LogStrategy,
            4: TextStrategy
        }

    def decompress(self, input_path: str, output_path: str):
        print(f"Decompressing {input_path}...")
        
        # 1. Read
        strat_id, metadata, compressed_data = IFCReader.read(input_path)
        
        # 2. Strategy
        if strat_id not in self.strategy_map:
            raise ValueError(f"Unknown strategy ID: {strat_id}")
        strategy = self.strategy_map[strat_id]()
        
        # Restore dictionaries
        if 'dict_main' in metadata and hasattr(strategy, 'dict_encoder'):
            strategy.dict_encoder.from_dict(metadata['dict_main'])
        if 'dict_cols' in metadata and hasattr(strategy, 'dict_encoders'):
            # Reconstruct column encoders
            for k, v in metadata['dict_cols'].items():
                from ..algorithms.dictionary import DictionaryEncoder
                enc = DictionaryEncoder()
                enc.from_dict(v)
                strategy.dict_encoders[int(k)] = enc
        
        # 3. Decode
        tokens = strategy.decode(compressed_data, metadata)
        
        # 4. Reconstruct
        data = strategy.reconstruct(tokens)
        
        # 5. Write Output
        with open(output_path, 'w', encoding='utf-8') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2)
            elif isinstance(data, str):
                f.write(data)
            else:
                f.write(str(data))
                
        print(f"Restored to {output_path}")
