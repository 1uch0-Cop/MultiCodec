import converter


def test_base64_roundtrip():
    text = "hola mundo"
    enc = converter.encode_base64(text)
    dec = converter.decode_base64(enc)
    assert dec == text


def test_hex_roundtrip():
    text = "hola"
    enc = converter.encode_hex(text)
    dec = converter.decode_hex(enc)
    assert dec == text


def test_rot13_roundtrip():
    text = "hola"
    enc = converter.encode_rot13(text)
    dec = converter.decode_rot13(enc)
    assert dec == text


def test_text_binary_roundtrip():
    text = "hi"
    b = converter.text_to_binary(text)
    t = converter.binary_to_text(b)
    assert t == text


def test_binary_to_decimal_and_hex():
    binary = "00001010"  # 10 decimal, 0x0a
    assert converter.binary_to_decimal(binary) == "10"
    assert converter.binary_to_hex(binary) == "a"


def test_smart_decode_hex():
    s = "686f6c61"
    res = converter.smart_decode(s)
    assert "hex" in res and res["hex"].startswith("hol")
