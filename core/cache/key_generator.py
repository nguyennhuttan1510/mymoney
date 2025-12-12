import hashlib
import urllib
from typing import Dict, Any

from core.cache.interface import KeyGenerator


class KeyGenerateDefault(KeyGenerator):
    def generate(self, *args, **kwargs):
        return ":".join(args)


class KeyHashing(KeyGenerator):
    def __init__(self, prefix:str):
        self.prefix = prefix

    def generate(self, params: Dict[str, Any]):
        sorted_params = sorted(params.items())
        # Convert param → query string
        query_string = urllib.parse.urlencode(sorted_params)
        # Hash để key gọn & an toàn
        hashed = hashlib.md5(query_string.encode()).hexdigest()

        return f"{self.prefix}:{hashed}"