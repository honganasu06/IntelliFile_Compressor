from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json

@dataclass
class FileMetadata:
    version: str = "1.0"
    strategy_name: str = "GENERIC"
    original_size: int = 0
    compressed_size: int = 0
    dictionary: Dict[int, str] = field(default_factory=dict)
    extra_params: Dict[str, Any] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        """Serialize metadata to JSON bytes."""
        data = {
            "v": self.version,
            "s": self.strategy_name,
            "os": self.original_size,
            "cs": self.compressed_size,
            "d": self.dictionary,
            "e": self.extra_params
        }
        return json.dumps(data).encode('utf-8')

    @classmethod
    def from_bytes(cls, data: bytes) -> 'FileMetadata':
        """Deserialize metadata from JSON bytes."""
        d = json.loads(data.decode('utf-8'))
        # Convert dictionary keys back to integers if they were stored as strings in JSON
        dictionary = {int(k): v for k, v in d.get("d", {}).items()}
        return cls(
            version=d.get("v", "1.0"),
            strategy_name=d.get("s", "GENERIC"),
            original_size=d.get("os", 0),
            compressed_size=d.get("cs", 0),
            dictionary=dictionary,
            extra_params=d.get("e", {})
        )
