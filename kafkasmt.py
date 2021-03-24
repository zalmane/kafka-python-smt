import json
from typing import Dict
from types import SimpleNamespace


class KafkaSmt:
    def __init__(self, config: Dict):
        pass

    def transform(self, message: bytes) -> bytes:
        parsed_json = SimpleNamespace(**json.loads(message.decode()))
        return json.dumps(
            self.transformJson(parsed_json).encode()
        )

    def transformJson(self, message: Dict) -> Dict:
        return message
