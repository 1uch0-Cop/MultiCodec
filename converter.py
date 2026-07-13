#!/usr/bin/env python3
"""MultiCodec: conversiones educativas de texto y representaciones de datos."""

from __future__ import annotations

import base64
import binascii
import codecs
import re
import urllib.parse


INVALID_BASE64 = "⚠️ Entrada Base64 inválida."
INVALID_BASE64_TEXT = (
    "⚠️ Base64 válido, pero el contenido no es texto UTF-8."
)
INVALID_HEX = "⚠️ Entrada hexadecimal inválida."
INVALID_HEX_TEXT = (
    "⚠️ Hexadecimal válido, pero el contenido no es texto UTF-8."
)
INVALID_BINARY = "⚠️ Secuencia binaria inválida."
INVALID_BINARY_TEXT = (
    "⚠️ Binario válido, pero el contenido no es texto UTF-8."
)
INVALID_URL = "⚠️ Codificación URL inválida."


def encode_base64(text: str) -> str:
    """Codifica texto UTF-8 como Base64."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode_base64(text: str) -> str:
    """Decodifica Base64 estricto y devuelve texto UTF-8."""
    compact = "".join(text.split())

    try:
        decoded = base64.b64decode(compact, validate=True)
    except (binascii.Error, ValueError):
        return INVALID_BASE64

    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return INVALID_BASE64_TEXT


def encode_hex(text: str) -> str:
    """Codifica texto UTF-8 como hexadecimal."""
    return text.encode("utf-8").hex()


def decode_hex(text: str) -> str:
    """Decodifica hexadecimal y devuelve texto UTF-8."""
    try:
        decoded = bytes.fromhex(text)
    except ValueError:
        return INVALID_HEX

    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return INVALID_HEX_TEXT


def encode_rot13(text: str) -> str:
    """Aplica ROT13 al texto."""
    return codecs.encode(text, "rot_13")


def decode_rot13(text: str) -> str:
    """Revierte ROT13; la operación es simétrica."""
    return codecs.decode(text, "rot_13")


def encode_url(text: str) -> str:
    """Codifica texto como componente de una URL."""
    return urllib.parse.quote(
        text,
        safe="",
        encoding="utf-8",
        errors="strict",
    )


def decode_url(text: str) -> str:
    """Decodifica secuencias porcentuales de una URL."""
    if re.search(r"%(?![0-9A-Fa-f]{2})", text):
        return INVALID_URL

    try:
        return urllib.parse.unquote(
            text,
            encoding="utf-8",
            errors="strict",
        )
    except UnicodeDecodeError:
        return INVALID_URL


def text_to_binary(text: str) -> str:
    """Representa cada byte UTF-8 con ocho bits."""
    return " ".join(
        f"{byte:08b}"
        for byte in text.encode("utf-8")
    )


def _clean_binary(binary: str) -> str | None:
    """Normaliza y valida una secuencia binaria."""
    compact = "".join(binary.split())

    if not compact:
        return None

    if any(bit not in "01" for bit in compact):
        return None

    return compact


def binary_to_text(binary: str) -> str:
    """Convierte grupos binarios de ocho bits en texto UTF-8."""
    compact = _clean_binary(binary)

    if compact is None or len(compact) % 8 != 0:
        return INVALID_BINARY

    decoded = bytes(
        int(compact[index:index + 8], 2)
        for index in range(0, len(compact), 8)
    )

    try:
        return decoded.decode("utf-8")
    except UnicodeDecodeError:
        return INVALID_BINARY_TEXT


def binary_to_decimal(binary: str) -> str:
    """Interpreta una secuencia binaria como entero decimal."""
    compact = _clean_binary(binary)

    if compact is None:
        return INVALID_BINARY

    return str(int(compact, 2))


def binary_to_hex(binary: str) -> str:
    """Interpreta una secuencia binaria como hexadecimal."""
    compact = _clean_binary(binary)

    if compact is None:
        return INVALID_BINARY

    return format(int(compact, 2), "x")


def looks_like_binary(value: str) -> bool:
    """Comprueba si una cadena puede representar bytes binarios."""
    compact = _clean_binary(value)

    return (
        compact is not None
        and len(compact) % 8 == 0
    )


def looks_like_hex(value: str) -> bool:
    """Comprueba que una cadena tenga estructura hexadecimal."""
    compact = "".join(value.split())

    return (
        bool(compact)
        and len(compact) % 2 == 0
        and re.fullmatch(
            r"[0-9A-Fa-f]+",
            compact,
        ) is not None
    )


def looks_like_base64(value: str) -> bool:
    """Comprueba si una cadena tiene estructura Base64 válida."""
    compact = "".join(value.split())

    if not compact or len(compact) % 4 != 0:
        return False

    try:
        base64.b64decode(compact, validate=True)
    except (binascii.Error, ValueError):
        return False

    return True


def looks_like_url_encoding(value: str) -> bool:
    """Detecta al menos una secuencia porcentual válida."""
    return re.search(
        r"%[0-9A-Fa-f]{2}",
        value,
    ) is not None


def _is_readable_text(text: str) -> bool:
    """Evita presentar bytes de control como texto útil."""
    if not text:
        return False

    readable = sum(
        character.isprintable()
        or character in "\n\r\t"
        for character in text
    )

    return readable / len(text) >= 0.85


def smart_decode(value: str) -> dict[str, str]:
    """Prueba automáticamente formatos detectables.

    ROT13 no puede identificarse de manera fiable solo por su
    estructura, por lo que se mantiene como conversión manual.
    """
    results: dict[str, str] = {}

    if looks_like_base64(value):
        decoded = decode_base64(value)

        if (
            not decoded.startswith("⚠️")
            and _is_readable_text(decoded)
        ):
            results["base64"] = decoded

    if looks_like_hex(value):
        decoded = decode_hex(value)

        if (
            not decoded.startswith("⚠️")
            and _is_readable_text(decoded)
        ):
            results["hex"] = decoded

    if looks_like_url_encoding(value):
        decoded = decode_url(value)

        if (
            decoded != value
            and not decoded.startswith("⚠️")
            and _is_readable_text(decoded)
        ):
            results["url"] = decoded

    if looks_like_binary(value):
        decoded_text = binary_to_text(value)

        if (
            not decoded_text.startswith("⚠️")
            and _is_readable_text(decoded_text)
        ):
            results["binary_text"] = decoded_text

        results["binary_decimal"] = binary_to_decimal(value)
        results["binary_hex"] = binary_to_hex(value)

    return results


def menu() -> None:
    """Muestra el menú principal."""
    print(
        """
