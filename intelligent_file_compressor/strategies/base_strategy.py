from abc import ABC, abstractmethod
from typing import Any, List, Dict

class BaseStrategy(ABC):
    """
    Abstract base class for all compression strategies.
    Enforces the strict pipeline: parse -> tokenize -> encode -> decode -> reconstruct.
    """

    @abstractmethod
    def parse(self, file_path: str) -> Any:
        """Read file and parse into structural data (dict, list, etc)."""
        pass

    @abstractmethod
    def tokenize(self, parsed_data: Any) -> List[Any]:
        """Convert parsed data into a flat list of tokens."""
        pass

    @abstractmethod
    def encode(self, tokens: List[Any]) -> bytes:
        """Compress tokens into binary data (e.g. using Huffman)."""
        pass

    @abstractmethod
    def decode(self, encoded_data: bytes, metadata: Dict[str, Any]) -> List[Any]:
        """Decompress binary data back into tokens."""
        pass

    @abstractmethod
    def reconstruct(self, tokens: List[Any]) -> Any:
        """Rebuild original data structure from tokens."""
        pass
