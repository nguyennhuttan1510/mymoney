import hashlib
import urllib.parse

def make_cache_key(prefix: str, params: dict):
    # Sắp xếp params để key luôn giống nhau khi thứ tự thay đổi
    sorted_params = sorted(params.items())

    # Convert param → query string
    query_string = urllib.parse.urlencode(sorted_params)

    # Hash để key gọn & an toàn
    hashed = hashlib.md5(query_string.encode()).hexdigest()

    return f"{prefix}:{hashed}"