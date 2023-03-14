import base64


def encode_int_to_base64(n: int) -> str:
    """Encode an integer to base64"""
    # Convert the integer to bytes in big-endian byte order
    b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    # Encode the bytes to base64 and return the result as a string
    return base64.b64encode(b).decode('utf-8')


def decode_int_from_base64(s: str) -> int:
    """Decode an integer from base64"""
    # Decode the base64 string to bytes
    b = base64.b64decode(s.encode('utf-8'))
    # Convert the bytes to an integer in big-endian byte order
    return int.from_bytes(b, 'big')