=== MultiCodec ===
 1. Texto → Base64
 2. Base64 → Texto
 3. Texto → Hexadecimal
 4. Hexadecimal → Texto
 5. Texto → ROT13
 6. ROT13 → Texto
 7. Texto → URL
 8. URL → Texto
 9. Texto → Binario
10. Binario → Texto
11. Binario → Decimal
12. Binario → Hexadecimal
13. Análisis automático
14. Salir
""".strip()
    )


def run_smart_decode() -> None:
    """Solicita una cadena y muestra los formatos detectados."""
    value = input("Cadena a analizar: ")
    results = smart_decode(value)

    if not results:
        print("\nNo se detectó una codificación compatible.")
        print("Nota: ROT13 debe probarse manualmente.")
        return

    print("\n=== Resultados ===")

    for format_name, decoded in results.items():
        print(f"\n[{format_name}]\n{decoded}")


def main() -> None:
    """Ejecuta la interfaz de línea de comandos."""
    actions = {
        "1": (
            "Texto: ",
            encode_base64,
            "Base64",
        ),
        "2": (
            "Base64: ",
            decode_base64,
            "Texto",
        ),
        "3": (
            "Texto: ",
            encode_hex,
            "Hexadecimal",
        ),
        "4": (
            "Hexadecimal: ",
            decode_hex,
            "Texto",
        ),
        "5": (
            "Texto: ",
            encode_rot13,
            "ROT13",
        ),
        "6": (
            "ROT13: ",
            decode_rot13,
            "Texto",
        ),
        "7": (
            "Texto: ",
            encode_url,
            "URL",
        ),
        "8": (
            "URL: ",
            decode_url,
            "Texto",
        ),
        "9": (
            "Texto: ",
            text_to_binary,
            "Binario",
        ),
        "10": (
            "Binario: ",
            binary_to_text,
            "Texto",
        ),
        "11": (
            "Binario: ",
            binary_to_decimal,
            "Decimal",
        ),
        "12": (
            "Binario: ",
            binary_to_hex,
            "Hexadecimal",
        ),
    }

    while True:
        menu()

        try:
            option = input(
                "\nSelecciona una opción: "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo de MultiCodec.")
            break

        if option == "14":
            print("Saliendo de MultiCodec.")
            break

        if option == "13":
            run_smart_decode()
            continue

        action = actions.get(option)

        if action is None:
            print("❌ Opción inválida.")
            continue

        prompt, function, label = action
        value = input(prompt)

        print(f"{label}: {function(value)}")


if __name__ == "__main__":
    main()
