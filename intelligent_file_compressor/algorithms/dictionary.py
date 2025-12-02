from typing import Dict, Any, List

class DictionaryEncoder:
    def __init__(self):
        self.forward = {}
        self.reverse = {}
        self.next_id = 1

    def get_id(self, value: Any) -> int:
        if value not in self.forward:
            self.forward[value] = self.next_id
            self.reverse[self.next_id] = value
            self.next_id += 1
        return self.forward[value]

    def get_value(self, id: int) -> Any:
        return self.reverse.get(id)

    def to_dict(self) -> Dict[int, Any]:
        return self.reverse

    def from_dict(self, data: Dict[str, Any]):
        # JSON keys are always strings, convert back to int
        self.reverse = {int(k): v for k, v in data.items()}
        self.forward = {v: k for k, v in self.reverse.items()}
        if self.reverse:
            self.next_id = max(self.reverse.keys()) + 1
