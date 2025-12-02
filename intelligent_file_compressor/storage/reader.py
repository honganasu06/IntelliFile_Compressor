import struct
import json
from typing import Tuple, Dict, Any

class IFCReader:
    """
    Reads data from IFC1 format.
    """
    MAGIC = b"IFC1"

    @staticmethod
    def read(input_path: str) -> Tuple[int, Dict[str, Any], bytes]:
        """
        Returns (strategy_id, metadata, compressed_data)
        """
        with open(input_path, 'rb') as f:
            magic = f.read(4)
            if magic != IFCReader.MAGIC:
                raise ValueError("Invalid file format: Not an IFC1 file")
            
            version = struct.unpack('B', f.read(1))[0]
            if version != 1:
                raise ValueError(f"Unsupported version: {version}")
                
            strategy_id = struct.unpack('B', f.read(1))[0]
            meta_len = struct.unpack('>I', f.read(4))[0]
            
            meta_bytes = f.read(meta_len)
            metadata = json.loads(meta_bytes.decode('utf-8'))
            
            compressed_data = f.read()
            
            return strategy_id, metadata, compressed_data
