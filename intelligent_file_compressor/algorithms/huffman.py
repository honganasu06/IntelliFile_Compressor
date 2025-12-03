import heapq
from collections import Counter
from typing import Dict, List, Any, Tuple, Iterator
from ..utils.bit_stream import BitWriter, BitReader

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
        self.total_tokens = sum(freq.values())
        
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

    def train(self, tokens: Iterator[Any]):
        """Builds the Huffman tree from tokens."""
        self.build_tree(tokens)

    def encode(self, tokens: Iterator[Any], writer: BitWriter):
        """
        Encodes tokens into the bit writer using existing tree.
        """
        if not self.codes:
            raise ValueError("Huffman tree not built. Call train() first.")
            
        for token in tokens:
            code = self.codes.get(str(token))
            if code is None:
                # Fallback or error? For now, error.
                # In a robust system, we might have an UNKNOWN token.
                raise KeyError(f"Token '{token}' not found in Huffman tree.")
            writer.write_string(code)

    def decode(self, reader: BitReader, codebook: Dict[str, str], limit: int = None) -> List[str]:
        """
        Decodes bits back to token keys (strings).
        """
        self.reverse_mapping = codebook
        decoded = []
        current_code = ""
        
        # This is a naive decoding. A better way is to traverse the tree.
        # But for now, we stick to the map lookup for simplicity of refactor.
        # We read bit by bit.
        
        try:
            while True:
                if limit is not None and len(decoded) >= limit:
                    break
                    
                bit = reader.read_bit()
                current_code += str(bit)
                if current_code in self.reverse_mapping:
                    decoded.append(self.reverse_mapping[current_code])
                    current_code = ""
        except EOFError:
            pass
                
        return decoded
