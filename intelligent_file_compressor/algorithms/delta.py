from typing import List

class DeltaEncoder:
    """
    Encodes a list of integers as differences between consecutive values.
    """
    
    @staticmethod
    def encode(values: List[int]) -> List[int]:
        if not values:
            return []
        
        deltas = [values[0]]
        for i in range(1, len(values)):
            deltas.append(values[i] - values[i-1])
        return deltas

    @staticmethod
    def decode(deltas: List[int]) -> List[int]:
        if not deltas:
            return []
            
        values = [deltas[0]]
        for i in range(1, len(deltas)):
            values.append(values[-1] + deltas[i])
        return values
