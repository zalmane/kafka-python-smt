import json
from typing import Dict


class KafkaSmt:
    def __init__(self, config: Dict):
        pass

    def transform(self, message: bytes) -> bytes:
        return json.dumps(self.transformJson(message.decode())).encode()

    def transformJson(self, message: Dict) -> Dict:
        return message
