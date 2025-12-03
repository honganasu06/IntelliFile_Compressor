import struct
import json
from typing import Dict, Any, BinaryIO

class IFCWriter:
    """
    Writes data in IFC1 format:
    MAGIC (4b) | VER (1b) | STRAT (1b) | META_LEN (4b) | META | DATA
    """
    MAGIC = b"IFC1"
    VERSION = 1

    @staticmethod
    def write_header(f: BinaryIO, strategy_id: int, metadata: Dict[str, Any]):
        meta_bytes = json.dumps(metadata).encode('utf-8')
        meta_len = len(meta_bytes)

        f.write(IFCWriter.MAGIC)
        f.write(struct.pack('B', IFCWriter.VERSION))
        f.write(struct.pack('B', strategy_id))
        f.write(struct.pack('>I', meta_len)) # Big-endian 4-byte int
        f.write(meta_bytes)
