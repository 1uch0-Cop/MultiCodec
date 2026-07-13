"""Pruebas automatizadas para MultiCodec."""

from __future__ import annotations

import pytest

import converter
import gui


@pytest.mark.parametrize(
    ("original", "encoded"),
    (
        ("hola", "aG9sYQ=="),
        ("Hackcop", "SGFja2NvcA=="),
        ("", ""),
    ),
)
def test_encode_base64(
    original: str,
    encoded: str,
) -> None:
    assert converter.encode_base64(original) == encoded


@pytest.mark.parametrize(
    "original",
    (
        "hola mundo",
        "Zorro ñ 🦊",
        "Atacama\nChile",
        "",
    ),
)
def test_base64_round_trip(original: str) -> None:
    encoded = converter.encode_base64(original)

    assert converter.decode_base64(encoded) == original


@pytest.mark.parametrize(
    "invalid_value",
    (
        "%%%",
        "aGVsbG8",
        "a===aaaa",
    ),
)
def test_decode_base64_rejects_invalid_input(
    invalid_value: str,
) -> None:
    assert (
        converter.decode_base64(invalid_value)
        == converter.INVALID_BASE64
    )


def test_decode_base64_detects_binary_content() -> None:
    assert (
        converter.decode_base64("/w==")
        == converter.INVALID_BASE64_TEXT
    )


@pytest.mark.parametrize(
    "original",
    (
        "hola",
        "Zorro ñ 🦊",
        "1234567890",
        "",
    ),
)
def test_hex_round_trip(original: str) -> None:
    encoded = converter.encode_hex(original)

    assert converter.decode_hex(encoded) == original


def test_decode_hex_accepts_spaces() -> None:
    assert converter.decode_hex("68 6f 6c 61") == "hola"


@pytest.mark.parametrize(
    "invalid_value",
    (
        "xyz",
        "123",
        "68-6f",
    ),
)
def test_decode_hex_rejects_invalid_input(
    invalid_value: str,
) -> None:
    assert (
        converter.decode_hex(invalid_value)
        == converter.INVALID_HEX
    )


def test_decode_hex_detects_binary_content() -> None:
    assert (
        converter.decode_hex("ff")
        == converter.INVALID_HEX_TEXT
    )


@pytest.mark.parametrize(
    "original",
    (
        "hola",
        "Ataque al amanecer",
        "Cybersecurity 2026",
        "",
    ),
)
def test_rot13_round_trip(original: str) -> None:
    encoded = converter.encode_rot13(original)

    assert converter.decode_rot13(encoded) == original


@pytest.mark.parametrize(
    "original",
    (
        "hola mundo",
        "https://hackcop.cl/ruta?q=zorro",
        "Zorro ñ 🦊",
        "",
    ),
)
def test_url_round_trip(original: str) -> None:
    encoded = converter.encode_url(original)

    assert converter.decode_url(encoded) == original


@pytest.mark.parametrize(
    "invalid_value",
    (
        "%",
        "%2",
        "%GG",
        "texto%4Z",
    ),
)
def test_decode_url_rejects_invalid_sequences(
    invalid_value: str,
) -> None:
    assert (
        converter.decode_url(invalid_value)
        == converter.INVALID_URL
    )


def test_decode_url_rejects_invalid_utf8() -> None:
    assert (
        converter.decode_url("%FF")
        == converter.INVALID_URL
    )


@pytest.mark.parametrize(
    "original",
    (
        "hola",
        "Atacama 🦊",
        "ñ",
        "123",
    ),
)
def test_binary_text_round_trip(original: str) -> None:
    binary = converter.text_to_binary(original)

    assert converter.binary_to_text(binary) == original


def test_text_to_binary_uses_utf8_bytes() -> None:
    assert (
        converter.text_to_binary("ñ")
        == "11000011 10110001"
    )


def test_binary_to_text_accepts_arbitrary_whitespace() -> None:
    binary = "01101000\n01101111 01101100\t01100001"

    assert converter.binary_to_text(binary) == "hola"


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "0101",
        "0101010X",
        "2",
    ),
)
def test_binary_to_text_rejects_invalid_input(
    invalid_value: str,
) -> None:
    assert (
        converter.binary_to_text(invalid_value)
        == converter.INVALID_BINARY
    )


def test_binary_to_text_detects_invalid_utf8() -> None:
    assert (
        converter.binary_to_text("11111111")
        == converter.INVALID_BINARY_TEXT
    )


