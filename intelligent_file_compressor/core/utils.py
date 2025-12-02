import os
import struct

def get_file_size(filepath: str) -> int:
    """Return the size of a file in bytes."""
    return os.path.getsize(filepath)

def int_to_bytes(n: int, length: int = 4, byteorder: str = 'big') -> bytes:
    """Convert integer to bytes."""
    return n.to_bytes(length, byteorder)

def bytes_to_int(b: bytes, byteorder: str = 'big') -> int:
    """Convert bytes to integer."""
    return int.from_bytes(b, byteorder)

def chunk_data(data: bytes, chunk_size: int):
    """Yield chunks of data."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]
