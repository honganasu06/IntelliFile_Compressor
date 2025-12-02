import struct
import json
from typing import Dict, Any

class IFCWriter:
    """
    Writes data in IFC1 format:
    MAGIC (4b) | VER (1b) | STRAT (1b) | META_LEN (4b) | META | DATA
    """
    MAGIC = b"IFC1"
    VERSION = 1

    @staticmethod
    def write(output_path: str, strategy_id: int, metadata: Dict[str, Any], compressed_data: bytes):
        meta_bytes = json.dumps(metadata).encode('utf-8')
        meta_len = len(meta_bytes)

        with open(output_path, 'wb') as f:
            f.write(IFCWriter.MAGIC)
            f.write(struct.pack('B', IFCWriter.VERSION))
            f.write(struct.pack('B', strategy_id))
            f.write(struct.pack('>I', meta_len)) # Big-endian 4-byte int
            f.write(meta_bytes)
            f.write(compressed_data)