@pytest.mark.parametrize(
    ("binary", "decimal"),
    (
        ("0", "0"),
        ("1", "1"),
        ("1010", "10"),
        ("11111111", "255"),
    ),
)
def test_binary_to_decimal(
    binary: str,
    decimal: str,
) -> None:
    assert converter.binary_to_decimal(binary) == decimal


@pytest.mark.parametrize(
    ("binary", "hexadecimal"),
    (
        ("0", "0"),
        ("1", "1"),
        ("1010", "a"),
        ("11111111", "ff"),
    ),
)
def test_binary_to_hex(
    binary: str,
    hexadecimal: str,
) -> None:
    assert converter.binary_to_hex(binary) == hexadecimal


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "10201",
        "hola",
    ),
)
def test_binary_numeric_conversions_reject_invalid_input(
    invalid_value: str,
) -> None:
    assert (
        converter.binary_to_decimal(invalid_value)
        == converter.INVALID_BINARY
    )
    assert (
        converter.binary_to_hex(invalid_value)
        == converter.INVALID_BINARY
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("01101000", True),
        ("01101000 01101001", True),
        ("0101", False),
        ("0101010X", False),
        ("", False),
    ),
)
def test_looks_like_binary(
    value: str,
    expected: bool,
) -> None:
    assert converter.looks_like_binary(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("686f6c61", True),
        ("68 6f 6c 61", True),
        ("abc", False),
        ("xyz", False),
        ("", False),
    ),
)
def test_looks_like_hex(
    value: str,
    expected: bool,
) -> None:
    assert converter.looks_like_hex(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("aG9sYQ==", True),
        ("SGFja2NvcA==", True),
        ("%%%", False),
        ("aGVsbG8", False),
        ("", False),
    ),
)
def test_looks_like_base64(
    value: str,
    expected: bool,
) -> None:
    assert converter.looks_like_base64(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        ("hola%20mundo", True),
        ("%68%6F%6C%61", True),
        ("hola mundo", False),
        ("%", False),
    ),
)
def test_looks_like_url_encoding(
    value: str,
    expected: bool,
) -> None:
    assert (
        converter.looks_like_url_encoding(value)
        is expected
    )


def test_smart_decode_detects_base64() -> None:
    assert converter.smart_decode("aG9sYQ==") == {
        "base64": "hola",
    }


def test_smart_decode_detects_hex() -> None:
    assert converter.smart_decode("686f6c61") == {
        "hex": "hola",
    }


def test_smart_decode_detects_url_encoding() -> None:
    assert converter.smart_decode("%68%6F%6C%61") == {
        "url": "hola",
    }


def test_smart_decode_detects_binary() -> None:
    binary = "01101000 01101111 01101100 01100001"

    assert converter.smart_decode(binary) == {
        "binary_text": "hola",
        "binary_decimal": "1752132705",
        "binary_hex": "686f6c61",
    }


def test_smart_decode_returns_empty_result() -> None:
    assert converter.smart_decode("texto normal") == {}


def test_smart_decode_does_not_guess_rot13() -> None:
    assert "rot13" not in converter.smart_decode(
        "uryyb"
    )


@pytest.mark.parametrize(
    ("mode", "value", "expected"),
    (
        (
            "base64_encode",
            "Hackcop",
            "SGFja2NvcA==",
        ),
        (
            "base64_decode",
            "aG9sYQ==",
            "hola",
        ),
        (
            "hex_encode",
            "hola",
            "686f6c61",
        ),
        (
            "hex_decode",
            "686f6c61",
            "hola",
        ),
        (
            "binary_decimal",
            "1010",
            "10",
        ),
        (
            "binary_hex",
            "11111111",
            "ff",
        ),
    ),
)
def test_gui_convert_value(
    mode: str,
    value: str,
    expected: str,
) -> None:
    assert gui.convert_value(mode, value) == expected


def test_gui_formats_smart_results() -> None:
    formatted = gui.convert_value(
        "smart",
        "686f6c61",
    )

    assert formatted == "[Hexadecimal]\nhola"


def test_gui_formats_empty_smart_result() -> None:
    formatted = gui.convert_value(
        "smart",
        "texto normal",
    )

    assert (
        "No se detectó una codificación compatible."
        in formatted
    )
    assert "ROT13" in formatted


def test_gui_rejects_unknown_mode() -> None:
    with pytest.raises(
        ValueError,
        match="Modo desconocido",
    ):
        gui.convert_value(
            "modo_inexistente",
            "hola",
        )
