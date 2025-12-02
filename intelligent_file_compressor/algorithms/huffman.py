import heapq
from collections import Counter
from typing import Dict, List, Any, Tuple

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanEncoder:
    """
    Canonical Huffman Encoder.
    """
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def build_tree(self, tokens: List[Any]) -> Dict[str, str]:
        """Build Huffman tree and return codebook."""
        # Convert tokens to string keys for frequency counting
        freq = Counter(str(t) for t in tokens)
        
        heap = []
        for key, count in freq.items():
            heapq.heappush(heap, HuffmanNode(key, count))

        if not heap:
            return {}
            
        if len(heap) == 1:
            node = heap[0]
            self.codes[node.char] = "0"
            self.reverse_mapping["0"] = node.char
            return self.codes

        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)

        root = heap[0]
        self._make_codes(root, "")
        return self.codes

    def _make_codes(self, node, current_code):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char
            return
        self._make_codes(node.left, current_code + "0")
        self._make_codes(node.right, current_code + "1")

    def encode(self, tokens: List[Any]) -> Tuple[bytes, Dict[str, str]]:
        """
        Encodes tokens into bytes. Returns (compressed_bytes, codebook).
        """
        self.codes = {}
        self.reverse_mapping = {}
        self.build_tree(tokens)
        
        bit_string = ""
        for token in tokens:
            bit_string += self.codes[str(token)]
            
        # Padding
        extra_padding = 8 - len(bit_string) % 8
        bit_string = "{0:08b}".format(extra_padding) + bit_string + ("0" * extra_padding)

        b = bytearray()
        for i in range(0, len(bit_string), 8):
            b.append(int(bit_string[i:i+8], 2))
            
        return bytes(b), self.reverse_mapping

    def decode(self, data: bytes, codebook: Dict[str, str]) -> List[str]:
        """
        Decodes bytes back to token keys (strings).
        Caller must convert keys back to original types if needed.
        """
        self.reverse_mapping = codebook
        
        bit_string = ""
        for byte in data:
            bit_string += f"{byte:08b}"

        extra_padding = int(bit_string[:8], 2)
        bit_string = bit_string[8:]
        if extra_padding > 0:
            bit_string = bit_string[:-extra_padding]

        decoded = []
        current_code = ""
        for bit in bit_string:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded.append(self.reverse_mapping[current_code])
                current_code = ""
                
        return decoded
