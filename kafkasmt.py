import json
from typing import Dict


class KafkaSmt:
    def __init__(self, config: Dict):
        pass

    def transform(self, message: bytes) -> bytes:
        parsed_json = json.loads(message.decode())
        return json.dumps(self.transformJson(parsed_json), default=lambda s: vars(s)).encode()

    def transformJson(self, message: Dict) -> Dict:
        return message
