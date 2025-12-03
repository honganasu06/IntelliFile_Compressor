from typing import BinaryIO, Iterator

class BitWriter:
    """
    Writes bits to a file stream.
    Buffers bits until a full byte is ready, then writes it.
    """
    def __init__(self, stream: BinaryIO):
        self.stream = stream
        self.buffer = 0
        self.count = 0

    def write_bit(self, bit: int):
        """Write a single bit (0 or 1)."""
        self.buffer = (self.buffer << 1) | bit
        self.count += 1
        if self.count == 8:
            self._flush_buffer()

    def write_bits(self, value: int, num_bits: int):
        """Write multiple bits from an integer value."""
        # This can be optimized, but loop is simple for now
        for i in range(num_bits - 1, -1, -1):
            bit = (value >> i) & 1
            self.write_bit(bit)

    def write_string(self, bit_string: str):
        """Write a string of '0's and '1's."""
        for char in bit_string:
            self.write_bit(int(char))

    def _flush_buffer(self):
        self.stream.write(bytes([self.buffer]))
        self.buffer = 0
        self.count = 0

    def close(self):
        """Flush remaining bits (padded with 0s) and close."""
        if self.count > 0:
            self.buffer = self.buffer << (8 - self.count)
            self.stream.write(bytes([self.buffer]))
        # We don't close the stream here, just the bit writer wrapper
        
class BitReader:
    """
    Reads bits from a bytes-like object or stream.
    """
    def __init__(self, data: bytes):
        self.data = data
        self.byte_idx = 0
        self.bit_idx = 0 # 0 to 7, from MSB to LSB
        self.data_len = len(data)

    def read_bit(self) -> int:
        if self.byte_idx >= self.data_len:
            raise EOFError("End of bit stream")
        
        byte = self.data[self.byte_idx]
        # Extract bit at current position (7 - bit_idx)
        bit = (byte >> (7 - self.bit_idx)) & 1
        
        self.bit_idx += 1
        if self.bit_idx == 8:
            self.bit_idx = 0
            self.byte_idx += 1
            
        return bit

    def read_bits(self, num_bits: int) -> int:
        value = 0
        for _ in range(num_bits):
            value = (value << 1) | self.read_bit()
        return value
