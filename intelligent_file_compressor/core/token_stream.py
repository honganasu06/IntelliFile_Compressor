from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class TokenType(Enum):
    STRUCT_START = auto()  # { or [
    STRUCT_END = auto()    # } or ]
    KEY_REF = auto()       # Dictionary key reference (int ID)
    VALUE_REF = auto()     # Dictionary value reference (int ID)
    LITERAL = auto()       # Raw string/bytes
    INT = auto()           # Integer value
    FLOAT = auto()         # Float value
    BOOL = auto()          # Boolean value
    NULL = auto()          # Null/None
    SEPARATOR = auto()     # , or : (might be implicit in some strategies)
    NEWLINE = auto()       # For text/logs
    TIMESTAMP = auto()     # For logs

@dataclass
class Token:
    type: TokenType
    value: Any = None
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value})"

    @staticmethod
    def from_key(key: str) -> 'Token':
        """Reconstruct a Token from a string key (e.g. 'LITERAL:hello')."""
        type_name, value_str = key.split(':', 1)
        token_type = TokenType[type_name]
        
        # Simple type casting based on TokenType
        value = value_str
        if token_type == TokenType.INT:
            value = int(value_str)
        elif token_type == TokenType.FLOAT:
            value = float(value_str)
        elif token_type == TokenType.BOOL:
            value = value_str == 'True'
        elif token_type == TokenType.NULL:
            value = None
        elif token_type == TokenType.NEWLINE:
            value = int(value_str)
            
        return Token(token_type, value)
